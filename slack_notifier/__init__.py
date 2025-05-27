# =============================================================================
# START OF MODULE METADATA
# =============================================================================
_module_info = {
    "name": "Slack Notifier",
    "description": "Slack Webhook notification functionality",
    "author": "BatteryShark",
    "version": "1.0.0",
    "platform": "any",
    "python_requires": ">=3.10",
    "dependencies": ["requests"],
    "environment_variables": {
        "SLACK_NOTIFIER_WEBHOOK_URL": {
            "description": "Slack Webhook URL",
            "default": "",
            "required": True
        },
        "SLACK_NOTIFIER_ENABLED": {
            "description": "Enable/disable notifications",
            "default": "true",
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
from .notifier import send_slack_notification
_module_exports = {
    "tools": [send_slack_notification]
}
# =============================================================================
# END OF EXPORTS
# ============================================================================= 