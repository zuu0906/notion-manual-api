import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
NOTION_PAGE_ID = os.environ.get("NOTION_PAGE_ID")

# 動作確認用
@app.route("/")
def home():
    return {"status": "ok"}


@app.route("/add", methods=["POST"])
def add_to_notion():
    try:
        data = request.get_json()
        content = data.get("content")

        if not content:
            return jsonify({"error": "No content provided"}), 400

        url = f"https://api.notion.com/v1/blocks/{NOTION_PAGE_ID}/children"

        headers = {
            "Authorization": f"Bearer {NOTION_API_KEY}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

        payload = {
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": content
                                }
                            }
                        ]
                    }
                }
            ]
        }

        response = requests.patch(url, headers=headers, json=payload)

        return jsonify({
            "status": response.status_code,
            "notion_response": response.json()
        }), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Render対応（超重要）
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
