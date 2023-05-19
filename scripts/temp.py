from pydantic import BaseModel


class Mixin(BaseModel):
    id: int = 123


class Mixin2(BaseModel):
    id: str = "abc"


class Model(Mixin, Mixin2):
    id: bool = True


if __name__ == "__main__":
    print(Model(id=456))
    print(Model())
