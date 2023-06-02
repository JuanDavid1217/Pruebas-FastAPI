from fastapi import FastAPI, HTTPException
from database import engine
from routers import general_route, admin_route, empleado_route, admin_casa_route, casa_route, IoT_route
import models
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(general_route.router)
app.include_router(admin_route.router)
app.include_router(empleado_route.router)
app.include_router(admin_casa_route.router)
app.include_router(casa_route.router)
app.include_router(IoT_route.router)

@app.get("/")
def raiz():
	return RedirectResponse(url="/docs/")
