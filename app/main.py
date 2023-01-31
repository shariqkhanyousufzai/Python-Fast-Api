from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.config import settings
from app.routers import auth, user, book, cart, order

from fastapi.responses import FileResponse

from fastapi import Form;

from .schemas.schemas import AccessFiles

from PIL import Image, ImageDraw, ImageFont

import random


IMAGEDIR = "./app/uploads/"

app = FastAPI()

origins = [
    settings.CLIENT_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(auth.router, tags=['Auth'], prefix='/api/auth')
app.include_router(user.router, tags=['Users'], prefix='/api/users')
app.include_router(book.router, tags=['Books'], prefix='/api/books')
app.include_router(cart.router, tags=['Cart'], prefix='/api/cart')
app.include_router(order.router, tags=['Order'], prefix='/api/order')


@app.get('/files/{image}',tags=['Access Any File From Uploads'])
async def get_files(image):
    # notice you can use FileResponse now because it expects a path
    return FileResponse(IMAGEDIR+image)


@app.get('/create_img/{text}')
async def create_img(text):
    my_image = Image.open('E:/Python/fastapi_mongodb/app/uploads/bookcover.png')
    width, height = my_image.size
    title_font = ImageFont.truetype('C:/Users/Shariq/Downloads/Roboto/Roboto-Black.ttf', 14)
    title_text = text
    image_editable = ImageDraw.Draw(my_image)
    image_editable.text(( ((width * 24) / 100) , height/2 ), title_text, (175,42,45), font=title_font)
    image_name = 'temp'+str(random.randint(1111,9999))
    my_image.save("./app/uploads/"+image_name+".png")
    return FileResponse(IMAGEDIR+image_name+".png")
    # return {'status':'success','data':'http://localhost:8000/files/'+image_name+".png"}
        

