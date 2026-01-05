from fastapi import FastAPI
from database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

from login import router as login_router
from register import router as register_router
from me import router as me_router

Base.metadata.create_all(bind=engine)


app = FastAPI()  

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login_router, tags=["Login"])
app.include_router(register_router, tags=["Register"])
app.include_router(me_router, tags=["User"])
