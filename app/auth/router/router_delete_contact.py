from fastapi import Depends, Response, HTTPException

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router

@router.delete("/contact/{contact_id:str}")
def delete_contact(
    contact_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    update_result = svc.word_repository.delete_contact_by_id(
        contact_id=contact_id, user_id=jwt_data.user_id
    )
    if update_result.modified_count > 0:
        return Response(status_code=200)
    raise HTTPException(status_code=404, detail=f"Contact {contact_id} not found")
