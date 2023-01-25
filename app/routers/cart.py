from fastapi import APIRouter, Depends
from bson.objectid import ObjectId
from ..schemas import schemas
from ..schemas import book_schema
from fastapi import APIRouter, Response, status, Depends, HTTPException
from bson.json_util import loads, dumps
import json
from app.oauth2 import AuthJWT
from app.config.database import Cart, Book
from .. import oauth2
from app.serializers.cartSerializers import cartResponseEntity
from app.serializers.userSerializers import serializeList,serializeDict
from fastapi import File,UploadFile,Form
from datetime import datetime
from ..config.config import settings
from ..schemas.cart_schema import CartBaseSchema
from app.serializers.globalSerializers import List
router = APIRouter()


@router.post('/add_to_cart')
async def add_to_cart(payload:CartBaseSchema,user_id: str = Depends(oauth2.require_user)):
    payload.user_id = user_id
    cart = Cart.insert_one(dict(payload))
    return {'status':'success','data':'Added To Cart'}


@router.post('/cart_items')
async def get_cart_items(user_id: str = Depends(oauth2.require_user)):
    
    cart = serializeList(Cart.find({'user_id': str(user_id)}))
    cart_data = List()
    for item in cart:
        book_item = serializeList(Book.find({'_id': ObjectId(str(item["book_id"]))}))
        for item_book in book_item:
            print(book_item)
            cart_data.push({
                'cart_id': item["_id"],
                'book_details' : {
                    'book_id': item_book["_id"],
                    'title': item_book["title"],
                    'price': item_book["price"],
                    'image': item_book["image"],
                },
                'quantity': item["quantiy"],
            })
    response_data = cart_data
    return {'status':'success','data':response_data}

