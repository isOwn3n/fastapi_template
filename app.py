from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from api.v1 import router as v1_router

app = FastAPI(default_response_class=ORJSONResponse)

app.include_router(v1_router, prefix="/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", reload=True)