from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@router.get("/getcallinfo")
def endpoint1(request: Request):
    client_ip = getattr(request, "client", None)
    client_ip = client_ip.host if client_ip else None
    headers = dict(request.headers)
    return {
        "client_ip": client_ip,
        "host": headers.get("host"),
        "method": request.method,
        "path": request.url.path,
        "query": request.url.query,
        "headers": headers,
    }