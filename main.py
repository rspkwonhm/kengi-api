from fastapi import FastAPI
from api.endpoints import watershed
from api.endpoints import rivClass
from api.endpoints import watershedMaster
from api.endpoints import watershedDetail
from api.endpoints.search import rainfallRecordDataListSearch
from api.endpoints.search import climateChangePredictionDataListSearch

app = FastAPI()

app.include_router(watershed.router, prefix="/api")

app.include_router(rivClass.router, prefix="/api")

app.include_router(watershedMaster.router, prefix="/api")

app.include_router(watershedDetail.router, prefix="/api")

app.include_router(rainfallRecordDataListSearch.router, prefix="/api")

app.include_router(climateChangePredictionDataListSearch.router, prefix="/api")