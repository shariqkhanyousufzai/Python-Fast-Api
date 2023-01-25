from fastapi import APIRouter, Depends
from bson.objectid import ObjectId
from ..schemas import schemas
from ..schemas import book_schema
from fastapi import APIRouter, Response, status, Depends, HTTPException
from bson.json_util import loads, dumps
import json
from app.oauth2 import AuthJWT
from app.config.database import Book
from .. import oauth2
from app.serializers.bookuserSerializers import bookEntity, bookResponseEntity
from app.serializers.userSerializers import serializeList,serializeDict
from fastapi import File,UploadFile,Form
from datetime import datetime
from ..config.config import settings



router = APIRouter()

@router.get('/')
async def get_books():
    book = serializeList(Book.find())
    return {'status':'success','data':book}


@router.post('/create',description="Need Token To Access")
async def create_book(title: str = Form(),summary: str = Form(),description: str = Form(),price: str = Form(),book_cover : UploadFile = File(),Authorize: str = Depends(oauth2.require_user)):
        
        # uploading image 
        try:
            contents = book_cover.file.read()
            with open('./app/uploads/'+book_cover.filename, 'wb') as f:
                    f.write(contents)
        except Exception:
            return {"message": "There was an error uploading the file"}
        finally:
            book_cover.file.close()
        # after image upload
        payload = {
            'title' : title,
            'summary' : summary,
            'description' : description,
            'price' : price,
            'image' : settings.APP_URL+'files?image='+book_cover.filename,
            'created_at' : datetime.now(),
            'updated_at' : datetime.now()
        }
        
        result = Book.insert_one(payload)
        new_book = bookResponseEntity(Book.find_one({'_id': result.inserted_id}))
        return {'status':'success','data':new_book}
        

@router.put('/update',description="Need Token To Access")
async def update_book(id, payload:book_schema.BookBaseSchema,Authorize: str = Depends(oauth2.require_user)):
    book = serializeDict(Book.find_one_and_update({'_id':ObjectId(str(id))},{
        '$set':dict(payload) 
    }
    ))
    return {'status':'success','data':book}


@router.delete('/delete',description="Need Token To Access")
async def delete_book(id,Authorize: str = Depends(oauth2.require_user)):
    book = Book.delete_one({'_id': ObjectId(str(id))})
    return {'status':'sucesss','data':'Book deleted Sucess'}



    