# Slackアイデア出しbot（Notion連携）
## 概要
- アイデアを送信することでOpanAIのAPIを通じてアイデアの要約および分類を行いNotionのデータベースに整理してくれるSlackのbotです。

## 動作例
https://github.com/hryuki/slack-bot-idea-collector/blob/main/movie/example.mp4

## 導入方法
### 1. SlackのAppを作成する.
---
- [公式ドキュメント](https://tools.slack.dev/bolt-python/ja-jp/getting-started/)をもとにSlackのAppを設定してください。
- この時"From a manifest"を選択し、[manifest.yaml](manifest.yaml)をもとにアプリを構築してください。

> ※[manifest.yaml](manifest.yaml)のrequest_urlには適宜自分で用意したURLを設定してください。ローカルで試す場合は[ngrok](https://ngrok.com/)などのローカルホスティングサービスがおすすめです。
> 
> ※urlの設定がうまくいかなかった場合は最後の手順まで実行してからurlの設定を行ってください。

- [.env.sample](env/.env.sample)を参考に`.env`ファイルを作成してください。
- SlackAppの管理画面のBasic InformationからSigning Secretを、OAuth & PermissionsからBot User OAuth Tokenを取得し、それぞれ`.env`ファイルの`SLACK_SIGNING_SECRET`および`SLACK_BOT_TOKEN`に値を挿入してください。

### 2. NotionのAPIを設定する.
---
- Notion APIのインテグレーションキーおよびアイデアのデータを格納したいデータベースIDを取得してください。
[参考ページはこちらです。](https://qiita.com/ulxsth/items/3434471ac91f8fa311cf)
- `.env`ファイルの`NOTION_SECRET`および`NOTION_DATABASE_ID`にそれぞれ値を挿入してください。

### 3. その他の環境変数を用意する
---
- OpenAIのAPIキーを`.env`ファイルの`OPENAI_API_KEY`に挿入してください。
- アイデアの周知を行いたいSlackチャンネルのIDを`.env`ファイルの`TARGET_CHANNEL`に挿入してください。（[SlackチャンネルのID取得方法](https://qiita.com/YumaInaura/items/0c4f4adb33eb21032c08)）

### 4. 環境構築
---
- 仮想環境を構築する
```
python -m venv venv
```
- 仮想環境をアクティベートする
```
source venv/bin/activate
```
- 必要なライブラリをインストールする
```
pip install -r requirements.txt
```
### 5. 実行
---
```
python app.py
```
- デフォルトではlocalhostの3000番に実行されます。それをもとに[ngrok](https://ngrok.com/)などのローカルホスティングサービスでpublicにurlを公開してください。
