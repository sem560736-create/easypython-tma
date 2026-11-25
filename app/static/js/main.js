/* EasyPython Mini App - Duolingo-style JavaScript */

const tg = window.Telegram.WebApp;
tg.expand();
tg.ready();
tg.setHeaderColor('#4caf50');
tg.setBackgroundColor('#f5f7fa');

// Get user ID from Telegram WebApp
const userId = tg.initDataUnsafe?.user?.id || 1;

// DOM elements
const streakChip = document.getElementById('streak-chip');
const levelBadge = document.getElementById('level-badge');
const levelValue = document.getElementById('level-value');
const xpValue = document.getElementById('xp-value');
const xpNext = document.getElementById('xp-next');
const xpTotal = document.getElementById('xp-total');
const xpBarFill = document.getElementById('xp-bar-fill');
const doneCount = document.getElementById('done-count');
const totalCount = document.getElementById('total-count');
const courseBarFill = document.getElementById('course-bar-fill');
const lessonsGrid = document.getElementById('lessons-grid');
const badgesContainer = document.getElementById('badges-container');

// Lesson view elements
const backBtn = document.getElementById('back-btn');
const detailKicker = document.getElementById('detail-kicker');
const detailTitle = document.getElementById('detail-title');
const detailXp = document.getElementById('detail-xp');
const detailTheory = document.getElementById('detail-theory');
const detailExercise = document.getElementById('detail-exercise');
const detailHint = document.getElementById('detail-hint');
const answerInput = document.getElementById('answer-input');
const checkBtn = document.getElementById('check-btn');
const resultMessage = document.getElementById('result-message');
const prevLessonBtn = document.getElementById('prev-lesson-btn');
const nextLessonBtn = document.getElementById('next-lesson-btn');

// State management
let lessons = [];
let currentLessonId = null;
let currentProgress = { completed: [], xp: 0, level: 1, streak: 0, user_id: userId };

// Load progress and lessons
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

// Update stats display
function updateStats() {
    if (levelValue) levelValue.textContent = currentProgress.level;
    if (xpValue) xpValue.textContent = currentProgress.xp;
    if (streakChip) streakChip.textContent = `🔥 ${currentProgress.streak}`;
    if (doneCount) doneCount.textContent = currentProgress.completed.length;
    if (totalCount) totalCount.textContent = lessons.length || 17;

    // XP progress bar (next level at 100 XP per level)
    const levelXp = currentProgress.xp % 100;
    const progress = (levelXp / 100) * 100;
    if (xpBarFill) {
        xpBarFill.style.width = `${Math.min(progress, 100)}%`;
    }
    if (xpNext) {
        xpNext.textContent = 100 - levelXp;
    }
    if (xpTotal) {
        xpTotal.textContent = `${currentProgress.xp} XP`;
    }

    // Course progress bar
    if (courseBarFill && lessons.length) {
        const coursePct = (currentProgress.completed.length / lessons.length) * 100;
        courseBarFill.style.width = `${Math.min(coursePct, 100)}%`;
    }

    renderBadges();
}

// Render badges based on progress
function renderBadges() {
    if (!badgesContainer) return;
    badgesContainer.innerHTML = '';

    const completed = currentProgress.completed;
    const xp = currentProgress.xp;
    const level = currentProgress.level;
    const streak = currentProgress.streak;

    const badgeDefinitions = [
        { name: 'Первый урок', icon: '🐍', locked: completed.length === 0 },
        { name: '5 уроков', icon: '⭐', locked: completed.length < 5 },
        { name: '10 уроков', icon: '🔥', locked: completed.length < 10 },
        { name: '100 XP', icon: '💎', locked: xp < 100 },
        { name: '10 дней подряд', icon: '📅', locked: streak < 10 },
        { name: 'Уровень 2', icon: '📈', locked: level < 2 },
        { name: '500 XP', icon: '👑', locked: xp < 500 }
    ];

    badgeDefinitions.forEach(badge => {
        const badgeEl = document.createElement('div');
        badgeEl.className = `badge ${badge.locked ? 'locked' : 'unlocked'}`;
        badgeEl.innerHTML = `<span class="badge-icon">${badge.locked ? '🔒' : badge.icon}</span> ${badge.name}`;
        badgesContainer.appendChild(badgeEl);
    });
}

// Render lessons grid
function renderLessons() {
    if (!lessonsGrid) return;
    lessonsGrid.innerHTML = '';

    lessons.forEach(lesson => {
        const isCompleted = currentProgress.completed.includes(lesson.id);
        const isLocked = lesson.id > 1 && !currentProgress.completed.includes(lesson.id - 1);
        const isActive = !isCompleted && !isLocked;

        let progressHtml = '';
        if (isCompleted) {
            progressHtml = '<div class="lesson-progress"><div class="lesson-progress-fill completed" style="width:100%"></div></div>';
        } else if (isActive) {
            progressHtml = '<div class="lesson-progress"><div class="lesson-progress-fill active" style="width:50%"></div></div>';
        }

        const buttons = isLocked
            ? '<button class="btn-locked" disabled>Заблокировано</button>'
            : `<button class="btn-start" onclick="openLesson(${lesson.id})">${isCompleted ? 'Пройдено ✓' : 'Начать'}</button>`;

        lessonsGrid.innerHTML += `
            <div class="lesson-card ${isLocked ? 'locked' : ''} ${isCompleted ? 'completed' : ''} ${isActive ? 'active' : ''}" onclick="${isLocked ? '' : `openLesson(${lesson.id})`}">
                <div class="lesson-number">Урок ${lesson.id}</div>
                <div class="lesson-title">${lesson.title || `Урок ${lesson.id}`}</div>
                <div class="lesson-desc">${getLessonDesc(lesson.id)}</div>
                ${progressHtml}
                ${buttons}
            </div>
        `;
    });
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
    return descs[id] || 'Python урок';
}

