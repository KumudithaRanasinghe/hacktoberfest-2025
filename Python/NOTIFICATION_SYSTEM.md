# 🔔 Notification System Documentation

## Overview

The Hacktoberfest 2025 Project Tracker includes a comprehensive notification system that provides real-time alerts, milestone achievements, and system messages to keep contributors engaged and informed.

## Features

### ✨ Core Features

- **Real-time Notifications**: Live updates without page refresh
- **Multiple Notification Types**: Success, info, warning, error, milestone, welcome, achievement, and system notifications
- **Priority Levels**: Urgent, high, normal, and low priority notifications
- **User-specific & Global**: Notifications can be targeted to specific users or broadcast globally
- **Persistent Storage**: Notifications are stored and persist across sessions
- **Auto-expiration**: Notifications can be set to expire after a specified time
- **Rich Content**: Support for action buttons, metadata, and custom styling

### 🎯 Notification Types

1. **Welcome Notifications** - Greet new contributors
2. **Milestone Notifications** - Celebrate contribution milestones (1, 2, 3 contributions)
3. **Achievement Notifications** - Celebrate Hacktoberfest completion (4+ contributions)
4. **System Notifications** - Important system-wide announcements
5. **Success/Info/Warning/Error** - General purpose notifications

### 🎨 User Interface

- **Notification Center**: Dedicated page showing all notifications with filtering and sorting
- **Navigation Badge**: Real-time unread notification count in the navigation bar
- **Notification Widget**: Embedded widget showing recent notifications on dashboard
- **Real-time Toasts**: Pop-up notifications for immediate alerts
- **Responsive Design**: Works on all device sizes

## File Structure

```
Python/src/
├── Contribute_Checker/
│   └── notification_system.py      # Backend notification manager
├── web_ui/
│   ├── app.py                       # Flask routes and API endpoints
│   ├── templates/
│   │   ├── notifications.html       # Main notifications page
│   │   ├── notification_widget.html # Embeddable widget
│   │   └── base.html               # Updated with notification badge
│   └── static/
│       ├── css/style.css           # Updated with notification styles
│       └── js/app.js               # Real-time notification system
└── notification_demo.py            # Demo script for testing
```

## Backend API

### Core Classes

#### `Notification`
Represents a single notification with the following properties:
- `id`: Unique identifier
- `title`: Notification title
- `message`: Notification content
- `type`: NotificationType enum
- `priority`: NotificationPriority enum
- `username`: Target user (None for global)
- `created_at`: Creation timestamp
- `read`: Read status
- `dismissed`: Dismissed status
- `expires_at`: Expiration timestamp
- `action_url`: Optional action URL
- `action_text`: Optional action button text
- `metadata`: Additional data

#### `NotificationManager`
Manages all notifications with methods for:
- Creating notifications
- Retrieving user/global notifications
- Marking as read/dismissed
- Cleanup and statistics
- Specialized creators for milestones and welcome messages

### API Endpoints

#### GET `/notifications`
Main notifications page with filtering and statistics

#### GET `/api/notifications`
Get notifications for a user
- Query params: `user`, `unread_only`, `limit`
- Returns: Array of notification objects

#### GET `/api/notifications/stats`
Get notification statistics
- Query params: `user`
- Returns: Statistics object with counts by type, priority, etc.

#### POST `/api/notifications/<id>/read`
Mark a notification as read
- Returns: `{success: boolean}`

#### POST `/api/notifications/<id>/dismiss`
Dismiss a notification
- Returns: `{success: boolean}`

#### POST `/api/notifications/mark-all-read`
Mark all notifications as read for a user
- Returns: `{success: boolean, count: number}`

#### POST `/api/notifications/clear-all`
Clear all notifications for a user
- Returns: `{success: boolean, count: number}`

#### POST `/api/notifications/create`
Create a new notification
- Body: Notification data
- Returns: `{success: boolean, notification_id: string}`

#### POST `/api/notifications/system`
Create a system-wide notification
- Body: System notification data
- Returns: `{success: boolean, notification_id: string}`

## Frontend Components

### Notification Center (`notifications.html`)

Full-featured notification management page with:
- **Statistics Dashboard**: Overview of notification counts
- **Filter Tabs**: Filter by all, unread, achievements, system
- **Notification List**: Detailed view of all notifications
- **Bulk Actions**: Mark all read, clear all
- **Real-time Updates**: Auto-refresh every 30 seconds

### Notification Widget (`notification_widget.html`)

Embeddable widget for other pages featuring:
- **Recent Notifications**: Shows last 5 notifications
- **Unread Count**: Badge showing unread count
- **Auto-refresh**: Updates every 30 seconds
- **Click to Read**: Mark notifications as read on click
- **Compact Design**: Fits in sidebar or dashboard

### Real-time System (`app.js`)

