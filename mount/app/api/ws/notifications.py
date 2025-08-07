from fastapi import WebSocket, APIRouter, Depends
from app.notifications.users import consume_user_notifications
from app.services.auth_dependency import logged_in, TokenWrapper
from app.services.connection import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

router = APIRouter(prefix='/notifications')


@router.websocket('/')
async def websocket_endpoint(
    websocket: WebSocket,
    db: AsyncSession = Depends(get_db),
):
    await websocket.accept()

    # Get token from Authorization header
    auth_header = websocket.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        await websocket.close(code=1008, reason="Missing or invalid Authorization header")
        return

    token = auth_header.split("Bearer ")[-1]
    token_obj = TokenWrapper(token)

    # Use logged_in to get user data from token
    status_code, success, message, user_data = await logged_in(token_obj, db)
    if not success:
        await websocket.close(code=1008, reason=message)
        return

    async def send_notification_to_ws(data):
        await websocket.send_json({
            "notification": data,
            "user": user_data["data"]  # user info from token
        })

    # Start consumer for this websocket connection
    consumer_task = asyncio.create_task(
        consume_user_notifications(send_notification_to_ws)
    )
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except Exception as e:
        await websocket.close(code=1011, reason=str(e))
    finally:
        if consumer_task:
            consumer_task.cancel()