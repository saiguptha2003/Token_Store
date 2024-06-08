
from routers import auth
from routers import playground
from fastapi import FastAPI
import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(playground.router)

@app.get('/')
def index():
    return "heo"