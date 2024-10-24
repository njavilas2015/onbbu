export interface ModelSchema {
    [key: string]: {
        type: ITypeData; // Ej: 'STRING', 'INTEGER', etc.
        allowNull?: boolean;
        defaultValue?: any;
        unique?: boolean;
        primaryKey?: boolean
        validate?: {
            [key: string]: any; // Validaciones personalizadas
        };
    };
}

export const type_data = [
    "UUID",
    "SMALLINT",
    "BIGINT",
    "INTEGER",

    "VARCHAR",

    "DATE",
    "TEXT",

    "BOOLEAN",

    "CIDR",
    "INET",
    "MACADDR",

    "JSON",
    "JSONB",
    "XML",


    "UUID[]",
    "SMALLINT[]",
    "BIGINT[]",
    "INTEGER[]",

    "VARCHAR[]",

    "DATE[]",
    "TEXT[]",

    "BOOLEAN[]",

    "CIDR[]",
    "INET[]",
    "MACADDR[]",

    "JSON[]",
    "JSONB[]",
    "XML[]"
] as const;

export type ITypeData = typeof type_data[number]

export const hooks = [
    "beforeCreate",
    "afterCreate",

    "beforeUpdate",
    "afterUpdate",

    "beforeDestroy",
    "afterDestroy",

    "beforeSave",
    "afterSave",

    "beforeUpsert",
    "afterUpsert",

    "beforeBulkCreate",
    "afterBulkCreate",

    "beforeBulkUpdate",
    "afterBulkUpdate",

    "beforeBulkDestroy",
    "afterBulkDestroy",

    "beforeCreateTable",
    "afterCreateTable",

    "beforeDropTable",
    "afterDropTable",

    "beforeValidate",
    "afterValidate",

    "beforeSave",
    "afterSave",

    "beforeDestroy",
    "afterDestroy",

    "beforeCount",
    "afterCount",

    "beforeQuery",

    "beforeFindOne",
    "afterFindOne",
] as const;

export type IHooks = typeof hooks[number]


export type IModelAttributesAsList<T> = {
    [K in keyof T]: T[K][];
};