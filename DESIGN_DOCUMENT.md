# EasyPython Mini App — Duolingo-Style UI Design Specification

> **Version:** 1.0  
> **Author:** Designer Agent  
> **Date:** 2026-11-25  
> **Context:** Telegram Mini App for learning Python, built on FastAPI + vanilla JS

---

## 1. Design Philosophy & Duolingo Visual Language

| Principle | Application |
|-----------|-------------|
| **Playful minimalism** | Clean cards, rounded corners, generous whitespace |
| **Progress at a glance** | Ring/bar progress, streak fire, XP, level badge |
| **Gamified micro-rewards** | Confetti on correct answer, streak celebration, badge unlock animation |
| **Immediate feedback** | Green/red toast, inline error hints, "try again" encouragement |
| **Character-driven** | Friendly mascot (🐍 Python snake) appears in empty states, celebrations |
| **Mobile-first, thumb-friendly** | Large tap targets (≥48×48 px), bottom-safe insets, one-hand reachable |

---

## 2. Color Palette

### 2.1 Core Brand Colors (Duolingo-inspired)

| Role | Hex | Usage |
|------|-----|-------|
| **Primary Green** | `#4CAF50` | Primary actions, progress fill, active states, header gradient start |
| **Primary Dark** | `#2E7D32` | Header gradient end, pressed buttons, dark text on green |
| **Primary Light** | `#E8F5E9` | Badge backgrounds, success toasts, hover states |
| **Accent Blue** | `#1A73E8` | Secondary actions, active lesson indicator, links |
| **Accent Orange** | `#FF9800` | Streak badge, warning states, XP gains |
| **Accent Purple** | `#7B1FA2` | Special achievements, leaderboard crown |

### 2.2 Semantic UI Colors

| Role | Light Mode | Dark Mode (auto via `prefers-color-scheme`) |
|------|------------|---------------------------------------------|
| **Background** | `#F5F7FA` | `#121212` |
| **Surface / Card** | `#FFFFFF` | `#1E1E1E` |
| **Surface Elevated** | `#FFFFFF` | `#2D2D2D` |
| **Text Primary** | `#212121` | `#FFFFFF` |
| **Text Secondary** | `#757575` | `#B0B0B0` |
| **Text Disabled** | `#9E9E9E` | `#707070` |
| **Border / Divider** | `#E0E0E0` | `#3A3A3A` |
| **Error Red** | `#C62828` | `#EF5350` |
| **Error Background** | `#FFEBEE` | `#3E1616` |
| **Success Green** | `#2E7D32` | `#66BB6A` |
| **Success Background** | `#E8F5E9` | `#163E16` |
| **Warning Orange** | `#FF9800` | `#FFB74D` |
| **Warning Background** | `#FFF3E0` | `#3E2A00` |

### 2.3 Gradients

```css
/* Header / Hero */
--gradient-header: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);

/* Primary Button */
--gradient-primary: linear-gradient(180deg, #4CAF50 0%, #43A047 100%);

/* Streak Badge */
--gradient-streak: linear-gradient(135deg, #FF9800 0%, #F57C00 100%);

/* Level Badge */
--gradient-level: linear-gradient(135deg, #1A73E8 0%, #1565C0 100%);

/* Celebration Confetti (CSS keyframes) */
--confetti-colors: #4CAF50, #1A73E8, #FF9800, #E91E63, #9C27B0;
```

---

## 3. Typography System

| Style | Font Family | Size | Weight | Line Height | Letter Spacing | Use Case |
|-------|-------------|------|--------|-------------|----------------|----------|
| **Display Large** | `'Nunito', system-ui, sans-serif` | 32px | 800 | 1.2 | -0.5px | Hero title ("EasyPython") |
| **Display Medium** | `'Nunito', system-ui, sans-serif` | 24px | 700 | 1.3 | -0.25px | Screen titles, modal headers |
| **Headline** | `'Nunito', system-ui, sans-serif` | 20px | 700 | 1.35 | 0px | Lesson card titles |
| **Title Large** | `'Nunito', system-ui, sans-serif` | 18px | 600 | 1.4 | 0px | Section headers |
| **Title Medium** | `'Nunito', system-ui, sans-serif` | 16px | 600 | 1.45 | 0.1px | Card subtitles, stat labels |
| **Body Large** | `'Inter', system-ui, sans-serif` | 16px | 400 | 1.6 | 0px | Main content, theory text |
| **Body Medium** | `'Inter', system-ui, sans-serif` | 14px | 400 | 1.55 | 0px | Descriptions, hints |
| **Body Small** | `'Inter', system-ui, sans-serif` | 12px | 400 | 1.5 | 0.2px | Metadata, timestamps |
| **Label Large** | `'Inter', system-ui, sans-serif` | 14px | 600 | 1.4 | 0.1px | Button text, badge text |
| **Label Small** | `'Inter', system-ui, sans-serif` | 11px | 600 | 1.4 | 0.5px | Chips, tags, lesson numbers |
| **Code** | `'JetBrains Mono', 'Fira Code', monospace` | 13px | 400 | 1.55 | 0px | Code snippets, editor |

