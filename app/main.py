from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.config import settings
from app.routers import auth, user, book

from fastapi.responses import FileResponse

from fastapi import Form;

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


@app.get('/files')
async def get_files(image):
    # notice you can use FileResponse now because it expects a path
    return FileResponse(IMAGEDIR+image)

