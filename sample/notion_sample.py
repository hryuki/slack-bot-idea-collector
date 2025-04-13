import requests
import os
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv('./env/.env')

NOTION_API_KEY = os.environ.get("NOTION_SECRET")
DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")

url = 'https://api.notion.com/v1/pages'

headers =  {
    'Notion-Version': '2022-06-28',
    'Authorization': 'Bearer ' + NOTION_API_KEY,
    'Content-Type': 'application/json',
}

json_data = {
    'parent': { 'database_id': DATABASE_ID },
    'properties': {
        '概要': {
            'title': [
                {
                    'text': {
                        'content': 'Pythonで追加'
                    }
                }
            ]
        },
        '作成者': {
            'rich_text': [
                {
                    'text': {
                        'content': '堀川'
                    }
                }
            ]
        },
        '作成日': {
            'date': {
                'start': '2023-10-01'
            }
        },
		'カテゴリ': {
            'multi_select': [
                {
                'name': 'Python'
                }
            ]
        },
        '内容': {
            'rich_text': [
                {
                    'text': {
                        'content': 'Pythonで追加'
                    }
                }
            ]
        },
    },
}

response = requests.post(url, headers=headers, json=json_data)
print(response)
print(response.status_code)
print(response.json())