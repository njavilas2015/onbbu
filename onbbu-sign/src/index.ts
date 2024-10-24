import jwt, { JsonWebTokenError } from "jsonwebtoken";
import moment from "moment";
import { IResponse } from "onbbu-core";

class Sign<IPayload extends jwt.JwtPayload> {

    private SECRET_KEY: string;

    constructor(secretKey?: string) {

        this.SECRET_KEY = secretKey || process.env.SECRET_KEY;
    }

    sign_token(payload: IPayload, expiresIn: string = "360d"): string {

        const token: string = jwt.sign(payload, this.SECRET_KEY, { expiresIn });

        return token;
    }

    private error_response(): IResponse<IPayload> {
        return { statusCode: "not authenticated", message: "Unauthorized, Invalid Token" };
    }

    verify_token(token?: string): IResponse<IPayload> {

        if (token === undefined) {
            return this.error_response()
        }

        try {

            const data: IPayload = jwt.verify(token, this.SECRET_KEY) as IPayload;

            if (data.exp <= moment().unix()) {
                return this.error_response()
            }

            const response: IPayload = {
                ...data,
                exp: moment.unix(data.exp).format(),
                iat: moment.unix(data.iat).format(),
            };

            return { statusCode: "success", data: response };

        } catch (error) {

            if (error instanceof JsonWebTokenError) {

                return this.error_response()
            }

            return this.error_response()
        }
    }
}

export default Sign;