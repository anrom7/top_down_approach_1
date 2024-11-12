"""LMS grade book ripoff"""

import json
from pprint import pprint
from collections import defaultdict

grade_book_type = dict[tuple[str, str, str, str], dict[str, dict[str, float | None]]]


def get_activities(syllabus: dict[str, dict[str, float]]) -> set[tuple[str, str]]:
    """
    Arranges groups of activities

    :param activities: list, all activities
    :return: set, groups of activities

    >>> get_activities({'Лабораторні роботи': {'Лабораторна робота 1': 1.5},
    ... 'Семінари': {'Семінар 1': 4.5, 'Семінар 2': 6},
    ... 'Лабораторні роботи': {
    ...     'Лабораторна робота 1': 2.0,
    ...     'Лабораторна робота 2': 0.5
    ... }}) == {('Семінари', 'Семінар 1'),
    ... ('Лабораторні роботи', 'Лабораторна робота 2'),
    ... ('Семінари', 'Семінар 2'), ('Лабораторні роботи', 'Лабораторна робота 1')}
    True
    """
    output = []
    for group in syllabus:
        for activity in syllabus[group]:
            output += [(group, activity)]

    return set(output)


def get_proper_student_grade(data: grade_book_type, syllabus: dict[str, dict[str, float]]) \
        -> dict[str, dict[str, dict[str, float | None]]]:
    """
    Makes a dictionary for all types of grades for each student

    :param data: dict, dictionary of all grades
    :return: dict, dictionary for all types of grades for each student.

    >>> get_proper_student_grade({\
    ('Фединяк', 'Степан', 'fedeniak.pn@ucu.edu.ua', 'ПКН24-Б1'): \
{\
'Лабораторні роботи': {'Лабораторна робота 1': 1.5},\
'Семінари': {'Семінар 1': 4.5, 'Семінар 2': 6}\
},\
('Фаренюк', 'Олег', 'fareniuk.pn@ucu.edu.ua', 'ПКН24-Б1'):\
{\
'Лабораторні роботи': {'Лабораторна робота 2': 2.0}}\
}, \
{\
'Семінари': {'Семінар 1': 6.0, 'Семінар 2': 6.0},\
'Лабораторні роботи': {'Лабораторна робота 1': 1.5, 'Лабораторна робота 2': 2.0}\
}) == \
{'Фединяк, Степан, fedeniak.pn@ucu.edu.ua, ПКН24-Б1': \
{'Семінари': {'Семінар 1': 4.5, 'Семінар 2': 6}, 'Лабораторні роботи': \
{'Лабораторна робота 1': 1.5, 'Лабораторна робота 2': None}}, \
'Фаренюк, Олег, fareniuk.pn@ucu.edu.ua, ПКН24-Б1': \
{'Семінари': {'Семінар 1': None, 'Семінар 2': None}, 'Лабораторні роботи': \
{'Лабораторна робота 1': None, 'Лабораторна робота 2': 2.0}}}
    True
    """

    def sort_key(x):
        return x[1]

    student_info, grades = list(data.keys()), list(data.values())
    all_activities = get_activities(syllabus)

    output = {}
    for student in student_info:
        grades = {}
        for topic, lab in all_activities:
            if topic not in grades:
                grades[topic] = {}

            if topic not in data[student] or lab not in data[student][topic]:
                grades[topic][lab] = None
                continue

            grades[topic] = dict(sorted(grades[topic].items(), key=sort_key))
            grades[topic][lab] = data[student][topic][lab]

        output[", ".join(student)] = grades

    return output


def add_activity(syllabus: dict[str, dict[str, float]], activity_group: str, activity: str, max_grade: float) -> dict[str, dict[str, float]]:
    '''
    Adds a new activity to the syllabus or ignores an existing activity 
    if the activity group and activity already exist in the syllabus.

    :param syllabus: dict[str, dict[str, float]], The dictionary that contains activity groups 
        as keys and nested dictionaries as values.
    :param activity_group: str, The name of the activity group.
    :param activity: str, The name of activity.
    :param max_grade: float, The maximum grade for the activity.

    :return: dict[str, dict[str, float]], The result syllabus.

    >>> add_activity({'ПКН23-А': {'Мідтерм 2023': 10}, \
                      'ПКН24-В': {'treasure': 1}}, \
                      'ПКН24-Б', 'Tower blocks', 1)
    {'ПКН23-А': {'Мідтерм 2023': 10}, \
'ПКН24-В': {'treasure': 1}, \
'ПКН24-Б': {'Tower blocks': 1}}
    >>> add_activity({'ПКН23-А': {'Мідтерм 2023': 10}, \
                      'ПКН24-В': {'treasure': 1}}, \
                      'ПКН24-В', 'Tower blocks', 1)
    {'ПКН23-А': {'Мідтерм 2023': 10}, \
'ПКН24-В': {'treasure': 1, 'Tower blocks': 1}}
    >>> add_activity({'ПКН23-А': {'Мідтерм 2023': 10}, \
                      'ПКН24-В': {'treasure': 1}}, \
                      'ПКН24-В', 'treasure', 0)
    {'ПКН23-А': {'Мідтерм 2023': 10}, \
'ПКН24-В': {'treasure': 1}}
    '''
    if not activity_group in syllabus:
        syllabus[activity_group] = {}
    if not activity in syllabus[activity_group]:
        syllabus[activity_group][activity] = max_grade

    return syllabus

