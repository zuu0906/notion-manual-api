from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
PAGE_ID = os.environ.get("PAGE_ID")

@app.route("/")
def home():
    return {"status": "ok"}

@app.route("/add", methods=["POST"])
def add_text():
    data = request.json
    content = data.get("content")

    url = f"https://api.notion.com/v1/blocks/{PAGE_ID}/children"

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

    return jsonify(response.json())
