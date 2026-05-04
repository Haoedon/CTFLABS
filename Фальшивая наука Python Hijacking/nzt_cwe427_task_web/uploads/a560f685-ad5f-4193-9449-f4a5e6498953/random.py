import os

print("\n[!] МОДУЛЬ RANDOM ПЕРЕХВАЧЕН!")
print("[!] Пытаюсь прочитать флаг...")

try:
    # Для локального теста читаем на 2 папки выше
    with open('../../flag.txt', 'r') as f:
        print("\nФЛАГ УСПЕШНО СЛИТ:", f.read())
except FileNotFoundError:
     print("\nФайл с флагом не найден.")
     
# Добавляем заглушку для функции randint, которую ожидает analyzer.py,
# чтобы программа не упала до того, как выведет наш флаг.
def randint(a, b):
    return "HACKED"