def write_json(filename: str, data: grade_book_type, syllabus: dict[str, dict[str, float]]):
    """
    Writes the all students' grades json file.

    :param filename: str, name of the file that should be written
    :param data: dict, dictionary of all grades
    :return: None
    """

    student_grades = get_proper_student_grade(data, syllabus)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(student_grades, file, ensure_ascii=False)


def grade_check(mark: str, max_grade: float) -> float | None:
    """
    Checks if the grade is correct.
    :param mark: str
    :param max_grade: float, maximum grade
    :return: float if grade correct, None otherwise
    """
    if not mark or float(mark) < 0 or float(mark) > max_grade:
        return None
    return float(mark)


def is_activity_correct(syllabus: dict[str, dict[str, float]], activity_group: str, activity: str) \
        -> bool:
    """
    Checks if the activity is correct.
    :param syllabus: dict[str, dict[str, float]], dict of all activities
    :param activity_group: str, activity group
    :param activity: str, activity
    :return: bool, True if activity is correct, False otherwise
    """
    if syllabus.get(activity_group, -1) == -1 or syllabus[activity_group].get(activity, -1) == -1:
        return False
    return True


def get_grades_from_file(filename: str, grade_book: grade_book_type,
                         syllabus: dict[str, dict[str, float]], ) \
        -> dict[(str, str, str, str), dict[str, dict[str, float]]]:
    """
    Record grades from a file.
    :param filename: str, file with marks
    :param grade_book: dict[(str, str, str, str), dict[str, dict[str, float]]], key is student info,
    :param syllabus: dict[str, dict[str, float]], dict of all activities with respective maximun
     grades
    value is a nested dict of grades
    :return:  dict[(str, str, str, str), dict[str, dict[str, float]]], grade book with inserted
    values
    >>> get_grades_from_file('grades.csv', { \
('Фединяк', 'Степан', 'fedyniak.pn@ucu.edu.ua','ПКН24-Б1'): {}, \
('Фаренюк', 'Олег', 'fareniuk.pn@ucu.edu.ua', 'ПКН24-Б1'): {}, \
('Степаненко', 'Степан', 'stepanenko.pn@ucu.edu.ua', 'ПКН24-Б2'): {}, \
('Рандомний', 'Поц', 'randomnyi.pn@ucu.edu.ua', 'ПКН24-Б1'): {}, \
('Норм', 'Кєнт', 'norm.pn@ucu.edu.ua', 'ПКН24-Б1'): {}, \
('Хто', 'Це', 'hto.pn@ucu.edu.ua', 'ПКН24-Б3'): {}}, \
{'Лабораторні роботи': {'Лабораторна робота 1': 2.0}})
    {('Фединяк', 'Степан', 'fedyniak.pn@ucu.edu.ua', 'ПКН24-Б1'): \
{'Лабораторні роботи': {'Лабораторна робота 1': 1.5}}, \
('Фаренюк', 'Олег', 'fareniuk.pn@ucu.edu.ua', 'ПКН24-Б1'): \
{'Лабораторні роботи': {'Лабораторна робота 1': 2.0}}, \
('Степаненко', 'Степан', 'stepanenko.pn@ucu.edu.ua', 'ПКН24-Б2'): \
{'Лабораторні роботи': {'Лабораторна робота 1': 0.5}}, \
('Рандомний', 'Поц', 'randomnyi.pn@ucu.edu.ua', 'ПКН24-Б1'): \
{'Лабораторні роботи': {'Лабораторна робота 1': 0.0}}, \
('Норм', 'Кєнт', 'norm.pn@ucu.edu.ua', 'ПКН24-Б1'): \
{'Лабораторні роботи': {'Лабораторна робота 1': 2.0}}, \
('Хто', 'Це', 'hto.pn@ucu.edu.ua', 'ПКН24-Б3'): \
{'Лабораторні роботи': {'Лабораторна робота 1': None}}}
    """
    with open(filename, "r", encoding="utf-8") as file_grade_book:
        lines = file_grade_book.readlines()

        for line in lines[1:]:
            activity_group, activity, surname, name, email, student_group, mark = \
                line.strip().split(",")

            if not is_activity_correct(syllabus, activity_group, activity):
                # print("Activity doesn't exist")
                continue

            mark = grade_check(mark, syllabus[activity_group][activity])

            grade_book[(surname, name, email, student_group)] \
                .setdefault(activity_group, {})[activity] = mark

    return grade_book