### Font Loading (Telegram WebApp compatible)
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Nunito:wght@600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

---

## 4. Spacing & Layout System

| Token | Value | Usage |
|-------|-------|-------|
| `--space-1` | 4px | Icon gaps, tight padding |
| `--space-2` | 8px | Chip padding, small gaps |
| `--space-3` | 12px | Standard card padding (mobile) |
| `--space-4` | 16px | Standard gap, card padding (desktop) |
| `--space-5` | 20px | Section padding |
| `--space-6` | 24px | Modal padding, hero padding |
| `--space-8` | 32px | Page margins, large gaps |
| `--space-10` | 40px | Hero vertical rhythm |

### Border Radius
| Token | Value |
|-------|-------|
| `--radius-sm` | 8px (buttons, chips, badges) |
| `--radius-md` | 12px (cards, inputs) |
| `--radius-lg` | 16px (modals, bottom sheets) |
| `--radius-xl` | 24px (hero header) |
| `--radius-full` | 999px (pills, avatar, progress rings) |

### Shadows (Elevation)
```css
--shadow-1: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06);  /* Card rest */
--shadow-2: 0 4px 12px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.06);  /* Card hover */
--shadow-3: 0 8px 24px rgba(0,0,0,0.12), 0 4px 8px rgba(0,0,0,0.08);  /* Modal, dropdown */
--shadow-sticky: 0 -2px 16px rgba(0,0,0,0.08);  /* Bottom nav shadow */
```

---

## 5. Component Hierarchy

```
App (Telegram WebApp)
├── Header (sticky, gradient)
│   ├── Mascot (🐍 animated)
│   ├── App Title "EasyPython"
│   └── Subtitle "Учитель Python в стиле Duolingo"
│
├── Stats Bar (sticky, elevated card)
│   ├── Level Badge (circular, gradient)
│   ├── XP Ring Progress (conic-gradient)
│   ├── Streak Fire (animated)
│   └── Lessons Progress (segmented ring)
│
├── Badge Row (horizontal scroll)
│   └── Badge Chip × N (locked/unlocked states)
│
├── Main Content Area
│   ├── Tab Bar (Lessons / Practice / Leaderboard)
│   │
│   ├── Lessons View (default)
│   │   ├── Module Accordion × M
│   │   │   ├── Module Header (title, progress ring, chevron)
│   │   │   └── Lesson Grid (2-col mobile, 3-col tablet)
│   │   │       └── Lesson Card × N
│   │   │           ├── Lock/Active/Complete indicator
│   │   │           ├── Lesson Number Badge
│   │   │           ├── Title + Description
│   │   │           ├── Mini Progress Bar (theory / exercise / quiz)
│   │   │           ├── XP Reward Label
│   │   │           └── Action Buttons (Start / Continue / Review)
│   │   └── Empty State (celebration when all done)
│   │
│   ├── Lesson Detail Modal (Bottom Sheet on mobile)
│   │   ├── Drag Handle
│   │   ├── Header (lesson #, title, close)
│   │   ├── Theory Section (collapsible, formatted markdown)
│   │   ├── Exercise Section
│   │   │   ├── Task Description
│   │   │   ├── Code Editor (Monaco-lite / textarea with syntax highlight)
│   │   │   ├── Hint Button (expandable)
│   │   │   ├── Run / Check Button (primary)
│   │   │   └── Feedback Toast (inline success/error)
│   │   ├── Quiz Section (if lesson.quiz exists)
│   │   │   ├── Question Card (radio options, instant feedback)
│   │   │   └── Progress Dots
│   │   └── Completion Celebration (confetti, XP earned, next lesson CTA)
│   │
│   ├── Practice View (spaced repetition)
│   │   ├── Daily Challenge Card
│   │   ├── Weak Areas (adaptive)
│   │   └── Quick Fire Round (timer-based)
│   │
│   └── Leaderboard View
│       ├── Tab: Friends / Global / Weekly
│       ├── Current User Row (highlighted)
│       └── User Row × N (avatar, name, level, XP, streak)
│
├── Bottom Navigation (Telegram WebApp safe area)
│   ├── Home (Lessons) — active
│   ├── Practice (flask icon)
│   ├── Leaderboard (trophy icon)
│   └── Profile (avatar icon)
│
└── Floating Action Button (FAB) — "Continue Learning" pulse animation
    └── Opens next unlocked lesson directly
```

---

## 6. Screen Wireframes & Figma-Style Descriptions

