import { IPromiseResponse } from 'onbbu-core'

export interface IFn {
    validate: (payload: unknown) => Promise<unknown>
    middleware: (payload: unknown) => Promise<unknown>
    service: (payload: unknown) => IPromiseResponse<unknown>
}

export type IExceptions = (name: string, step: string, error: unknown) => IPromiseResponse<unknown>

export interface IPayload {
    name: string,
    payload: unknown
}