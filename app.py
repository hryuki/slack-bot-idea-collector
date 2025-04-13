import os
from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
from slack_sdk import WebClient
from dotenv import load_dotenv
from datetime import datetime
from openai_processor import OpenAIProcessor

from notion_connector import add_idea_to_database


# 環境変数を読み込む
load_dotenv('./env/.env')

TARGET_CHANNEL = os.environ.get("TARGET_CHANNEL")

app = App(
  #環境変数はlambdaから設定してください。
  token=os.environ.get("SLACK_BOT_TOKEN"),
  signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
  # これがない場合、app_mentionに反応はできるけどsayする前にLambdaが終了してしまい、ボットが返信完了できない
  process_before_response=True,
)

idea_processor = OpenAIProcessor(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


# メンションのイベントを受信したときに実行されるコード
@app.event("message")
def onAppDM(client: WebClient, event: dict):
    client.chat_postMessage(
        channel=event['channel'],
        thread_ts=event['ts'],
        blocks=[
            {
                "type": "section",
                "block_id": "message-block",
                "text": {
                    "type": "mrkdwn",
                    "text": "アイデアをデータベースに追加しますか？",
                }
            },
            {
                "type": "actions",
                "block_id": "button-block",
                # ボタンのアクションを指定
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "アイデアを追加する"},
                        "value": "clicked",
                        # この action_id を @app.action リスナーで指定します
                        "action_id": "add-idea-button",
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "キャンセル"},
                        "value": "clicked",
                        # この action_id を @app.action リスナーで指定します
                        "action_id": "cancel-button",
                    },
                ]
            }
        ],
        text="アイデアをデータベースに追加しますか？",
    )
    
@app.action("add-idea-button")
def handle_add_idea_button(ack: function, body: dict, client: WebClient):
    # ボタンのアクションを受け取ったときの処理
    ack()
    # ボタンを無効化する
    client.chat_update(
        channel=body['channel']['id'],
        ts=body['container']['message_ts'],
        text="アイデアを追加します。\nしばらくお待ちください。",
    )
    # スレッドの過去のメッセージを取得する
    thread_messages = client.conversations_replies(
        channel=body['channel']['id'],
        ts=body['container']['thread_ts'],
    )
    # スレッドの最初のメッセージを取得する
    idea_text: str = thread_messages['messages'][0]['text']
    _idea_text = idea_text.replace("\n", "")
    # アイデアの要約とカテゴリを取得する
    summary, categories = idea_processor.process_idea_text(idea_text)
    # メッセージを送信する
    client.chat_postMessage(
        channel=TARGET_CHANNEL,
        markdown_text=""\
            f"<@{body['user']['id']}>さんからアイデアが提案されました。\n\n"\
            f"- **概要**\n  - {summary}\n"\
            f"- **カテゴリ**\n  - {', '.join(categories)}\n\n"\
            f"- **内容**\n  - {_idea_text}"
    )
    # Notionにアイデアを追加する関数を呼び出す
    add_idea_to_database(
        summary=summary,
        creator=body['user']['username'],
        creation_date=datetime.now().strftime("%Y-%m-%d"),
        categories=categories,
        content=idea_text,
    )
    client.chat_update(
        channel=body['channel']['id'],
        ts=body['container']['message_ts'],
        text="アイデアを追加しました。",
    )

@app.action("cancel-button")
def handle_cancel_button(ack: function, body: dict, client: WebClient):
    # ボタンのアクションを受け取ったときの処理
    ack()
    # ボタンを無効化する
    client.chat_update(
        channel=body['channel']['id'],
        ts=body['container']['message_ts'],
        text="アイデア追加をキャンセルしました。",
    )

if __name__ == "__main__":
    # Lambdaのテスト用
    app.start(port=int(os.environ.get("PORT", 3000)))