> **Notation:**  
> `[]` = component, `{}` = state variant, `<>` = dynamic data  
> All dimensions in **dp** (density-independent pixels).  
> Mobile breakpoint: **375×667** (iPhone SE baseline).  
> Tablet breakpoint: **768×1024**.

---

### 6.1 Home / Lessons Screen (Primary)

```
┌─────────────────────────────────────────────────────────────┐
│  ╔═════════════════════════════════════════════════════════╗  │
│  ║  🐍  EasyPython          ← Gradient Header (--gradient-header)  ║  │
│  ║      Учитель Python в стиле Duolingo                       ║  │
│  ╚═════════════════════════════════════════════════════════╝  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │   LV.3   │  │   240    │  │  🔥 7    │  │  5/17    │  │  │
│  │  │  Level   │  │    XP    │  │  Streak  │  │ Lessons  │  │  │
│  │  │  ◉◉◉◉◌   │  │ ██████░░ │  │          │  │ ◉◉◉◉◌◌◌  │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │  │
│  └─────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  🏆 Первый урок  🔒 5 уроков  🔒 10 уроков  🏆 100 XP  │  │  ← horizontal scroll
│  └─────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  [Уроки ▼]  [Практика]  [Лидерборд]      ← Segmented Tab Bar  │
│  └─────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  ┌──────────────────────┐  ┌──────────────────────┐    │  │
│  │  │  📦  Модуль 1: Основы │  │  📦  Модуль 2: Управление │  │  ← Accordion headers
│  │  │  ◉◉◉◉◉◉◉◉◌◌  5/8    │  │  ◉◉◉◉◌◌◌◌◌◌  2/8    │    │
│  │  └──────────────────────┘  └──────────────────────┘    │  │
│  │  ┌─────────────┐ ┌─────────────┐  ← Lesson Grid (2-col)  │
│  │  │  1  Привет!  │ │  2  Перем.  │                           │
│  │  │  ✅ Пройдено │ │  🟢 Активен │                           │
│  │  │  ████████████ │ │  ██████░░░░ │                           │
│  │  │  +10 XP      │ │  +10 XP     │                           │
│  │  │  [Пройдено]  │ │  [Начать]   │                           │
│  │  │  [Повторить] │ │  [Теория]   │                           │
│  │  └─────────────┘ └─────────────┘                           │
│  │  ┌─────────────┐ ┌─────────────┐                           │
│  │  │  3  Операции │ │  4  Ввод    │                           │
│  │  │  🔒 Заблок.  │ │  🔒 Заблок. │                           │
│  │  │  ░░░░░░░░░░  │ │  ░░░░░░░░░░  │                           │
│  │  │  [Заблокиров.]│ │  [Заблокиров.]│                          │
│  │  └─────────────┘ └─────────────┘                           │
│  └─────────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  🟢  Продолжить урок 2    ← FAB (pulse animation)        │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

#### Component Specs

| Component | States | Key Interactions |
|-----------|--------|------------------|
| **Gradient Header** | Default | Parallax scroll (mascot moves slightly) |
| **Stat Card** | Default / Loading skeleton | Tap → detail modal (level breakdown, streak calendar) |
| **XP Ring** | Animated on XP gain | Conic-gradient fill, 600ms spring |
| **Streak Fire** | Idle / Burning (streak>0) / Celebration (streak milestones) | Lottie-style CSS animation |
| **Badge Chip** | Locked (gray, 🔒) / Unlocked (green, 🏆) / New (pulse ring) | Tap → tooltip with requirement |
| **Module Accordion** | Collapsed / Expanded / Loading | Chevron rotate 180°, height auto animate |
| **Lesson Card** | Locked / Active / Completed / Current (pulse border) | Tap primary → open lesson; Tap secondary → theory only |
| **Mini Progress Bar** | 0% / Partial / 100% | Three segments: theory, exercise, quiz |
| **FAB** | Hidden (scrolled top) / Visible / Pulse (next lesson ready) | Tap → open next unlocked lesson |

---

### 6.2 Lesson Detail Modal (Bottom Sheet)

```
┌─────────────────────────────────────────────────────────────┐
│  ══════════════════════════════════════════════════════════  ← Drag handle
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Урок 2: Переменные и типыデータ        [×] Close     │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  📚 Теория                                    [▼]      │  │  ← Collapsible
│  │  ─────────────────────────────────────────────────    │  │
│  │  Где: В любой программе, где нужно хранить данные... │  │
│  │  Типы: int, float, str, bool                         │  │
│  │  ```python                                           │  │
│  │  name = 'Alex'     # str                             │  │
│  │  age = 25          # int                             │  │
│  │  is_student = True # bool                            │  │
│  │  ```                                                 │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  📝 Задание                                            │  │
│  │  ─────────────────────────────────────────────────    │  │
│  │  Создайте три переменные: name (строка), age (целое), │  │
│  │  is_student (булево). Выведите их через print().      │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │ name = 'Alex'                                   │  │  │  ← Code Editor
│  │  │ age = 25                                        │  │  │     (monospace,
│  │  │ is_student = True                               │  │  │      syntax highlight)
│  │  │ print(name)                                     │  │  │
│  │  │ print(age)                                      │  │  │
│  │  │ print(is_student)                               │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  │  [💡 Подсказка]  ▼                                    │  │  ← Expandable hint
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │ Сначала создайте переменные отдельными строками,│  │  │
│  │  │ потом выведите их через print(). Внутри print() │  │  │
│  │  │ нельзя писать присваивание.                     │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  │  ─────────────────────────────────────────────────    │  │
│  │  [       Проверить ответ       ]  ← Primary BTN       │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  ❓ Квиз (1/1)                                        │  │
│  │  ─────────────────────────────────────────────────    │  │
│  │  Какой тип у переменной x = 5?                        │  │
│  │  ○ int       ● str       ○ bool       ○ list          │  │
│  │  ◉◉◉◉◉◉◉◉◌◌  Progress dots                            │  │
│  │  [Следующий вопрос]                                   │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

