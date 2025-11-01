# ip 118.31.237.235 pwd:12345678

import asyncio
import json

import redis.asyncio as aioredis

REDIS_URL = "redis://:12345678@118.31.237.235:6379"

STREAMS = {
    "fbmessage": "fb_group",
    "insmessage": "ins_group"
}


async def setup_group(redis, stream, group):
    try:
        await redis.xgroup_create(stream, group, id="0", mkstream=True)
    except Exception as e:
        if "BUSYGROUP" in str(e):
            pass

async def produce_message(stream_key, message: dict):
    redis = aioredis.from_url(REDIS_URL, decode_responses=True)
    await redis.xadd(stream_key, {"message": json.dumps(message)}, maxlen=10000)
    await redis.aclose()

async def consumer_worker(stream, group, consumer_name):
    redis = aioredis.from_url(REDIS_URL, decode_responses=True)
    await setup_group(redis, stream, group)

    while True:
        # 阻塞读取
        res = await redis.xreadgroup(group, consumer_name, {stream: ">"}, count=1, block=5000)
        if res:
            _, msgs = res[0]
            for msg_id, fields in msgs:
                data = json.loads(fields["message"])
                try:
                    print(f"[{consumer_name}] Processing {msg_id}: {data}")
                    # 模拟处理逻辑
                    await asyncio.sleep(1)
                    # 处理成功 → ack
                    await redis.xack(stream, group, msg_id)
                    print(f"[{consumer_name}] ✅ Acked {msg_id}")
                    await redis.xdel(stream, msg_id)
                except Exception as e:
                    print(f"[{consumer_name}] ❌ Failed {msg_id}, will retry later: {e}")

async def main():
    # 启动消费者
    await asyncio.gather(
        consumer_worker("fbmessage", "fb_group", "fb_worker_1"),
        consumer_worker("insmessage", "ins_group", "ins_worker_1"),
    )

if __name__ == "__main__":
    asyncio.run(main())
