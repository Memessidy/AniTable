import requests, json
token = ''

database_id = ''


def parse_notion_data(data):
    page_id = data["id"]
    data = data["properties"]
    try:
        anime_name_field = data["Название аниме"]["title"][0]["plain_text"]
    except:
        anime_name_field = ""
    try:
        anime_autodate_field = data["AutoDate"]["checkbox"]
    except:
        anime_autodate_field = ""
    try:
        anime_type_field = data["Тип"]["select"]["name"]
    except:
        anime_type_field = ""
    try:
        anime_status_field = data["Статус"]["select"]["name"]
    except:
        anime_status_field = ""
    try:
        anime_episode_field = data["Серия"]["rich_text"][0]["plain_text"]
    except:
        anime_episode_field = ""
    try:
        start_date = str(data["Date"]["date"]["start"])
    except:
        start_date = ""
    try:
        end_date = str(data["Date"]["date"]["end"])
    except:
        end_date = ""

    try:
        anime_number = data["№"]["number"]
    except:
        anime_number = ""

    anime_date_field = {"start": start_date, "end": end_date}

    anime_created_time_field = data["Created time (not for use)"]["created_time"]
    anime_edited_time_field = data["Edited time (not for use)"]["last_edited_time"]
    current_anime = {"page_id": page_id, "Номер аниме":anime_number, "Название аниме": anime_name_field, "Тип": anime_type_field,
                     "Статус": anime_status_field, "Серия": anime_episode_field,
                     "Date": anime_date_field, "Autodate": anime_autodate_field,
                     "Дата создания": anime_created_time_field, "Дата изменения": anime_edited_time_field}

    return current_anime


def get_data_from_notion(database_id, token):
    headers = {"Authorization": "Bearer " + token, "Notion-Version": "2021-08-16"}
    anime_list = []
    query = {}
    base_url = "https://api.notion.com/v1/databases/"
    response = requests.post(base_url + database_id + "/query", headers=headers, data=query)
    for value in response.json()['results']:
        anime_list.append(parse_notion_data(value))

    return anime_list


def create_page(database_id, token, data):
    create_url = 'https://api.notion.com/v1/pages'

    headers = {
        'Authorization': 'Bearer ' + token,
        "Content-Type": "application/json",
        'Notion-Version': '2021-08-16'
    }

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
                    "name": data['Статус']
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
                "number": data['Дата выхода']
            },
            "Voice acting": {
                "rich_text": [
                    {
                        "text": {
                            "content": data["Voice acting"]
                        }
                    }
                ]
            },
            "Date": {"date": {"start": data['start_date']}},

            "Ресурс": {"url": data["Ресурс"]}

        }
    }

    data = json.dumps(new_page_data)

    res = requests.request("POST", create_url, headers=headers, data=data)
    print(res.status_code)
    print(res.text)



def parse_date_from_autocreation(date_and_time):
    year, month, oth = date_and_time.split("-")
    day = oth.split("T")[0]
    time = oth.split("T")[1][:-5]
    hours = time.split(":")[0]
    minutes = time.split(":")[1]

    date_and_time = {"year": year, "month": month, "day": day, "hours": hours, "minutes": minutes}
    string_date = f"{date_and_time['year']}-{date_and_time['month']}-{date_and_time['day']}"
    return string_date


def update_page(pageId, token, checkbox_status=False, start_date="", end_date=""):
    updateUrl = f"https://api.notion.com/v1/pages/{pageId}"

    headers = {
        'Authorization': 'Bearer ' + token,
        "Content-Type": "application/json",
        'Notion-Version': '2021-08-16'
    }

    if all([start_date, end_date]):
        date = {"start": start_date, "end": end_date}
    elif start_date and not end_date:
        date = {"start": start_date}

    updateData = {
        "properties":
            {
                "AutoDate":{
                        "checkbox": checkbox_status
                },
                "Date":{
                    "date":date

                    }
                }

            }
    data = json.dumps(updateData)

    response = requests.request("PATCH", updateUrl, headers=headers, data=data)

    # print(response.text)
    return response.status_code



def main():
    result = get_data_from_notion(database_id=database_id, token=token)
    for anime in result:
        number = anime['Номер аниме']
        anime_name = anime['Название аниме']
        page_id = anime['page_id']
        autodate = anime['Autodate']
        status = anime['Статус']

        if autodate and status == 'Просмотрено':

            creation_date = parse_date_from_autocreation(anime['Дата создания'])
            change_date = parse_date_from_autocreation(anime['Дата изменения'])

            if creation_date == change_date:

                status_code = update_page(pageId=page_id, token=token, checkbox_status=False, start_date=creation_date)

            else:
                status_code = update_page(pageId=page_id, token=token, checkbox_status=False, start_date=creation_date,
                            end_date=change_date)

            print(status_code)
            if status_code == 200:
                print(f"У аниме № {number} : [{anime_name}] выключена AutoDate")


if __name__ == '__main__':
    main()