#### States & Transitions

| Trigger | From State | To State | Animation |
|---------|------------|----------|-----------|
| Tap lesson card | Lessons Grid | Lesson Modal (bottom sheet) | Slide up 300ms cubic-bezier(0.25, 0.46, 0.45, 0.94) |
| Correct answer | Exercise | Success Toast + Confetti + XP Ring fill | Confetti 800ms, XP ring 600ms spring |
| Wrong answer | Exercise | Error Toast + Shake editor | Shake 400ms, toast slide down |
| All exercises done | Exercise | Completion Celebration | Full-screen confetti, XP counter animate, "Next Lesson" CTA |
| Drag down / Tap backdrop | Lesson Modal | Lessons Grid | Slide down 250ms |
| Tap "Theory" on completed | Lessons Grid | Lesson Modal (read-only) | Same slide up, editor disabled |

---

### 6.3 Practice Screen (Spaced Repetition)

```
┌─────────────────────────────────────────────────────────────┐
│  ╔═════════════════════════════════════════════════════════╗  │
│  ║  🧪  Практика — Ежедневный вызов                        ║  │
│  ╚═════════════════════════════════════════════════════════╝  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  🎯  Дневной челлендж: 3 задания за 50 XP               │  │
│  │  ⏱  Осталось времени: 12:34                            │  │
│  │  [Начать]  ← Primary, large tap target                  │  │
│  └─────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  📉  Твои слабые места (адаптивно)                      │  │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │  │
│  │  │  Циклы for  │ │  Условия    │ │  Списки     │       │  │
│  │  │  45% мастер.│ │  60% мастер.│ │  70% мастер.│       │  │
│  │  │  [Тренировка]│ │  [Тренировка]│ │  [Тренировка]│      │  │
│  │  └─────────────┘ └─────────────┘ └─────────────┘       │  │
│  └─────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  ⚡  Быстрый раунд — 60 секунд                          │  │
│  │  ❓  print(2 ** 3) → ?                                  │  │
│  │  [6] [8] [9] [Ошибка]   ← Large option buttons         │  │
│  │  ◉◉◉◉◉◉◉◉◌◌  8/10    ⏱ 0:45                           │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

### 6.4 Leaderboard Screen

```
┌─────────────────────────────────────────────────────────────┐
│  ╔═════════════════════════════════════════════════════════╗  │
│  ║  🏆  Лидерборд                    [👥 Друзья] [🌍 Все]  ║  │
│  ╚═════════════════════════════════════════════════════════╝  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  #  Аватар    Имя           Уровень  XP    Стрик       │  │
│  │  1  👑  @alex_coder    LV.8   1,240  🔥 23             │  │
│  │  2  🥈  @maria_py      LV.7   1,100  🔥 18             │  │
│  │  3  🥉  @python_nub    LV.6   980    🔥 12             │  │
│  │  …                                                │  │
│  │  12  🟢  @you          LV.3   240    🔥 7    ← You     │  │
│  └─────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  🎖  Твои достижения этой недели:                       │  │
│  │  +150 XP  •  3 урока  •  7 дней подряд  •  1 квиз      │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

### 6.5 Profile / Settings Bottom Sheet

