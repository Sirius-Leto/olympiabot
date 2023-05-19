from .__mixins import NameDescriptionMixin, IdMixin, ReferenceMixinFactory


class GradeBase(NameDescriptionMixin):
    ...


class GradeCreate(GradeBase):
    ...


class GradeView(IdMixin, GradeBase):
    ...

    class Config:
        orm_mode = True


class GradeReference(ReferenceMixinFactory(GradeView)):
    ...


class ComplexGrade(NameDescriptionMixin):
    ...


class ComplexGradeCreate(ComplexGrade):
    grades: list[GradeReference]


class ComplexGradeView(IdMixin, ComplexGrade):
    grades: list[GradeView]

    class Config:
        orm_mode = True


class ComplexGradeReference(ReferenceMixinFactory(ComplexGradeView)):
    ...
