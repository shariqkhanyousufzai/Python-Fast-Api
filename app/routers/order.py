from fastapi import APIRouter, Depends
from bson.objectid import ObjectId
from ..schemas import schemas
from ..schemas import book_schema
from fastapi import APIRouter, Response, status, Depends, HTTPException
from bson.json_util import loads, dumps
import json
from app.oauth2 import AuthJWT
from app.config.database import Cart, Book, Order
from .. import oauth2
from app.serializers.cartSerializers import cartResponseEntity
from app.serializers.userSerializers import serializeList,serializeDict
from fastapi import File,UploadFile,Form
from datetime import datetime
from ..config.config import settings
from ..schemas.order_schema import OrderBaseSchema
from app.serializers.globalSerializers import List
router = APIRouter()


@router.post('/create')
async def create(payload:OrderBaseSchema,user_id: str = Depends(oauth2.require_user)):
    
    cart = serializeList(Cart.find({'user_id' : str(user_id)}))
    cart_details = List()
    cart_data = List()
    cart_total = 0
    for item in cart:
        book_item = serializeList(Book.find({'_id': ObjectId(str(item["book_id"]))}))
        for item_book in book_item:
            cart_details.push({
                'items' : {
                    'book_id': item_book["_id"],
                    'title': item_book["title"],
                    'price': item_book["price"],
                    'image': item_book["image"],
                },
                'quantity': item["quantiy"],
            })
            cart_total = cart_total + int(item_book["price"])

    payload.user_id = user_id
    payload.cart_items = cart_details
    payload.order_total = cart_total
    order =  Order.insert_one(dict(payload))
    await deleteCart(str(user_id))
    new_order = serializeList(Order.find({'_id': order.inserted_id}))
    return {'status':'success','data': new_order}


async def deleteCart(user_id):
    Cart.delete_many({'user_id':str(user_id)})
    return True


@router.get('/orders')
async def orders(user_id: str = Depends(oauth2.require_user)):
    orders = serializeList(Order.find({'user_id':str(user_id)}))
    return {'status':'success','data':orders}



@router.get('/order_detail/{order_id}')
async def order_detail(order_id,user_id: str = Depends(oauth2.require_user)):
    order = serializeDict(Order.find_one({'_id': ObjectId(str(order_id))}))
    return {'status':'success','data':order}

# @router.get('/cart_items')
# async def get_cart_items(user_id: str = Depends(oauth2.require_user)):
    
#     cart = serializeList(Cart.find({'user_id': str(user_id)}))
#     cart_details = List()
#     cart_data = List()
#     cart_total = 0
#     for item in cart:
#         book_item = serializeList(Book.find({'_id': ObjectId(str(item["book_id"]))}))
#         for item_book in book_item:
#             cart_details.push({
#                 'cart_id': item["_id"],
#                 'book_details' : {
#                     'book_id': item_book["_id"],
#                     'title': item_book["title"],
#                     'price': item_book["price"],
#                     'image': item_book["image"],
#                 },
#                 'quantity': item["quantiy"],
#             })
#             cart_total = cart_total + int(item_book["price"])
#     cart_data.push({'cart_items': cart_details})
#     cart_data.push({'cart_total': cart_total})
#     response_data = cart_data
#     return {'status':'success','data':response_data}

