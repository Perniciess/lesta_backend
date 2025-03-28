import os
from fastapi import APIRouter, UploadFile
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.model import process_file_tfidf


router = APIRouter(
    prefix="",
    tags=["app"],
    default_response_class=HTMLResponse
)


templates = Jinja2Templates(directory="app")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("view.html", {"request": request})


@router.post("/upload")
async def upload_file(request: Request, file: UploadFile):
    # Сохраняем временный файл
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # Обрабатываем файл
    result = process_file_tfidf(temp_path)
    os.remove(temp_path)
    
    # Сортируем слова по TF-IDF (по убыванию) и берем топ-50
    sorted_words = sorted(
        result["word_stats"].items(),
        key=lambda x: x[1]["tfidf"],
        reverse=True
    )[:50]
    
    # Передаем данные в шаблон
    return templates.TemplateResponse(
        "view.html",
        {
            "request": request,
            "filename": file.filename,
            "words": sorted_words
        }
    )