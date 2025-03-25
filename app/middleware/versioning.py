from fastapi import Request, HTTPException


def get_api_version(request: Request):
    accept = request.headers.get("Accept", "application/vnd.api.v1+json")
    if "v1" in accept:
        return "v1"
    raise HTTPException(status_code=406, detail="Unsupported API version")
