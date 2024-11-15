from selenium import webdriver
from bs4 import BeautifulSoup
from itertools import groupby
import re

def parseTimetable(timetable):
    workdays = []
    saturdays = []
    sundays = []
    for line1 in timetable.find_all("tr"):
        departures = []
        for line2 in line1.find_all("td"):
            departures.append(line2.text.replace('\n', ''))
        if (len(departures) != 0):
            if departures[0] != ' ' and re.fullmatch(r"^\d{2}:\d{2} ", departures[0]):
                workdays.append(departures[0][:-1])
            if len(departures) >= 2 and re.fullmatch(r"^\d{2}:\d{2} ", departures[0]):
                saturdays.append(departures[1][:-1])
            if len(departures) == 3 and re.fullmatch(r"^\d{2}:\d{2} ", departures[0]):
                sundays.append(departures[2][:-1])
        if (len(departures) == 0):
            workdays.append("sep")
            saturdays.append("sep")
            sundays.append("sep")
    return (workdays, saturdays, sundays)

def parseTimetable_o(timetable):
    workdays = []
    saturdays = []
    sundays = []
    for line1 in timetable.find_all("tr"):
        departures = []
        for line2 in line1.find_all("td"):
            departures.append(line2.text.replace('\n', ' ')[1:-1])
        if (len(departures) != 0):
            if departures[0] != ' ':
                workdays.append(departures[0])
            if len(departures) >= 2:
                saturdays.append(departures[1])
            if len(departures) == 3:
                sundays.append(departures[2])
        if (len(departures) == 0):
            workdays.append("sep")
            saturdays.append("sep")
            sundays.append("sep")
    return (workdays, saturdays, sundays)


def printTimetable(name, timetable):
    print(name)
    for i in [list(directions) for key, directions in groupby(timetable, lambda x: x != "sep") if key][0]:
        print(i, end=' ')
    print('\n', end='')
    for i in [list(directions) for key, directions in groupby(timetable, lambda x: x != "sep") if key][1]:
        print(i, end=' ')
    print('\n')
    return ()

url = input('Enter route url or press enter:')
name = url[(url.find('hkod')+5):(url.find('&'))]

if url == '':
    f = open("./page.html", 'r', encoding='UTF-8')
    page_source = f.read()
    f.close()
else:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    page_source = driver.page_source
    f = open("./page.html", 'w', encoding='UTF-8')
    f.write(page_source)
    f.close()
    driver.quit()

f = open("./route_info.txt", "w", encoding="UTF-8")
f.write(name)

soup = BeautifulSoup(page_source, "html.parser")

options = soup.find_all("div", class_="custom-option-item maproute")
for i, option in enumerate(options):
    options[i] = (option.text.title() + '\n')
options.insert(1, "All stops reverse\n")

timetable = soup.find("div", class_="departure-times-body")
main = parseTimetable(timetable)

timetables_o = soup.find_all("table", class_="line-table")
for i, timetable in enumerate(timetables_o):
     if i > 1:
        timetables_o[i] = parseTimetable_o(timetable)


stops = soup.find_all("div", class_="line-pass-item")
i = 0
for stop in stops:
    stop_data = stop.find("p").text.strip()
    stop_data = stop_data.replace("I", "ı")
    dot = stop_data.find(".")
    if stop_data[:2] == "1.":
        if i == 0:
            f.write('\n' + options[i])
            for day in main:
                split = [list(directions) for key, directions in groupby(day, lambda x: x != "sep") if key]
                if split:
                    for j in split[0]:
                        f.write(j + ' ')
                f.write('\n')
        if i == 1 and len([list(directions) for key, directions in groupby(main[0], lambda x: x != "sep") if key]) >=2:
            f.write('\n' + options[i])
            for day in main:
                split = [list(directions) for key, directions in groupby(day, lambda x: x != "sep") if key]
                if len(split) > 0:
                    for j in split[1]:
                        f.write(j + ' ')
                f.write('\n')
        if i == 1 and len([list(directions) for key, directions in groupby(main[0], lambda x: x != "sep") if key]) < 2:
            i += 1
        if i > 1:
            f.write('\n' + options[i])
            for day in range(3):
                for j in timetables_o[i][day][2:]:
                    f.write(j + ' ')
                f.write('\n')
        i += 1
    f.write(stop_data.title()[(dot + 2):] + '\n')

info = soup.find("div", class_="line-info")
string = info.text.replace('\n', ' ')
f.write('\n' + string[(string.find('dk')-3):string.find('dk')] + 'minutes')
print("Route parsed!")

f.close()