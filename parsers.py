from objects import Lesson, Teacher, Subject, Room
from utils import parse_date, parse_time


class UntisParser:
    def __init__(self, data: dict):
        self.data = data['data']['result']['data']
        self.objects = []

        for element in self.data['elements']:
            id = element['id']

            # INFO: possible parser extensions here
            if element['type'] == 1:
                pass
            elif element['type'] == 2:
                name = element['name']
                self.objects.append(Teacher(id, name))
            elif element['type'] == 3:
                name = element['name']
                long_name = element['longName']
                self.objects.append(Subject(id, name, long_name))
            elif element['type'] == 4:
                name = element['name']
                long_name = element['longName']
                capacity = element['roomCapacity']
                self.objects.append(Room(id, name, long_name, capacity))

    def get_object(self, id: int, obj_type):
        for obj in self.objects:
            if obj.id == id and isinstance(obj, obj_type):
                return obj
        
        return None

    def get_lessons(self):
        lessons = []

        joined_list = [x for y in self.data['elementPeriods'].values() for x in y]

        for element in joined_list:
            id = element['id']
            text = element['lessonText']
            date = parse_date(element['date'])
            start = parse_time(element['startTime'])
            end = parse_time(element['endTime'])
            teachers = []
            subject = None
            rooms = []
            exam = element['is']['exam'] if 'is' in element and 'exam' in element['is'] else False
            substitution = element['is']['substitution'] if 'is' in element and 'substitution' in element['is'] else False
            additional = element['is']['additional'] if 'is' in element and 'additional' in element['is'] else False

            for info in element['elements']:
                info_id = info['id']

                if info['type'] == 1:
                    pass
                elif info['type'] == 2:
                    teachers.append(self.get_object(info_id, Teacher))
                elif info['type'] == 3:
                    subject = self.get_object(info_id, Subject)
                elif info['type'] == 4:
                    rooms.append(self.get_object(info_id, Room))

            lesson = Lesson(id, text, teachers, subject, rooms, start, end, date, exam, substitution, additional)
            lessons.append(lesson)

        return lessons