```
┌─────────────────────────────────────────────────────────────┐
│  ══════════════════════════════════════════════════════════  ← Drag handle
│  ┌───────────────────────────────────────────────────────┐  │
│  │  👤  @username                    [✏️ Редактировать]  │  │
│  │  LV.3  🐍 Pythonista            240 / 300 XP         │  │
│  │  ████████████░░░░░░░░░░  80% до LV.4                  │  │
│  │  🔥 7 дней подряд  •  5/17 уроков  •  12 бейджей     │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  🏆  Бейджи                                          │  │
│  │  [🏆 Первый урок] [🏆 5 уроков] [🔒 10 уроков] ...   │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  ⚙️  Настройки                                       │  │
│  │  [🔔 Уведомления]      Вкл/Выкл                       │  │
│  │  [🌙 Тёмная тема]      Авто / Светлая / Тёмная        │  │
│  │  [🔊 Звуки]            Вкл/Выкл                       │  │
│  │  [🎉 Анимации]         Вкл / Умеренные / Выкл         │  │
│  │  [🗑️ Сбросить прогресс]  ← Destructive, confirmation  │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  ℹ️  О приложении  v1.2.0                             │  │
│  │  EasyPython — учите Python в Telegram                 │  │
│  │  [Политика конфиденциальности] [Поддержка]            │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 7. Interaction & Motion Specifications

### 7.1 Micro-animations

| Trigger | Animation | Duration | Easing |
|---------|-----------|----------|--------|
| Lesson card hover/tap | `transform: translateY(-2px) scale(1.01)` | 150ms | `cubic-bezier(0.25, 0.46, 0.45, 0.94)` |
| XP ring fill on correct | `conic-gradient` from current% → new% | 600ms | `spring(1, 80, 10)` |
| Streak fire burn | CSS keyframes: scale 1→1.1→1, opacity pulse | 1000ms loop | `ease-in-out` |
| Badge unlock | Scale 0→1.2→1 + green ring expand | 500ms | `cubic-bezier(0.34, 1.56, 0.64, 1)` |
| Confetti burst | 30 particles, random velocity, fade out | 1200ms | `cubic-bezier(0.25, 0.46, 0.45, 0.94)` |
| Modal slide up/down | `translateY(100%) → 0` / `0 → 100%` | 300ms / 250ms | `cubic-bezier(0.25, 0.46, 0.45, 0.94)` |
| Tab switch | Cross-fade + indicator slide | 200ms | `ease-out` |
| Accordion expand | `max-height: 0 → content` + chevron rotate | 300ms | `cubic-bezier(0.25, 0.46, 0.45, 0.94)` |
| Button press (active) | `scale(0.98)` | 100ms | `ease-out` |
| FAB pulse | `box-shadow` spread 0→20px, opacity 0.4→0 | 1500ms loop | `ease-in-out` |

### 7.2 Reduced Motion (`prefers-reduced-motion: reduce`)

- Disable all loops (streak fire, FAB pulse, confetti)
- Instant transitions (0ms) for slide, fade, scale
- Keep functional feedback (color change, checkmark)

---

## 8. Accessibility (WCAG 2.1 AA)

| Requirement | Implementation |
|-------------|----------------|
| **Contrast** | All text ≥ 4.5:1 (large text ≥ 3:1) against background |
| **Focus Visible** | 3px solid `#1A73E8` outline + 2px offset on all interactive elements |
| **Touch Targets** | Minimum 48×48 dp (Telegram WebApp guideline) |
| **Screen Reader** | Semantic HTML: `<header>`, `<main>`, `<section>`, `<button>`, `aria-label`, `aria-expanded`, `aria-live="polite"` for toasts |
| **Keyboard** | Full Tab navigation, Enter/Space activate, Escape closes modals |
| **Language** | `lang="ru"` on `<html>`, `lang="en"` on code snippets |
| **Reduced Motion** | Respect `prefers-reduced-motion` media query |
| **Dark Mode** | Full support via `prefers-color-scheme` + manual toggle |

---

## 9. Responsive Breakpoints

| Breakpoint | Width | Layout Changes |
|------------|-------|----------------|
| **Mobile** | 320–480px | 2-col lesson grid, bottom sheet modals, FAB, sticky header+stats |
| **Large Mobile** | 481–767px | 2-col lesson grid, modal centered (max-width 480px) |
| **Tablet** | 768–1023px | 3-col lesson grid, side-by-side theory/exercise, modal 600px |
| **Desktop** | ≥1024px | 4-col lesson grid, two-panel layout (lessons list + detail), no bottom nav |

---

## 10. Telegram WebApp Integration Notes

| Feature | Implementation |
|---------|----------------|
| **Header Color** | `tg.setHeaderColor('#4CAF50')` (matches gradient start) |
| **Background Color** | `tg.setBackgroundColor('#F5F7FA')` |
| **Expand** | `tg.expand()` on load |
| **Haptic Feedback** | `tg.HapticFeedback.impactOccurred('light')` on button tap; `'medium'` on correct answer; `'heavy'` on error |
| **Main Button** | `tg.MainButton.setText('Продолжить')` → shows next lesson CTA in Telegram UI |
| **Back Button** | `tg.BackButton.show()` in lesson modal; hides on close |
| **Safe Area** | CSS `env(safe-area-inset-bottom)` for bottom nav/FAB |
| **Theme Params** | Read `tg.themeParams` for `bg_color`, `text_color`, `button_color` to auto-adapt |

