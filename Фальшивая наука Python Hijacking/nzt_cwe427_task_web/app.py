from flask import Flask, request, render_template
from werkzeug.utils import secure_filename  # <--- ИМПОРТИРУЕМ ФУНКЦИЮ ЗАЩИТЫ
import os
import subprocess
import uuid
import shutil
import sys

app = Flask(__name__)

# Папка, где будут создаваться временные директории для загрузок
UPLOAD_BASE_FOLDER = 'uploads'
os.makedirs(UPLOAD_BASE_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    # Создаем уникальную папку (песочницу) для текущего запуска
    session_id = str(uuid.uuid4())
    session_path = os.path.join(UPLOAD_BASE_FOLDER, session_id)
    os.makedirs(session_path)

    # Сохраняем загруженные пользователем файлы
    files = request.files.getlist('user_files[]')
    for file in files:
        if file.filename:
            # ЗАКРЫВАЕМ Arbitrary File Write:
            # Очищаем имя файла от ../ и абсолютных путей
            safe_filename = secure_filename(file.filename)
            
            # Защита на случай, если после очистки имя стало пустым 
            # (например, если хакер назвал файл "../")
            if safe_filename:
                file.save(os.path.join(session_path, safe_filename))

    # Копируем системный скрипт в песочницу
    shutil.copy('analyzer.py', session_path)

    # СОХРАНЯЕМ CWE-427 (Module Hijacking):
    # Запускаем analyzer.py в изолированной папке (cwd=session_path).
    # Python будет искать импортируемые модули (например, math) сначала здесь.
    try:
        result = subprocess.run(
            [sys.executable, 'analyzer.py'],
            cwd=session_path,
            capture_output=True,
            text=True,
            timeout=5 # Защита от бесконечных циклов в коде участника
        )
        output = result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        output = "Ошибка: Превышено время ожидания выполнения скрипта (Таймаут 5 сек)."
    except Exception as e:
        output = f"Системная ошибка: {str(e)}"

    # ДЛЯ БОЕВОГО CTF: Обязательно удаляйте песочницу после выполнения,
    # иначе сервер быстро забьется мусором от сотен запусков.
    # Раскомментируйте строку ниже для продакшена:
    # shutil.rmtree(session_path, ignore_errors=True)
    
    return f"<h3>Результат выполнения скрипта:</h3><pre style='background:#f4f4f4; padding:10px; border:1px solid #ccc;'>{output}</pre><br><a href='/'>Назад</a>"

if __name__ == '__main__':
    app.run(debug=True, port=5000)