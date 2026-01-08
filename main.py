from fastapi import FastAPI
from database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

from login import router as login_router
from register import router as register_router
from me import router as me_router
from add_history import router as add_history_router
from get_user_history import router as get_history_router
from analyze_animal import app as analyze_animal
from get_last_history import router as get_last_history
from contribute import router as contribute

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
app.include_router(add_history_router, tags=["AddHistory"])
app.include_router(get_history_router, tags=["GetHistory"])
app.include_router(analyze_animal, tags=["AnalyzeAnimal"])
app.include_router(get_last_history, tags=["GetLastHistory"])
app.include_router(contribute, Tags=["Contribute"])