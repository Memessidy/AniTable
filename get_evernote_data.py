import csv

file = r""
with open(file=file, mode='r', encoding='utf-8') as f:
    lines = f.readlines()


def get_date(date):
    date = date.strip("(").strip(")").strip()
    date = date.split("-")
    date = [i.strip() for i in date if i]

    try:
        start_date = date[0]
    except IndexError:
        start_date = ""
    try:
        end_date = date[1]
    except IndexError:
        end_date = ""
    start_date = start_date.split('.')
    end_date = end_date.split(".")
    if all([all([i.isdigit() for i in start_date]), all([i.isdigit() for i in end_date])]):
        start_date.reverse()
        end_date.reverse()
        return [f'20{"-".join(start_date)}', f'20{"-".join(end_date)}']
    elif all([i.isdigit() for i in start_date]):
        start_date.reverse()
        return f'20{"-".join(start_date)}'


def get_data_evernote_ver_2(data_list, name_column):
    current_column = ""
    type = ""
    result = {}
    result["Тип"] = []

    for item in data_list:

        if all([bool(item.strip()), "[" not in item, not (item.strip().strip(".").isdigit())]):
            if item.strip() == "#full-length":
                type = "Полнометражное"
                continue
            elif item.strip() == "#serial":
                type = "Многосерийное"
                continue
            elif item.strip() == "#ova":
                type = "Ova / Special"
                continue

            item = item.strip()
            current_column = item

            res = result.get(current_column)
            if res is None:
                result[current_column] = []

            if current_column == name_column:
                if type == "Полнометражное":
                    res = result.get("Серия")
                    if res is None:
                        result["Серия"] = []

                res = result.get("Status")
                if res is None:
                    result["Status"] = []

        elif all(["[" not in item, item.strip().strip(".").isdigit()]):
            pass

        elif "[" in item and not(item.strip().strip(".").isdigit()):

            if current_column == name_column:
                if "[x]" in item:
                    result["Status"].append(True)
                    result[current_column].append(item[3:].strip())
                else:
                    result["Status"].append(False)
                    result[current_column].append(item[2:].strip())
                if type == "Полнометражное":
                    result['Серия'].append("1/1")
                    result["Тип"].append(type)
                else:
                    result["Тип"].append(type)
            else:
                result[current_column].append(item[2:].strip())

    return result


def validate_data_evernote(data: dict):
    counts = {}
    list_data = []
    name_columns = []

    for k, v in data.items():
        name_columns.append(k)
        counts[k] = len(v)

    max_val = max(counts.values())

    for k, v in data.items():
        if len(v) < max_val:
            for _ in range(max_val - len(v)):
                data[k].append("...")

    for ind in range(max_val):
        list_data.append([])
        for key in data.keys():
            value = data[key][ind]

            if key == 'Дата просмотра':
                start_date = ""
                end_date = ""
                value = get_date(value)
                if type(value) is str:
                    start_date = value
                    end_date = ""
                elif type(value) is list:
                    start_date = value[0]
                    end_date = value[1]

                list_data[ind].append(start_date)
                list_data[ind].append(end_date)
                continue
            elif key in ("Дата выхода", "Серия", "Voice acting", "Ресурс"):
                value = value.strip("(").strip(")").strip()
                value = "" if value == "..." else value
                if key == "Voice acting":
                    value = "" if value.strip() == "[]" else value
            else:
                value = "" if value in ("...", "..") else value
            list_data[ind].append(value)

    return list_data, name_columns


def some_prepare(data:list):
    x0 = data[1].copy()
    x1 = data[5].copy()

    data[1][8] = ""
    data[1][9] = ""

    data[5][8] = ""
    data[5][9] = ""

    data.append(x0)
    data.append(x1)

    data.sort(key=lambda x:x[8])

    for i, v in enumerate(data):
        v.insert(0, i+1)

    return data


def load_anime_table():
    res = get_data_evernote_ver_2(data_list=lines, name_column="Название аниме")
    res, columns = validate_data_evernote(data=res)
    res = some_prepare(res)
    return res, columns


if __name__ == '__main__':
    for i in load_anime_table()[0]:
        print(i)