"""
Review & Send Controller
Human-in-the-loop review system and email sender
"""

import os
import json
import glob
from typing import List, Dict, Optional
from agents.base_agent import BaseAgent
from agents.crm import CRMManager


class ReviewController(BaseAgent):
    """Controller for reviewing and sending email drafts"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        super().__init__(config_path)
        self.crm = CRMManager(config_path)
        self.drafts_dir = self.config.get("paths", {}).get("drafts_dir", "data/drafts/")
        self.sent_dir = self.config.get("paths", {}).get("sent_dir", "data/sent/")
        
    def get_pending_drafts(self) -> List[Dict]:
        """Get all drafts pending review"""
        pattern = os.path.join(self.drafts_dir, "*.json")
        draft_files = glob.glob(pattern)
        
        drafts = []
        for filepath in draft_files:
            draft = self.load_json(filepath)
            if draft and draft.get("status") == "pending_review":
                draft["filepath"] = filepath
                drafts.append(draft)
                
        # Sort by match score (highest first)
        drafts.sort(key=lambda x: x.get("match_score", 0), reverse=True)
        
        return drafts
        
    def review_drafts_interactive(self):
        """Interactive review interface for drafts"""
        drafts = self.get_pending_drafts()
        
        if not drafts:
            print("\n✓ No drafts pending review\n")
            return
            
        print(f"\n{'='*70}")
        print(f"  CONVICURE EMAIL REVIEW - {len(drafts)} drafts pending")
        print(f"{'='*70}\n")
        
        for i, draft in enumerate(drafts, 1):
            self._display_draft(i, len(drafts), draft)
            
            action = self._get_user_action()
            
            if action == "approve":
                self._approve_draft(draft)
            elif action == "edit":
                self._edit_draft(draft)
            elif action == "reject":
                self._reject_draft(draft)
            elif action == "skip":
                continue
            elif action == "quit":
                print("\n✓ Review session ended\n")
                return
                
        print(f"\n✓ All drafts reviewed\n")
        
    def _display_draft(self, current: int, total: int, draft: Dict):
        """Display draft for review"""
        print(f"\n{'='*70}")
        print(f"DRAFT #{current}/{total} - Review Required")
        print(f"{'='*70}\n")
        
        print(f"Prospect: {draft.get('prospect_name')}")
        print(f"Match Score: {draft.get('match_score')}/100")
        print(f"To: {draft.get('to_email', 'EMAIL NEEDED')}")
        
        hooks = draft.get("hooks_used", [])
        if hooks:
            print(f"\nConnection Points:")
            for hook in hooks:
                print(f"  • {hook}")
                
        print(f"\n{'-'*70}")
        print(f"SUBJECT: {draft.get('subject')}\n")
        print(draft.get('body'))
        print(f"{'-'*70}\n")
        
    def _get_user_action(self) -> str:
        """Get user's review decision"""
        while True:
            choice = input("Actions: [A]pprove  [E]dit  [R]eject  [S]kip  [Q]uit\n> ").strip().lower()
            
            if choice in ['a', 'approve']:
                return 'approve'
            elif choice in ['e', 'edit']:
                return 'edit'
            elif choice in ['r', 'reject']:
                return 'reject'
            elif choice in ['s', 'skip']:
                return 'skip'
            elif choice in ['q', 'quit']:
                return 'quit'
            else:
                print("Invalid choice. Please enter A, E, R, S, or Q.")
                
    def _approve_draft(self, draft: Dict):
        """Approve and send draft"""
        print("\n→ Draft approved. Sending email...")
        
        # Check daily limit
        if self._check_daily_limit():
            self.logger.warning("Daily email limit reached")
            print("⚠ Daily email limit reached. Email queued for tomorrow.")
            draft["status"] = "queued"
            self.save_json(draft, draft["filepath"])
            return
            
        # Send email (placeholder - would use Gmail API in production)
        success = self._send_email(draft)
        
        if success:
            draft["status"] = "sent"
            draft["sent_date"] = self.get_timestamp()
            
            # Move to sent folder
            sent_path = os.path.join(self.sent_dir, os.path.basename(draft["filepath"]))
            self.save_json(draft, sent_path)
            
            # Remove from drafts
            os.remove(draft["filepath"])
            
            # Update CRM
            self.crm.update_prospect_status(draft["prospect_id"], "Sent")
            self.crm.add_interaction(
                draft["prospect_id"],
                "email_sent",
                f"Subject: {draft['subject']}"
            )
            
            print("✓ Email sent successfully\n")
            self.log_activity("email_sent", {
                "prospect": draft["prospect_name"],
                "subject": draft["subject"]
            })
        else:
            print("✗ Email send failed\n")
            
    def _edit_draft(self, draft: Dict):
        """Allow user to edit draft"""
        print("\n=== EDIT MODE ===\n")
        
        print(f"Current Subject: {draft.get('subject')}")
        new_subject = input("New Subject (or press Enter to keep): ").strip()
        if new_subject:
            draft["subject"] = new_subject
            
        print(f"\nCurrent Body:\n{draft.get('body')}\n")
        print("Enter new body (end with empty line twice):")
        
        lines = []
        empty_count = 0
        while True:
            line = input()
            if line == "":
                empty_count += 1
                if empty_count >= 2:
                    break
            else:
                empty_count = 0
                lines.append(line)
                
        if lines:
            draft["body"] = "\n".join(lines)
            
        draft["status"] = "edited"
        draft["edited_date"] = self.get_timestamp()
        self.save_json(draft, draft["filepath"])
        
        print("\n✓ Draft updated. Review again:")
        self._display_draft(1, 1, draft)
        
        # Re-review
        action = self._get_user_action()
        if action == "approve":
            self._approve_draft(draft)
            
    def _reject_draft(self, draft: Dict):
        """Reject draft"""
        reason = input("\nRejection reason (optional): ").strip()
        
        draft["status"] = "rejected"
        draft["rejected_date"] = self.get_timestamp()
        draft["rejection_reason"] = reason
        
        self.save_json(draft, draft["filepath"])
        
        # Update CRM
        self.crm.update_prospect_status(draft["prospect_id"], "Passed", reason)
        
        print("✓ Draft rejected\n")
        self.log_activity("draft_rejected", {
            "prospect": draft["prospect_name"],
            "reason": reason
        })
        
    def _check_daily_limit(self) -> bool:
        """Check if daily email limit has been reached"""
        daily_limit = self.config.get("email", {}).get("daily_limit", 10)
        
        # Count emails sent today
        sent_files = glob.glob(os.path.join(self.sent_dir, "*.json"))
        today = self.get_timestamp()[:10]
        
        sent_today = 0
        for filepath in sent_files:
            draft = self.load_json(filepath)
            if draft and draft.get("sent_date", "")[:10] == today:
                sent_today += 1
                
        return sent_today >= daily_limit
        
    def _send_email(self, draft: Dict) -> bool:
        """
        Send email via Gmail API
        
        NOTE: This is a placeholder. In production, implement Gmail API integration.
        For now, just logs the email that would be sent.
        """
        self.logger.info(f"[EMAIL SEND] To: {draft.get('to_email')}")
        self.logger.info(f"[EMAIL SEND] Subject: {draft.get('subject')}")
        self.logger.info(f"[EMAIL SEND] Body:\n{draft.get('body')}")
        
        # In production, use Gmail API:
        # from google.oauth2.credentials import Credentials
        # from googleapiclient.discovery import build
        # ... Gmail API implementation ...
        
        # For now, return True to simulate successful send
        return True


if __name__ == "__main__":
    # Run interactive review
    controller = ReviewController()
    controller.review_drafts_interactive()
