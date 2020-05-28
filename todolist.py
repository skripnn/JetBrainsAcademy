from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///list.db?check_same_thread=False')

Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='unnamed task')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return f'{self.task}, {self.deadline}'


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

class Menu:

    menu = ['Exit',
            "Today's tasks",
            "Week's tasks",
            'All tasks',
            'Add task']

    def __init__(self):
        self.print_menu()

    def print_menu(self):
        for n, i in enumerate(self.menu):
            if n == 0:
                last_item = f'{n}) {i}'
                continue
            print(f'{n}) {i}')
        print(last_item)

    def input(self, n):
        print('')
        n = self.menu[int(n)]
        if n == 'Exit':
            print('Bye!')
            exit()
        elif n == "Today's tasks":
            self.todays_task()
        elif n == "Week's tasks":
            self.weeks_tasks()
        elif n == 'All tasks':
            self.all_tasks()
        elif n == 'Add task':
            self.add_task()

        print('')
        self.print_menu()

    def all_tasks(self):
        session = Session()
        rows = session.query(Task).all()
        if len(rows) == 0:
            print('Nothing to do!')
        else:
            print('All tasks:')
            for n, row in enumerate(rows, 1):
                deadline = row.deadline.day + row.deadline.strftime("%b")
                print(f'{n}. {row}. {deadline}')
        print('')

    def weeks_tasks(self):
        day = datetime.today().date()
        for _ in range(7):
            print(f'{day.strftime("%A")} {day.day} {day.strftime("%b")}:')
            self.print_tasks(day)
            day += timedelta(days=1)

    def print_tasks(self, day):
        session = Session()
        rows = session.query(Task).filter(Task.deadline == day).all()
        if len(rows) == 0:
            print('Nothing to do!')
        else:
            for n, row in enumerate(rows, 1):
                print(f'{n}. {row}')
        print('')

    def todays_task(self):
        day = datetime.today().date()
        print(f'Today {day.day} {day.strftime("%b")}:')
        self.print_tasks(day)

    def add_task(self):
        task = input('Enter activity\n')
        date = input('Enter deadline\n')
        deadline = datetime.strptime(date, '%Y-%m-%d').date()
        session = Session()
        new_row = Task(task=task,
                       deadline=deadline)
        session.add(new_row)
        session.commit()
        print('The task has been added!')


if __name__ == '__main__':
    menu = Menu()
    while True:
        menu.input(input())
