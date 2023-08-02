from fastapi import FastAPI
from app.speech import speechrouter;
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# cors
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(speechrouter)
