#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import os.path
import sys
from datetime import date
import click

click.echo(click.style("hello", fg="green"))

def add_student(staff, name, course, year):
    
    staff.append(
        {
            "name": name,
            "course": course,
            "year": year
        }
    )
    return staff

def display_students(staff):

    #Отобразить список студентов.

    
    if staff:
            # Заголовок таблицы.
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 8,
            '-' * 20
        )

        print(line)
        print(
            '| {:^4} | {:^30} | {:^8} | {:^20} |'.format(
                "No",
                "Ф.И.О.",
                "Курс",
                "Год поступления"
            )
        )
        print(line)
        
        for idx,student in enumerate(staff, 1):
            print(
                '| {:>4} | {:<30} | {:^8} | {:^20} |'.format(
                    idx,
                    student.get('name', ''),
                    student.get('course', ''),
                    student.get('year', 0)
                )
            )
            print(line)
    else:
        print("Список студентов пуст.")

def select_students(staff, period):
        """
        Выбрать работников с заданным стажем.
        """
        # Получить текущую дату.
        today = date.today()
        # Сформировать список студентов
        result = []
        for employee in staff:
            if today.year - employee.get('year', today.year) >= period:
                result.append(employee)
            # Возвратить список выбранных студентов.
            return result

def save_students(file_name, staff):
        """
        Сохранить всех работников в файл JSON.
        """
        # Открыть файл с заданным именем для записи.
        with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
            json.dump(staff, fout, ensure_ascii=False, indent=4)

def load_students(file_name):
        """
        Загрузить всех работников из файла JSON.
        """
        
        with open(file_name, "r", encoding="utf-8") as fin:
            return json.load(fin)

def main(command_line=None):
        
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="The data file name"
    )
        
    parser = argparse.ArgumentParser("students")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    subparsers = parser.add_subparsers(dest="command")
       
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new student"
    )
    add.add_argument(
        "-n",
        "--name",
        action="store",
        required=True,
        help="The stedent's name"
    )
    add.add_argument(
        "-c",
        "--course",
        action="store",
        help="The student's course"
    )
    add.add_argument(
        "-y",
        "--year",
        action="store",
        type=int,
        required=True,
        help="The year of hiring"
    )
       
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all students"

    )
       
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the students"
    )
    select.add_argument(
        "-P",
        "--period",
        action="store",
        type=int,
        required=True,
        help="The required period"
    )
       
    args = parser.parse_args(command_line)
           
    is_dirty = False
    if os.path.exists(args.filename):
        students = load_students(args.filename)
    else:
        students = []
            # Добавить студента.
    if args.command == "add":
        students = add_student(
        students,
        args.name,
        args.course,
        args.year
    )
        is_dirty = True
           
    elif args.command == "display":
            display_students(students)

           
    elif args.command == "select":
        selected = select_students(students, args.period)
        display_students(selected)
           
    if is_dirty:
            save_students(args.filename, students)

if __name__ == "__main__":
    main()