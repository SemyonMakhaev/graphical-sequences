# Графические разбиения
Модуль для порождения всех реализаций заданного графического разбиения

## Автор
Семён Махаев, КБ-301

## Использование
python3 realizations.py [-h] [-dir directory] [-d] degree [degree ...]

#### Позиционные аргументы
degree - Степень очередной вершины графического разбиения

#### Опциональные аргументы
-h, --help - Вывод справки
-dir directory, --directory directory - Директория для вывода картинок
-d, --debug - Запуск дополнительных проверок

#### Запуск тестов
python tests.py

## Зависимости
* networkx
* matplotlib.pyplot
* argparse
* os
* shutil
* logging
* unittest
