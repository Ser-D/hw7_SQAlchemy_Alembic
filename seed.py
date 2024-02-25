import random
from datetime import datetime, timedelta

from faker import Faker
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from conf.db import session
from conf.models import Teacher, Student, Group, Discipline, Grade

fake = Faker('uk-UA')

GRADES_COUNT = 20


def seeder():
    disciplines_list = [
        'Business',
        'Communication',
        'Humanities',
        'Social Sciences',
        'Science',
        'Mathematics'
    ]

    group_list = [
        'group_1',
        'group_2',
        'group_3'
    ]

    def seed_groups():
        for _ in range(3):
            group = Group(
                name=group_list[_]
            )
            session.add(group)
        session.commit()

    def seed_students():
        group_ids = session.scalars(select(Group.id)).all()
        for _ in range(30):
            student = Student(
                fullname=fake.name(),
                group_id=random.choice(group_ids)
            )
            session.add(student)
        session.commit()

    def seed_teachers():
        for _ in range(5):
            teacher = Teacher(
                fullname=fake.name()
            )
            session.add(teacher)
        session.commit()

    def seed_disciplines():
        teacher_ids = session.scalars(select(Teacher.id)).all()
        for discipline in disciplines_list:
            session.add(Discipline(name=discipline, teacher_id=random.choice(teacher_ids)))
        session.commit()

    def seed_grades():
        start_date = datetime.strptime("01.01.2023", "%d.%m.%Y")
        student_ids = session.scalars(select(Student.id)).all()
        discipline_ids = session.scalars(select(Discipline.id)).all()

        for student_id in student_ids:
            for _ in range(GRADES_COUNT):
                random_subject_id = random.choice(discipline_ids)
                date_grade = start_date + timedelta(random.randint(1, 360))
                grade = Grade(
                    grade=random.randint(0, 100),
                    grade_date=date_grade.date(),
                    student_id=student_id,
                    discipline_id=random_subject_id
                )
                session.add(grade)
        session.commit()

    try:
        seed_groups()
        seed_students()
        seed_teachers()
        seed_disciplines()
        seed_grades()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
    finally:
        session.close()


if __name__ == '__main__':
    seeder()
