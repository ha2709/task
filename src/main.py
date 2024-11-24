from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.task import router as task
from .routers.user import router as user

app = FastAPI()

# Configure CORS
origins = [
    "*"
    # "https://setting-ui-sandbox-84f3a22716a0.herokuapp.com",
    # Add other origins as needed
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include the router
app.include_router(task, prefix="/api/v1/task")
app.include_router(user, prefix="/api/v1/user")
