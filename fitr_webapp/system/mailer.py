from flask import current_app as app
from requests import post

def send_short_message(address, subject, message):
    with app.app_context():
        return post(
            f"https://api.mailgun.net/v3/{app.config['MG_DOMAIN_NAME_API']}/messages",
            auth=("api", app.config["MG_API_KEY"]),
            data={
                "from": f"Fitr <fitr@{app.config['MG_DOMAIN_NAME']}>",
                "to": [address],
                "subject": subject,
                "text": message
            })