// Open lesson detail view
function openLesson(lessonId) {
    const lesson = lessons.find(l => l.id === lessonId);
    if (!lesson) return;

    currentLessonId = lessonId;

    document.getElementById('view-menu').classList.remove('is-active');
    document.getElementById('view-lesson').classList.add('is-active');

    if (detailKicker) detailKicker.textContent = `Урок ${lessonId}`;
    if (detailTitle) detailTitle.textContent = lesson.title || `Урок ${lessonId}`;
    if (detailXp) detailXp.textContent = `+10 XP`;
    if (detailTheory) detailTheory.textContent = lesson.theory || `Теория урока ${lessonId}`;
    if (detailExercise) detailExercise.textContent = lesson.exercise || `Напишите код для урока ${lessonId}`;
    if (detailHint) detailHint.textContent = lesson.hint || 'Подсказка скоро будет';
    if (answerInput) answerInput.value = '';
    if (resultMessage) resultMessage.innerHTML = '';
    if (prevLessonBtn) prevLessonBtn.hidden = lessonId <= 1;
    if (nextLessonBtn) nextLessonBtn.hidden = isCompletedOrLocked(lessonId + 1);
}

// Check if a lesson is completed or locked
function isCompletedOrLocked(id) {
    if (id > lessons.length) return true;
    return currentProgress.completed.includes(id) || (id > 1 && !currentProgress.completed.includes(id - 1));
}

// Close lesson view
function closeLesson() {
    document.getElementById('view-lesson').classList.remove('is-active');
    document.getElementById('view-menu').classList.add('is-active');
    renderLessons();
}

// Check answer
async function checkAnswer() {
    if (!currentLessonId) return;
    const answer = answerInput ? answerInput.value.trim() : '';
    if (!answer) {
        if (resultMessage) resultMessage.innerHTML = '<div class="error-box">Напишите код перед проверкой!</div>';
        return;
    }

    try {
        const resp = await fetch(`/check/${currentLessonId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ answer: answer, user_id: userId })
        });
        const result = await resp.json();

        if (result.correct) {
            if (!currentProgress.completed.includes(currentLessonId)) {
                currentProgress.completed.push(currentLessonId);
                currentProgress.xp += 10;
                currentProgress.level = Math.floor(currentProgress.xp / 100) + 1;
                currentProgress.streak = (currentProgress.streak || 0) + 1;
            }

            updateStats();
            renderBadges();
            renderLessons();

            // Show XP award
            showXPAward('+10 XP');

            if (resultMessage) resultMessage.innerHTML = '<div class="success-box">✅ Верно! +10 XP</div>';

            // Save progress
            try {
                await fetch(`/save-progress`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(currentProgress)
                });
            } catch (e) {
                console.error('Save progress error:', e);
            }

            // Enable next lesson
            if (nextLessonBtn) nextLessonBtn.hidden = isCompletedOrLocked(currentLessonId + 1);
        } else {
            if (resultMessage) resultMessage.innerHTML = `<div class="error-box">❌ ${result.feedback || 'Попробуйте ещё раз'}</div>`;
        }
    } catch (e) {
        if (resultMessage) resultMessage.innerHTML = '<div class="error-box">Ошибка проверки</div>';
    }
}

// Show XP award animation
function showXPAward(text) {
    const existing = document.getElementById('xp-award');
    if (existing) existing.remove();

    const award = document.createElement('div');
    award.id = 'xp-award';
    award.className = 'xp-award';
    award.textContent = text;
    award.style.position = 'fixed';
    award.style.top = '50%';
    award.style.left = '50%';
    award.style.transform = 'translate(-50%, -50%)';
    award.style.background = 'rgba(88, 204, 2, 0.95)';
    award.style.color = '#fff';
    award.style.padding = '16px 32px';
    award.style.borderRadius = '24px';
    award.style.fontSize = '1.5rem';
    award.style.fontWeight = '800';
    award.style.zIndex = '1000';
    award.style.boxShadow = '0 8px 32px rgba(0,0,0,0.3)';
    award.style.animation = 'floatUp 1.5s ease-out forwards';
    document.body.appendChild(award);

    setTimeout(() => {
        if (award.parentNode) award.parentNode.removeChild(award);
    }, 1500);
}

// Event listeners
if (backBtn) backBtn.addEventListener('click', closeLesson);
if (checkBtn) checkBtn.addEventListener('click', checkAnswer);

// Initialize
loadProgress();

// Add floatUp animation if not present
if (!document.getElementById('float-up-style')) {
    const style = document.createElement('style');
    style.id = 'float-up-style';
    style.textContent = `
        @keyframes floatUp {
            0% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
            100% { transform: translate(-50%, -120%) scale(1.2); opacity: 0; }
        }
    `;
    document.head.appendChild(style);
}
