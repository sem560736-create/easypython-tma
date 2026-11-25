"""FastAPI backend for EasyPython Telegram Mini App"""

import os
import sys
from typing import List, Dict
from datetime import datetime

# Добавляем корневую директорию проекта в path для импортов
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Подключаем Telegram-бота (webhook) к приложению,
# чтобы маршрут /webhook/{token} существовал даже при запуске app.main:app
from bot_webhook import mount as mount_bot_webhook

from lessons import LESSONS, GLOSSARY
from database import Database

app = FastAPI(title="EasyPython Mini App", docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files only if directory exists
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Database path - use /tmp on cloud platforms to avoid read-only filesystem
db_path = os.environ.get("DB_PATH", os.path.join(os.path.dirname(__file__), "students.db"))
db = Database(db_path)

@app.get("/", response_class=FileResponse)
async def root():
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.get("/progress", response_class=JSONResponse)
async def get_progress(user_id: int = 0):
    if user_id == 0:
        return {
            "completed": [],
            "completed_count": 0,
            "total_lessons": len(LESSONS),
            "score": 0,
            "streak": 0,
            "xp": 0,
            "level": 1,
            "user_id": 0
        }
    student = db.get_or_create(user_id, None, None)
    completed = db.completed_ids(user_id)
    return {
        "completed": completed,
        "completed_count": len(completed),
        "total_lessons": len(LESSONS),
        "score": student.get("score", 0),
        "streak": student.get("streak", 0),
        "xp": student.get("xp", 0),
        "level": student.get("level", 1),
        "user_id": user_id
    }

@app.get("/lessons", response_class=JSONResponse)
async def get_lessons(user_id: int = 0):
    completed_ids = []
    if user_id != 0:
        completed_ids = db.completed_ids(user_id)
    result = []
    for l in LESSONS:
        result.append({
            "id": l.id,
            "title": l.title,
            "lesson_type": "theory",
            "completed": l.id in completed_ids
        })
    return result

@app.get("/lesson/{lesson_id}", response_class=JSONResponse)
async def get_lesson_endpoint(lesson_id: int):
    if lesson_id < 1 or lesson_id > len(LESSONS):
        raise HTTPException(status_code=404, detail="Урок не найден")
    
    lesson = LESSONS[lesson_id - 1]
    return {
        "id": lesson.id,
        "title": lesson.title,
        "lesson_type": "theory",
        "theory": lesson.theory,
        "exercise": lesson.exercise,
        "hint": lesson.hint,
        "correct_answer": lesson.correct_answer,
        "correct_feedback": lesson.correct_feedback,
        "wrong_feedback": lesson.wrong_feedback,
        "quiz": lesson.quiz
    }

@app.post("/check/{lesson_id}", response_class=JSONResponse)
async def check_lesson_answer(lesson_id: int, payload: Dict):
    answer = payload.get("answer", "")
    user_id = payload.get("user_id", 0)
    if lesson_id < 1 or lesson_id > len(LESSONS):
        raise HTTPException(status_code=404, detail="Урок не найден")
    
    lesson = LESSONS[lesson_id - 1]
    is_correct = lesson.check_answer(answer)
    
    # Логируем попытку в БД
    if user_id != 0:
        db.log_attempt(user_id, lesson_id, answer, is_correct)
        if is_correct:
            db.mark_completed(user_id, lesson_id, points=10)
        # Получаем обновлённый прогресс (создаём ученика при необходимости)
        student = db.get_or_create(user_id, None, None)
        xp = student.get("xp", 0)
        level = student.get("level", 1)
        streak = student.get("streak", 0)
    else:
        xp, level, streak = 0, 1, 0
    
    return {
        "correct": is_correct,
        "feedback": lesson.correct_feedback if is_correct else lesson.wrong_feedback,
        "xp": xp,
        "level": level,
        "streak": streak
    }

@app.post("/save-progress", response_class=JSONResponse)
async def save_progress(payload: Dict):
    user_id = payload.get("user_id", 0)
    if user_id == 0:
        return {"status": "error", "message": "user_id required"}
    
    completed = payload.get("completed", [])
    xp = payload.get("xp", 0)
    level = payload.get("level", 1)
    streak = payload.get("streak", 0)
    
    conn = db._connect()
    cur = conn.cursor()
    cur.execute(
        "UPDATE students SET xp = ?, level = ?, streak = ?, completed = ?, "
        "last_activity = ? WHERE user_id = ?",
        (
            xp,
            level,
            streak,
            ",".join(str(x) for x in completed),
            datetime.now().isoformat(timespec="seconds"),
            user_id,
        ),
    )
    conn.commit()
    
    return {"status": "saved"}

@app.get("/leaderboard", response_class=JSONResponse)
async def get_leaderboard():
    # Топ учеников из БД
    students = db.get_all_students()
    return students

@app.get("/health")
async def health():
    return {"status": "ok"}

# Подключаем Telegram-бота (webhook), чтобы маршрут /webhook/{token} существовал
bot_bot = mount_bot_webhook(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)