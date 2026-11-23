"""Структура базы данных и работа с прогрессом учеников."""

import os
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional


class Database:
    """Хранит прогресс учеников в SQLite."""

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None
        self._init_db()

    # ------------------------------------------------------------------ #
    # Служебные методы
    # ------------------------------------------------------------------ #
    def _connect(self) -> sqlite3.Connection:
        if self._conn is None:
            # check_same_thread=False: FastAPI выполняет синхронные обработчики
            # в пуле потоков, поэтому соединение переиспользуется из разных потоков.
            self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
        return self._conn

    def _init_db(self) -> None:
        conn = self._connect()
        cur = conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                user_id        INTEGER PRIMARY KEY,
                username       TEXT,
                first_name     TEXT,
                completed      TEXT DEFAULT '',
                xp             INTEGER DEFAULT 0,
                level          INTEGER DEFAULT 1,
                score          INTEGER DEFAULT 0,
                streak         INTEGER DEFAULT 0,
                created_at     TEXT,
                last_activity  TEXT
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS attempts (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER,
                lesson_id   INTEGER,
                answer      TEXT,
                is_correct  INTEGER,
                created_at  TEXT
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS badges (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER,
                name        TEXT,
                earned_at   TEXT
            )
            """
        )

        # Таблица для хранения состояния "ожидаем ответ"
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS pending_answers (
                user_id      INTEGER,
                lesson_id    INTEGER,
                PRIMARY KEY (user_id)
            )
            """
        )

        # Миграция: добавляем колонки xp, level если их нет
        cur.execute("PRAGMA table_info(students)")
        columns = {row["name"] for row in cur.fetchall()}
        if "xp" not in columns:
            cur.execute("ALTER TABLE students ADD COLUMN xp INTEGER DEFAULT 0")
        if "level" not in columns:
            cur.execute("ALTER TABLE students ADD COLUMN level INTEGER DEFAULT 1")

        conn.commit()
        # Соединение не закрываем — будем переиспользовать его

    # ------------------------------------------------------------------ #
    # Состояние "ожидаем ответ" (pending_answers)
    # ------------------------------------------------------------------ #
    def set_pending(self, user_id: int, lesson_id: int) -> None:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO pending_answers (user_id, lesson_id) VALUES (?, ?)"
            " ON CONFLICT(user_id) DO UPDATE SET lesson_id = excluded.lesson_id",
            (user_id, lesson_id),
        )
        conn.commit()

    def get_pending(self, user_id: int) -> Optional[int]:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "SELECT lesson_id FROM pending_answers WHERE user_id = ?",
            (user_id,),
        )
        row = cur.fetchone()
        return row["lesson_id"] if row else None

    def clear_pending(self, user_id: int) -> None:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM pending_answers WHERE user_id = ?",
            (user_id,),
        )
        conn.commit()

    # ------------------------------------------------------------------ #
    # Ученики
    # ------------------------------------------------------------------ #
    def get_or_create(self, user_id: int, username: str | None,
                      first_name: str | None) -> Dict:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE user_id = ?", (user_id,))
        row = cur.fetchone()

        if row is None:
            now = datetime.now().isoformat(timespec="seconds")
            cur.execute(
                "INSERT INTO students (user_id, username, first_name, created_at,"
                " last_activity) VALUES (?, ?, ?, ?, ?)",
                (user_id, username, first_name, now, now),
            )
            conn.commit()
            cur.execute("SELECT * FROM students WHERE user_id = ?", (user_id,))
            row = cur.fetchone()

        return self._to_dict(row)

    def get(self, user_id: int) -> Optional[Dict]:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        return self._to_dict(row) if row else None

    # ------------------------------------------------------------------ #
    # Прогресс
    # ------------------------------------------------------------------ #
    def completed_ids(self, user_id: int) -> List[int]:
        student = self.get(user_id)
        if not student:
            return []
        raw = student.get("completed") or ""
        return [int(x) for x in raw.split(",") if x.strip().isdigit()]

    def mark_completed(self, user_id: int, lesson_id: int, points: int = 10) -> None:
        completed = self.completed_ids(user_id)
        if lesson_id in completed:
            return

        completed.append(lesson_id)
        completed.sort()

        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "UPDATE students SET score = score + ?, completed = ?, last_activity = ? WHERE user_id = ?",
            (
                points,
                ",".join(str(x) for x in completed),
                datetime.now().isoformat(timespec="seconds"),
                user_id,
            ),
        )
        conn.commit()

    def log_attempt(self, user_id: int, lesson_id: int,
                    answer: str, is_correct: bool) -> None:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO attempts (user_id, lesson_id, answer, is_correct, created_at)"
            " VALUES (?, ?, ?, ?, ?)",
            (
                user_id,
                lesson_id,
                answer[:1000],
                1 if is_correct else 0,
                datetime.now().isoformat(timespec="seconds"),
            ),
        )
        conn.commit()

    def stats(self, user_id: int) -> Dict:
        student = self.get(user_id) or {}
        completed = self.completed_ids(user_id)

        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "SELECT COUNT(*) AS total, COALESCE(SUM(is_correct), 0) AS correct"
            " FROM attempts WHERE user_id = ?",
            (user_id,),
        )
        row = cur.fetchone()

        return {
            "completed": completed,
            "completed_count": len(completed),
            "score": student.get("score", 0),
            "attempts": row["total"] if row else 0,
            "correct": row["correct"] if row else 0,
        }

    def reset(self, user_id: int) -> None:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "UPDATE students SET completed = '', score = 0, xp = 0, level = 1 WHERE user_id = ?",
            (user_id,),
        )
        cur.execute("DELETE FROM attempts WHERE user_id = ?", (user_id,))
        conn.commit()

    def get_all_students(self) -> List[Dict]:
        """Возвращает всех учеников для лидерборда."""
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "SELECT user_id, username, first_name, xp, level, completed, streak"
            " FROM students ORDER BY xp DESC LIMIT 20"
        )
        rows = cur.fetchall()
        return [self._to_dict(row) for row in rows]

    def award_badge(self, user_id: int, badge_name: str) -> None:
        """Назначает бейдж пользователю."""
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO badges (user_id, name, earned_at) VALUES (?, ?, ?)",
            (user_id, badge_name, datetime.now().isoformat(timespec="seconds")),
        )
        conn.commit()

    def get_badges(self, user_id: int) -> List[str]:
        """Возвращает список бейджей пользователя."""
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "SELECT name FROM badges WHERE user_id = ?",
            (user_id,),
        )
        rows = cur.fetchall()
        return [row["name"] for row in rows]


    # ------------------------------------------------------------------ #
    @staticmethod
    def _to_dict(row: sqlite3.Row) -> Dict:
        return {key: row[key] for key in row.keys()}
