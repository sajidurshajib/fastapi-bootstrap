import aio_pika
import json
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel

class RabbitBroker:
    def __init__(self, url: str):
        self.url = url
        self.connection: AbstractRobustConnection | None = None
        self.channel: AbstractRobustChannel | None = None

    async def connect(self):
        if not self.connection or self.connection.is_closed:
            self.connection = await aio_pika.connect_robust(self.url)
            self.channel = await self.connection.channel()

    async def publish(self, queue_name: str, msg: dict):
        await self.connect()
        queue = await self.channel.declare_queue(queue_name, durable=True)
        body = json.dumps(msg).encode()
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=body),
            routing_key=queue.name
        )

    async def consume(self, queue_name: str, callback):
        await self.connect()
        queue = await self.channel.declare_queue(queue_name, durable=True)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    data = json.loads(message.body.decode())
                    await callback(data)

    async def close(self):
        if self.connection and not self.connection.is_closed:
            await self.connection.close()