---

## 11. Implementation Roadmap (Phased)

| Phase | Scope | Components | Est. Effort |
|-------|-------|------------|-------------|
| **1. Foundation** | Design tokens, CSS variables, typography, reset | `design-tokens.css`, `variables.css`, `typography.css` | 1 day |
| **2. Core Layout** | Header, Stats Bar, Badge Row, Tab Bar, Bottom Nav | `Header`, `StatsBar`, `BadgeRow`, `TabBar`, `BottomNav` | 2 days |
| **3. Lessons Grid** | Module Accordion, Lesson Card (all states), Mini Progress | `ModuleAccordion`, `LessonCard`, `MiniProgressBar` | 2 days |
| **4. Lesson Modal** | Bottom sheet, Theory (markdown render), Code Editor, Quiz, Feedback | `LessonModal`, `CodeEditor`, `Quiz`, `FeedbackToast` | 3 days |
| **5. Gamification** | XP Ring, Streak Fire, Confetti, Badge Unlock, Level Up | `XPRing`, `StreakFire`, `Confetti`, `Badge`, `LevelUp` | 2 days |
| **6. Practice & Leaderboard** | Daily Challenge, Weak Areas, Quick Fire, Leaderboard Table | `PracticeView`, `LeaderboardView` | 2 days |
| **7. Profile & Settings** | Profile Sheet, Badge Gallery, Settings Toggles | `ProfileSheet`, `Settings` | 1 day |
| **8. Polish & A11y** | Reduced motion, dark mode, focus styles, i18n prep, testing | — | 2 days |

**Total:** ~15 days for full Duolingo-style experience.

---

## 12. Code Snippets — Critical Components

### 12.1 CSS Custom Properties (design-tokens.css)

```css
/* ===================================================================
   EasyPython Design Tokens — Duolingo-inspired
   =================================================================== */
:root {
  /* Brand */
  --color-primary: #4CAF50;
  --color-primary-dark: #2E7D32;
  --color-primary-light: #E8F5E9;
  --color-accent-blue: #1A73E8;
  --color-accent-orange: #FF9800;
  --color-accent-purple: #7B1FA2;

  /* Semantic Light */
  --bg-primary: #F5F7FA;
  --bg-surface: #FFFFFF;
  --bg-elevated: #FFFFFF;
  --text-primary: #212121;
  --text-secondary: #757575;
  --text-disabled: #9E9E9E;
  --border-color: #E0E0E0;
  --error: #C62828;
  --error-bg: #FFEBEE;
  --success: #2E7D32;
  --success-bg: #E8F5E9;
  --warning: #FF9800;
  --warning-bg: #FFF3E0;

  /* Gradients */
  --gradient-header: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  --gradient-primary: linear-gradient(180deg, var(--color-primary) 0%, #43A047 100%);
  --gradient-streak: linear-gradient(135deg, var(--color-accent-orange) 0%, #F57C00 100%);
  --gradient-level: linear-gradient(135deg, var(--color-accent-blue) 0%, #1565C0 100%);

  /* Spacing */
  --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px;
  --space-5: 20px; --space-6: 24px; --space-8: 32px; --space-10: 40px;

  /* Radius */
  --radius-sm: 8px; --radius-md: 12px; --radius-lg: 16px; --radius-xl: 24px; --radius-full: 999px;

  /* Shadows */
  --shadow-1: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06);
  --shadow-2: 0 4px 12px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.06);
  --shadow-3: 0 8px 24px rgba(0,0,0,0.12), 0 4px 8px rgba(0,0,0,0.08);
  --shadow-sticky: 0 -2px 16px rgba(0,0,0,0.08);

  /* Typography */
  --font-display: 'Nunito', system-ui, sans-serif;
  --font-body: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  --text-display-lg: clamp(28px, 5vw, 32px);
  --text-display-md: clamp(22px, 4vw, 24px);
  --text-headline: clamp(18px, 3.5vw, 20px);
  --text-title-lg: 18px; --text-title-md: 16px;
  --text-body-lg: 16px; --text-body-md: 14px; --text-body-sm: 12px;
  --text-label-lg: 14px; --text-label-sm: 11px;
  --text-code: 13px;

  /* Transitions */
  --ease-standard: cubic-bezier(0.25, 0.46, 0.45, 0.94);
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
  --duration-fast: 150ms; --duration-normal: 250ms; --duration-slow: 350ms;
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #121212;
    --bg-surface: #1E1E1E;
    --bg-elevated: #2D2D2D;
    --text-primary: #FFFFFF;
    --text-secondary: #B0B0B0;
    --text-disabled: #707070;
    --border-color: #3A3A3A;
    --error: #EF5350; --error-bg: #3E1616;
    --success: #66BB6A; --success-bg: #163E16;
    --warning: #FFB74D; --warning-bg: #3E2A00;
    --shadow-1: 0 1px 3px rgba(0,0,0,0.3), 0 1px 2px rgba(0,0,0,0.2);
    --shadow-2: 0 4px 12px rgba(0,0,0,0.4), 0 2px 4px rgba(0,0,0,0.3);
    --shadow-3: 0 8px 24px rgba(0,0,0,0.5), 0 4px 8px rgba(0,0,0,0.4);
  }
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### 12.2 Lesson Card Component (Vanilla JS + CSS)

```html
<!-- lesson-card.html (template) -->
<article class="lesson-card" data-lesson-id="{{id}}" data-state="{{state}}">
  <!-- State: locked | active | completed | current -->
  <div class="lesson-card__status" aria-hidden="true">
    <span class="status-indicator"></span>
  </div>

  <header class="lesson-card__header">
    <span class="lesson-card__number">Урок {{id}}</span>
    <h3 class="lesson-card__title">{{title}}</h3>
  </header>

  <p class="lesson-card__desc">{{description}}</p>

  <div class="lesson-card__progress" role="progressbar" aria-valuenow="{{progress}}" aria-valuemin="0" aria-valuemax="100" aria-label="Прогресс урока">
    <div class="lesson-card__progress-fill" style="width: {{progress}}%"></div>
    <!-- Segmented: theory / exercise / quiz -->
    <div class="lesson-card__progress-segments" aria-hidden="true">
      <span style="--segment-width: {{theoryPct}}%"></span>
      <span style="--segment-width: {{exercisePct}}%"></span>
      <span style="--segment-width: {{quizPct}}%"></span>
    </div>
  </div>

  <div class="lesson-card__xp" aria-label="Награда: {{xp}} XP">
    <span class="xp-icon">⭐</span> +{{xp}} XP
  </div>

  <div class="lesson-card__actions">
    <button class="btn btn--primary" {{disabled}} data-action="start">
      {{primaryText}}
    </button>
    <button class="btn btn--secondary" {{disabled}} data-action="theory">
      {{secondaryText}}
    </button>
  </div>
