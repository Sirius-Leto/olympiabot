import datetime
import json
from pathlib import Path

if __name__ == '__main__':
    path_to_file = Path(r"C:\Users\dante\PycharmProjects\sirius-olympiad\src\static\parsed.json")
    with open(path_to_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for i in data["instances"]:
        begin = i.get("begin-date")
        end = i.get("end-date")

        if begin:
            # "01-01-1970",
            dt = datetime.datetime.strptime(begin, "%d-%m-%Y")
            if dt.year < 2000:
                i["begin-date"] = None

        if end:
            dt = datetime.datetime.strptime(end, "%d-%m-%Y")
            if dt.year < 2000:
                i["end-date"] = None

    with open(path_to_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
