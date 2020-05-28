from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///list.db?check_same_thread=False')

Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return f'{self.task}, {self.deadline}'


Base.metadata.create_all(engine)


class Menu:
    state = None

    menu = ['Exit',
            "Today's tasks",
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
        if self.state is None:
            print('')
            n = int(n)
            if n == 0:
                print('Bye!')
                exit()
            elif n == 1:
                self.todays_task()
            elif n == 2:
                print('Enter task')
                self.state = self.menu[n]

        elif self.state == self.menu[2]:
            self.add_task(n)
            self.state = None

        if self.state is None:
            print('')
            self.print_menu()

    def todays_task(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        rows = session.query(Task).all()
        if len(rows) == 0:
            print('Nothing to do!')
        else:
            print('Today:')
            for row in rows:
                print(f'{row.id}. {row}')

    def add_task(self, task):
        Session = sessionmaker(bind=engine)
        session = Session()
        new_row = Task(task=task)
        session.add(new_row)
        session.commit()
        print('The task has been added!')


if __name__ == '__main__':
    menu = Menu()
    while True:
        menu.input(input())