</article>
```

```css
/* lesson-card.css */
.lesson-card {
  background: var(--bg-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-4);
  box-shadow: var(--shadow-1);
  border: 2px solid transparent;
  transition: transform var(--duration-fast) var(--ease-standard),
              box-shadow var(--duration-fast) var(--ease-standard),
              border-color var(--duration-fast) var(--ease-standard);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  min-height: 200px; /* consistent height */
}

.lesson-card:hover:not(.lesson-card--locked) {
  transform: translateY(-2px);
  box-shadow: var(--shadow-2);
}

.lesson-card:active:not(.lesson-card--locked) {
  transform: translateY(0) scale(0.99);
}

/* States */
.lesson-card--locked {
  opacity: 0.6;
  filter: grayscale(0.4);
  pointer-events: none;
}

.lesson-card--completed {
  border-color: var(--color-primary);
}

.lesson-card--active {
  border-color: var(--color-accent-blue);
}

.lesson-card--current {
  animation: pulse-border 2s ease-in-out infinite;
}

@keyframes pulse-border {
  0%, 100% { border-color: var(--color-accent-blue); box-shadow: 0 0 0 0 rgba(26,115,232,0.4); }
  50% { border-color: var(--color-primary); box-shadow: 0 0 0 4px rgba(76,175,80,0.2); }
}

/* Progress bar */
.lesson-card__progress {
  height: 6px;
  background: var(--border-color);
  border-radius: var(--radius-full);
  overflow: hidden;
  position: relative;
}

.lesson-card__progress-fill {
  height: 100%;
  background: var(--gradient-primary);
  border-radius: var(--radius-full);
  transition: width var(--duration-slow) var(--ease-standard);
}

.lesson-card__progress-segments {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  display: flex;
}

.lesson-card__progress-segments span {
  flex: 1;
  background: repeating-linear-gradient(
    90deg,
    transparent,
    transparent calc(var(--segment-width) - 2px),
    rgba(0,0,0,0.1) calc(var(--segment-width) - 2px),
    rgba(0,0,0,0.1) var(--segment-width)
  );
}

/* Buttons */
.lesson-card__actions {
  display: flex;
  gap: var(--space-2);
  margin-top: auto;
}

.btn {
  flex: 1;
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-sm);
  font: 600 var(--text-label-lg) var(--font-body);
  cursor: pointer;
  transition: background var(--duration-fast), transform var(--duration-fast);
  border: 2px solid transparent;
}

