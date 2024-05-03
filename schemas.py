from pydantic import BaseModel


class NoteBase(BaseModel):
    title: str
    text: str

    class Config:
        orm_mode = True



class NoteCreate(NoteBase):
    class Config:
        orm_mode = True
