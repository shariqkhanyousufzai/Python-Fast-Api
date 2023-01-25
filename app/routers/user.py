from fastapi import APIRouter, Depends
from bson.objectid import ObjectId
from ..schemas import schemas
from app.serializers.userSerializers import userResponseEntity, userListEntity, userEntity, serializeList, serializeDict
from fastapi import APIRouter, Response, status, Depends, HTTPException
from bson.json_util import loads, dumps
import json
from app.oauth2 import AuthJWT
from app.config.database import User
from .. import oauth2

router = APIRouter()


@router.get('/me', response_model=schemas.UserResponse,description="Need Token To Access")
def get_me(user_id: str = Depends(oauth2.require_user)):
    user = userResponseEntity(User.find_one({'_id': ObjectId(str(user_id))}))
    return {"status": "success", "user": user}


@router.get('/all',description="Need Token To Access")
async def get_users(Authorize: str = Depends(oauth2.require_user)):
    user = serializeList(User.find())
    return {"status":"succss","user": user}


@router.get('/find_by_id/{id}',status_code=status.HTTP_201_CREATED,description="Need Token To Access")
async def find_user_by_id(id,Authorize: str = Depends(oauth2.require_user)):
    user = userEntity(User.find_one({'_id':ObjectId(str(id))}))
    return {"status":"success","user":user}

@router.post('/find_by_email',status_code=status.HTTP_201_CREATED,description="Need Token To Access")
async def find_user_by_email(payload: schemas.FindUserByEmail, Authorize: str = Depends(oauth2.require_user)):
    user = userEntity(User.find_one({"email": payload.email}))
    return {"status":"success","user": user}


@router.put('/update_user/{id}',description="Need Token To Access")
async def update_user(id,payload: schemas.UpdateUserSchema):
    user = serializeDict(User.find_one_and_update({'_id' : ObjectId(id)},{
        "$set":dict(payload)
    }))
    return {"status":"success","user": payload}


@router.delete('/delete_user/{id}',status_code=status.HTTP_201_CREATED,description="Need Token To Access")
async def delete_user(id):
    user = User.find_one_and_delete({'_id':ObjectId(str(id))})
    return {"status":"success","data":"User Deleted"}