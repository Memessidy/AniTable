import requests, json
from get_evernote_data import load_anime_table

token = ''
database_id = ''

anime_table, anime_columns = load_anime_table()

def get_dictionary_from_table(table):
    anime_dict = {}
    for i in table:
        anime_dict.clear()

        anime_dict["Название аниме"] = i[2]
        anime_dict['Номер аниме'] = i[0]
        anime_dict["Тип"] = i[1]
        anime_dict['Статус'] = i[3]
        anime_dict['Серия'] = i[4]
        anime_dict['X№'] = i[5]
        anime_dict['IDP'] = i[6]
        anime_dict['Дата выхода'] = i[7]
        anime_dict['Voice acting'] = i[8]
        anime_dict['Начало просмотра'] = i[9]
        anime_dict['Конец просмотра'] = i[10]
        anime_dict['Ресурс'] = i[11]

        yield anime_dict


def create_page(database_id, token, data):
    create_url = 'https://api.notion.com/v1/pages'

    headers = {
        'Authorization': 'Bearer ' + token,
        "Content-Type": "application/json",
        'Notion-Version': '2021-08-16'
    }

    date_of_review = int(data['Дата выхода']) if data['Дата выхода'] else None

    res_ource = data['Ресурс'] if data['Ресурс'] else None

    start_date = data['Начало просмотра']
    end_date = data['Конец просмотра']
    status = data['Статус']
    voice_acting = data['Voice acting']

    if status:
        status = "Просмотрено"
    else:
        status = 'Брошено'

    release_date = data['Дата выхода'] if data['Дата выхода'] else None

    new_page_data = {
        "parent": {"database_id": database_id},
        "properties": {
            "Название аниме": {
                "title": [
                    {
                        "text": {
                            "content": data['Название аниме']
                        }
                    }
                ]
            },
            "Статус": {
                "select": {
                    "name": status
                }

            },
            "Тип": {
                "select": {
                    "name": data['Тип']
                }
            },
            "Номер аниме": {
                "number": data['Номер аниме']
            },
            "Серия": {
                "rich_text": [
                    {
                        "text": {
                            "content": data["Серия"]
                        }
                    }
                ]
            },
            "X№": {
                "rich_text": [
                    {
                        "text": {
                            "content": data["X№"]
                        }
                    }
                ]
            },
            "IDP": {
                "rich_text": [
                    {
                        "text": {
                            "content": data["IDP"]
                        }
                    }
                ]
            },
            "Дата выхода": {
                "number": date_of_review
            },

            "Ресурс": {"url": res_ource}

        }
    }

    if all([start_date, end_date]):
        date_of_watching = {"Date": {"date": {"start": start_date, "end": end_date}}}
    elif start_date:
        date_of_watching = {"Date": {"date": {"start": start_date}}}
    else:
        date_of_watching = ''

    if voice_acting:
        va = {"Voice acting": {"select": {"name": voice_acting.upper()}}}
        new_page_data['properties'].update(va)

    if date_of_watching:
        new_page_data['properties'].update(date_of_watching)

    data = json.dumps(new_page_data)

    res = requests.request("POST", create_url, headers=headers, data=data)
    return res

# res_codes = []
#
# for index, item in enumerate(get_dictionary_from_table(anime_table)):
#     res = create_page(database_id, token, data=item)
#     print(index+1, res.status_code, res.text)
#     res_codes.append(res.status_code)
#     if res.status_code == "400":
#         break
#
# res_codes = [i==200 for i in res_codes]
# print(f"Все коды == 200: {all(res_codes)}")
