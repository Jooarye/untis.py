from objects import Time, Date


def parse_date(date: int):
    year = date // 10000
    month = (date - year * 10000) // 100
    day = date % 100

    return Date(day, month, year)


def parse_time(time: int):
    hours = time // 100
    minutes = time % 100
    
    return Time(hours, minutes)


def selection_sort(data: list, key=lambda x, y: x > y):
    for j in range(len(data) - 1):
        minimum = j

        for i in range(j+1, len(data)):
            if key(data[i], data[minimum]):
                minimum = i

        data[j], data[minimum] = data[minimum], data[j]

    return data


def select(data: list, key=lambda x: True):
    return [x for x in data if key(x)]