"""
In-app notification system for the Hacktoberfest 2025 Project Tracker.
Handles real-time notifications, user alerts, and system messages.
"""

import json
import uuid
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


class NotificationType(Enum):
    """Types of notifications in the system."""
    SUCCESS = "success"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    MILESTONE = "milestone"
    WELCOME = "welcome"
    ACHIEVEMENT = "achievement"
    SYSTEM = "system"


class NotificationPriority(Enum):
    """Priority levels for notifications."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


@dataclass
class Notification:
    """Represents a single notification."""
    id: str
    title: str
    message: str
    type: NotificationType
    priority: NotificationPriority
    user_id: Optional[str] = None
    username: Optional[str] = None
    created_at: datetime = None
    read: bool = False
    dismissed: bool = False
    expires_at: Optional[datetime] = None
    action_url: Optional[str] = None
    action_text: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert notification to dictionary for JSON serialization."""
        data = asdict(self)
        data['type'] = self.type.value
        data['priority'] = self.priority.value
        data['created_at'] = self.created_at.isoformat()
        if self.expires_at:
            data['expires_at'] = self.expires_at.isoformat()
        return data
    
    def is_expired(self) -> bool:
        """Check if the notification has expired."""
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at


class NotificationManager:
    """Manages in-app notifications for users."""
    
    def __init__(self):
        """Initialize the notification manager."""
        self.notifications: Dict[str, Notification] = {}
        self.user_notifications: Dict[str, List[str]] = {}  # username -> notification_ids
        self.global_notifications: List[str] = []  # For system-wide notifications
    
    def create_notification(
        self,
        title: str,
        message: str,
        notification_type: NotificationType = NotificationType.INFO,
        priority: NotificationPriority = NotificationPriority.NORMAL,
        username: Optional[str] = None,
        expires_in_hours: Optional[int] = 24,
        action_url: Optional[str] = None,
        action_text: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a new notification.
        
        Args:
            title: Notification title
            message: Notification message
            notification_type: Type of notification
            priority: Priority level
            username: Target username (None for global notification)
            expires_in_hours: Hours until notification expires (None for no expiration)
            action_url: Optional URL for notification action
            action_text: Optional text for action button
            metadata: Additional data for the notification
            
        Returns:
            str: Notification ID
        """
        notification_id = str(uuid.uuid4())
        expires_at = None
        if expires_in_hours:
            expires_at = datetime.now() + timedelta(hours=expires_in_hours)
        
        notification = Notification(
            id=notification_id,
            title=title,
            message=message,
            type=notification_type,
            priority=priority,
            username=username,
            expires_at=expires_at,
            action_url=action_url,
            action_text=action_text,
            metadata=metadata or {}
        )
        
        self.notifications[notification_id] = notification
        
        if username:
            # User-specific notification
            if username not in self.user_notifications:
                self.user_notifications[username] = []
            self.user_notifications[username].append(notification_id)
        else:
            # Global notification
            self.global_notifications.append(notification_id)
        
        return notification_id
    
    def get_user_notifications(
        self,
        username: str,
        include_global: bool = True,
        unread_only: bool = False,
        limit: Optional[int] = None
    ) -> List[Notification]:
        """
        Get notifications for a specific user.
        
        Args:
            username: Username to get notifications for
            include_global: Whether to include global notifications
            unread_only: Whether to only return unread notifications
            limit: Maximum number of notifications to return
            
        Returns:
            List[Notification]: List of notifications
        """
        notification_ids = []
        
        # Add user-specific notifications
        if username in self.user_notifications:
            notification_ids.extend(self.user_notifications[username])
        
        # Add global notifications if requested
        if include_global:
            notification_ids.extend(self.global_notifications)
        
        # Get notification objects and filter
        notifications = []
        for notif_id in notification_ids:
            if notif_id in self.notifications:
                notification = self.notifications[notif_id]
                
                # Skip expired notifications
                if notification.is_expired():
                    continue
                
                # Skip dismissed notifications
                if notification.dismissed:
                    continue
                
                # Filter by read status if requested
                if unread_only and notification.read:
                    continue
                
                notifications.append(notification)
        
        # Sort by priority and creation time
        notifications.sort(key=lambda n: (
            n.priority.value == "urgent",
            n.priority.value == "high",
            n.priority.value == "normal",
            n.created_at
        ), reverse=True)
        
        # Apply limit if specified
        if limit:
            notifications = notifications[:limit]
        
        return notifications
    
    def mark_as_read(self, notification_id: str) -> bool:
        """
        Mark a notification as read.
        
        Args:
            notification_id: ID of the notification to mark as read
            
        Returns:
            bool: True if successful, False if notification not found
        """
        if notification_id in self.notifications:
            self.notifications[notification_id].read = True
            return True
        return False
    
    def mark_as_dismissed(self, notification_id: str) -> bool:
        """
        Mark a notification as dismissed.
        
        Args:
            notification_id: ID of the notification to dismiss
            
        Returns:
            bool: True if successful, False if notification not found
        """
        if notification_id in self.notifications:
            self.notifications[notification_id].dismissed = True
            return True
        return False
    
    def delete_notification(self, notification_id: str) -> bool:
        """
        Permanently delete a notification.
        
        Args:
            notification_id: ID of the notification to delete
            
        Returns:
            bool: True if successful, False if notification not found
        """
        if notification_id not in self.notifications:
            return False
        
        # Remove from notifications dict
        del self.notifications[notification_id]
        
        # Remove from user notifications
        for username, notif_ids in self.user_notifications.items():
            if notification_id in notif_ids:
                notif_ids.remove(notification_id)
        
        # Remove from global notifications
        if notification_id in self.global_notifications:
            self.global_notifications.remove(notification_id)
        
        return True
    
    def get_notification_stats(self, username: Optional[str] = None) -> Dict[str, int]:
        """
        Get notification statistics for a user or globally.
        
        Args:
            username: Username to get stats for (None for global stats)
            
        Returns:
            Dict[str, int]: Statistics including total, unread, by type, etc.
        """
        if username:
            notifications = self.get_user_notifications(username)
        else:
            notifications = list(self.notifications.values())
        
        stats = {
            'total': len(notifications),
            'unread': sum(1 for n in notifications if not n.read),
            'read': sum(1 for n in notifications if n.read),
            'dismissed': sum(1 for n in notifications if n.dismissed),
        }
        
        # Count by type
        for notif_type in NotificationType:
            stats[f'type_{notif_type.value}'] = sum(
                1 for n in notifications if n.type == notif_type
            )
        
        # Count by priority
        for priority in NotificationPriority:
            stats[f'priority_{priority.value}'] = sum(
                1 for n in notifications if n.priority == priority
            )
        
        return stats
    
    def cleanup_expired(self) -> int:
        """
        Remove all expired notifications.
        
        Returns:
            int: Number of notifications cleaned up
        """
        expired_ids = [
            notif_id for notif_id, notification in self.notifications.items()
            if notification.is_expired()
        ]
        
        for notif_id in expired_ids:
            self.delete_notification(notif_id)
        
        return len(expired_ids)
    
    def create_milestone_notification(
        self,
        username: str,
        contribution_count: int,
        is_hacktoberfest_complete: bool = False
    ) -> str:
        """
        Create a milestone achievement notification.
        
        Args:
            username: Username who achieved the milestone
            contribution_count: Number of contributions
            is_hacktoberfest_complete: Whether Hacktoberfest is complete
            
        Returns:
            str: Notification ID
        """
        if is_hacktoberfest_complete:
            title = "🏆 Hacktoberfest 2025 Complete!"
            message = f"Congratulations! You've completed Hacktoberfest 2025 with {contribution_count} contributions!"
            action_url = f"/contributor/{username}"
            action_text = "View Profile"
        else:
            remaining = 4 - contribution_count
            title = f"🌟 Milestone: {contribution_count} Contributions!"
            message = f"Great job! You've made {contribution_count} contributions. Only {remaining} more to complete Hacktoberfest!"
            action_url = f"/contributor/{username}"
            action_text = "View Progress"
        
        return self.create_notification(
            title=title,
            message=message,
            notification_type=NotificationType.MILESTONE if not is_hacktoberfest_complete else NotificationType.ACHIEVEMENT,
            priority=NotificationPriority.HIGH if is_hacktoberfest_complete else NotificationPriority.NORMAL,
            username=username,
            action_url=action_url,
            action_text=action_text,
            metadata={
                'contribution_count': contribution_count,
                'is_complete': is_hacktoberfest_complete
            }
        )
    
    def create_welcome_notification(self, username: str, name: str) -> str:
        """
        Create a welcome notification for new contributors.
        
        Args:
            username: GitHub username
            name: Full name
            
        Returns:
            str: Notification ID
        """
        return self.create_notification(
            title="👋 Welcome to Hacktoberfest 2025!",
            message=f"Welcome {name}! You're all set to start contributing. Make 4 contributions to complete Hacktoberfest!",
            notification_type=NotificationType.WELCOME,
            priority=NotificationPriority.NORMAL,
            username=username,
            action_url="/add-contribution",
            action_text="Add Contribution",
            expires_in_hours=72
        )
    
    def create_system_notification(
        self,
        title: str,
        message: str,
        priority: NotificationPriority = NotificationPriority.NORMAL,
        expires_in_hours: Optional[int] = 48
    ) -> str:
        """
        Create a system-wide notification.
        
        Args:
            title: Notification title
            message: Notification message
            priority: Priority level
            expires_in_hours: Hours until expiration
            
        Returns:
            str: Notification ID
        """
        return self.create_notification(
            title=title,
            message=message,
            notification_type=NotificationType.SYSTEM,
            priority=priority,
            username=None,  # Global notification
            expires_in_hours=expires_in_hours
        )


# Global notification manager instance
notification_manager = NotificationManager()