from datetime import datetime
from pydantic import BaseModel, EmailStr, constr
from fastapi import Form, File, UploadFile, Request, FastAPI
from fastapi import FastAPI, Form, Header
from starlette.responses import HTMLResponse



class OrderBaseSchema(BaseModel):
    cart_items: object 
    user_id : str
    order_total : int 
    created_at: datetime | None = None 
    updated_at: datetime | None = None

    class Config:
        orm_mode = True





