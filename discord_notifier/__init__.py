# =============================================================================
# START OF MODULE METADATA
# =============================================================================
_module_info = {
    "name": "Discord Notifier",
    "description": "Discord Webhook notification functionality",
    "author": "BatteryShark",
    "version": "1.0.0",
    "platform": "any",
    "python_requires": ">=3.10",
    "dependencies": ["requests"],
    "environment_variables": {
        "DISCORD_NOTIFIER_WEBHOOK_URL": {
            "description": "Discord Webhook URL",
            "default": "",
            "required": True
        },
        "DISCORD_NOTIFIER_ENABLED": {
            "description": "Enable/disable notifications",
            "default": "true",
            "required": False
        },
        "DISCORD_NOTIFIER_BOT_NAME": {
            "description": "Bot name",
            "default": "MCP Helper",
            "required": False
        }
    }
}
# =============================================================================
# END OF MODULE METADATA
# =============================================================================
# =============================================================================
# START OF EXPORTS
# =============================================================================
from .notifier import send_discord_notification
_module_exports = {
    "tools": [send_discord_notification]
}
# =============================================================================
# END OF EXPORTS
# =============================================================================
