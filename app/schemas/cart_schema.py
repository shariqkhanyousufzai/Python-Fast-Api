from datetime import datetime
from pydantic import BaseModel, EmailStr, constr
from fastapi import Form, File, UploadFile, Request, FastAPI
from fastapi import FastAPI, Form, Header
from starlette.responses import HTMLResponse



class CartBaseSchema(BaseModel):
    book_id: str 
    user_id : str
    quantiy : int | None = 1
    created_at: datetime | None = None 
    updated_at: datetime | None = None

    class Config:
        orm_mode = True





