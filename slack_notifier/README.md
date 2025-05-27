# Slack Notifier Plugin

A simple and efficient Slack webhook notification plugin for AgentKit that allows you to send notifications to Slack channels via incoming webhooks.

## Features

- 🚀 Easy Slack webhook integration
- 📝 Simple text formatting with markdown support
- 🔧 Environment-based configuration
- 📝 Comprehensive logging
- ⚡ Lightweight with minimal dependencies

## Installation

### Dependencies

This plugin requires the following Python packages:
- `requests` (for HTTP requests to Slack webhooks)
- `python-dotenv` (for loading environment variables, optional for development)

Install dependencies:
```bash
pip install requests python-dotenv
```

## Configuration

The plugin uses environment variables for configuration. You can set these in your environment or use a `.env` file.

### Required Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SLACK_NOTIFIER_WEBHOOK_URL` | Your Slack webhook URL | ✅ Yes |

### Optional Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SLACK_NOTIFIER_ENABLED` | Enable/disable notifications | `true` | ❌ No |
| `SLACK_NOTIFIER_BOT_NAME` | Bot name displayed in Slack | `MCP Helper` | ❌ No |

### Setting up Slack Webhook

1. Go to your Slack workspace
2. Navigate to Apps → Manage → Custom Integrations → Incoming Webhooks
3. Click "Add to Slack"
4. Choose the channel where you want to post messages
5. Configure the webhook (name, icon, etc.)
6. Copy the webhook URL
7. Set the `SLACK_NOTIFIER_WEBHOOK_URL` environment variable

Alternatively, you can create a Slack app with incoming webhooks:
1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Create a new app
3. Go to "Incoming Webhooks" and activate them
4. Add a new webhook to workspace
5. Copy the webhook URL

## Usage

### Basic Usage

```python
from slack_notifier import send_slack_notification

# Simple message
send_slack_notification("Hello, Slack!")

# Message with title
send_slack_notification("Deployment completed successfully!", title="🚀 Deployment Status")
send_slack_notification("System alert!", title="⚠️ Alert")
```

### Function Signature

```python
def send_slack_notification(message, title=""):
    """
    Send a notification to Slack via webhook.
    
    Args:
        message (str): The main message content
        title (str, optional): Title for the message. Defaults to "".
    
    Returns:
        bool: True if message was sent successfully, False otherwise
    """
```

### Environment Configuration Example

Create a `.env` file in your project root:

```env
SLACK_NOTIFIER_WEBHOOK_URL=https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX
SLACK_NOTIFIER_ENABLED=true
```

### Disabling Notifications

To temporarily disable notifications without removing the webhook URL:

```env
SLACK_NOTIFIER_ENABLED=false
```

## Message Formatting

The plugin supports basic Slack markdown formatting:

- **Bold text**: `*bold*` or `_bold_`
- *Italic text*: `_italic_`
- `Code`: `` `code` ``
- Links: `<https://example.com|Link Text>`
- Mentions: `<@username>` or `<@U1234567890>`
- Channels: `<#channel-name>` or `<#C1234567890>`

### Example with Formatting

```python
send_slack_notification(
    "Deployment to *production* completed successfully!\n"
    "• Duration: `2m 34s`\n"
    "• Status: ✅ Success\n"
    "• URL: <https://myapp.com|View App>",
    title="🚀 Production Deployment"
)
```

## Testing

You can test the plugin directly by running the module:

```bash
cd slack_notifier
python notifier.py
```

This will send a test message "Hello, world!" with the title "Test Message" to your configured Slack webhook.

## Error Handling

The plugin includes comprehensive error handling:

- **Missing webhook URL**: Function returns `False` and logs an error
- **Network errors**: Function returns `False` and logs the error
- **Slack API errors**: Function returns `False` and logs the HTTP status code
- **Disabled notifications**: Function returns `False` and logs an info message

## Logging

The plugin uses Python's built-in logging module. Configure your application's logging to see Slack notifier messages:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Examples

### Integration with Error Handling

```python
import logging
from slack_notifier import send_slack_notification

def process_data():
    try:
        # Your processing logic here
        result = perform_complex_operation()
        send_slack_notification(
            f"Data processing completed. Processed *{result['count']}* items.",
            title="✅ Processing Complete"
        )
    except Exception as e:
        logging.error(f"Processing failed: {e}")
        send_slack_notification(
            f"Data processing failed: `{str(e)}`",
            title="❌ Processing Error",
            bot_name="Error Reporter"
        )
```

### Monitoring Script

```python
import time
from slack_notifier import send_slack_notification

def monitor_system():
    send_slack_notification("System monitoring started", title="🔍 Monitor Status")
    
    while True:
        # Your monitoring logic
        if system_health_check():
            send_slack_notification("System is healthy", title="💚 Health Check")
        else:
            send_slack_notification("System issues detected!", title="🚨 Alert")
        
        time.sleep(300)  # Check every 5 minutes
```

### Advanced Formatting Example

```python
def send_deployment_notification(app_name, version, status, duration):
    status_emoji = "✅" if status == "success" else "❌"
    
    message = f"""
*Application:* {app_name}
*Version:* `{version}`
*Duration:* {duration}
*Status:* {status_emoji} {status.title()}
    """.strip()
    
    send_slack_notification(
        message,
        title=f"🚀 Deployment {status.title()}",
        bot_name="Deployment Bot"
    )
```

## Troubleshooting

### Common Issues

1. **Webhook URL not working**: Ensure the URL is correct and the webhook hasn't been deleted
2. **Messages not appearing**: Check that the webhook has permission to post in the target channel
3. **Import errors**: Ensure `requests` is installed (`pip install requests`)
4. **Formatting issues**: Check that your markdown syntax is correct for Slack

### Debug Mode

Enable debug logging to see detailed information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Webhook URL Format

Slack webhook URLs should look like:
```
https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX
```

If your URL doesn't match this pattern, double-check your webhook configuration.

## Slack API Reference

This plugin uses Slack's Incoming Webhooks feature. For more advanced functionality, refer to:
- [Slack Incoming Webhooks Documentation](https://api.slack.com/messaging/webhooks)
- [Slack Message Formatting](https://api.slack.com/reference/surfaces/formatting)
- [Slack Block Kit](https://api.slack.com/block-kit) (for more complex message layouts)

## License

This plugin is part of the AgentKit plugins collection. See the main repository for license information.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 