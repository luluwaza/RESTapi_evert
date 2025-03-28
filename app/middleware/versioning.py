from fastapi import Request, HTTPException


def get_api_version(request: Request):
    accept = request.headers.get("Accept", "api.v1")
    if accept.strip().lower() == "api.v1":
        return "v1"
    raise HTTPException(status_code=406, detail="Unsupported API version")
