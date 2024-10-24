import { Codec, connect, ConnectionOptions, NatsConnection, StringCodec, Subscription } from "nats";
import { IExceptions, IFn, IPayload } from "./types";
import { internalError, InternalError, IPromiseResponse, NotAuthenticated, NotFoundError, ValidationError } from "onbbu-core";

export const exceptions = (async (name: string, step: string, error: unknown): IPromiseResponse<string> => {

    if (error instanceof InternalError) {
        return { statusCode: 'error', message: internalError }
    }

    if (error instanceof NotAuthenticated) {
        return { statusCode: 'not authenticated', message: error.message }
    }

    if (error instanceof NotFoundError) {
        return { statusCode: 'not found', message: error.message }
    }

    if (error instanceof ValidationError) {
        return { statusCode: 'validation error', message: error.message }
    }

    return { statusCode: 'error', message: internalError }
})

class Postsynaptic {

    private opts: ConnectionOptions;
    private nc: NatsConnection;
    private sc: Codec<string>;
    private subject: string;

    private contracts: Map<string, IFn>

    exceptions: IExceptions

    constructor(name: string, opts?: ConnectionOptions) {

        this.contracts = new Map<string, IFn>();

        this.sc = StringCodec();

        this.opts = {
            ...{ servers: `${process.env.NATS_HOST}:${process.env.NATS_PORT}` },
            ...opts
        }

        this.subject = name;

        this.exceptions = exceptions
    }

    public contract(contract: string, fn: IFn): void {

        if (typeof fn.validate !== 'function') {
            throw new Error(`All middleware for contract ${contract} must be functions`);
        }

        if (typeof fn.middleware !== 'function') {
            throw new Error(`All middleware for contract ${contract} must be functions`);
        }

        if (typeof fn.service !== 'function') {
            throw new Error(`the service for contract ${contract} must be functions`);
        }

        this.contracts.set(contract, fn)
    }

    private errorResponse(message: string): string {
        return JSON.stringify({ statusCode: 'error', message });
    }

    private validate(value: IPayload): string | null {

        if (typeof value.name !== 'string' || typeof value.payload !== 'object') {
            return this.errorResponse("Error parser data in api");
        }

        return null;
    }

    private async validate_error(name: string, error: unknown): Promise<string> {
        try {

            let raw: object = await this.exceptions(this.subject, name, error)

            return JSON.stringify(raw)

        } catch (error) {

            return this.errorResponse("InternalError")
        }
    }

    private async process(data: string): Promise<string> {

        const payload: IPayload = JSON.parse(data)

        const validationError = this.validate(payload);

        if (validationError) {
            return validationError;
        }

        if (!this.contracts.has(payload.name)) {
            return this.errorResponse("Contract not found")
        }

        const { middleware, service, validate } = this.contracts.get(payload.name)

        try {

            let raw = payload.payload

            raw = await validate(raw)

            raw = await middleware(raw)

            raw = await service(raw)

            return JSON.stringify(raw);

        } catch (error) {

            return await this.validate_error(payload.name, error);
        }
    }

    private async ensureConnection(): Promise<void> {

        if (!this.nc) {

            this.nc = await connect(this.opts);

            this.nc.closed()
                .then((err) => {

                    if (err) {
                        console.error(`service exited because of error: ${err.message}`)
                    }
                });
        }
    }

    async live(): Promise<void> {

        await this.ensureConnection();

        const sub: Subscription = this.nc.subscribe(this.subject, { queue: "worker" });

        for await (const m of sub) {

            this.process(this.sc.decode(m.data))

                .then((payload: string) => m.respond(this.sc.encode(payload)))

                .catch((err) => console.error(err));
        }
    }

    async die(): Promise<void> {

        await this.nc.flush();

        return this.nc.close();
    }
}

export default Postsynaptic