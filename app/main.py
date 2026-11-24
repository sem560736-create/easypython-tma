"""FastAPI backend for EasyPython Telegram Mini App"""

import os
import sys
from typing import List, Dict
from datetime import datetime

# Добавляем корневую директорию проекта в path для импортов
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
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

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTMLResponse("""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EasyPython - Учитель Python</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: system-ui, -apple-system, sans-serif;
            background: #f5f7fa;
            color: #333;
            line-height: 1.6;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 0;
        }
        header {
            background: linear-gradient(135deg, #4caf50, #2e7d32);
            color: white;
            padding: 30px 20px;
            text-align: center;
            border-radius: 0 0 100px 100px;
            position: relative;
            overflow: hidden;
        }
        header::before {
            content: "🐍";
            position: absolute;
            top: -20px;
            right: 20px;
            font-size: 3rem;
            opacity: 0.2;
        }
        h1 { font-size: 2rem; margin-bottom: 8px; }
        .subtitle { font-size: 1rem; opacity: 0.9; }

        .stats-row {
            display: flex;
            justify-content: space-around;
            background: white;
            padding: 20px 0;
            margin: -20px 0 0;
            border-radius: 0 0 100px 100px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            position: relative;
            z-index: 1;
        }
        .stat-item {
            text-align: center;
        }
        .stat-value {
            font-size: 1.5rem;
            font-weight: bold;
            color: #4caf50;
        }
        .stat-label {
            font-size: 0.85rem;
            color: #757575;
        }

        .lessons-grid {
            padding: 20px;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 15px;
        }
        .lesson-card {
            background: white;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border: 2px solid transparent;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .lesson-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        .lesson-card.locked {
            opacity: 0.5;
            filter: grayscale(0.5);
            cursor: not-allowed;
        }
        .lesson-card.locked:hover {
            transform: none;
            box-shadow: none;
        }
        .lesson-card.completed {
            border-color: #4caf50;
        }
        .lesson-card.active {
            border-color: #1a73e8;
        }
        .lesson-number {
            font-size: 0.75rem;
            font-weight: bold;
            color: #757575;
            margin-bottom: 8px;
        }
        .lesson-title {
            font-size: 1.1rem;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .lesson-desc {
            font-size: 0.9rem;
            color: #666;
            margin-bottom: 15px;
        }
        .lesson-progress {
            height: 6px;
            background: #e0e0e0;
            border-radius: 3px;
            margin-bottom: 10px;
        }
        .lesson-progress-fill {
            height: 100%;
            background: #4caf50;
            border-radius: 3px;
            width: 0%;
            transition: width 0.3s;
        }
        .lesson-buttons {
            display: flex;
            gap: 8px;
        }
        .btn-primary {
            flex: 1;
            background: #4caf50;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            font-size: 0.9rem;
        }
        .btn-primary:disabled {
            background: #9e9e9e;
            cursor: not-allowed;
        }
        .btn-primary:hover:not(:disabled) {
            background: #43a047;
        }
        .btn-secondary {
            flex: 1;
            background: white;
            color: #4caf50;
            border: 2px solid #4caf50;
            padding: 10px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            font-size: 0.9rem;
        }
        .btn-secondary:hover {
            background: #e8f5e9;
        }

        .badges {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 15px 0;
        }
        .badge {
            background: #f1f8e9;
            color: #2e7d32;
            padding: 8px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .badge.locked {
            background: #eee;
            color: #9e9e9e;
        }

        .footer {
            padding: 30px 20px;
            text-align: center;
            color: #757575;
            font-size: 0.9rem;
        }

        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }
        .modal.active {
            display: flex;
        }
        .modal-content {
            background: white;
            border-radius: 16px;
            padding: 24px;
            max-width: 400px;
            width: 90%;
            max-height: 90vh;
            overflow-y: auto;
            position: relative;
        }
        .close-modal {
            position: absolute;
            top: 12px;
            right: 12px;
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: #757575;
        }
        .modal h2 {
            margin-bottom: 16px;
            color: #333;
        }
        .code-editor {
            background: #1e1e1e;
            color: #d4d4d4;
            border-radius: 8px;
            padding: 16px;
            margin: 16px 0;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.9rem;
            overflow-x: auto;
            white-space: pre-wrap;
        }
        .error-box {
            background: #ffebee;
            color: #c62828;
            padding: 12px;
            border-radius: 8px;
            margin: 12px 0;
        }
        .success-box {
            background: #e8f5e9;
            color: #2e7d32;
            padding: 12px;
            border-radius: 8px;
            margin: 12px 0;
        }

        .streak-badge {
            background: #ff9800;
            color: white;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin: 10px 0;
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🐍 EasyPython</h1>
            <div class="subtitle">Учитель Python в стиле Duolingo</div>
        </header>

        <div class="stats-row">
            <div class="stat-item">
                <div class="stat-value" id="level-value">1</div>
                <div class="stat-label">Уровень</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="xp-value">0</div>
                <div class="stat-label">Опыт</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="streak-value">0</div>
                <div class="stat-label">Дней подряд</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="lesson-value">1</div>
                <div class="stat-label">Уроков из 17</div>
            </div>
        </div>

        <div id="badges-container" class="badges"></div>

        <div class="lessons-grid" id="lessons-grid">
            <!-- Уроки будут загружены через JS -->
        </div>

        <footer class="footer">
            <p>EasyPython — учите Python в Telegram</p>
        </footer>
    </div>

    <div class="modal" id="lesson-modal">
        <div class="modal-content">
            <button class="close-modal" onclick="closeLessonModal()">×</button>
            <h2 id="modal-title">Урок</h2>
            <div id="modal-theory"></div>
            <div id="modal-exercise"></div>
            <div class="code-editor" id="modal-hint"></div>
            <textarea class="code-input" id="answer-input" placeholder="Напишите ваш код здесь..."></textarea>
            <button class="check-btn" onclick="checkAnswer()">Проверить ответ</button>
            <div id="result-message"></div>
            <button class="btn-primary" onclick="closeLessonModal()">Закрыть</button>
        </div>
    </div>

    <script>
        const tg = window.Telegram.WebApp;
        tg.expand();
        tg.ready();
        tg.setHeaderColor('#4caf50');
        tg.setBackgroundColor('#f5f7fa');

        // Получаем user_id из Telegram WebApp
        const userId = tg.initDataUnsafe.user.id;

        let lessons = [];
        let currentProgress = { completed: [], xp: 0, level: 1, streak: 0, user_id: userId };
        const modal = document.getElementById('lesson-modal');

        async function loadProgress() {
            try {
                const resp = await fetch(`/progress?user_id=${userId}`);
                currentProgress = await resp.json();
            } catch (e) {
                currentProgress = { completed: [], xp: 0, level: 1, streak: 0, user_id: userId };
            }
            updateStats();
            renderBadges();
            loadLessons();
        }

        async function loadLessons() {
            try {
                const resp = await fetch(`/lessons?user_id=${userId}`);
                lessons = await resp.json();
            } catch (e) {
                lessons = [];
                for (let i = 1; i <= 17; i++) {
                    lessons.push({ id: i, title: `Урок ${i}`, lesson_type: 'theory', completed: false });
                }
            }
            renderLessons();
        }

        async function checkAnswer() {
            const lessonId = parseInt(document.getElementById('modal-title').textContent.split(':')[0].replace('Урок ', ''));
            const answer = document.getElementById('answer-input').value.trim();
            const resultDiv = document.getElementById('result-message');
            if (!answer) {
                resultDiv.innerHTML = '<div class="error-box">Напишите код перед проверкой!</div>';
                return;
            }
            try {
                const resp = await fetch(`/check/${lessonId}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ answer: answer, user_id: userId })
                });
                const result = await resp.json();
                if (result.correct) {
                    currentProgress.completed.push(lessonId);
                    currentProgress.xp += 10;
                    currentProgress.level = Math.floor(currentProgress.xp / 100) + 1;
                    updateStats();
                    renderBadges();
                    renderLessons();
                    await fetch(`/save-progress`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(currentProgress)
                    });
                } else {
                    resultDiv.innerHTML = '<div class="error-box">❌ ' + (result.feedback || 'Попробуйте ещё раз') + '</div>';
                }
            } catch (e) {
                resultDiv.innerHTML = '<div class="error-box">Ошибка проверки</div>';
            }
        }

        function renderBadges() {
            const container = document.getElementById('badges-container');
            const completed = currentProgress.completed;
            const xp = currentProgress.xp;
            const level = currentProgress.level;
            const streak = currentProgress.streak;
            
            // Определение статуса бейджей
            const firstLesson = completed.length === 0;
            const fiveLessons = completed.length >= 5;
            const tenLessons = completed.length >= 10;
            const hundredXP = xp >= 100;
            const tenStreak = streak >= 10;
            const levelUp = level >= 2;
            const highXP = xp >= 500;
            
            const badges = [
                { name: 'Первый урок', locked: firstLesson },
                { name: '5 уроков', locked: !fiveLessons },
                { name: '10 уроков', locked: !tenLessons },
                { name: '100 XP', locked: !hundredXP },
                { name: '10 дней подряд', locked: !tenStreak },
                { name: 'Уровень 2', locked: !levelUp },
                { name: '500 XP', locked: !highXP }
            ];
            
            container.innerHTML = badges.map(b => `
                <div class="badge ${b.locked ? 'locked' : 'unlocked'}">
                    ${b.locked ? '🔒' : '🏆'} ${b.name}
                </div>
            `).join('');
        }

        function renderLessons() {
            const grid = document.getElementById('lessons-grid');
            grid.innerHTML = lessons.map(lesson => {
                const isCompleted = currentProgress.completed.includes(lesson.id);
                const isLocked = lesson.id > 1 && !currentProgress.completed.includes(lesson.id - 1);
                const isActive = lesson.id === 1 || (!isCompleted && !isLocked);
                let progressHtml = '';
                if (isCompleted) {
                    progressHtml = '<div class="lesson-progress"><div class="lesson-progress-fill" style="width:100%"></div></div>';
                } else if (isActive) {
                    progressHtml = '<div class="lesson-progress"><div class="lesson-progress-fill" style="width:50%"></div></div>';
                }
                const buttons = isLocked
                    ? '<button class="btn-primary" disabled>Заблокировано</button><button class="btn-secondary" disabled>—</button>'
                    : `<button class="btn-primary" onclick="openLesson(${lesson.id})">${isCompleted ? 'Пройдено ✓' : 'Начать'}</button>` +
                      `<button class="btn-secondary" onclick="openLesson(${lesson.id})">${isCompleted ? 'Повторить' : 'Теория'}</button>`;
                return `
                    <div class="lesson-card ${isLocked ? 'locked' : ''} ${isCompleted ? 'completed' : ''} ${isActive ? 'active' : ''}">
                        <div class="lesson-number">Урок ${lesson.id}</div>
                        <div class="lesson-title">${lesson.title}</div>
                        <div class="lesson-desc">${getLessonDesc(lesson.id)}</div>
                        ${progressHtml}
                        <div class="lesson-buttons">
                            ${buttons}
                        </div>
                    </div>
                `;
            }).join('');
        }

        function getLessonDesc(id) {
            const descs = {
                1: 'Вывод текста на экран через print',
                2: 'Переменные и типы данных',
                3: 'Математические операции',
                4: 'Ввод данных от пользователя',
                5: 'Условные операторы if/else',
                6: 'Циклы for и while',
                7: 'Работа со списками',
                8: 'Работа со словарями',
                9: 'Создание функций',
                10: 'Чтение и запись файлов',
                11: 'Обработка ошибок try/except',
                12: 'Импорт модулей',
                13: 'Классы и объекты',
                14: 'Внешние библиотеки',
                15: 'Проект: калькулятор',
                16: 'Проект: трекер привычек',
                17: 'Итоги и ресурсы'
            };
            return descs[id] || 'Новый урок';
        }

        async function openLesson(lessonId) {
            try {
                const resp = await fetch(`/lesson/${lessonId}`);
                const data = await resp.json();
                document.getElementById('modal-title').textContent = `Урок ${lessonId}: ${data.title}`;
                document.getElementById('modal-theory').innerHTML = data.theory.replace(/```python\\n([\\s\\S]*?)```/g, '<div class="code-editor">$1</div>');
                document.getElementById('modal-exercise').innerHTML = `
                    <div style="margin-bottom: 10px; font-weight: bold;">📝 Задание:</div>
                    <div style="background: #fff3e0; padding: 12px; border-radius: 8px; margin-bottom: 15px;">${data.exercise}</div>
                `;
                document.getElementById('modal-hint').innerHTML = `💡 ${data.hint}`;
                document.getElementById('answer-input').value = '';
                document.getElementById('result-message').innerHTML = '';
                modal.classList.add('active');
            } catch (e) {
                alert('Не удалось загрузить урок');
            }
        }

        async function checkAnswer() {
            const lessonId = parseInt(document.getElementById('modal-title').textContent.split(':')[0].replace('Урок ', ''));
            const answer = document.getElementById('answer-input').value.trim();
            const resultDiv = document.getElementById('result-message');
            if (!answer) {
                resultDiv.innerHTML = '<div class="error-box">Напишите код перед проверкой!</div>';
                return;
            }
            try {
                const resp = await fetch(`/check/${lessonId}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ answer: answer })
                });
                const result = await resp.json();
                if (result.correct) {
                    resultDiv.innerHTML = '<div class="success-box">✅ ' + (result.feedback || 'Правильно!') + '</div>';
                    currentProgress.completed.push(lessonId);
                    currentProgress.xp += 10;
                    currentProgress.level = Math.floor(currentProgress.xp / 100) + 1;
                    updateStats();
                    renderBadges();
                    renderLessons();
                    await fetch('/save-progress', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(currentProgress)
                    });
                } else {
                    resultDiv.innerHTML = '<div class="error-box">❌ ' + (result.feedback || 'Попробуйте ещё раз') + '</div>';
                }
            } catch (e) {
                resultDiv.innerHTML = '<div class="error-box">Ошибка проверки</div>';
            }
        }

        function closeLessonModal() {
            modal.classList.remove('active');
        }
        modal.addEventListener('click', (e) => {
            if (e.target === modal) closeLessonModal();
        });

        loadProgress();
    </script>
</body>
</html>
""")

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