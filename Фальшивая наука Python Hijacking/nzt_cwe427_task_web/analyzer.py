import os
import random # <-- Теперь это уязвимая точка (модуль на чистом Python)
import time

print("--- NZTmedicine Data Analyzer ---")
print("Инициализация окружения...")
time.sleep(0.5)

# Имитация работы с библиотекой random
val = random.randint(100, 999)
print(f"Анализ базовых метрик завершен (Код: {val}).")
print("Ошибок не обнаружено. Данные валидны.")