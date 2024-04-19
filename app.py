# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
import json
import requests

app = Flask(__name__)

@app.route('/webhooks/pull-requests/create', methods=['POST'])
def handle_pull_requests_create():
    data = request.json
    print("Received data:", data)

    # Extract Bitbucket payload info
    pr_author = data['actor']['display_name']
    pr_title = data['pullrequest']['title']
    pr_description = data['pullrequest']['description']
    pr_link = data['pullrequest']['links']['html']['href']

    # Branch info
    source_branch = data['pullrequest']['source']['branch']['name']
    destination_branch = data['pullrequest']['destination']['branch']['name']

    # Microsoft Teams card message
    teams_message = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "summary": "New Pull Request",
        "themeColor": "0078D7",
        "title": f"{pr_title}",
        "sections": [{
            "text": f"🔀 {source_branch} → {destination_branch}",
            "facts": [
            {
                "name": "🦹 Author",
                "value": f"{pr_author}"
            },
            {
                "name": "📦 Repository",
                "value": f"{data['repository']['name']}"
            },
	    {
		"name": "📝 Description",
	      	"value": f"{pr_description if pr_description else '💃🏻'}"
	    },
	    {
                "name": "🔗",
                "value": f"[See Pull Request]({pr_link})"
            }],
        }]
    }

    # Microsoft Teams' webhook URL
    teams_webhook_url = 'your-ms-teams-webhook-url'

    # Send message to Microsoft Teams
    response = requests.post(teams_webhook_url, json=teams_message)
    return jsonify({'status': 'sent to Microsoft Teams', 'response': response.text}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