def add_student(grade_book: grade_book_type, student_info: tuple[str, str, str, str]) \
        -> grade_book_type:
    """
    Adds a student to a gradebook if the student is not in it, else does nothing

    :params: gradebook: dict - grabook with students and grades
    :params: student_info: tuple - student information (last name, first name, email, group)

    :Returns:
    dict - updated gradebook with the added student
    >>> add_student({('Стерненко', 'Сергій', 'sternenko.pn@ucu.edu.ua', 'ПКН24-Б2'): {}},\
 ('Студент', 'Павло', 'student.pn@ucu.edu.ua', 'ПКН24-Б1'))
    {('Стерненко', 'Сергій', 'sternenko.pn@ucu.edu.ua', 'ПКН24-Б2'): {},\
 ('Студент', 'Павло', 'student.pn@ucu.edu.ua', 'ПКН24-Б1'): {}}
    """

    if student_info not in grade_book:
        grade_book[student_info] = {}
    return grade_book


def stud_grade_book_to_json(filename: str, stud_mail: str, grade_book: grade_book_type):
    """
    This function records a gradebook for one student,
    whose email is recorded in stud_mail param.
    in a json file.
    -------------------------------------------------
    param: filename(str) "your_file_name.json",
    stud_mail(str) student's email adress,
    grade_book(dict) grade_book to write to json file.
    return: 'Done successfully' or 'The Error occured: two or more equal emails'

    >>> STUD_GRB = {('Name1', 'Lastname1', 'n1l1@gmail.com', 'ПКН24-Б1'):\
{"Лабораторні роботи (22 бали)":\
{"Лабораторна робота 1": 1.5,"Лабораторна робота 2": 2.4, \
"Лабораторна робота 3": 5.6,"Лабораторна робота 4": 2.5,\
"Лабораторна робота 5": 8.7},"Тести по лекційним матеріалам":\
{'Тест 1': 1.4,'Тест 2': 3.5,'Тест 3': 2.5,'Тест 4': 1.3},\
"Тести на LMS": {'Тест 1': 1,'Тест 2': 1,'Тест 3': 1,'Тест 4': 0.8,\
'Тест 5': 3.2,'Тест 6': 1.4,'Тест 7': 3.6}},\
('Name2', 'Lastname2', 'n2l2@gmail.com', 'ПКН24-Б1'):\
{"Лабораторні роботи (22 бали)":\
{"Лабораторна робота 1": 0.5,"Лабораторна робота 2": 2.4, \
"Лабораторна робота 3": 5.8,"Лабораторна робота 4": 2.3,\
"Лабораторна робота 5": 3.7},"Тести по лекційним матеріалам":\
{'Тест 1': 1.4,'Тест 2': 2.5,'Тест 3': 2.5,'Тест 4': 1.3},\
"Тести на LMS": {'Тест 1': 1.8,'Тест 2': 2.6,'Тест 3': 0.0,'Тест 4': 0.0,\
'Тест 5': 3.2,'Тест 6': 1.4,'Тест 7': 3.6}}}
    >>> import tempfile
    >>> with tempfile.NamedTemporaryFile(mode= 'w+', suffix=".json", delete = False) as temp_input:
    ...    res = stud_grade_book_to_json(temp_input.name, 'n1l1@gmail.com', STUD_GRB)
    ...    with open(temp_input.name, 'r', encoding = 'utf-8') as temp_output:
    ...        print(temp_output.read())
    ...    print(res)
    {
        "Name1, Lastname1, n1l1@gmail.com, ПКН24-Б1": {
            "Лабораторні роботи (22 бали)": {
                "Лабораторна робота 1": 1.5,
                "Лабораторна робота 2": 2.4,
                "Лабораторна робота 3": 5.6,
                "Лабораторна робота 4": 2.5,
                "Лабораторна робота 5": 8.7
            },
            "Тести по лекційним матеріалам": {
                "Тест 1": 1.4,
                "Тест 2": 3.5,
                "Тест 3": 2.5,
                "Тест 4": 1.3
            },
            "Тести на LMS": {
                "Тест 1": 1,
                "Тест 2": 1,
                "Тест 3": 1,
                "Тест 4": 0.8,
                "Тест 5": 3.2,
                "Тест 6": 1.4,
                "Тест 7": 3.6
            }
        }
    }
    Done successfully
    >>> import tempfile
    >>> with tempfile.NamedTemporaryFile(mode= 'w+', suffix=".json", delete = False) as temp_input:
    ...    res = stud_grade_book_to_json(temp_input.name, 'check@gmail.com', STUD_GRB)
    ...    with open(temp_input.name, 'r', encoding = 'utf-8') as temp_output:
    ...        print(temp_output.read())
    ...    print(res)
    <BLANKLINE>
    The Error occured: no student with that email
    """
    needed = list(filter(lambda x: stud_mail in x, grade_book.keys()))
    if len(needed) == 1:
        output_diction = {
        ", ".join(key): value for key, value in grade_book.items()
        if key == needed[0]
        }
        with open(filename, mode="w", encoding="utf-8") as file:
            json.dump(output_diction, file, ensure_ascii=False,
            indent=4, separators=(",", ": "))
        return 'Done successfully'
    elif len(needed) >= 1:
        return 'The Error occured: two or more equal emails'
    else:
        return 'The Error occured: no student with that email'

