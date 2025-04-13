import requests
import os
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv('./env/.env')

NOTION_API_KEY = os.environ.get("NOTION_SECRET")
DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")

API_URL = 'https://api.notion.com/v1/pages'

headers =  {
    'Notion-Version': '2022-06-28',
    'Authorization': 'Bearer ' + NOTION_API_KEY,
    'Content-Type': 'application/json',
}

def add_idea_to_database(
    summary: str,
    creator: str,
    creation_date: str,
    categories: list[str],
    content: str,
):
    """
    Notionのデータベースにアイデアを追加する関数
    :param summary: アイデアの概要
    :param creator: アイデアの作成者
    :param creation_date: アイデアの作成日
    :param categories: アイデアのカテゴリリスト
    :param content: アイデアの内容
    :return: Notion APIのレスポンス
    """
    # データベースに追加するためのJSONデータを作成
    json_data = {
        'parent': { 'database_id': DATABASE_ID },
        'properties': {
            '概要': {
                'title': [
                    {
                        'text': {
                            'content': summary
                        }
                    }
                ]
            },
            '作成者': {
                'rich_text': [
                    {
                        'text': {
                            'content': creator
                        }
                    }
                ]
            },
            '作成日': {
                'date': {
                    'start': creation_date
                }
            },
            'カテゴリ': {
                'multi_select': [
                    {
                        'name': category
                    }
                    for category in categories
                ]
            },
            '内容': {
                'rich_text': [
                    {
                        'text': {
                            'content': content
                        }
                    }
                ]
            },
        },
    }
    # Notion APIにPOSTリクエストを送信
    response = requests.post(API_URL, headers=headers, json=json_data)
    # レスポンスを確認
    if response.status_code == 200:
        print("アイデアが正常に追加されました。")
    else:
        print(f"エラーが発生しました: {response.status_code}")
        print(response.json())
    return response
