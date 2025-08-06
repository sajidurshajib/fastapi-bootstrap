from fastapi import WebSocket, APIRouter


router = APIRouter(prefix='/notifications')

@router.websocket('/')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        # await websocket.send_text(f"Hello {data}")
        await websocket.send_json({"greet":"Hello", "name": data})