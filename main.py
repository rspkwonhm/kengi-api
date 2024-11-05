from fastapi import FastAPI
from api.endpoints import watershed
from api.endpoints import rivClass
from api.endpoints import watershedMaster

app = FastAPI()

@app.get("/")
async def read_root():
  return {"message": "Hello, FastAPI!"}

app.include_router(watershed.router, prefix="/api")

app.include_router(rivClass.router, prefix="/api")

app.include_router(watershedMaster.router, prefix="/api")