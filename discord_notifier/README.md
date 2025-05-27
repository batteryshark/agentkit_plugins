# Discord Notifier Plugin

A simple and efficient Discord webhook notification plugin for AgentKit that allows you to send notifications to Discord channels via webhooks.

## Features

- 🚀 Easy Discord webhook integration
- 🎨 Rich embed support with customizable titles and colors
- 🤖 Configurable bot name
- 🔧 Environment-based configuration
- 📝 Comprehensive logging
- ⚡ Lightweight with minimal dependencies

## Installation

### Dependencies

This plugin requires the following Python packages:
- `requests` (for HTTP requests to Discord webhooks)
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
| `DISCORD_NOTIFIER_WEBHOOK_URL` | Your Discord webhook URL | ✅ Yes |

### Optional Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DISCORD_NOTIFIER_ENABLED` | Enable/disable notifications | `true` | ❌ No |
| `DISCORD_NOTIFIER_BOT_NAME` | Bot name displayed in Discord | `General Helper` | ❌ No |

### Setting up Discord Webhook

1. Go to your Discord server
2. Navigate to Server Settings → Integrations → Webhooks
3. Click "New Webhook"
4. Configure the webhook (name, channel, avatar)
5. Copy the webhook URL
6. Set the `DISCORD_NOTIFIER_WEBHOOK_URL` environment variable

## Usage

### Basic Usage

```python
from discord_notifier import send_discord_notification

# Simple message
send_discord_notification("Hello, Discord!")

# Message with title
send_discord_notification("Deployment completed successfully!", title="🚀 Deployment Status")

# Custom bot name
send_discord_notification("System alert!", title="⚠️ Alert", bot_name="System Monitor")
```

### Function Signature

```python
def send_discord_notification(message, title="", bot_name=None):
    """
    Send a notification to Discord via webhook.
    
    Args:
        message (str): The main message content
        title (str, optional): Title for the embed. Defaults to "".
        bot_name (str, optional): Custom bot name. Defaults to environment variable or "General Helper".
    
    Returns:
        bool: True if message was sent successfully, False otherwise
    """
```

### Environment Configuration Example

Create a `.env` file in your project root:

```env
DISCORD_NOTIFIER_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN
DISCORD_NOTIFIER_ENABLED=true
DISCORD_NOTIFIER_BOT_NAME=My Custom Bot
```

### Disabling Notifications

To temporarily disable notifications without removing the webhook URL:

```env
DISCORD_NOTIFIER_ENABLED=false
```

## Testing

You can test the plugin directly by running the module:

```bash
cd discord_notifier
python notifier.py
```

This will send a test message "Hello, world!" to your configured Discord webhook.

## Error Handling

The plugin includes comprehensive error handling:

- **Missing webhook URL**: Function returns `False` and logs an error
- **Network errors**: Function returns `False` and logs the error
- **Discord API errors**: Function returns `False` and logs the HTTP status code
- **Disabled notifications**: Function returns `False` and logs an info message

## Logging

The plugin uses Python's built-in logging module. Configure your application's logging to see Discord notifier messages:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Examples

### Integration with Error Handling

```python
import logging
from discord_notifier import send_discord_notification

def process_data():
    try:
        # Your processing logic here
        result = perform_complex_operation()
        send_discord_notification(
            f"Data processing completed. Processed {result['count']} items.",
            title="✅ Processing Complete"
        )
    except Exception as e:
        logging.error(f"Processing failed: {e}")
        send_discord_notification(
            f"Data processing failed: {str(e)}",
            title="❌ Processing Error",
            bot_name="Error Reporter"
        )
```

### Monitoring Script

```python
import time
from discord_notifier import send_discord_notification

def monitor_system():
    send_discord_notification("System monitoring started", title="🔍 Monitor Status")
    
    while True:
        # Your monitoring logic
        if system_health_check():
            send_discord_notification("System is healthy", title="💚 Health Check")
        else:
            send_discord_notification("System issues detected!", title="🚨 Alert")
        
        time.sleep(300)  # Check every 5 minutes
```

## Troubleshooting

### Common Issues

1. **Webhook URL not working**: Ensure the URL is correct and the webhook hasn't been deleted
2. **Messages not appearing**: Check that the webhook has permission to post in the target channel
3. **Import errors**: Ensure `requests` is installed (`pip install requests`)

### Debug Mode

Enable debug logging to see detailed information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## License

This plugin is part of the AgentKit plugins collection. See the main repository for license information.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests to improve this plugin.

## Changelog

### v1.0.0
- Initial release
- Basic Discord webhook functionality
- Environment-based configuration
- Rich embed support
- Comprehensive error handling and logging 