from app.services.config import config
from app.services.rabbit_broker import RabbitBroker
import asyncio

broker = RabbitBroker(config.rabbit_dsn)

async def notify_user_login(user_id: int, username: str, msg: str):
    message = {
        "event": "user_login",
        "user_id": user_id,
        "username": username,
        "msg": msg
    }
    await broker.publish("notifications", message)

async def consume_user_notifications(callback):
    async def handle_notification(data):
        await callback(data)  # Send notification to websocket or other handler

    await broker.consume("notifications", handle_notification)

# Example usage to start consumer (run in background or as a separate task)
# asyncio.create_task(consume_user_notifications())
