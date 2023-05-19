from .__mixins import IdMixin, TimestampMixin, NameDescriptionMixin, TagsViewMixin, ReferenceMixinFactory


class EventTypeBase(TimestampMixin, NameDescriptionMixin):
    ...


class EventTypeCreate(EventTypeBase):
    ...


class EventTypeView(IdMixin, TagsViewMixin, EventTypeBase):
    class Config:
        orm_mode = True


class EventTypeReference(ReferenceMixinFactory(EventTypeView)):
    ...
