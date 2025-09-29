from fastapi import FastAPI

# import routers
from modules.users.routes import createUser, readUser, updateUser, deleteUser

app = FastAPI(title="Users API")

# include routers (each file defines APIRouter named `router`)
app.include_router(createUser.router)
app.include_router(readUser.router)
app.include_router(updateUser.router)
app.include_router(deleteUser.router)