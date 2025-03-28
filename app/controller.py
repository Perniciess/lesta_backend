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
    # Сохраняем файл в папку uploads
    uploads_dir = "uploads"
    os.makedirs(uploads_dir, exist_ok=True)
    file_path = os.path.join(uploads_dir, file.filename)
    
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Обрабатываем все документы
    results = process_file_tfidf(uploads_dir)
    
    # Получаем данные для текущего файла
    current_doc = file.filename
    if current_doc not in results:
        return templates.TemplateResponse("view.html", {
            "request": request,
            "error": "Ошибка обработки файла"
        })

    # Сортируем и ограничиваем топ-50 результатов
    sorted_words = sorted(
        results[current_doc].items(),
        key=lambda x: x[1]["tfidf"],
        reverse=True
    )[:50]

    return templates.TemplateResponse("view.html", {
        "request": request,
        "filename": current_doc,
        "words": sorted_words
    })