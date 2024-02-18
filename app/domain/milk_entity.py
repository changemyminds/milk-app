from datetime import datetime


class MilkEntity:
    def __init__(self, id: int, time_range: str, cc: int, create_time: datetime):
        self.id = id
        self.time_range = time_range
        self.cc = cc
        self.create_time = create_time

    @classmethod
    def new(cls, time_range: str, cc: int, create_time: datetime):
        return cls(id=None, time_range=time_range, cc=cc, create_time=create_time)
