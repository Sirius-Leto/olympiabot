from pathlib import Path
import json
import datetime

if __name__ == '__main__':
    path_to_file = Path(r"C:\Users\dante\PycharmProjects\sirius-olympiad\src\static\parsed.json")
    with open(path_to_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for i in data["instances"]:
        begin = i.get("begin-date")
        end = i.get("end-date")

        if begin:
            r = eval(begin)
            r: datetime.date
            i["begin-date"] = r.strftime("%d-%m-%Y")

        if end:
            r = eval(end)
            r: datetime.date
            i["end-date"] = r.strftime("%d-%m-%Y")

    with open(path_to_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
