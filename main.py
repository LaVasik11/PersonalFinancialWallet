import json
from datetime import datetime


class PersonalFinancialWallet():
    def __init__(self, balance: int = 0, filename: str = "records.json"):
        self.balance = balance
        self.filename = filename

    def show_balance(self) -> int:
        """Возвращает текущий баланс и отображает его в кансоль."""
        print(f'Баланс: {self.balance}')
        return self.balance

    def show_records(self, category, page=1, page_size=5):
        with open(self.filename, 'r', encoding='utf-8') as records:
            data = json.load(records)

        filtered_records = [record for record in data if record['Категория'].lower() == category.lower()]
        total_records = len(filtered_records)
        total_pages = (total_records + page_size - 1) // page_size
        start_index = (page - 1) * page_size
        end_index = min(start_index + page_size, total_records)

        for i in range(start_index, end_index):
            for k, v in filtered_records[i].items():
                record = f"{k}: {v}"
                print(record)

            print(len(record) * '-')

        print(f"Страница {page}/{total_pages}")

        return page, total_pages

    def paginate_records(self):
        page = 1
        while True:
            category = input("Введите 'доход' или 'расход' для просмотра соответствующих записей: ")
            if category.lower() == 'доход' or category.lower() == 'расход':
                break
            else:
                print("Некорректный ввод. Попробуйте снова.")

        page, total_pages = self.show_records(category, page)
        while True:
            print("Введите '>' для следующей страницы | '<' для предыдущей,")
            print("'>>' для последней | '<<' для первой,")
            print("'s' для поиска | 'ch' для редактирования | 'x' для выхода:")
            action = input().lower()
            if action == '>':
                if page < total_pages:
                    page += 1
                    page, total_pages = self.show_records(category, page)
                else:
                    print("Больше страниц нет.")
            elif action == '<':
                if page > 1:
                    page -= 1
                    self.show_records(category, page)
                else:
                    print("Вы находитесь на первой странице.")

            elif action == '>>':
                page = total_pages
                self.show_records(category, page)
            elif action == '<<':
                page = 1
                self.show_records(category, page)

            elif action == 'ch':
                id_record = int(input("Введите id записи которую хотите отредактировать: "))
                self.edit_entry(id_record)

            elif action in 'xх':
                break
            else:
                print("Некорректный ввод. Попробуйте снова.")

    def create_record(self, record: dict = None):
        if record is None:
            current_date = datetime.now().strftime('%Y-%m-%d')
        else:
            current_date = record['Дата']

        while True:
            if record is None:
                category_input = input("Введите категорию ([+] - доход, [-] - расход): ")
                if category_input == '+' or category_input.lower() == 'доход':
                    category = 'доход'
                    break
                elif category_input == '-' or category_input.lower() == 'расход':
                    category = 'расход'
                    break
                else:
                    print("Некорректная категория. Пожалуйста, введите '+' для дохода или '-' для расхода.")
            else:
                category = record['Категория']
                break

        while True:
            amount_input = input("Введите сумму: ") or record['Сумма']
            try:
                amount = int(amount_input)
                if amount <= 0:
                    raise ValueError("Сумма должна быть положительным числом")
                break

            except ValueError:
                print("Некорректная сумма. Пожалуйста, введите положительное число.")

        description = input("Введите описание: ") or record['Описание']

        if category == 'доход':
            self.balance += amount
        elif category == 'расход':
            self.balance -= amount

        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not data:
            data = []

        if record is None:
            id = max(item.get('id', 0) for item in data) + 1
        else:
            id = record['id']

        new_record = {
            "id": id,
            "Дата": current_date,
            "Категория": category,
            "Сумма": amount,
            "Описание": description,
        }

        return new_record
    def add_records(self):
        """Добавляет новую запись в файл {self.records}"""
        try:
            with open(self.filename, 'a', encoding='utf-8') as records:
                new_record = self.create_record()

                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                if not data:
                    data = []

                data.append(new_record)

                with open(self.filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

                print("Запись успешно добавлена!")

        except ValueError as e:
            print("Ошибка:", e)
        except Exception as e:
            print("Произошла ошибка при добавлении записи:", e)

    def edit_record(self, record_id: int):
        with open(self.filename, 'r', encoding='utf-8') as f:
            records = json.load(f)

        index_to_edit = None
        for i, record in enumerate(records):
            if record.get('id') == record_id:
                index_to_edit = i
                break

        if index_to_edit is not None:
            new_record = self.create_record(records[index_to_edit])
            records[index_to_edit] = new_record

            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(records, f, ensure_ascii=False, indent=2)

            print(f"Запись с ID {record_id} изменена!")
        else:
            print(f"Запись с ID {record_id} не найдена.")

    def search_record(self):
        print('Введите значения параметров по которым будет осуществляться поиск:')
        id = input('')




r = PersonalFinancialWallet()
r.search_record()


