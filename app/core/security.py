from fastapi import Depends, HTTPException, status


# Simulate current user (replace this with real auth later)
def get_current_user():
    return {"username": "lucas", "role": "admin"}


def require_role(required_role: str):
    def role_dependency(user=Depends(get_current_user)):
        if user["role"] != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this resource",
            )
        return user

    return role_dependency
