from sqlalchemy import func, desc, select, and_

from conf.models import Grade, Teacher, Student, Group, Discipline
from conf.db import session

import sys


def select_01():
    """
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM students s
    JOIN grades g ON s.id = g.student_id
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 5;
    """
    result = (
        session.query(
            Student.id,
            Student.fullname,
            func.round(func.avg(Grade.grade), 2).label("average_grade"),
        )
        .select_from(Student)
        .join(Grade)
        .group_by(Student.id)
        .order_by(desc("average_grade"))
        .limit(5)
        .all()
    )
    return print(result)


def select_02():
    """
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM grades g
    JOIN students s ON s.id = g.student_id
    where g.discipline_id = 1
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 1;
    """
    result = (
        session.query(
            Student.id,
            Student.fullname,
            func.round(func.avg(Grade.grade), 2).label("average_grade"),
        )
        .select_from(Grade)
        .join(Student)
        .filter(Grade.discipline_id == 1)
        .group_by(Student.id)
        .order_by(desc("average_grade"))
        .limit(1)
        .all()
    )
    return print(result)


def select_03():
    """
    SELECT
        groups.name AS group_name,
        discipline.name AS discipline_name,
        ROUND(AVG(grades.grade), 2) AS average_grade
    from grades
    join students ON grades.student_id = students.id
    join groups ON students.group_id = groups.id
    join disciplines  ON grades.discipline_id = disciplines.id
    where disciplines.id = 2
    GROUP BY
        groups.name,
        disciplines.name
    order by
        groups.name;
    """
    result = (
        session.query(
            Group.name,
            Discipline.name,
            func.round(func.avg(Grade.grade), 2).label("average_grade"),
        )
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .join(Discipline)
        .filter(Discipline.id == 3)
        .group_by(Group.name, Discipline.name)
        .order_by(Group.name)
        .all()
    )
    return print(result)


def select_04():
    """
    SELECT
        groups.name AS group_name,
        students.fullname AS student_name,
        ROUND(AVG(gr.grade), 2) AS avenger_grade
    FROM grades gr
    JOIN students ON gr.student_id = students.id
    JOIN groups ON students.group_id = groups.id
    JOIN disciplines ON gr.discipline_id = disciplines.id
    GROUP BY
        groups.name,
        students.fullname ;
    """
    result = (
        session.query(Group.name, func.round(func.avg(Grade.grade)))
        .select_from(Grade)
        .join(Student)
        .join(Discipline)
        .join(Group)
        .group_by(Group.name)
        .all()
    )
    return print(result)


def select_05():
    """SELECT
        teachers.fullname AS teacher,
        disciplines.name AS discipline_name
    from disciplines
    JOIN teachers on disciplines.teacher_id = teachers.id
    where teacher_id = 2
    GROUP by teachers.fullname, disciplines.name;"""

    result = (
        session.query(Teacher.fullname, Discipline.name)
        .select_from(Discipline)
        .join(Teacher)
        .filter(Teacher.id == 2)
        .group_by(Teacher.fullname, Discipline.name)
        .all()
    )
    return print(result)


def select_06():
    """
    ````SELECT
            students.fullname AS student_name,
            groups.name AS group_name
        from students
        JOIN groups on groups.id = students.group_id
        where groups.id = 2
    """

    result = (
        session.query(Student.fullname, Group.name)
        .select_from(Student)
        .join(Group)
        .filter(Group.id == 2)
        .all()
    )
    return print(result)


def select_07():
    """
    select
        students.fullname AS student_name,
        groups.name AS group_name,
        disciplines.name AS disciplines_name,
        grades.grade AS student_grade
    FROM grades
    JOIN students on grades.student_id = students.id
    JOIN groups on students.group_id = groups.id
    JOIN disciplines on grades.discipline_id = disciplines.id
    where groups.id = 1 AND disciplines.id = 9
    ORDER BY students.fullname"""

    result = (
        session.query(Student.fullname, Group.name, Discipline.name, Grade.grade)
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .join(Discipline)
        .filter(and_(Group.id == 1, Discipline.id == 3))
        .order_by(Student.fullname)
        .all()
    )
    return print(result)


