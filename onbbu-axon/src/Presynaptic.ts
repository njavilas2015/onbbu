import { Codec, connect, ConnectionOptions, Msg, NatsConnection, StringCodec } from "nats";
import { IPromiseResponse } from "onbbu-core";

class Presynaptic {
    private opts: ConnectionOptions;
    private nc: NatsConnection;
    private sc: Codec<string>;
    private subject: string;

    constructor(subject: string, opts?: ConnectionOptions) {

        const { NATS_HOST, NATS_PORT } = process.env;

        this.sc = StringCodec();

        this.opts = {
            servers: `${NATS_HOST}:${NATS_PORT}`,
            ...opts
        }

        this.subject = subject;

        this.live()
    }

    public async live(): Promise<void> {

        this.nc = await connect(this.opts);

        console.info(`Connected to ${this.nc.getServer()}`);

        this.nc.closed().then((err) => {
            if (err) {
                console.error(`Service exited due to error: ${err.message}`);
            }
        });
    }

    public async die(): Promise<void> {

        if (this.nc) {

            await this.nc.flush();

            await this.nc.close();
        }
    }

    public async sendSignal<IRequest, IResponse>(payload: IRequest, name: string): IPromiseResponse<IResponse> {

        const raw_payload: string = JSON.stringify({ name, payload })

        const message: Msg = await this.nc.request(this.subject, this.sc.encode(raw_payload));

        return JSON.parse(this.sc.decode(message.data));
    }

    async sendSignalAsync<T>(payload: T, name: string): Promise<void> {

        const data: Uint8Array = this.sc.encode(JSON.stringify({ name, payload }));

        this.nc.request(this.subject, data);
    }
}

export default Presynaptic