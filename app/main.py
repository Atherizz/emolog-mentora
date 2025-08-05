from fastapi import FastAPI
from app.api.routes import emolog

app = FastAPI(title="Emolog API")

app.include_router(emolog.router, prefix="/api")

# @app.on_event("startup")
# # def on_startup():
# #     from app.db.session import create_db_and_tables
# #     create_db_and_tables()
