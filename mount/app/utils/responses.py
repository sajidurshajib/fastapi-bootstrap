import json
from fastapi import Response

def standard_response(status, success, message, data):
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            pass
    return Response(
        status_code=status,
        content={
            "success": success,
            "message": message,
            "data": data if data is not None else {}
        }
    )