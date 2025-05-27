import requests
import os
import logging


def send_discord_notification(message,title="",bot_name=os.getenv("DISCORD_NOTIFIER_BOT_NAME", "General Helper")):
    if os.getenv("DISCORD_NOTIFIER_ENABLED", "true").lower() == "false":
        logging.info("Discord notifications are disabled")
        return False
    
    embed = {
    "title": title,
    "description": message,
    "color": 10181046
    }

    data = {
    "username": bot_name,
    "embeds": [embed]
    }

    response = requests.post(os.getenv("DISCORD_NOTIFIER_WEBHOOK_URL"), json=data)

    if response.status_code != 204:
        logging.error('Could not send message to Discord webhook')
        return False
    logging.info('Message sent to Discord webhook')
    return True

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    send_discord_notification("Hello, world!")