from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from modules.auth.router import router as auth_router
from modules.users.router import router as users_router
from modules.targets.router import router as targets_router
from modules.initial_data.router import router as initial_data_router
from modules.shared.db import db, create_db_pool, close_db_pool
from modules.shared.seed import seed_data
from modules.shared.schema import TABLES  # Import TABLES from schema.py

app = FastAPI(title="Modular FastAPI Application")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(targets_router, prefix="/targets", tags=["targets"])
app.include_router(initial_data_router, prefix="/initial-data", tags=["initial-data"])

# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": f"An error occurred: {str(exc)}"}
    )

# Lifecycle events
@app.on_event("startup")
async def startup():
    await create_db_pool()
    for table_sql in TABLES:
        print(f"creating tables ...")
        await db.execute(table_sql)
    await seed_data()  # Run seeding after tables are created

@app.on_event("shutdown")
async def shutdown():
    await close_db_pool()