def select_08():
    """
    SELECT
        teachers.fullname AS teacher_name,
        disciplines.name AS discipline_name,
        ROUND(AVG(grades.grade), 2) AS average_grade
    FROM disciplines
    JOIN teachers ON disciplines.teacher_id = teachers.id
    JOIN grades ON grades.student_id = disciplines.id
    WHERE teachers.id = '3'
    GROUP by
        teachers.fullname,
        disciplines.name;
    """
    result = (
        session.query(Teacher.fullname, Discipline.name, func.round(func.avg(Grade.grade)))
        .select_from(Discipline)
        .join(Teacher)
        .join(Grade)
        .filter(Teacher.id == 3)
        .group_by(Teacher.fullname, Discipline.name)
        .all()
    )
    return print(result)


def select_09():
    """
    SELECT
        students.fullname AS student_name,
        disciplines.name AS discipline_name
    FROM disciplines
    JOIN grades ON grades.discipline_id  = disciplines.id
    JOIN students ON grades.student_id = students.id
    WHERE students.id = '1'
    GROUP BY
        student_name,
        discipline_name;
    """
    result = (
        session.query(Student.fullname, Discipline.name)
        .select_from(Discipline)
        .join(Grade)
        .join(Student)
        .filter(Student.id == 1)
        .group_by(Student.fullname, Discipline.name)
        .all()
    )
    return print(result)


def select_10():
    """
    select distinct
        students.fullname AS student_name,
        disciplines.name AS discipline_name,
        teachers.fullname AS teacher_name
    FROM disciplines
    JOIN grades ON grades.discipline_id  = disciplines.id
    JOIN teachers ON disciplines.teacher_id = teachers.id
    JOIN students ON grades.student_id = students.id
    WHERE students.id = 30 --AND teacher_id = 1
    GROUP BY
        students.fullname, disciplines.name, teachers.fullname ;
    """
    result = (
        session.query(Student.fullname, Discipline.name, Teacher.fullname)
        .select_from(Discipline)
        .join(Grade)
        .join(Teacher)
        .join(Student)
        .filter(Student.id == 30)
        .group_by(Student.fullname, Discipline.name, Teacher.fullname)
        .all()
    )
    return print(result)


def select_11():
    """
    SELECT ROUND(AVG(grades.grade)) as Avenger_grade
    FROM grades
    JOIN students on grades.student_id = students.id
    JOIN disciplines on grades.discipline_id = disciplines.id
    WHERE grades.student_id = 28 and disciplines.teacher_id = 1
    """

    result = (
        session.query(func.round(func.avg(Grade.grade)).label("Avenger_grade"))
        .select_from(Grade)
        .join(Discipline)
        .filter(and_(Discipline.teacher_id == 4, Grade.student_id == 3))
        .all()
    )
    return print(result)


def select_12():
    """
    select max(grade_date)
    from grades g
    join students s on s.id = g.student_id
    where g.discipline_id = 2 and s.group_id  =3;

    select s.id, s.fullname, g.grade, g.grade_date
    from grades g
    join students s on g.student_id = s.id
    where g.discipline_id = 2 and s.group_id = 3 and g.grade_date = (
        select max(grade_date)
        from grades g2
        join students s2 on s2.id=g2.student_id
        where g2.discipline_id = 2 and s2.group_id = 3
    );
    :return:
    """

    subquery = (
        select(func.max(Grade.grade_date))
        .join(Student)
        .filter(and_(Grade.discipline_id == 2, Student.group_id == 3))
    ).scalar_subquery()

    result = (
        session.query(Student.id, Student.fullname, Grade.grade, Grade.grade_date)
        .select_from(Grade)
        .join(Student)
        .filter(
            and_(
                Grade.discipline_id == 2,
                Student.group_id == 3,
                Grade.grade_date == subquery,
            )
        )
        .all()
    )

    return print(result)


def main(cmd: str):
    cmd_dict = {
        "1": select_01,
        "2": select_02,
        "3": select_03,
        "4": select_04,
        "5": select_05,
        "6": select_06,
        "7": select_07,
        "8": select_08,
        "9": select_09,
        "10": select_10,
        "11": select_11,
        "12": select_12,
    }

    def func_runner(cmd):
        return cmd_dict.get(cmd)

    if cmd in cmd_dict.keys():
        res = func_runner(cmd)
        if res:
            res()


if __name__ == "__main__":
    main(sys.argv[1])
