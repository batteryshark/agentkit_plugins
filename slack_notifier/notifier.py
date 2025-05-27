import requests
import os
import logging


def send_slack_notification(message, title=""):
    """
    Send a notification to Slack via webhook.
    
    Args:
        message (str): The main message content
        title (str, optional): Title for the message. Defaults to "".
        bot_name (str, optional): Custom bot name. Defaults to environment variable or "MCP Helper".
    
    Returns:
        bool: True if message was sent successfully, False otherwise
    """
    if os.getenv("SLACK_NOTIFIER_ENABLED", "true").lower() == "false":
        logging.info("Slack notifications are disabled")
        return False
    
    webhook_url = os.getenv("SLACK_NOTIFIER_WEBHOOK_URL")
    if not webhook_url:
        logging.error("SLACK_NOTIFIER_WEBHOOK_URL environment variable is not set")
        return False
    

    data = {"blocks": []}
    if title:
        data["blocks"].append({
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": title
            }
        })

    data["blocks"].append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": message
        }
    })

    
    try:
        response = requests.post(webhook_url, json=data)
        
        if response.status_code == 200 and response.text == "ok":
            logging.info('Message sent to Slack webhook')
            return True
        else:
            logging.error(f'Failed to send message to Slack webhook. Status: {response.status_code}, Response: {response.text}')
            return False
            
    except requests.exceptions.RequestException as e:
        logging.error(f'Error sending message to Slack webhook: {e}')
        return False


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    send_slack_notification("Hello, world!", title="Test Message") 