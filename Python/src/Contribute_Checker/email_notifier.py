"""
Email notification system with JWT token generation for Hacktoberfest contributors.
"""

# PyJWT provides the `jwt` module. It's an optional dependency for email token
# generation. Import lazily and provide a helpful error if it's not available.
try:
    import jwt
except Exception:  # ImportError could be caused by absence or import-time errors
    jwt = None
import smtplib
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailNotifier:
    """Handles email notifications and JWT token generation for contributors."""
    
    def __init__(self, smtp_server: str = None, smtp_port: int = 587, 
                 sender_email: str = None, sender_password: str = None,
                 jwt_secret: str = None):
        
        """
        Initialize the email notifier.
        
        Args:
            smtp_server (str, optional): SMTP server address. Defaults to gmail SMTP
            smtp_port (int, optional): SMTP port. Defaults to 587
            sender_email (str, optional): Email address to send from (uses env variable if not provided)
            sender_password (str, optional): Email password (uses env variable if not provided)
            jwt_secret (str, optional): Secret key for JWT tokens (uses env variable if not provided)
        """
        self.smtp_server = smtp_server or os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = smtp_port
        self.sender_email = sender_email or os.getenv("SENDER_EMAIL", "")
        self.sender_password = sender_password or os.getenv("SENDER_PASSWORD", "")
        self.jwt_secret = jwt_secret or os.getenv("JWT_SECRET", "your-secret-key-change-this")
        self.notification_history: List[Dict] = []
    
    
    def generate_verification_token(self, email: str, username: str, 
                                    expires_in_hours: int = 24) -> str:
        """
        Generate a JWT verification token for a contributor.
        
        
        Args:
            email (str): Contributor's email address
            username (str): Contributor's GitHub username
            expires_in_hours (int, optional): Token expiration time in hours
            
        Returns:
            str: JWT token
        """
        # Ensure jwt is available
        if jwt is None:
            raise RuntimeError(
                "PyJWT is required for token generation. Install with: pip install PyJWT"
            )

        payload = {
            "email": email,
            "username": username,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=expires_in_hours),
            "type": "email_verification"
        }
        token = jwt.encode(payload, self.jwt_secret, algorithm="HS256")
        return token
    
    def generate_milestone_token(self, email: str, username: str, 
                                milestone: int, expires_in_hours: int = 48) -> str:
        """
        Generate a JWT token for milestone achievement.
        
        Args:
            email (str): Contributor's email address
            username (str): Contributor's GitHub username
            milestone (int): Milestone number (e.g., 4 for Hacktoberfest completion)
            expires_in_hours (int, optional): Token expiration time in hours
            
        Returns:
            str: JWT token
        """
        # Ensure jwt is available
        if jwt is None:
            raise RuntimeError(
                "PyJWT is required for token generation. Install with: pip install PyJWT"
            )

        payload = {
            "email": email,
            "username": username,
            "milestone": milestone,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=expires_in_hours),
            "type": "milestone"
        }
        token = jwt.encode(payload, self.jwt_secret, algorithm="HS256")
        return token
    
    def verify_token(self, token: str) -> Tuple[bool, Optional[Dict]]:
        """
        Verify and decode a JWT token.
        
        Args:
            token (str): JWT token to verify
            
        Returns:
            Tuple[bool, Optional[Dict]]: (is_valid, token_data)
        """
        # Ensure jwt is available
        if jwt is None:
            return False, {"error": "PyJWT not installed. Install with: pip install PyJWT"}

        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
            return True, payload
        except jwt.ExpiredSignatureError:
            return False, {"error": "Token has expired"}
        except jwt.InvalidTokenError:
            return False, {"error": "Invalid token"}
    
    def send_milestone_notification(self, recipient_email: str, username: str, 
                                   contribution_count: int, is_hacktoberfest_complete: bool) -> bool:
        """
        Send an email notification for milestone achievement.
        
        Args:
            recipient_email (str): Recipient's email address
            username (str): GitHub username
            contribution_count (int): Number of contributions
            is_hacktoberfest_complete (bool): Whether Hacktoberfest is complete
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        if not self.sender_email or not self.sender_password:
            print("⚠️  Email credentials not configured. Skipping email notification.")
            return False
        
        try:
            # Generate tokens
            verification_token = self.generate_verification_token(recipient_email, username)
            milestone_token = self.generate_milestone_token(recipient_email, username, contribution_count)
            
            # Create email message
            message = MIMEMultipart("alternative")
            message["Subject"] = f"🎉 Milestone Achievement - {contribution_count} Contributions!"
            message["From"] = self.sender_email
            message["To"] = recipient_email
            
            # Create HTML email body
            if is_hacktoberfest_complete:
                html_body = self._get_completion_email(username, contribution_count, verification_token, milestone_token)
                subject = "🏆 Congratulations! You've Completed Hacktoberfest 2025!"
                message["Subject"] = subject
            else:
                html_body = self._get_milestone_email(username, contribution_count, verification_token, milestone_token)
            
            # Attach HTML part
            part = MIMEText(html_body, "html")
            message.attach(part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            # Record notification
            self.notification_history.append({
                "recipient": recipient_email,
                "username": username,
                "timestamp": datetime.now().isoformat(),
                "milestone": contribution_count,
                "status": "sent"
            })
            
            print(f"✅ Email notification sent to {recipient_email}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email to {recipient_email}: {str(e)}")
            self.notification_history.append({
                "recipient": recipient_email,
                "username": username,
                "timestamp": datetime.now().isoformat(),
                "milestone": contribution_count,
                "status": f"failed: {str(e)}"
            })
            return False
    
    def send_welcome_email(self, recipient_email: str, name: str, username: str) -> bool:
        """
        Send a welcome email to a new contributor.
        
        Args:
            recipient_email (str): Recipient's email address
            name (str): Contributor's full name
            username (str): GitHub username
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        if not self.sender_email or not self.sender_password:
            print("⚠️  Email credentials not configured. Skipping welcome email.")
            return False
        
        try:
            verification_token = self.generate_verification_token(recipient_email, username)
            
            message = MIMEMultipart("alternative")
            message["Subject"] = "👋 Welcome to Hacktoberfest 2025!"
            message["From"] = self.sender_email
            message["To"] = recipient_email
            
            html_body = self._get_welcome_email(name, username, verification_token)
            part = MIMEText(html_body, "html")
            message.attach(part)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            self.notification_history.append({
                "recipient": recipient_email,
                "username": username,
                "timestamp": datetime.now().isoformat(),
                "type": "welcome",
                "status": "sent"
            })
            
            print(f"✅ Welcome email sent to {recipient_email}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send welcome email to {recipient_email}: {str(e)}")
            return False
    
    @staticmethod
    def _get_welcome_email(name: str, username: str, token: str) -> str:
        """Generate HTML content for welcome email."""
        return f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9; border-radius: 8px;">
                    <h1 style="color: #ff6b6b; text-align: center;">👋 Welcome to Hacktoberfest 2025!</h1>
                    
                    <p>Hi <strong>{name}</strong>,</p>
                    
                    <p>We're thrilled to have you join our Hacktoberfest 2025 community! 🎉</p>
                    
                    <p>Your GitHub username <strong>@{username}</strong> has been registered. You're all set to start making contributions and earning your place on our leaderboard!</p>
                    
                    <div style="background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0;">
                        <h3 style="color: #856404;">🎯 Quick Tips:</h3>
                        <ul style="color: #856404;">
                            <li>Make 4 contributions to complete Hacktoberfest!</li>
                            <li>Check our leaderboard to see how you're progressing</li>
                            <li>You'll receive notifications as you reach milestones</li>
                            <li>Verify your email with this token: <code style="background-color: #f1f1f1; padding: 5px; border-radius: 3px;">{token[:20]}...</code></li>
                        </ul>
                    </div>
                    
                    <p style="margin-top: 30px; color: #666; font-size: 12px;">
                        Best regards,<br>
                        <strong>Hacktoberfest 2025 Team</strong>
                    </p>
                </div>
            </body>
        </html>
        """
    
    @staticmethod
    def _get_milestone_email(username: str, count: int, verification_token: str, milestone_token: str) -> str:
        """Generate HTML content for milestone email."""
        remaining = 4 - count
        return f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f0f9ff; border-radius: 8px;">
                    <h1 style="color: #4a90e2; text-align: center;">🌟 Milestone Achievement!</h1>
                    
                    <p>Hey <strong>@{username}</strong>,</p>
                    
                    <p style="font-size: 18px; font-weight: bold;">You've reached <span style="color: #4a90e2;">{count} contributions</span>! 🎊</p>
                    
                    <div style="background-color: #d4edff; padding: 15px; border-left: 4px solid #4a90e2; margin: 20px 0;">
                        <h3 style="color: #0066cc;">Progress to Hacktoberfest Completion:</h3>
                        <div style="width: 100%; background-color: #ccc; border-radius: 5px; overflow: hidden;">
                            <div style="width: {(count / 4) * 100}%; background-color: #4a90e2; height: 30px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">
                                {count}/4
                            </div>
                        </div>
                        <p>Only <strong>{remaining} more</strong> contributions to go!</p>
                    </div>
                    
                    <p style="text-align: center; color: #666; font-size: 12px; margin-top: 20px;">
                        Milestone Token: <code style="background-color: #f1f1f1; padding: 5px; border-radius: 3px;">{milestone_token[:30]}...</code>
                    </p>
                    
                    <p style="margin-top: 30px; color: #666; font-size: 12px; text-align: center;">
                        Keep up the great work! 💪
                    </p>
                </div>
            </body>
        </html>
        """
    
    @staticmethod
    def _get_completion_email(username: str, count: int, verification_token: str, milestone_token: str) -> str:
        """Generate HTML content for Hacktoberfest completion email."""
        return f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; color: white;">
                    <h1 style="text-align: center; font-size: 32px;">🏆 CONGRATULATIONS! 🏆</h1>
                    
                    <p style="font-size: 18px; text-align: center;">You've completed <strong>Hacktoberfest 2025!</strong></p>
                    
                    <div style="background-color: rgba(255,255,255,0.2); padding: 20px; border-radius: 8px; margin: 20px 0; text-align: center;">
                        <h2 style="margin: 0; color: #ffd700;">✨ {count} Contributions ✨</h2>
                        <p style="margin-top: 10px; font-size: 16px;">You are officially a Hacktoberfest 2025 contributor!</p>
                    </div>
                    
                    <ul style="font-size: 16px; margin: 20px 0;">
                        <li>🎖️ You've earned your place on our leaderboard</li>
                        <li>👥 You've helped advance open source projects</li>
                        <li>🌍 You're part of a global community</li>
                        <li>📜 Check your email for your achievement certificate</li>
                    </ul>
                    
                    <p style="text-align: center; margin-top: 30px; font-size: 14px;">
                        Your completion token: <code style="background-color: rgba(0,0,0,0.2); padding: 5px; border-radius: 3px; font-family: monospace;">{milestone_token[:35]}...</code>
                    </p>
                    
                    <p style="text-align: center; margin-top: 30px; font-style: italic; font-size: 14px;">
                        Thank you for making the world a better place through open source! 💙
                    </p>
                </div>
            </body>
        </html>
        """
    
    def get_notification_history(self) -> List[Dict]:
        """Get the history of sent notifications."""
        return self.notification_history
    
    def clear_notification_history(self) -> None:
        """Clear the notification history."""
        self.notification_history.clear()
