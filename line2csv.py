import sys
import re
import csv

def line2csv(path):
    file = open(path, "rt", encoding="utf-8")

    date_pattern = re.compile(r"^\d{4}/\d{2}/\d{2}")
    time_pattern = re.compile(r"^\d{2}:\d{2}")
    name_pattern = re.compile(r"\t.+\t")

    table = []
    table.append(['date', 'time', 'name', 'message'])

    lines = file.readlines()
    is_multiline = False

    for i, t in enumerate(lines):
        t = t.replace("\r", "")
        t = t.replace("\n", "")

        date_result = date_pattern.search(t)
        time_result = time_pattern.search(t)
        name_result = name_pattern.search(t)
        
        if is_multiline:
            message += str(t)
            if t!="" and t[-1] == "\"":
                message = message[:-1]
                is_multiline = False
                row = [date, time, name, message]
                table.append(row)
                
        if date_result:
            date = date_result.group()
        if time_result:
            time = time_result.group()
            if name_result:
                name = name_result.group()[1:-1:]
                message = t[name_result.span()[1]:]
            else:
                name = "event"
                message = t[time_result.span()[1]+1:]
            
            if message != "" and message[0] == "\"":
                is_multiline = True
                message = message[1:]
                
            if not is_multiline:
                row = [date, time, name, message]
                table.append(row)


    with open("line.csv", "w", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator='\n')
        for i in table:
            writer.writerow(i)

if __name__ == '__main__':
    line2csv(sys.argv[1])