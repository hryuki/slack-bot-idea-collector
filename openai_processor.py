from openai import OpenAI
import json

class OpenAIProcessor:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)

    def process_idea_text(self, idea_text: str) -> tuple[str, list[str]]:
        """
        アイデアのテキストを要約し、カテゴリに分類するメソッド
        :param idea_text: アイデアのテキスト
        :return: 要約とカテゴリのリスト
        """
        # OpenAI APIを使用してアイデアの要約とカテゴリ分類を行う
        response = self.client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[{
                "role": "user",
                "content": self.create_input_text(idea_text)
            }],
            response_format={ "type": "json_object" }
        )
        response_text = response.choices[0].message.content
        response_json = json.loads(response_text)
        summary = response_json["summary"]
        categories = response_json["category"]
        return summary, categories

    def create_input_text(self, idea_text: str) -> str:
        return ""\
            "以下のアイデアを要約したうえでアイデアをカテゴリに分類してください。\n"\
            "応答は以下のjson形式に従ってください。"\
            '{"summary": "アイデアの要約(string)", "category": "アイデアをカテゴリ分けしたリスト形式の回答。カテゴリ例:webアプリ,ブロックチェーン,食育など(list[string])"}\n\n'\
            f"### アイデア\n{idea_text}"