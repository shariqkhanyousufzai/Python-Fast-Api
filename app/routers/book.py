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

router = APIRouter()

@router.get('/')
async def get_books():
    book = serializeList(Book.find())
    return {'status':'success','data':book}


@router.post('/create')
async def create_book(title: str = Form(),summary: str = Form(),description: str = Form(),price: str = Form(),file : UploadFile = File()):
        
        # uploading image 
        # contents = file.file.read()
        # with open('./app/uploads/'+file.filename, 'wb') as f:
        #     f.write(contents)
        try:
            contents = file.file.read()
            with open('./app/uploads/'+file.filename, 'wb') as f:
                    f.write(contents)
        except Exception:
            return {"message": "There was an error uploading the file"}
        finally:
            file.file.close()
        # after image upload
        payload = {
            'title' : title,
            'summary' : summary,
            'description' : description,
            'price' : price,
            'image' : file.filename,
            'created_at' : datetime.now(),
            'updated_at' : datetime.now()
        }
        
        result = Book.insert_one(payload)
        new_book = bookResponseEntity(Book.find_one({'_id': result.inserted_id}))
        return {'status':'success','data':new_book}


@router.put('/update')
async def update_book(id, payload:book_schema.BookBaseSchema):
    book = serializeDict(Book.find_one_and_update({'_id':ObjectId(str(id))},{
        '$set':dict(payload) 
    }
    ))
    return {'status':'success','data':book}


@router.delete('/delete')
async def delete_book(id):
    book = Book.delete_one({'_id': ObjectId(str(id))})
    return {'status':'sucesss','data':'Book deleted Sucess'}


@router.post('/create_with_file')
async def create_fild(file: UploadFile = File()):
    try:
        contents = file.file.read()
        with open('./app/uploads/'+file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}


    