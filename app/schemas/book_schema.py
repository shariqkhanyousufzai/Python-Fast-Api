from datetime import datetime
from pydantic import BaseModel, EmailStr, constr
from fastapi import Form, File, UploadFile, Request, FastAPI
from fastapi import FastAPI, Form, Header
from starlette.responses import HTMLResponse



class BookBaseSchema(BaseModel):
    title: str 
    image : str
    summary: str 
    description: str 
    price: float 
    created_at: datetime | None = None 
    updated_at: datetime | None = None

    class Config:
        orm_mode = True