def del_activity(
    syllabus: dict[str, dict[str, float]],
    grade_book: dict[tuple[str, str, str, str], dict[str, dict[str, float | None]]],
    activity_group: str,
    activity: str
) -> None:
    """
    Removes an activity from the syllabus and grade book for each student.

    :param syllabus: syllabus that contains information on activity groups and their maximum scores.
    :param grade_book: grade book with students' grades.
    :param activity_group: name of the activity group from which the activity will be removed.
    :param activity: name of the activity that we need to remove.
    :return: None
    >>> syllabus = {"Лабораторні роботи": {"Лабораторна робота 1": 3, "Лабораторна робота 2": 2}}
    >>> grade_book = {("Фединяк", "Степан", "fedyniak.pn@ucu.edu.ua", "ПКН24-Б1"):  \
{"Лабораторні роботи":{"Лабораторна робота 1": 3, "Лабораторна робота 2": 2}}}
    >>> del_activity(syllabus, grade_book, "Лабораторні роботи", "Лабораторна робота 1")
    >>> syllabus
    {'Лабораторні роботи': {'Лабораторна робота 2': 2}}
    >>> grade_book
    {('Фединяк', 'Степан', 'fedyniak.pn@ucu.edu.ua', 'ПКН24-Б1'): {'Лабораторні роботи':\
 {'Лабораторна робота 2': 2}}}
    """
    if activity_group in syllabus:
        if activity in syllabus[activity_group]:
            del syllabus[activity_group][activity]
            if not syllabus[activity_group]:
                del syllabus[activity_group]
    for _, activities in grade_book.items():
        if activity_group in activities:
            if activity in activities[activity_group]:
                del activities[activity_group][activity]
                if not activities[activity_group]:
                    del activities[activity_group]

def mark_transform(grade_book: grade_book_type) -> dict[str, str]:
    """
    Returns all students marks with letter grade system

    :param grade_book:  dict[(str, str, str, str), dict[str, dict[str, float]]],key is student names
    :return: dict[str,str], name and surname of the student with their respective mark

    >>> mark_transform({('Фединяк', 'Степан', 'fedyniak.pn@ucu.edu.ua', 'ПКН24-Б1'):\
 {"Лабораторні роботи (22 бали)": {"Лабораторна робота 1": '1.0',"Лабораторна робота 2": '1.0',\
"Лабораторна робота 3": '1.0',"Лабораторна робота 4": '1.0',"Лабораторна робота 5": '1.0',\
"Лабораторна робота 6": '1.0',"Лабораторна робота 7": '1.0',"Лабораторна робота 8": '1.0',\
"Лабораторна робота 9": '1.0',"Лабораторна робота 10": '1.0',"Лабораторна робота 11": '1.0'},\
"Проміжний іспит (20 балів)": {'Теоретичне завдання': '1.0','Завдання на програмування': '1.0'}\
,"Тести по лекційним матеріалам (3 бали по 0.5 за кожен)": {'Тест 1': '1.0','Тест 2': '1.0',\
'Тест 3': '1.0','Тест 4': '1.0','Тест 5': '1.0','Тест 6': '1.0'},\
"Тести на LMS (3 бали по 0.3 за кожен)": {'Тест 1': '1.0','Тест 2': '1.0','Тест 3': '1.0',\
'Тест 4': '1.0','Тест 5': '1.0','Тест 6': '1.0','Тест 7': '1.0','Тест 8': '1.0','Тест 9': '1.0',\
'Тест 10': '1.0'},"Міні-проєкти (22 бали)": {'міні-проєкт 1': '1.0','міні-проєкт 2': '1.0'},\
"Фінальний іспит (30 балів)": {'Теоретичне завдання': '1.0','Завдання на програмування': '1.0',},\
"Додаткові бали (10 балів)": '1.0'}})
    {'Фединяк Степан': 'F'}
    """
    mark = 0
    student = ""
    letter_mark = ""
    final = {}
    for i in grade_book:
        for e in grade_book.get(i):
            if isinstance(grade_book.get(i).get(e), str):
                mark += float(grade_book.get(i).get(e))
                break
            for g in grade_book.get(i).get(e):
                mark += float(grade_book.get(i).get(e).get(g))
        student += i[0] + " " + i[1]
        if not mark:
            letter_mark = "-"
        if mark >= 90:
            letter_mark = "A"
        elif 90 > mark >= 85:
            letter_mark = "B"
        elif 85 > mark >= 75:
            letter_mark = "C"
        elif 75 > mark >= 65:
            letter_mark = "D"
        elif 65 > mark >= 60:
            letter_mark = "E"
        elif 60 > mark >= 0:
            letter_mark = "F"
        final.setdefault(student, letter_mark)
        mark = 0
        student = ""
    return final

