from fastapi import FastAPI
from server.routers.arXiv import arXiv_router

app = FastAPI()

# Importing the routers
app.include_router(arXiv_router)
