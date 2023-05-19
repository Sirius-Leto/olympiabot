from typing import List

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from .__base import Base
from .__mixins import IdMixin, NameDescriptionMixin


class Grade(IdMixin, NameDescriptionMixin, Base):
    __tablename__ = "grades"


# 9th grade, 10th grade, 11th grade included in the 9-11th grade
# 12th grade, 13th grade included in the 12-13th grade
# make connection between 9,10,11 and 9-11
class ComplexGrade(IdMixin, NameDescriptionMixin, Base):
    __tablename__ = "complex_grades"

    grades: Mapped[List[Grade]] = relationship("Grade", secondary="complex_grades_x_grades",
                                               backref="connected_complex_grades")


complex_grades_x_grades = Table(
    "complex_grades_x_grades",
    Base.metadata,
    Column("complex_grade_id", ForeignKey("complex_grades.id"), primary_key=True),
    Column("grade_id", ForeignKey("grades.id"), primary_key=True),
)
