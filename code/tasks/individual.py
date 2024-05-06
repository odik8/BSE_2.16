#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from datetime import datetime

from jsonschema import ValidationError, validate


def get_birthdate():
    while True:
        try:
            date_str = input("Введите дату рождения в формате ДД.ММ.ГГГГ: ")
            birthdate = datetime.strptime(date_str, "%d.%m.%Y").date()
            return birthdate
        except ValueError:
            print("Ошибка Неправильный формат даты. Попробуйте снова.")


def add_person(list_of_people):
    print("\nДобавление нового человека:")
    last_name = input("Введите фамилию: ")
    first_name = input("Введите имя: ")
    phone_number = input("Введите номер телефона: ")
    birthdate = get_birthdate()

    person = {
        "фамилия": last_name,
        "имя": first_name,
        "номер телефона": phone_number,
        "дата рождения": str(birthdate),
    }

    list_of_people.append(person)
    list_of_people.sort(key=lambda x: x["дата рождения"])
    print("Человек добавлен\n")


def find_person_by_phone(people, phone):
    for person in people:
        if person["номер телефона"] == phone:
            return person
    return None


def print_person_info(list_of_people):
    match list_of_people:
        case []:
            print("Человек не найден.\n")
        case {
            "фамилия": f,
            "имя": i,
            "номер телефона": nt,
            "дата рождения": dr,
        }:
            print("\nИнформация о человеке:")
            print(f"Фамилия: {f}")
            print(f"Имя: {i}")
            print(f"Номер телефона: {nt}")
            print(f"Дата рождения: {dr}\n")


def save_to_json(file_name, list_of_people):
    """
    Сохранить всех в файл JSON.
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кириллицы установим ensure_ascii=False
        print(list_of_people)
        json.dump(list_of_people, fout, ensure_ascii=False, indent=4)
    print("Данные успешно сохранены в файл", file_name)


def load_from_json(file_name):
    """
    Загрузить всех из JSON
    """
    with open(file_name, "r", encoding="utf-8") as fin:
        document = json.load(fin)

        if all(list(map(lambda x: check_validation_json(x), document))):
            return document
        else:
            False


def check_validation_json(file_name):
    with open("code/tasks/schema.json") as fs:
        schema = json.load(fs)

    try:
        validate(instance=file_name, schema=schema)
        return True
    except ValidationError:
        return False


def main():
    list_of_people = []

    while True:
        print("\n1. Добавить человека")
        print("2. Найти человека по номеру телефона")
        print("3. Вывести список людей")
        print("4. Сохранить в json")
        print("5. Загрузить из json")
        print("6. Выйти")
        choice = input("Выберите действие (1/2/3/4/5/6): ")

        match choice:
            case "1":
                add_person(list_of_people)

            case "2":
                phone_to_find = input("Введите номер телефона для поиска: ")
                found_person = find_person_by_phone(
                    list_of_people, phone_to_find
                )
                print_person_info(found_person)

            case "3":
                for _ in list_of_people:
                    print_person_info(_)

            case "4":
                file_name = (
                    str(input("Введите имя файла(без расширения): ")) + ".json"
                )
                save_to_json(file_name, list_of_people)

            case "5":
                file_name = (
                    str(input("Введите имя файла(без расширения): ")) + ".json"
                )
                list_of_people = load_from_json(file_name)
            case "6":
                print("Программа завершена.\n")
                break

            case _:
                print("Некорректный ввод. Попробуйте снова.\n")


if __name__ == "__main__":
    main()
