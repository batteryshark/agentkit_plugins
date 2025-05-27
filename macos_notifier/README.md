# MacOS Notifier Plugin

MacOS user notification functionality for sending system notifications to users.

## Overview

The MacOS Notifier Plugin provides a simple interface for sending native MacOS notifications to users. It integrates with the macOS Notification Center to display popup notifications with customizable titles, messages, and sounds.

## Features

- **Native MacOS Notifications**: Uses the system's built-in notification center
- **Customizable Sounds**: Configure notification sounds or use system defaults
- **Optional Titles**: Support for both titled and simple message notifications
- **Enable/Disable Toggle**: Environment variable to turn notifications on/off
- **Error Handling**: Graceful failure handling with logging

## Platform Requirements

- **Platform**: macOS (darwin) only
- **Python**: 3.10 or higher
- **Permissions**: May require notification permissions in System Preferences

## Tool Calls

### `send_notification`
Send a MacOS notification popup to the user.

**Parameters:**
- `message` (string): The notification message to display
- `title` (string, optional): Optional notification title

**Returns:** Boolean indicating success/failure

**Example:**
```python
# Simple notification
success = await send_notification("Task completed successfully!")

# Notification with title
success = await send_notification(
    message="Your file has been processed", 
    title="Processing Complete"
)

# Check if notification was sent
if success:
    print("Notification sent successfully")
else:
    print("Failed to send notification")
```

## Configuration

The plugin uses environment variables for configuration:

### Optional Settings
- `MACOS_NOTIFIER_DEFAULT_SOUND`: Default notification sound (default: "Ping")
- `MACOS_NOTIFIER_ENABLED`: Enable/disable notifications (default: "true")

### Available Sounds
Common macOS notification sounds include:
- `Ping` (default)
- `Pop`
- `Blow`
- `Bottle`
- `Frog`
- `Funk`
- `Glass`
- `Hero`
- `Morse`
- `Purr`
- `Sosumi`
- `Submarine`
- `Tink`

## Setup

### 1. Install Dependencies
```bash
pip install pync>=2.0.0 pydantic>=2.0.0
```

### 2. Configure Environment (Optional)
```bash
export MACOS_NOTIFIER_DEFAULT_SOUND="Pop"
export MACOS_NOTIFIER_ENABLED="true"
```

### 3. Grant Permissions
On first use, macOS may prompt for notification permissions. Grant access in:
- System Preferences → Security & Privacy → Privacy → Notifications

## Error Handling

The plugin handles various error scenarios gracefully:

- **Disabled Notifications**: Returns `False` when `MACOS_NOTIFIER_ENABLED` is set to "false"
- **Permission Denied**: Catches and logs permission-related errors
- **System Errors**: Handles underlying pync library exceptions
- **Invalid Sounds**: Falls back to system default if custom sound fails

## Use Cases

### Development & Debugging
```python
# Notify when long-running process completes
await send_notification("Build completed!", "Development")

# Alert on errors
await send_notification("Error in module X", "Debug Alert")
```

### User Workflows
```python
# File processing completion
await send_notification("Your document is ready", "Export Complete")

# Reminder notifications
await send_notification("Meeting in 5 minutes", "Calendar Reminder")
```

### System Monitoring
```python
# System status updates
await send_notification("Backup completed successfully", "System Status")

# Resource alerts
await send_notification("Disk space low", "System Warning")
```

## Integration Examples

### With Other Plugins
```python
# Combine with file operations
file_saved = await save_file("document.txt", content)
if file_saved:
    await send_notification("File saved successfully", "File Manager")

# Combine with web requests
response = await fetch_data("https://api.example.com")
await send_notification(f"Received {len(response)} items", "API Update")
```

### Conditional Notifications
```python
# Only notify on important events
if error_level == "critical":
    await send_notification("Critical error occurred!", "System Alert")

# Batch operation completion
processed_count = await process_files(file_list)
await send_notification(f"Processed {processed_count} files", "Batch Complete")
```

## Troubleshooting

### Common Issues

1. **No Notifications Appearing**
   - Check notification permissions in System Preferences
   - Verify `MACOS_NOTIFIER_ENABLED` is not set to "false"
   - Ensure Do Not Disturb is not enabled

2. **Silent Notifications**
   - Check system volume settings
   - Verify notification sound settings in System Preferences
   - Try different sound names

3. **Permission Errors**
   - Grant notification access in System Preferences
   - Restart the application after granting permissions

### Debug Mode
```python
# Test notification functionality
import os
os.environ["MACOS_NOTIFIER_ENABLED"] = "true"
result = await send_notification("Test message", "Debug")
print(f"Notification result: {result}")
```

## Dependencies

- `pync>=2.0.0`: Python interface to macOS notification center
- `pydantic>=2.0.0`: Data validation and serialization

## Limitations

- **macOS Only**: This plugin only works on macOS systems
- **User Presence**: Notifications require an active user session
- **System Permissions**: Requires notification permissions to be granted
- **Rate Limiting**: macOS may rate-limit excessive notifications

## Integration

The MacOS Notifier Plugin integrates seamlessly with agentkit's tool system and can be used alongside other plugins to provide user feedback for various operations and workflows. 