import json
from datetime import datetime


def transliterate_russian(text):
    """Транслитерация русского текста в латиницу"""
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo',
        'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M',
        'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
        'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch',
        'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
    }

    result = []
    for char in text:
        if char in translit_dict:
            result.append(translit_dict[char])
        else:
            result.append(char)

    return ''.join(result)


class Task:
    """Класс для представления задачи"""

    def __init__(self, title, description, due_date, priority):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority

    def to_dict(self):
        """Преобразование задачи в словарь для сохранения"""
        return {
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date,
            'priority': self.priority
        }

    def __str__(self):
        """Строковое представление задачи"""
        return f"{self.title} | Due: {self.due_date} | Priority: {self.priority} | {self.description}"

class TaskManager:
    """Класс для управления списком задач"""

    def __init__(self):
        self.tasks = []

    def add_task(self, title, description, due_date, priority):
        """Добавление новой задачи"""
        task = Task(title, description, due_date, priority)
        self.tasks.append(task)
        print("Задача добавлена.")

    def delete_task(self):
        """Удаление задачи по индексу или названию"""
        if not self.tasks:
            print("Нет задач для удаления.")
            return None

        print("\nВсе задачи:")
        for i, task in enumerate(self.tasks):
            print(f"{i}. {task}")

        choice = input("\nУдалить по индексу (i) или по названию (n)? ").strip.lower()

        if choice == 'i':
            try:
                index = int(input("Введите индекс задачи для удаления: "))
                if 0 <= index < len(self.tasks):
                    self.tasks.pop(index)
                    print("Задача удалена.")
                else:
                    print("Ошибка: неверный индекс.")
            except ValueError:
                print("Ошибка: введите корректный индекс.")
        elif choice == 'n':
            name = input("Введите название задачи для удаления: ").strip()
            found = False
            for i, task in enumerate(self.tasks):
                if task.title == name:
                    self.tasks.pop(i)
                    print("Задача удалена.")
                    found = True
                    break
            if not found:
                print("Ошибка: задача с таким названием не найдена.")
        else:
            print("Ошибка: неверный выбор.")

    def sort_by_priority(self):
        """Сортировка задач по приоритету (быстрая сортировка)"""
        if not self.tasks:
            print("Нет задач для сортировки.")
            return

        self.tasks = self.quick_sort_priority(self.tasks)
        print("Задачи отсортированы по приоритету.")

    def quick_sort_priority(self, tasks):
        """Быстрая сортировка по приоритету"""
        if len(tasks) <= 1:
            return tasks

        pivot = tasks[len(tasks) // 2].priority
        left = [task for task in tasks if task.priority < pivot]
        middle = [task for task in tasks if task.priority == pivot]
        right = [task for task in tasks if task.priority > pivot]

        return self.quick_sort_priority(left) + middle + self.quick_sort_priority(right)

    def sort_by_date(self):
        """Сортировка задач по дате (сортировка слиянием)"""
        if not self.tasks:
            print("Нет задач для сортировки.")
            return

        self.tasks = self.merge_sort_date(self.tasks)
        print("Задачи отсортированы по дате выполнения.")

    def merge_sort_date(self, tasks):
        """Сортировка слиянием по дате"""
        if len(tasks) <= 1:
            return tasks

        mid = len(tasks) // 2
        left = self.merge_sort_date(tasks[:mid])
        right = self.merge_sort_date(tasks[mid:])

        return self.merge(left, right)

    def merge(self, left, right):
        """Слияние двух отсортированных списков"""
        result = []
        i, j = 0, 0

        while i < len(left) and j < len(right):
            if left[i].due_date <= right[j].due_date:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def search_task(self, keyword):
        """Линейный поиск задачи по ключевому слову"""
        found_tasks = []
        for task in self.tasks:
            if keyword.lower() in task.title.lower():
                found_tasks.append(task)

        if found_tasks:
            print(f"\nНайдено задач: {len(found_tasks)}")
            for task in found_tasks:
                print(task)
        else:
            print("Задачи не найдены.")

    def show_all_tasks(self):
        """Отображение всех задач"""
        if not self.tasks:
            print("Нет задач для отображения.")
        else:
            print("\nВсе задачи:")
            for task in self.tasks:
                print(task)
    def export_tasks(self):
        """Экспорт задач в файл"""
        if not self.tasks:
            print("Нет задач для экспорта.")
            return

        file_format = input("Выберите формат файла (txt/json): ").strip().lower()

        if file_format not in ['txt', 'json']:
            print("Ошибка: неверный формат файла.")
            return

        # Получаем первое поле (название первой задачи)
        first_task_title = self.tasks[0].title

        # Проверяем, есть ли русские буквы и транслитерируем
        has_cyrillic = any('\u0400' <= char <= '\u04FF' for char in first_task_title)

        if has_cyrillic:
            file_prefix = transliterate_russian(first_task_title).replace(" ", "_").lower()
        else:
            file_prefix = first_task_title.replace(" ", "_").lower()

        # Формируем имя файла
        task_count = len(self.tasks)
        filename = f"{file_prefix}_{task_count}.{file_format}"

        # Сохраняем в файл
        if file_format == 'txt':
            with open(filename, 'w', encoding='utf-8') as f:
                for task in self.tasks:
                    f.write(str(task) + '\n')
            print(f"Задачи экспортированы в файл: {filename}")
        elif file_format == 'json':
            with open(filename, 'w', encoding='utf-8') as f:
                task_dict = [task.to_dict() for task in self.tasks]
                json.dump(task_dict, f, ensure_ascii=False, indent=4)
            print(f"Задачи экспортированы в файл: {filename}")

def validate_date(date_string):
    """Проверка корректности формата даты"""
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_priority(priority_string):
    """Проверка корректности приоритета"""
    try:
        priority = int(priority_string)
        if 1 <= priority <= 5:
            return True
        return False
    except ValueError:
        return False

def main():
    """Главная функция программы"""
    manager = TaskManager()

    while True:
        print("\nМеню:")
        print("1. Добавить задачу")
        print("2. Удалить задачу")
        print("3. Сортировать задачи по приоритету")
        print("4. Сортировать задачи по дате")
        print("5. Найти задачу")
        print("6. Показать все задачи")
        print("7. Выйти")

        choice = input("Выберите действие: ").strip()

        if choice == '1':
            # Добавление задачи
            title = input("Введите название задачи: ").strip()
            if not title:
                print("Ошибка: название не может быть пустым.")
                continue

            description = input("Введите описание задачи: ").strip()

            while True:
                due_data = input("Введите дату выполнения (YYYY-MM-DD): ")
                if validate_date(due_data):
                    break
                else:
                    print("Ошибка: неверный формат даты. Используйте YYYY-MM-DD.")

            while True:
                priority = input("Введите приоритет задачи (1 - высокий, 5 - низкий): ").strip()
                if validate_priority(priority):
                    priority = int(priority)
                    break
                else:
                    print("Ошибка: приоритет должен быть от 1 до 5.")

            manager.add_task(title, description, due_data, priority)

        elif choice == '2':
            # Удаление задачи
            manager.delete_task()

        elif choice == '3':
            # Сортировка по приоритету
            manager.sort_by_priority()

        elif choice == '4':
            # Сортировка по дате
            manager.sort_by_date()

        elif choice == '5':
            # Поиск задачи
            keyword = input("Введите ключевое слово для поиска: ").strip()
            if keyword:
                manager.search_task(keyword)
            else:
                print("Ошибка: введите ключевое слово.")

        elif choice == '6':
            # Показать все задачи
            manager.show_all_tasks()

        elif choice == '7':
            # Выход и экспорт
            if manager.tasks:
                export_choice = input("Хотите экспортировать задачи перед выходом? (да/нет): ").strip().lower()
                if export_choice in ['да', 'yes', 'y', 'д']:
                    manager.export_tasks()
            print("До свидания!")
            break

        else:
            print("Ошибка: неверный выбор. Выберите действие от 1 до 7.")


if __name__ == '__main__':
    main()
