JavaScript class providing:
- **Polling**: Check for new notifications every 30 seconds
- **Toast Notifications**: Real-time pop-up alerts
- **Sound Notifications**: Optional audio alerts
- **Visibility API**: Pause when tab is not active
- **Auto-cleanup**: Remove old toast notifications

## Usage Examples

### Creating Notifications

```python
from Contribute_Checker.notification_system import notification_manager, NotificationType, NotificationPriority

# Welcome notification
notification_manager.create_welcome_notification('username', 'Full Name')

# Milestone notification
notification_manager.create_milestone_notification('username', 3, False)

# Custom notification
notification_manager.create_notification(
    title='Custom Alert',
    message='This is a custom notification',
    notification_type=NotificationType.INFO,
    priority=NotificationPriority.HIGH,
    username='target_user',
    action_url='/some-page',
    action_text='Take Action'
)

# System notification
notification_manager.create_system_notification(
    title='Maintenance Notice',
    message='System maintenance scheduled for tonight',
    priority=NotificationPriority.URGENT
)
```

### Frontend Integration

```javascript
// Get notifications
fetch('/api/notifications?user=username')
  .then(response => response.json())
  .then(notifications => {
    console.log('User notifications:', notifications);
  });

// Mark as read
fetch('/api/notifications/123/read', { method: 'POST' })
  .then(response => response.json())
  .then(result => {
    console.log('Marked as read:', result.success);
  });

// Real-time notifications
const notificationSystem = new NotificationSystem();
// Automatically starts polling for new notifications
```

### Template Integration

```html
<!-- Include notification widget -->
{% include 'notification_widget.html' %}

<!-- Notification badge in navigation -->
<a href="/notifications" class="nav-link position-relative">
  <i class="fas fa-bell"></i>
  <span class="badge bg-danger" id="notificationBadge">3</span>
</a>
```

## Testing

### Demo Script

Run the demo script to populate the system with sample data:

```bash
cd Python
python notification_demo.py
```

This creates:
- 5 sample contributors
- Various contributions with milestone notifications
- System notifications
- Custom achievement notifications

### Manual Testing

1. **Start the web server**:
   ```bash
   cd Python/src
   python run_web_ui.py
   ```

2. **Visit the notification center**:
   http://localhost:5000/notifications

3. **Test API endpoints**:
   ```bash
   # Get notifications
   curl http://localhost:5000/api/notifications?user=alice_dev
   
   # Get statistics
   curl http://localhost:5000/api/notifications/stats
   
   # Create notification
   curl -X POST http://localhost:5000/api/notifications/create \
     -H "Content-Type: application/json" \
     -d '{"title":"Test","message":"Test message","type":"info","username":"alice_dev"}'
   ```

## Configuration

### Environment Variables

The notification system respects these environment variables:
- `NOTIFICATION_POLL_INTERVAL`: Polling interval in milliseconds (default: 30000)
- `NOTIFICATION_SOUND_ENABLED`: Enable/disable notification sounds (default: true)

### Customization

#### Styling
Modify `static/css/style.css` to customize notification appearance:
- `.notification-item`: Individual notification styling
- `.notification-widget`: Widget container styling
- `.notification-toast`: Real-time toast styling

#### Behavior
Modify `static/js/app.js` to customize:
- Polling intervals
- Sound notifications
- Auto-dismiss timers
- Notification limits

## Performance Considerations

- **Efficient Polling**: Only polls when tab is active
- **Limited Results**: API endpoints support pagination
- **Auto-cleanup**: Expired notifications are automatically removed
- **Memory Management**: Real-time toasts are auto-removed
- **Debounced Updates**: UI updates are debounced to prevent excessive redraws

## Future Enhancements

Potential improvements for future versions:
- **WebSocket Support**: Replace polling with real-time WebSocket connections
- **Push Notifications**: Browser push notifications for offline users
- **Email Integration**: Send email summaries of important notifications
- **Mobile App**: Native mobile app with push notification support
- **Notification Templates**: Customizable notification templates
- **User Preferences**: Allow users to customize notification settings
- **Analytics**: Track notification engagement and effectiveness

## Troubleshooting

### Common Issues

1. **Notifications not updating**: Check browser console for JavaScript errors
2. **Badge not showing**: Verify API endpoints are accessible
3. **Toast not appearing**: Check browser permissions for notifications
4. **High memory usage**: Ensure old notifications are being cleaned up

### Debug Mode

Enable debug logging by setting `DEBUG=true` in the Flask app configuration.

## Contributing

When contributing to the notification system:
1. Follow the existing code style and patterns
2. Add appropriate error handling
3. Update tests for new functionality
4. Document new API endpoints
5. Consider backward compatibility

## License

This notification system is part of the Hacktoberfest 2025 Project Tracker and follows the same license terms.