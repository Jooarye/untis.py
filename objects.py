from typing import List
from datetime import date


class UntisObject:
    def __init__(self, id: int):
        self.id = id


class Date:
    def __init__(self, day: int, month: int, year: int):
        self.day = day
        self.month = month
        self.year = year

    @staticmethod
    def from_datetime(d: date):
        return Date(d.day, d.month, d.year)

    def __eq__(self, other):
        return self.day == other.day and self.month == other.month and self.year == other.year

    def __str__(self):
        return f"{self.month:0>2d}/{self.day:0>2d}/{self.year:0>4d}"


class Time:
    def __init__(self, hours: int, minutes: int):
        self.hours = hours
        self.minutes = minutes

    def __eq__(self, other):
        return self.hours == other.hours and self.minutes == other.minutes

    def __gt__(self, other):
        return self.hours > other.hours or (self.hours == other.hours and self.minutes > other.minutes)

    def __lt__(self, other):
        return self.hours < other.hours or (self.hours == other.hours and self.minutes < other.minutes)

    def __str__(self):
        pm = self.hours >= 13
        hrs = self.hours if not pm and self.hours != 13 else self.hours - 12

        return f"{hrs:0>2d}:{self.minutes:0>2d} {'pm' if pm else 'am'}"


class Teacher(UntisObject):
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        super(Teacher, self).__init__(id)


class Subject(UntisObject):
    def __init__(self,
            id: int, name: str, 
            long_name: str):
        self.id = id
        self.name = name
        self.long_name = long_name
        super(Subject, self).__init__(id)


class Room(UntisObject):
    def __init__(self,
            id: int, name: str, 
            long_name: str, capacity: int):
        self.id = id
        self.name = name
        self.long_name = long_name
        self.capacity = capacity
        super(Room, self).__init__(id)


class Lesson(UntisObject):
    def __init__(
            self, 
            id: int, text: str,
            teachers: List[Teacher], subject: Subject,
            rooms: List[Room], start: Time,
            end: Time, date: Date,
            exam: bool, substitution: bool,
            additional: bool):
        self.id = id
        self.text = text
        self.teachers = teachers
        self.subject = subject if isinstance(subject, Subject) else None
        self.rooms = rooms
        self.start = start
        self.end = end
        self.date = date
        self.exam = exam
        self.substitution = substitution
        self.additional = additional
        self.standard = not substitution and not additional
        super(Lesson, self).__init__(id)

    def __str__(self):
        return f"Lesson({self.id}, {self.subject.long_name if self.subject else 'None'}, {self.teachers[0].name if self.teachers else 'None'}, {self.rooms[0].name if self.rooms else 'None'}, {str(self.date)}, {str(self.start)}-{str(self.end)}, exam={self.exam}, substitution={self.substitution}, additional={self.additional})"

    def __repr__(self):
        return self.__str__()