def letter_report(letter: str, gradebook: grade_book_type) -> list:
    '''
    Receives gradebook and letter and builds report of students with particular grade
    :param letter: letter to get students with this mark
    :param grade_book: grade book dict
    :return: list[student1, student2] list of students with particular grade
    >>> letter_report('F', {('Фединяк', 'Степан', 'fedyniak.pn@ucu.edu.ua', 'ПКН24-Б1'):\
 {"Лабораторні роботи (22 бали)": {"Лабораторна робота 1": '1.0',"Лабораторна робота 2": '1.0',\
"Лабораторна робота 3": '1.0',"Лабораторна робота 4": '1.0',"Лабораторна робота 5": '1.0',\
"Лабораторна робота 6": '1.0',"Лабораторна робота 7": '1.0',"Лабораторна робота 8": '1.0',\
"Лабораторна робота 9": '1.0',"Лабораторна робота 10": '1.0',"Лабораторна робота 11": '1.0'},\
"Проміжний іспит (20 балів)": {'Теоретичне завдання': '1.0','Завдання на програмування': '1.0'}\
,"Тести по лекційним матеріалам (3 бали по 0.5 за кожен)": {'Тест 1': '1.0','Тест 2': '1.0',\
'Тест 3': '1.0','Тест 4': '1.0','Тест 5': '1.0','Тест 6': '1.0'},\
"Тести на LMS (3 бали по 0.3 за кожен)": {'Тест 1': '1.0','Тест 2': '1.0','Тест 3': '1.0',\
'Тест 4': '1.0','Тест 5': '1.0','Тест 6': '1.0','Тест 7': '1.0','Тест 8': '1.0','Тест 9': '1.0',\
'Тест 10': '1.0'},"Міні-проєкти (22 бали)": {'міні-проєкт 1': '1.0','міні-проєкт 2': '1.0'},\
"Фінальний іспит (30 балів)": {'Теоретичне завдання': '1.0','Завдання на програмування': '1.0',},\
"Додаткові бали (10 балів)": '1.0'}})
    ['Фединяк Степан']
    '''
    by_letter = []
    transformed = mark_transform(gradebook)
    for student, lettermark in transformed.items():
        if lettermark == letter:
            by_letter.append(student)
    return by_letter

def activity_report(grade_book: dict[(str, str, str, str), dict[str, dict[str, float]]],
                    activity_group: str):
    """
    Returns activity grades of all students

    :param grade_book:  dict[(str, str, str, str), dict[str, dict[str, float]]],key is student names
    :param activity_group: name of activity group
    :return: dict[(str, str, str, str), dict[str, float]], information of student and all
    grades from activity

    >>> students = {('Степан', 'Фединяк', 'step.fed@gmail.com', 'ПКН24-Б1'):\
{"Лабораторні роботи (22 бали)":\
{"Лабораторна робота 1": 1.5,"Лабораторна робота 2": 2.4, \
"Лабораторна робота 3": 5.6,"Лабораторна робота 4": 2.5,\
"Лабораторна робота 5": 8.7},"Тести по лекційним матеріалам":\
{'Тест 1': 1.4,'Тест 2': 3.5,'Тест 3': 2.5,'Тест 4': 1.3},\
"Тести на LMS": {'Тест 1': 1,'Тест 2': 1,'Тест 3': 1,'Тест 4': 0.8,\
'Тест 5': 3.2,'Тест 6': 1.4,'Тест 7': 3.6}}}
    >>> activity_report(students, "Лабораторні роботи (22 бали)") == \
{('Степан', 'Фединяк', 'step.fed@gmail.com', 'ПКН24-Б1'): \
{"Лабораторна робота 1": 1.5,"Лабораторна робота 2": 2.4, \
"Лабораторна робота 3": 5.6,"Лабораторна робота 4": 2.5,\
"Лабораторна робота 5": 8.7}}
    True
    """
    result = {}
    for student, activities in grade_book.items():
        result[student] = activities.get(activity_group, {})

    return result


