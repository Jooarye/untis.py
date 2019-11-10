from .utils import selection_sort, select
from .parsers import UntisParser
from requests import get, post
from getpass import getpass
from .objects import Date
from json import loads


def get_json_info(username: str, password: str, school: str, date: Date, id: str, log=True):
    data_url = "https://cissa.webuntis.com/WebUntis/api/public/timetable/weekly/data?elementType={eType}&elementId={eId}&date={dYear}-{dMonth}-{dDay}&formatId={fId}"
    login_url = "https://cissa.webuntis.com/WebUntis/j_spring_security_check"

    if log:
        print("[*] Logging into Untis ...")

    response = post(login_url, headers={
        "Host": "cissa.webuntis.com",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept": "application/json", "Accept-Language": "en-GB,en;q=0.5", "Accept-Encoding": "gzip, deflate, br",
        "Referer": f"https://cissa.webuntis.com/WebUntis/?school={school.replace(' ', '+')}",
        "Content-Type": "application/x-www-form-urlencoded", "Origin": "https://cissa.webuntis.com",
        "Content-Length": "76"
    }, data={
        "school": school, "j_username": username,
        "j_password": password, "token": ""
    })

    cookies = " ".join([v for k, v in response.headers.items() if k.lower() == "set-cookie"])

    if 'auth' not in cookies:
        raise Exception("Login failed!")

    if log:
        print("[*] Pulling information ...")

    data_response = get(data_url.format(**{
        "eType": "1", "eId": id,
        "dYear": str(date.year), "dMonth": str(date.month),
        "dDay": str(date.day), "fId": 1
    }), headers={
        "Cookie": cookies, "Host": "cissa.webuntis.com",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept": "application/json", "Accept-Language": "en-GB,en;q=0.5", "Accept-Encoding": "gzip, deflate, br",
        "Referer": f"https://cissa.webuntis.com/WebUntis/?school={school.replace(' ', '+')}"
    })

    return data_response.content


if __name__ == '__main__':
    logging = False
    school = input("School > ")
    date = input("Date > ")
    user = input("Username > ")
    password = getpass(prompt="Password > ")

    day, month, year = (int(x) for x in date.split('.'))

    d = Date(day, month, year)

    if logging:
        print("[*] Parsing info ...")

    parser = UntisParser(loads(get_json_info(user, password, school, d, "305", log=logging)))

    lessons = select(parser.get_lessons(), key=lambda x: x.date == d)
    lessons_sorted = selection_sort(lessons, key=lambda x, y: x.end < y.start)

    print("\n".join([str(x) for x in lessons_sorted]))
