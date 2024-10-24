import { RedisClientOptions, RedisModules, RedisFunctions, RedisScripts } from 'redis'; // Asegúrate de importar estos tipos según tu configuración
import { Base } from '.';
import { randomUUID } from 'crypto';

export class ZSetRedis<T> extends Base {
    key: string;

    constructor(key: string, options?: RedisClientOptions<RedisModules, RedisFunctions, RedisScripts>) {
        super(options);
        this.key = key;
    }

    async add(value: T) {

        const score = await this.client.zCard(this.key);

        await this.client.zAdd(this.key, { score: score + 1, value: JSON.stringify(value) });
    }

    async get(): Promise<T[]> {

        const raw: string[] = await this.client.zRange(this.key, 0, -1);

        return raw.map(v => JSON.parse(v));
    }

    async update(value: T, newScore: number) {
        await this.client.zAdd(this.key, { score: newScore, value: JSON.stringify(value) });
    }

    async destroy(value: T) {
        await this.client.zRem(this.key, JSON.stringify(value));
    }

    async drop() {
        await this.client.del(this.key);
    }

    async rank(value: T): Promise<number | null> {
        return await this.client.zRank(this.key, JSON.stringify(value));
    }
}



interface IModel {
    name: string
    age: number
}

async function main() {

    const instance: IModel = {
        name: "Javier Avila",
        age: 29
    }

    const list = new ZSetRedis<IModel>(randomUUID(), {
        url: `redis://redis.sarys.ar:6379`,
        password: "akwdwhbqffweaprihrqfhhkkqonqrwpc7nmbe7ni53vhpiyyqh"
    })

    list.add(instance)

    const data: IModel[] = await list.get()

    console.log(data)

    /*
    list.destroy(instance)
    
    
    instance.age = 30
    
    list.update(1, instance)
    
    list.drop()*/
}

main()