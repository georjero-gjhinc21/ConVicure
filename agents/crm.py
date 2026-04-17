"""
CRM Manager
Manages investor pipeline, tracking, and follow-ups
"""

import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from agents.base_agent import BaseAgent


class CRMManager(BaseAgent):
    """Agent responsible for pipeline management and tracking"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        super().__init__(config_path)
        self.pipeline_db_path = self.config.get("paths", {}).get(
            "pipeline_db", "data/prospects/pipeline.json"
        )
        self.stages = self.config.get("crm", {}).get("stages", [
            "Identified", "Researched", "Drafted", "Sent", "Responded",
            "Meeting Scheduled", "Meeting Completed", "Passed", "Closed"
        ])
        
    def get_pipeline(self) -> Dict:
        """Get current pipeline state"""
        pipeline = self.load_json(self.pipeline_db_path)
        if not pipeline:
            pipeline = {"prospects": {}, "updated": self.get_timestamp()}
        return pipeline
        
    def update_prospect_status(self, prospect_id: str, new_status: str, notes: str = ""):
        """
        Update prospect's status in pipeline
        
        Args:
            prospect_id: Unique prospect identifier
            new_status: New status (must be in configured stages)
            notes: Optional notes about the status change
        """
        if new_status not in self.stages:
            raise ValueError(f"Invalid status: {new_status}")
            
        pipeline = self.get_pipeline()
        
        if prospect_id not in pipeline["prospects"]:
            pipeline["prospects"][prospect_id] = {
                "id": prospect_id,
                "status": new_status,
                "history": [],
                "notes": [],
                "created": self.get_timestamp()
            }
        else:
            # Add to history
            old_status = pipeline["prospects"][prospect_id]["status"]
            pipeline["prospects"][prospect_id]["history"].append({
                "from": old_status,
                "to": new_status,
                "timestamp": self.get_timestamp()
            })
            pipeline["prospects"][prospect_id]["status"] = new_status
            
        if notes:
            pipeline["prospects"][prospect_id]["notes"].append({
                "timestamp": self.get_timestamp(),
                "note": notes
            })
            
        pipeline["updated"] = self.get_timestamp()
        self.save_json(pipeline, self.pipeline_db_path)
        
        self.logger.info(f"Updated {prospect_id}: {new_status}")
        
    def get_prospects_by_status(self, status: str) -> List[Dict]:
        """Get all prospects at a specific pipeline stage"""
        pipeline = self.get_pipeline()
        return [
            p for p in pipeline["prospects"].values()
            if p.get("status") == status
        ]
        
    def get_follow_ups_due(self) -> List[Dict]:
        """Get prospects that need follow-up"""
        pipeline = self.get_pipeline()
        follow_up_config = self.config.get("crm", {}).get("follow_up", {})
        
        first_follow_up_days = follow_up_config.get("first", 5)
        second_follow_up_days = follow_up_config.get("second", 12)
        
        now = datetime.now()
        due_for_follow_up = []
        
        for prospect in pipeline["prospects"].values():
            if prospect.get("status") != "Sent":
                continue
                
            # Find when email was sent
            sent_events = [
                h for h in prospect.get("history", [])
                if h.get("to") == "Sent"
            ]
            
            if not sent_events:
                continue
                
            sent_date = datetime.fromisoformat(sent_events[-1]["timestamp"])
            days_since_sent = (now - sent_date).days
            
            # Check if follow-up is due
            follow_up_count = len([
                n for n in prospect.get("notes", [])
                if "follow-up" in n.get("note", "").lower()
            ])
            
            if follow_up_count == 0 and days_since_sent >= first_follow_up_days:
                due_for_follow_up.append({
                    **prospect,
                    "days_since_sent": days_since_sent,
                    "follow_up_number": 1
                })
            elif follow_up_count == 1 and days_since_sent >= second_follow_up_days:
                due_for_follow_up.append({
                    **prospect,
                    "days_since_sent": days_since_sent,
                    "follow_up_number": 2
                })
                
        return due_for_follow_up
        
    def get_pipeline_metrics(self) -> Dict:
        """Calculate pipeline metrics"""
        pipeline = self.get_pipeline()
        prospects = pipeline.get("prospects", {})
        
        # Count by stage
        stage_counts = {stage: 0 for stage in self.stages}
        for prospect in prospects.values():
            status = prospect.get("status")
            if status in stage_counts:
                stage_counts[status] += 1
                
        # Calculate conversion rates
        total = len(prospects)
        sent = stage_counts.get("Sent", 0) + stage_counts.get("Responded", 0) + \
               stage_counts.get("Meeting Scheduled", 0) + stage_counts.get("Meeting Completed", 0)
        responded = stage_counts.get("Responded", 0) + stage_counts.get("Meeting Scheduled", 0) + \
                    stage_counts.get("Meeting Completed", 0)
        meetings = stage_counts.get("Meeting Scheduled", 0) + stage_counts.get("Meeting Completed", 0)
        
        metrics = {
            "total_prospects": total,
            "stage_breakdown": stage_counts,
            "response_rate": round(responded / sent * 100, 1) if sent > 0 else 0,
            "meeting_rate": round(meetings / sent * 100, 1) if sent > 0 else 0,
            "follow_ups_due": len(self.get_follow_ups_due())
        }
        
        return metrics
        
    def add_interaction(self, prospect_id: str, interaction_type: str, details: str):
        """
        Log an interaction with a prospect
        
        Args:
            prospect_id: Prospect identifier
            interaction_type: Type of interaction (email_sent, email_received, call, meeting, etc.)
            details: Details about the interaction
        """
        pipeline = self.get_pipeline()
        
        if prospect_id not in pipeline["prospects"]:
            self.logger.warning(f"Prospect {prospect_id} not found in pipeline")
            return
            
        if "interactions" not in pipeline["prospects"][prospect_id]:
            pipeline["prospects"][prospect_id]["interactions"] = []
            
        pipeline["prospects"][prospect_id]["interactions"].append({
            "type": interaction_type,
            "details": details,
            "timestamp": self.get_timestamp()
        })
        
        pipeline["updated"] = self.get_timestamp()
        self.save_json(pipeline, self.pipeline_db_path)
        
        self.logger.info(f"Logged {interaction_type} for {prospect_id}")
        
    def generate_dashboard(self) -> str:
        """Generate a text dashboard of pipeline status"""
        metrics = self.get_pipeline_metrics()
        follow_ups = self.get_follow_ups_due()
        
        dashboard = f"""
