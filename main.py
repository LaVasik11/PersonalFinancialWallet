import json
from datetime import datetime


class PersonalFinancialWallet():
    def __init__(self, balance: int = 0, filename: str = "records.json"):
        self.filename = filename
        self.balance = self.find_out_balance() + balance

    def show_balance(self) -> int:
        """Возвращает текущий баланс и отображает его в консоль."""
        print(f'Баланс: {self.balance}\n')
        return self.balance

    def find_out_balance(self) -> int:
        """Присваивает атрибуту balance сумму на основе всех доходов и расходов из переданного файла."""
        balance = 0
        with open(self.filename, 'r', encoding='utf-8') as f:
            records = json.load(f)

        for i in records:
            if i.get('Категория') == 'доход':
                balance += i.get('Сумма')
            else:
                balance -= i.get('Сумма')

        return balance

    def show_records(self, records: list = None, page_size: int = 5):
        """
        Показывает постранично все записи.
        Так же запрашивает у пользователя следующие действие.
        Основная функция через которую происходит вся работа.
        """
        if not records:
            with open(self.filename, 'r', encoding='utf-8') as f:
                records = json.load(f)
                print(type(records))

        total_pages: int = len(records) // page_size + (1 if len(records) % page_size > 0 else 0)
        current_page: int = 1

        balance = False
        
        while True:      
            start: int = (current_page - 1) * page_size
            end: int = start + page_size
            page_records: list = records[start:end]

            for record in page_records:
                for k, v in record.items():
                    record = f"{k}: {v}"
                    print(record)

                print(len(record) * '-')

            print(f"Страница {current_page} из {total_pages}\n")
            
            if balance:
                self.show_balance()
                balance = False

            print("'>' - следующия страница | '<' - предыдущая страница,")
            print("'>>' - последняя | '<<' - первая,")
            print("'s' - поиск записи | 'ch' - редактирование записи,")
            print("'a' - добавление записи | 'b' - показать баланс | 'x' - выход:")
            command = input().lower()

            print('\n\n\n')

            if command == '>':
                if current_page < total_pages:
                    current_page += 1
                else:
                    print("Это последняя страница.\n")

            elif command == '<':
                if current_page > 1:
                    current_page -= 1
                else:
                    print("Это первая страница.\n")

            elif command == '>>':
                if current_page < total_pages:
                    current_page = total_pages

            elif command == '<<':
                if current_page > 1:
                    current_page = 1

            elif command == 'ch':
                id_record = int(input("Введите id записи которую хотите отредактировать: "))
                self.edit_record(id_record)
                with open(self.filename, 'r', encoding='utf-8') as f:
                    records = json.load(f)

            elif command == 's':
                self.search_record()

            elif command == 'a':
                self.add_records()

            elif command == 'b':
                balance = True

            elif command in 'xх':
                break

            else:
                print("Неизвестная команда. Пожалуйста, попробуйте снова.")

    def create_record(self, record: dict = None) -> dict:
        """Создает новую запись запрашивая у пользователя данные для неё."""
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

        description = input("Введите описание: ")
        
        if description == '':
            if record:
                description = record['Описание']

        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not data:
            data = []

        if record is None:
            id_record = max(item.get('id', 0) for item in data) + 1
        else:
            id_record = record['id']

        new_record = {
            "id": id_record,
            "Дата": current_date,
            "Категория": category,
            "Сумма": amount,
            "Описание": description,
        }

        return new_record

    def change_balance(self, record: dict, old_record:dict = None):
        """
        Меняет атрибут balance в зависимости от записи которую передали в функцию.
        В функцию можно передать вторую запись,
        что бы убрать её значение из баланса(сделано для изменения записей).
        """
        if record.get("Категория") == 'доход':
            print(self.balance, record.get('Сумма'))
            self.balance += record.get('Сумма')
        elif record.get("Категория") == 'расход':
            self.balance -= record.get('Сумма')

        if old_record:
            if old_record.get("Категория") == 'доход':
                self.balance -= old_record.get('Сумма')
            elif old_record.get("Категория") == 'расход':
                self.balance += old_record.get('Сумма')

    def add_records(self):
        """Добавляет новую запись в файл переданный при создании класса."""
        new_record = self.create_record()

        self.change_balance(new_record)

        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not data:
            data = []

        data.append(new_record)

        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print("Запись успешно добавлена!")

    def edit_record(self, record_id: int):
        """Изменяет запись по её id."""
        with open(self.filename, 'r', encoding='utf-8') as f:
            records = json.load(f)

        index_to_edit = None
        for i, record in enumerate(records):
            if record.get('id') == record_id:
                index_to_edit = i
                break

        if index_to_edit is not None:
            new_record = self.create_record(records[index_to_edit])
            self.change_balance(new_record, records[index_to_edit])
            records[index_to_edit] = new_record

            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(records, f, ensure_ascii=False, indent=2)

            print(f"Запись с ID {record_id} изменена!")
        else:
            print(f"Запись с ID {record_id} не найдена.")

    def search_record(self):
        """Осуществляет поиск по записям в зависимости от выбранных параметров."""
        print("Введите значения параметров по которым будет осуществляться поиск:")

        while True:
            category_input = input("Введите категорию ([+] - доход, [-] - расход): ")
            if category_input == '+' or category_input.lower() == 'доход':
                category = 'доход'
                break
            elif category_input == '-' or category_input.lower() == 'расход':
                category = 'расход'
                break
            elif category_input == '':
                category = ''
                break
            else:
                print("Некорректная категория. Пожалуйста, введите '+' для дохода или '-' для расхода.")

        while True:
            amount_input = input("Введите сумму: ")
            try:
                amount = int(amount_input)
                if amount <= 0:
                    raise ValueError("Сумма должна быть положительным числом")
                break

            except ValueError:
                amount = 0
                break

        description = input("Введите описание: ")

        id_record = input("id: ")
        id_record = int(id_record) if id_record.isdigit() else 0

        date = input("Дата: ")
        if date:
            date = str(datetime.strptime(date, '%Y-%m-%d')).split()[0]

        search_params = {
            "id": id_record,
            "Дата": date,
            "Категория": category,
            "Сумма": amount,
            "Описание": description,
        }

        found_records = []

        with open(self.filename, 'r', encoding='utf-8') as f:
            records = json.load(f)

        for record in records:
            if all(record.get(key) == value for key, value in search_params.items() if value):
                found_records.append(record)

        if found_records:
            print("Найденные записи:")
            self.show_records(found_records)
        else:
            print("Записей, удовлетворяющих заданным параметрам, не найдено.")