def get_mean_by_activity_report(
        grade_book: grade_book_type,
        activity_groups: list[str]
) -> dict[str, float]:
    """
    Receives grade book and activity group(s) and builds a report
    of a mean grade of all students per an activity group
    :param grade_book: grade book dict
    :param activity_groups: list of activity group names
    :return: dict[str, float], report of a mean grade per activity group
    >>> grade_book = {('Степан', 'Фединяк', 'step.fed@gmail.com', 'ПКН24-Б1'):\
{"Лабораторні роботи (22 бали)":\
{"Лабораторна робота 1": 1.5,"Лабораторна робота 2": 2.4, \
"Лабораторна робота 3": 5.6,"Лабораторна робота 4": 2.5,\
"Лабораторна робота 5": 8.7},"Тести по лекційним матеріалам":\
{'Тест 1': 1.4,'Тест 2': 3.5,'Тест 3': 2.5,'Тест 4': 1.3},\
"Тести на LMS": {'Тест 1': 1,'Тест 2': 1,'Тест 3': 1,'Тест 4': 0.8,\
'Тест 5': 3.2,'Тест 6': 1.4,'Тест 7': 3.6}},\
("Юлія", "Колодій", "you.lia@gmail.com", "ПКН24-Б1"): \
{"Лабораторні роботи (22 бали)":\
{"Лабораторна робота 1": 3.2,"Лабораторна робота 2": 2.2, \
"Лабораторна робота 3": 7.0,"Лабораторна робота 4": 3.3,\
"Лабораторна робота 5": 5.8},"Тести по лекційним матеріалам":\
{'Тест 1': 2.4,'Тест 2': 4.0,'Тест 3': 2.8,'Тест 4': 1.5},\
"Тести на LMS": {'Тест 1': 1,'Тест 2': 0.8,'Тест 3': 0.8,'Тест 4': 0.8,\
'Тест 5': 4.0,'Тест 6': 1,'Тест 7': 3.6}}}
    >>> get_mean_by_activity_report(grade_book, ["Лабораторні роботи (22 бали)"]) == \
    {"Лабораторні роботи (22 бали)": 21.1}
    True
    >>> get_mean_by_activity_report(grade_book, ["Тести на LMS", "Тести по лекційним матеріалам", "Wrong group"]) == \
    {"Тести на LMS": 12.0, "Тести по лекційним матеріалам": 9.7}
    True
    >>> grade_book = {**grade_book, ("Vlad", "Bobryk", "email@gmail.com", "ПКН24-Б1"): {"Тести по лекційним матеріалам": {}, "Тести на LMS": {}}}
    >>> get_mean_by_activity_report(grade_book, ["Тести на LMS", "Тести по лекційним матеріалам"]) == \
    {"Тести на LMS": 8.0, "Тести по лекційним матеріалам": 6.47}
    True
    """
    mean_report = defaultdict(int)
    total_report = get_total_by_activity_report(grade_book, activity_groups)
    student_count = len(total_report)

    for _, activities in total_report.items():
        for activity, total in activities.items():
            mean_report[activity] += total

    return {act: round(total / student_count, 2) for act, total in mean_report.items()}


