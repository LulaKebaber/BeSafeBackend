from fastapi import Depends, HTTPException, status, Response

from app.utils import AppModel

from ..service import Service, get_service
from ..adapters.jwt_service import JWTData
from .dependencies import parse_jwt_user_data
from . import router


class RegisterUserRequest(AppModel):
    username: str
    name: str
    phone: str
    password: str


class UpdateLocationRequest(AppModel):
    latitude: float
    longitude: float


@router.post("/users", status_code=status.HTTP_201_CREATED)
def register_user(
    input: RegisterUserRequest,
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    if svc.repository.get_user_by_username(input.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already taken.",
        )

    svc.repository.create_user(input.dict())

    return Response(status_code=200)


@router.patch("/users", status_code=status.HTTP_200_OK)
def update_user_location(
    input: UpdateLocationRequest,
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    account_updated = svc.repository.update_location(jwt_data.user_id, input.dict())
    
    if account_updated.modified_count > 0:
        return Response(status_code=200)
    return Response(status_code=404)



