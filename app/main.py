from pathlib import Path
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette import status

BASE_DIR = Path(__file__).parent

app = FastAPI()

# monta os estáticos (css, imagens, etc.)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/")
def root():
    # redireciona raiz para /login
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

@app.get("/login")
def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def post_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    # autenticação de exemplo
    if username == "admin" and password == "123":
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "Usuário ou senha inválidos", "username": username},
        status_code=400
    )
