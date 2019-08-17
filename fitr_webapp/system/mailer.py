from flask import current_app as app
import requests

def send_simple_message():
    with app.app_context():
        return requests.post(
            f"https://api.mailgun.net/v3/{app.config['MG_DOMAIN_NAME']}/messages",
            auth=("api", app.config["MG_API_KEY"]),
            data={"from": f"Fitr <fitr@{app.config['MG_DOMAIN_NAME']}>",
                  "to": ["bar@example.com"],
                  "subject": "Hello",
                  "text": "Testing some Mailgun awesomness!"})