╔══════════════════════════════════════════════════════════════╗
║             CONVICURE FUNDRAISING PIPELINE                   ║
╚══════════════════════════════════════════════════════════════╝

Total Prospects: {metrics['total_prospects']}

PIPELINE STAGES:
"""
        
        for stage in self.stages:
            count = metrics['stage_breakdown'].get(stage, 0)
            bar = "█" * (count // 2) if count > 0 else ""
            dashboard += f"  {stage:20s} {count:3d} {bar}\n"
            
        dashboard += f"""
CONVERSION METRICS:
  Response Rate:  {metrics['response_rate']}%
  Meeting Rate:   {metrics['meeting_rate']}%
  
FOLLOW-UPS DUE: {metrics['follow_ups_due']}
"""
        
        if follow_ups:
            dashboard += "\nREQUIRES FOLLOW-UP:\n"
            for fu in follow_ups[:5]:  # Show top 5
                dashboard += f"  • {fu['id']} (Day {fu['days_since_sent']}, Follow-up #{fu['follow_up_number']})\n"
                
        return dashboard


if __name__ == "__main__":
    # Test CRM manager
    crm = CRMManager()
    
    # Update some test prospects
    crm.update_prospect_status("lifesci_ventures", "Sent", "Initial outreach sent")
    crm.update_prospect_status("stanford_capital", "Researched")
    crm.update_prospect_status("lyme_ventures", "Meeting Scheduled")
    
    # Show dashboard
    print(crm.generate_dashboard())
    
    # Show metrics
    metrics = crm.get_pipeline_metrics()
    print("\nMETRICS:")
    print(json.dumps(metrics, indent=2))
