https://github.com/todomd

https://github.com/todo-md/todo-md

# Top-Down

1.Start with an initial problem statement.

2.Define subtask at the first level.

3.Divide subtasks at a higher level into more specific tasks.

4.Repeat step (3) until each subtask is trivial.

5.Refine the algorithm into real code.



# Gradebook
Розробити аналог грейдбуку в cms.

### Todo

- [x] Створити gradebook ~3d #feat @john 2020-03-20
  - [x] Створення пустого грейдбука - **Копач Тарас**
  - [x] Додавання студента
    - [x] Створити функцію add_student(grade_book, student_info) - **Копач Тарас**
  - [x] Видалення активності
    - [x] Створити функцію del_activity(gradebook, activity) - **Бугір Єлизавета**
  - [x] Додавання активності
    - [x] Створити функцію add_activity(gradebook, activity) - **Косів Марта**

- [x] Виставлення оцінок
  - [x] Функція grade_check(grade, activity) перевіряє чи оцінка не від'ємна, і чи вона не 
    більше максимуму - **Іван Зарицький**
  - [x] Функція is_activity_correct(syllabus, activity_group, activity) - **Іван Зарицький**
  - [x] Виставлення оцінок за окрему активність окремим студентам - **Іван Зарицький**
  - [x] Виставлення оцінок за окрему активність завантаженням з файла - **Іван Зарицький**

- [x] Виведення звітів
  - [x] Вивести сумарний бал по кожному студенту згідно типів активностей. **Vladyslav Bobryk**
  - [x] Створити функцію activity_report(grade_book, activity) - **Mukola Balyk**
  - [x] Вивести середній бал усіх студентів по одній або декільком активностям. **Vladyslav Bobryk**
  - [x] Вивести список студентів з балом, що перетворений у літеру A-E **Deputat Anton**
  - [x] Вивести список студентів, згідно вказаної літери **Zakhar Veresniuk**

- [x] Збереження грейдбуку у файл
  - [x] Збереження грейдбуку усіх студентів з оцінками у json файл.
  - [x] Збереження грейдбуку для студента з оцінками у json файл. **Лиханський Олександр**

- [x] Додати можливість комунікації з програмою за допомогою консольного інтерфейсу
  - [x] Функція main для запуску програми. **Roman Leshchuk**
  - [x] Функція introduction для виведення правил та команд. **Roman Leshchuk**
  - [x] Функція get_user_input для отримання команди від користувача. **Roman Leshchuk**
