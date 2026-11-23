#!/usr/bin/env python3
"""Тест EasyPython Mini App - проверка всех уроков, правильных и неправильных ответов"""

import sys
import urllib.error
sys.path.insert(0, '/Users/samir/Documents/deepseek-harness/default-workspace/bot_v2')

from lessons import LESSONS, GLOSSARY

def test_all_lessons_correct():
    """Тест: все уроки принимают правильные ответы"""
    print("=" * 60)
    print("ТЕСТ 1: Все уроки принимают правильные ответы")
    print("=" * 60)
    
    all_passed = True
    for lesson in LESSONS:
        result = lesson.check_answer(lesson.correct_answer)
        status = "✅" if result else "❌"
        print(f"{status} Урок {lesson.id}: {lesson.title}")
        if not result:
            all_passed = False
            print(f"   ОШИБКА: правильный ответ не принят!")
    
    if all_passed:
        print("\n✅ Все уроки принимают правильные ответы")
    else:
        print("\n❌ Некоторые уроки не принимают правильные ответы")
    return all_passed

def test_common_incorrect_answers():
    """Тест: распространённые неправильные ответы"""
    print("\n" + "=" * 60)
    print("ТЕСТ 2: Проверка неправильных ответов")
    print("=" * 60)
    
    test_cases = [
        # (lesson_id, wrong_answer, expected_correct)
        (1, "print (\"Hello, World!\")", False),  # пробел между print и (
        (1, "Hello, World!", False),  # без print
        (1, "print(Hello, World!)", False),  # без кавычек
        (1, "print()", False),  # пустой print
        (2, "name = 'Alex', age = 25", False),  # одна строка без print
        (2, "print(name = 'Alex')", False),  # присваивание внутри print
        (2, "name = 'Alex'\nprint(name)", True),  # переменные + print
        (5, "if age > 0\n    print('Positive')", False),  # без двоеточия
        (6, "for i in range(5):\nprint(i)", False),  # неправильный range
        (10, "f = open('test.txt', 'w')", False),  # без with
        (11, "try:\n    x = 1/0", False),  # без except
        (12, "import math\nprint(sqrt(16))", False),  # без math.
        (13, "class Dog:\n    def bark():\n        return \"Gav-gav!\"", False),  # без self
    ]
    
    all_passed = True
    for lesson_id, wrong_answer, expected in test_cases:
        lesson = LESSONS[lesson_id - 1]
        result = lesson.check_answer(wrong_answer)
        status = "✅" if result == expected else "❌"
        print(f"{status} Урок {lesson_id}: '{wrong_answer[:50]}...' -> {result} (ожидалось: {expected})")
        if result != expected:
            all_passed = False
    
    if all_passed:
        print("\n✅ Все тесты на неправильные ответы пройдены")
    else:
        print("\n❌ Некоторые тесты провалены")
    return all_passed

def test_error_fix_function():
    """Тест функции get_error_fix из main.py"""
    print("\n" + "=" * 60)
    print("ТЕСТ 3: Функция get_error_fix (анализ ошибок)")
    print("=" * 60)
    
    try:
        import main as main_module
        fix_func = main_module.get_error_fix
    except:
        print("Не удалось импортировать get_error_fix из main.py")
        return False
    
    test_cases = [
        ("print (\"Hello\")", "print(\"Hello\")", "пробел между print и ("),
        ("print(name = 'Alex')", "print(\"Hello\")", "присваивание внутри print"),
        ("Hello, World!", "print(\"Hello, World!\")", "нет print"),
        ("print(Hello)", "print(\"Hello\")", "нет кавычек"),
        ("print()", "print(\"Hello\")", "пустой print"),
    ]
    
    all_passed = True
    for user_code, correct_code, description in test_cases:
        fix = fix_func(user_code, correct_code)
        if fix and "Что исправить" in fix:
            print(f"✅ {description}: фикс найден")
        else:
            print(f"❌ {description}: фикс НЕ найден")
            all_passed = False
    
    return all_passed

def test_database():
    """Тест базы данных"""
    print("\n" + "=" * 60)
    print("ТЕСТ 4: База данных")
    print("=" * 60)
    
    from database import Database
    import tempfile
    import os
    
    test_db_path = tempfile.mktemp(suffix=".db")
    db = Database(test_db_path)
    
    # Тест создания пользователя
    student = db.get_or_create(123, "testuser", "Test")
    print(f"✅ Пользователь создан: {student.get('user_id')}")
    
    # Тест completed_ids
    completed = db.completed_ids(123)
    print(f"✅ Пройденные уроки: {completed}")
    
    # Тест mark_completed
    db.mark_completed(123, 1, points=10)
    completed = db.completed_ids(123)
    print(f"✅ После прохождения урока 1: {completed}")
    
    # Тест stats
    stats = db.stats(123)
    print(f"✅ Статистика: {stats}")
    
    # Тест сброса
    db.reset(123)
    completed = db.completed_ids(123)
    print(f"✅ После сброса: {completed}")
    
    # Очистка
    os.remove(test_db_path)
    print("✅ Тест базы данных пройден")
    return True

def test_all_endpoints():
    """Тест всех API endpoints"""
    print("\n" + "=" * 60)
    print("ТЕСТ 5: API Endpoints")
    print("=" * 60)
    
    import urllib.request
    import json
    
    base_url = "http://localhost:8000"
    
    tests = [
        ("GET", "/health", None, 200),
        ("GET", "/progress", None, 200),
        ("GET", "/lessons", None, 200),
        ("GET", "/lesson/1", None, 200),
        ("GET", "/lesson/99", None, 404),
    ]
    
    all_passed = True
    for method, path, payload, expected_status in tests:
        try:
            if method == "GET":
                try:
                    response = urllib.request.urlopen(f"{base_url}{path}", timeout=5)
                    status = response.getcode()
                    data = json.loads(response.read().decode())
                except urllib.error.HTTPError as e:
                    status = e.code
                    body = e.read().decode()
                    try:
                        data = json.loads(body)
                    except:
                        data = {}
            else:
                data = json.dumps(payload).encode()
                req = urllib.request.Request(
                    f"{base_url}{path}",
                    data=data,
                    headers={"Content-Type": "application/json"},
                    method=method
                )
                try:
                    response = urllib.request.urlopen(req, timeout=5)
                    status = response.getcode()
                except urllib.error.HTTPError as e:
                    status = e.code
                    body = e.read().decode()
                    try:
                        data = json.loads(body)
                    except:
                        data = {}
            
            if status == expected_status:
                print(f"✅ {method} {path} -> {status}")
            else:
                print(f"❌ {method} {path} -> {status} (ожидалось {expected_status})")
                all_passed = False
        except Exception as e:
            print(f"❌ {method} {path} -> Ошибка: {str(e)}")
            all_passed = False
    
    return all_passed

if __name__ == "__main__":
    results = []
    results.append(("Все уроки принимают правильные ответы", test_all_lessons_correct()))
    results.append(("Проверка неправильных ответов", test_common_incorrect_answers()))
    results.append(("Функция get_error_fix", test_error_fix_function()))
    results.append(("База данных", test_database()))
    results.append(("API Endpoints", test_all_endpoints()))
    
    print("\n" + "=" * 60)
    print("ИТОГОВЫЙ ОТЧЁТ")
    print("=" * 60)
    for name, passed in results:
        status = "✅" if passed else "❌"
        print(f"{status} {name}")
    
    all_passed = all(p for _, p in results)
    print(f"\n{'Все тесты пройдены!' if all_passed else 'Есть провальные тесты!'}")
    sys.exit(0 if all_passed else 1)