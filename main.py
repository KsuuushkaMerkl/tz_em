from fastapi import FastAPI

from core.db import create_session, init_db
from core.init_admin import create_default_admin
from core.seed import seed_access_rules
from user.endpoints import router as user_router
from access.endpoints import router as access_router
from mock.endpoints import router as mocks_router


app = FastAPI()

app.include_router(user_router)
app.include_router(access_router)
app.include_router(mocks_router)


@app.on_event("startup")
def startup_event():
    init_db()
    db = create_session()
    try:
        create_default_admin(db)
        seed_access_rules(db)
    finally:
        db.remove()
