"""
Resend Email Integration
Handles email sending via Resend API (configured through Cloudflare)
"""

import os
import logging
from typing import Dict, Optional
import requests


class ResendEmailer:
    """Email sender using Resend API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Resend email client
        
        Args:
            api_key: Resend API key (or from environment)
        """
        self.api_key = api_key or os.getenv("RESEND_API_KEY")
        if not self.api_key:
            raise ValueError("RESEND_API_KEY not found in environment or config")
            
        self.api_url = "https://api.resend.com/emails"
        self.logger = logging.getLogger(__name__)
        
    def send_email(self, 
                   to_email: str,
                   subject: str,
                   body: str,
                   from_email: str = "info@convicure.com",
                   from_name: str = "George Vincent") -> Dict:
        """
        Send email via Resend API
        
        Args:
            to_email: Recipient email address
            subject: Email subject line
            body: Email body (plain text)
            from_email: Sender email (default: info@convicure.com)
            from_name: Sender display name
            
        Returns:
            Response dict with success status and message ID
        """
        # Prepare email data
        email_data = {
            "from": f"{from_name} <{from_email}>",
            "to": [to_email],
            "subject": subject,
            "text": body,
            "reply_to": from_email  # Replies go to info@convicure.com
        }
        
        # Send via Resend API
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                self.api_url,
                json=email_data,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                self.logger.info(f"Email sent successfully: {result.get('id')}")
                return {
                    "success": True,
                    "message_id": result.get("id"),
                    "error": None
                }
            else:
                error_msg = response.json().get("message", "Unknown error")
                self.logger.error(f"Resend API error: {error_msg}")
                return {
                    "success": False,
                    "message_id": None,
                    "error": error_msg
                }
                
        except requests.exceptions.Timeout:
            self.logger.error("Resend API request timed out")
            return {
                "success": False,
                "message_id": None,
                "error": "Request timed out"
            }
        except Exception as e:
            self.logger.error(f"Email send error: {e}")
            return {
                "success": False,
                "message_id": None,
                "error": str(e)
            }
            
    def verify_domain(self) -> Dict:
        """
        Verify that convicure.com domain is properly configured in Resend
        
        Returns:
            Domain verification status
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(
                "https://api.resend.com/domains",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                domains = response.json().get("data", [])
                convicure_domain = next(
                    (d for d in domains if d.get("name") == "convicure.com"),
                    None
                )
                
                if convicure_domain:
                    status = convicure_domain.get("status")
                    self.logger.info(f"Domain status: {status}")
                    return {
                        "verified": status == "verified",
                        "status": status,
                        "domain": "convicure.com"
                    }
                else:
                    return {
                        "verified": False,
                        "status": "not_found",
                        "domain": "convicure.com"
                    }
            else:
                return {
                    "verified": False,
                    "status": "error",
                    "error": response.json().get("message")
                }
                
        except Exception as e:
            self.logger.error(f"Domain verification error: {e}")
            return {
                "verified": False,
                "status": "error",
                "error": str(e)
            }


if __name__ == "__main__":
    # Test Resend integration
    emailer = ResendEmailer()
    
    # Verify domain
    print("\n=== Verifying Domain ===")
    domain_status = emailer.verify_domain()
    print(f"Domain: {domain_status.get('domain')}")
    print(f"Status: {domain_status.get('status')}")
    print(f"Verified: {domain_status.get('verified')}")
    
    # Test email (commented out - uncomment to test)
    # print("\n=== Sending Test Email ===")
    # result = emailer.send_email(
    #     to_email="test@example.com",
    #     subject="Test Email from ConViCure System",
    #     body="This is a test email sent via Resend API."
    # )
    # print(f"Success: {result['success']}")
    # if result['success']:
    #     print(f"Message ID: {result['message_id']}")
    # else:
    #     print(f"Error: {result['error']}")