def get_total_by_activity_report(
        grade_book: grade_book_type,
        activity_groups: list[str] = None
) -> dict[str, dict[str, float]]:
    """
    Receives grade book and activity group(s) and builds a report with
    all students' total grade per activity group
    :param grade_book: grade book dict
    :param activity_groups: list of activity group names (optional)
    :return: dict[str, dict[str, float]], report with each student and total grade per activity group
    >>> grade_book = {('Степан', 'Фединяк', 'step.fed@gmail.com', 'ПКН24-Б1'):\
{"Лабораторні роботи (22 бали)":\
{"Лабораторна робота 1": 1.5,"Лабораторна робота 2": 2.4, \
"Лабораторна робота 3": 5.6,"Лабораторна робота 4": 2.5,\
"Лабораторна робота 5": 8.7},"Тести по лекційним матеріалам":\
{'Тест 1': 1.4,'Тест 2': 3.5,'Тест 3': 2.5,'Тест 4': 1.3},\
"Тести на LMS": {'Тест 1': 1,'Тест 2': 1,'Тест 3': 1,'Тест 4': 0.8,\
'Тест 5': 3.2,'Тест 6': 1.4,'Тест 7': 3.6}},\
("Юлія", "Колодій", "you.lia@gmail.com", "ПКН24-Б1"): \
{"Лабораторні роботи (22 бали)":\
{"Лабораторна робота 1": 3.2,"Лабораторна робота 2": 2.2, \
"Лабораторна робота 3": 7.0,"Лабораторна робота 4": 3.3,\
"Лабораторна робота 5": 5.8},"Тести по лекційним матеріалам":\
{'Тест 1': 2.4,'Тест 2': 4.0,'Тест 3': 2.8,'Тест 4': 1.5},\
"Тести на LMS": {'Тест 1': 1,'Тест 2': 0.8,'Тест 3': 0.8,'Тест 4': 0.8,\
'Тест 5': 4.0,'Тест 6': 1,'Тест 7': 3.6}}}
    >>> get_total_by_activity_report(grade_book, ["Лабораторні роботи (22 бали)"]) == \
{('Степан', 'Фединяк', 'step.fed@gmail.com', 'ПКН24-Б1'): {"Лабораторні роботи (22 бали)": 20.7},\
("Юлія", "Колодій", "you.lia@gmail.com", "ПКН24-Б1"): {"Лабораторні роботи (22 бали)": 21.5},}
    True
    >>> get_total_by_activity_report(grade_book, ["Тести на LMS", "Тести по лекційним матеріалам", "Wrong group"]) == \
{('Степан', 'Фединяк', 'step.fed@gmail.com', 'ПКН24-Б1'): {"Тести на LMS": 12, "Тести по лекційним матеріалам": 8.7},\
("Юлія", "Колодій", "you.lia@gmail.com", "ПКН24-Б1"): {"Тести на LMS": 12, "Тести по лекційним матеріалам": 10.7},}
    True
    >>> get_total_by_activity_report(grade_book) == \
{('Степан', 'Фединяк', 'step.fed@gmail.com', 'ПКН24-Б1'): {"Тести на LMS": 12, "Тести по лекційним матеріалам": 8.7, "Лабораторні роботи (22 бали)": 20.7},\
("Юлія", "Колодій", "you.lia@gmail.com", "ПКН24-Б1"): {"Тести на LMS": 12, "Тести по лекційним матеріалам": 10.7, "Лабораторні роботи (22 бали)": 21.5},}
    True
    """
    report = defaultdict(dict)
    for student, student_activity_groups in grade_book.items():
        for group in activity_groups or student_activity_groups:
            if (found := student_activity_groups.get(group)) is not None:
                grades = found.values()
                report[student][group] = sum(grades)

    return report


def add_grade_for_student(grade_book: grade_book_type, syllabus, name: str, surname: str,
                          email: str, group: str, activity_group: str, activity: str, grade: str):
    """
    Put grade for one student
    :param group: group of student
    :param email: email of student
    :param surname: surname of student
    :param name: name of student
    :param syllabus: syllabus with activities
    :param grade_book: grade book
    :param activity_group: str, activity group
    :param activity: str, activity
    :param grade: float, grade
    :return: None
    """
    if not is_activity_correct(syllabus, activity_group, activity):
        return

    mark = grade_check(grade, syllabus[activity_group][activity])

    grade_book[(surname, name, email, group)].setdefault(activity_group, {})[activity] = mark


def introduction(functions_interface: dict[str, tuple[object, int, str]]):
    """
    Returns gradebook introduction

    Args:
        functions_interface (dict[str, tuple[object, int, str]]): functions with descriptions

    Returns:
        str: string introduction

    >>> introduction({\
        "help": (\
            lambda args : print(introduction(functions_interface), end=""),\
            0,\
            "Виводить це повідомлення"\
        ),\
        "get_activities": (\
            lambda args : print(get_activities(activities)),\
            0,\
            "Виводить всі активності у форматі (група, активність)"\
        ),\
        "write_json": (\
            lambda args : write_json(args[0], gradebook),\
            1,\
            "Записує грейдбук у JSON файл. Аргумент - назва файлу"\
        )\
    })
    'Вітаємо в консольному інтерфейсі Gradebook! Ось перелік доступних команд:\\n\
help (для виклику необхідно 0 додаткових аргументів): Виводить це повідомлення.\\n\
get_activities (для виклику необхідно 0 додаткових аргументів): \
Виводить всі активності у форматі (група, активність).\\n\
write_json (для виклику необхідно 1 додаткових аргументів): \
Записує грейдбук у JSON файл. Аргумент - назва файлу.\\n\
Щоб вийти, введіть Q у будь-який момент.\\n\
Аргументи та команду потрібно розділяти крапкою з комою та пробілом: "; ".\\n\
Введіть команду у форматі: назва_команди; аргумент_1; аргумент_2; аргумент_3\\n'
    """
    res = "Вітаємо в консольному інтерфейсі Gradebook! Ось перелік доступних команд:\n"

    for item in functions_interface.items():
        res += f"{item[0]} (для виклику необхідно {item[1][1]} додаткових аргументів): \
{item[1][2] if item[1][2] else "Опис відсутній"}.\n"

    res += "Щоб вийти, введіть Q у будь-який момент.\n"
    res += "Аргументи та команду потрібно розділяти крапкою з комою та пробілом: \"; \".\n"
    res += "Введіть команду у форматі: назва_команди; аргумент_1; аргумент_2; аргумент_3\n"

    return res


