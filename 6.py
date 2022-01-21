import requests

KEY = ""
database_id = ''

base_url = "https://api.notion.com/v1/databases/"
header = {"Authorization": KEY, "Notion-Version": "2021-08-16"}

query = {"filter": {"and": [
    {
        "property": "AutoDate",
        "checkbox": {
            "equals": "true"
        }
    },
    {
        "property": "Статус",
        "select": {
            "equals": "Просмотрено"
        }
    }
]
},
    "sorts": [
        {
            "property": "Created time (not for use)",
            "direction": "descending"
        }
    ]
}

response = requests.post(base_url + database_id + "/query", headers=header, data=query)

item = 0
anime_name_field = response.json()["results"][item]["properties"]["Название аниме"]["title"][0]["plain_text"]
anime_autodate_field = response.json()["results"][item]["properties"]["AutoDate"]["checkbox"]
anime_type_field = response.json()["results"][item]["properties"]["Тип"]["select"]["name"]
anime_status_field = response.json()["results"][item]["properties"]["Статус"]["select"]["name"]
anime_episode_field = response.json()["results"][item]["properties"]["Серия"]["rich_text"][0]["plain_text"]

try:
    start_date = str(response.json()["results"][item]["properties"]["Date"]["date"]["start"])
except TypeError:
    start_date = ""
try:
    end_date = str(response.json()["results"][item]["properties"]["Date"]["date"]["end"])
except TypeError:
    end_date = ""

anime_date_field = {"start": start_date, "end": end_date}

anime_created_time_field = response.json()["results"][item]["properties"]["Created time (not for use)"]["created_time"]
anime_edited_time_field = response.json()["results"][item]["properties"]["Edited time (not for use)"][
    "last_edited_time"]

current_anime = {"Название аниме": anime_name_field, "Тип": anime_type_field, "Статус": anime_status_field,
                 "Серия": anime_episode_field,
                 "Date": anime_date_field, "Autodate": anime_autodate_field, "Дата создания": anime_created_time_field,
                 "Дата изменения": anime_edited_time_field}