.btn:active { transform: scale(0.98); }
.btn:disabled { opacity: 0.5; cursor: not-allowed; }

.btn--primary {
  background: var(--gradient-primary);
  color: white;
  border-color: var(--color-primary-dark);
}

.btn--primary:hover:not(:disabled) {
  filter: brightness(1.05);
}

.btn--secondary {
  background: var(--bg-surface);
  color: var(--color-primary);
  border-color: var(--color-primary);
}

.btn--secondary:hover:not(:disabled) {
  background: var(--color-primary-light);
}
```

### 12.3 XP Ring Component (Conic Gradient)

```html
<div class="xp-ring" role="img" aria-label="Опыт: 240 из 300 XP до следующего уровня">
  <svg class="xp-ring__svg" viewBox="0 0 100 100" aria-hidden="true">
    <circle class="xp-ring__bg" cx="50" cy="50" r="45" fill="none" stroke="var(--border-color)" stroke-width="8"/>
    <circle class="xp-ring__progress" cx="50" cy="50" r="45" fill="none" stroke="url(#xp-gradient)" stroke-width="8" stroke-linecap="round" style="--progress: 0.8"/>
    <defs>
      <linearGradient id="xp-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#4CAF50"/>
        <stop offset="100%" stop-color="#1A73E8"/>
      </linearGradient>
    </defs>
  </svg>
  <div class="xp-ring__content">
    <span class="xp-ring__level">LV.{{level}}</span>
    <span class="xp-ring__xp">{{xp}} / {{nextLevelXp}} XP</span>
  </div>
</div>
```

```css
.xp-ring {
  width: 80px; height: 80px;
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.xp-ring__svg { width: 100%; height: 100%; transform: rotate(-90deg); }

.xp-ring__progress {
  stroke-dasharray: 283; /* 2 * PI * 45 */
  stroke-dashoffset: calc(283 * (1 - var(--progress)));
  transition: stroke-dashoffset 600ms var(--ease-spring);
}

.xp-ring__content {
  position: absolute;
  text-align: center;
  pointer-events: none;
}

.xp-ring__level {
  display: block;
  font: 700 16px var(--font-display);
  background: var(--gradient-level);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.xp-ring__xp {
  font: 400 11px var(--font-body);
  color: var(--text-secondary);
}
```

---

## 13. Assets & Resources Needed

| Asset | Format | Specs | Source |
|-------|--------|-------|--------|
| **Mascot (🐍 Python)** | Lottie JSON / SVG + CSS | 3 states: idle, celebrate, think | Custom or [LottieFiles](https://lottiefiles.com) |
| **Streak Fire** | Lottie JSON | Looping, 3 sizes (24/32/48dp) | Custom |
| **Confetti** | Canvas/JS (no external) | 30 particles, brand colors | `confetti.js` (lightweight) |
| **Badge Icons** | SVG | 24×24, 6 variants | Custom |
| **Illustrations** | SVG | Empty states, celebrations | [undraw.co](https://undraw.co) or custom |
| **Fonts** | WOFF2 | Inter, Nunito, JetBrains Mono | Google Fonts (self-hosted) |

---

## 14. Acceptance Criteria (Definition of Done)

| Criterion | Verification |
|-----------|--------------|
| **Visual parity** | Matches wireframes ±2px on mobile (375px) and tablet (768px) |
| **Theme support** | Light/Dark auto + manual toggle works without flash |
| **Reduced motion** | All animations disable via OS setting |
| **Keyboard nav** | Tab order logical, focus visible, Escape closes modals |
| **Screen reader** | NVDA/VoiceOver announces progress, states, toasts |
| **Touch targets** | All interactive ≥48×48dp |
| **Performance** | LCP < 2.5s, CLS < 0.1, TBT < 150ms on 3G |
| **Telegram WebApp** | Header/bg colors set, Main/Back buttons work, haptics fire |
| **Offline** | Service worker caches lessons; stale-while-revalidate |
| **i18n ready** | All strings extracted to `messages.json` (ru/en placeholders) |

---

## 15. Appendix — Current Codebase Mapping

| Existing File | Current UI | Target Component |
|---------------|------------|------------------|
| `app/main.py` (lines 43–592) | Single-page HTML with inline CSS/JS | Split into: `index.html`, `styles.css`, `app.js`, components/ |
| `lessons.py` | `LESSONS` array with theory/exercise/quiz | API `/lessons`, `/lesson/:id` (already exists) |
| `database.py` | SQLite with xp, level, streak, badges | Used by `/progress`, `/save-progress`, `/leaderboard` |
| `test_mini_app.py` | Unit tests for lesson checking | Extend with E2E (Playwright) for UI flows |

---

*End of Design Specification*  
*Ready for implementation handoff to Frontend Engineer*