def get_user_input(functions_interface:
dict[str, tuple[object, int, str]]) -> tuple[object, list[str]] | None:
    """
    Gets command from user

    Args:
        functions_interface (dict[str, tuple[object, int, str]]): functions with description

    Returns:
        (tuple[object, list[str]] | None): function to call and arguments or None if should quit
    """
    while True:
        print(">>> ", end="")
        inp = input().strip()

        if inp.lower() == "q":
            return None

        parts = [part for part in inp.split("; ") if part]

        if not parts:
            print("Неправильний формат команди.")
            continue
        if parts[0].lower() not in functions_interface.keys():
            print("Такої команди не існує.")
            continue
        if len(parts) - 1 != functions_interface[parts[0].lower()][1]:
            print("Неправильна кількість аргументів.")
            continue

        return functions_interface[parts[0].lower()][0], parts[1:]


def main():
    """
    Main interface function
    """

    functions_interface = {
        "help": (
            lambda args: print(introduction(functions_interface), end=""),
            0,
            "Виводить це повідомлення"
        ),
        "get_activities": (
            lambda args: print(get_activities(syllabus)),
            0,
            "Виводить всі активності у форматі (група, активність)"
        ),
        "write_json": (
            lambda args: write_json(args[0], gradebook, syllabus),
            1,
            "Записує грейдбук у JSON файл. Аргумент - назва файлу"
        ),
        "get_grades_from_file": (
            lambda args: get_grades_from_file(args[0], gradebook, syllabus),
            1,
            "Читає оцінки за активності за файлу та записує у grade_book. Аргумент - назва файлу"
        ),
        "add_grade_for_student": (
            lambda args: add_grade_for_student(gradebook, syllabus, *args),
            1,
            "Виставляє оцінку студенту. Аргументи - прізвище, ім'я, пошта, група студента, "
            "група активності, активність, оцінка"
        ),
        "get_mean_by_activity_report": (
            lambda args: pprint(get_mean_by_activity_report(gradebook, args[0].split(','))),
            1,
            "Виводить середній бал усіх студентів за обраними активностями у форматі (назва активності: середній бал).\n"
            "Аргумент - список активностей (1 або більше) через кому"
        ),
        "get_total_by_activity_report": (
            lambda args: pprint(get_total_by_activity_report(
                gradebook,
                args[0].split(',') if args[0] != "ALL"
                else [elem[0] for elem in get_activities(syllabus)]
            )),
            1,
            "Виводить сумарний бал для кожного зі студентів згідно обраних або всіх активностей у форматі (студент: навза активності: сумарний бал).\n"
            "Аргумент - список груп активностей (1 або більше) через кому або ALL для всіх активностей"
        ),
        "letter_report": (
            lambda args: print(letter_report(args[0], gradebook)),
            1,
            "Виводить список студентів згідно з оцінкою у вигляді літери.\n"
            "Аргумент - літера згідно якої потрібно вивести всіх студентів з такою оцінкою"
        ),
        "stud_grade_book_to_json": (
            lambda args: stud_grade_book_to_json(args[0], args[1], gradebook),
            2,
            "Записує грейдбук для одного студента у JSON файл. Аргумент 1 - назва файлу,\
(filename.json), аргумент 2 - email студента (email@gmail.com)."
        ),
        "add_student": (
            lambda args: add_student(gradebook, tuple(args)),
            4,
            "Додає студента до грейдбуку. Приймає 4 аргументи, приклад вводу, щоб додати студента:\
 add_student Прізвище; Ім'я; пошта; група"
        ),
        "del_activity": (
            lambda args: del_activity(syllabus, gradebook, args[0], args[1]),
            2,
            "Видаляє активність з силабуса та журналу оцінок для кожного студента \
у форматі (група, активність)"
        ),
        "add_activity": (
            lambda args: add_activity(syllabus, args[0], args[1], float(args[2])),
            3,
            "Додає активність в силабус за групою активності, назвою та максимальним балом"
        )
    }

    gradebook = {}
    syllabus = {'Лабораторні_роботи': {'Лабораторна_робота_1': 2.0, 'Лабораторна_робота 2': 2.0},
                'Тести': {'Тест_1': 1.0, 'Тест_2': 1.0},
                'Мідтерм': {'Мідтерм_теорія': 5.0, 'Мідтерм_практика': 15.0}}

    functions_interface["help"][0]([])

    while True:
        data = get_user_input(functions_interface)

        if data is None:
            return

        try:
            data[0](data[1])
        except Exception:
            print("Виникла неочікувана помилка. Спробуйте перевірити введені аргументи")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    main()
