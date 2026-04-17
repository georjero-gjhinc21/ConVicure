"""
Personalization Engine
Generates personalized email drafts for investor outreach
"""

import json
import os
from typing import Dict
from agents.base_agent import BaseAgent


class PersonalizationEngine(BaseAgent):
    """Agent responsible for creating personalized email drafts"""
    
    def create_draft(self, prospect: Dict) -> Dict:
        """
        Create personalized email draft for a prospect
        
        Args:
            prospect: Prospect with intelligence data
            
        Returns:
            Draft email dictionary
        """
        self.logger.info(f"Creating draft for: {prospect.get('name')}")
        
        # Extract intelligence
        intelligence = prospect.get("intelligence", {})
        hooks = intelligence.get("personalization_hooks", [])
        
        if not hooks:
            self.logger.warning(f"No personalization hooks found for {prospect.get('name')}")
            
        # Generate email components
        subject = self._generate_subject(prospect, intelligence)
        body = self._generate_body(prospect, intelligence)
        
        # Create draft object
        draft = {
            "prospect_name": prospect.get("name"),
            "to_email": prospect.get("email", ""),  # Needs to be found in research
            "subject": subject,
            "body": body,
            "match_score": prospect.get("match_score"),
            "hooks_used": hooks[:3],  # Top 3 hooks
            "created_date": self.get_timestamp(),
            "status": "pending_review",
            "prospect_id": prospect.get("name", "").lower().replace(" ", "_")
        }
        
        # Save draft
        self._save_draft(draft)
        
        # Log activity
        self.log_activity("draft_created", {
            "prospect": prospect.get("name"),
            "subject": subject
        })
        
        return draft
        
    def _generate_subject(self, prospect: Dict, intelligence: Dict) -> str:
        """Generate personalized email subject line"""
        company_info = self.knowledge.get("company", {})
        
        system_prompt = """You are an expert at writing effective cold email subject lines
        for biotech fundraising. Create a subject line that:
        - Is 5-8 words
        - References a specific connection point
        - Is professional but not generic
        - Avoids spam triggers ("opportunity", "urgent", etc.)
        - Makes the investor curious
        
        Return ONLY the subject line, no quotes, no explanation."""
        
        hooks = intelligence.get("personalization_hooks", [])
        portfolio = intelligence.get("portfolio_analysis", {})
        
        prompt = f"""Create a subject line for this investor outreach:
        
        INVESTOR: {prospect.get('name')}
        FOCUS: {prospect.get('focus')}
        
        PERSONALIZATION HOOKS:
        {json.dumps(hooks[:3], indent=2)}
        
        PORTFOLIO CONNECTIONS:
        {json.dumps(portfolio.get('relevant_companies', [])[:2], indent=2)}
        
        CONVICURE: {company_info.get('tagline')}
        FOUNDER: Stanford-affiliated researcher (14,600+ citations)
        
        Create a compelling subject line that uses one of these connection points.
        Return ONLY the subject line."""
        
        try:
            subject = self.call_claude(prompt, system_prompt=system_prompt, max_tokens=100)
            return subject.strip().strip('"').strip("'")
        except Exception as e:
            self.logger.error(f"Subject generation error: {e}")
            return "Stanford Lyme disease breakthrough"
            
    def _generate_body(self, prospect: Dict, intelligence: Dict) -> str:
        """Generate personalized email body"""
        company_info = self.knowledge.get("company", {})
        email_guidelines = self.knowledge.get("email_guidelines", {})
        signature = self.config.get("email", {}).get("signature", "")
        
        system_prompt = f"""You are an expert at writing effective cold emails for biotech 
        fundraising. Follow these strict guidelines:
        
        STRUCTURE:
        1. Hook (1 sentence) - Reference specific connection point
        2. Context (2-3 sentences) - Brief company intro with differentiation
        3. Ask (1 sentence) - Request brief conversation
        
        RULES:
        - 150-200 words total
        - Professional but warm tone
        - No salesy language
        - No attachments mentioned
        - No false urgency
        - Show you've done research
        - Be specific, not generic
        
        PROHIBITED:
        - Drug molecule names: {json.dumps(email_guidelines.get('prohibited_content', []))}
        - No "Dear Investor" or generic greetings
        - No Stanford attribution claims
        - No TBI mentions
        - No attachments in cold outreach
        
        Return ONLY the email body text, no subject line, no signature block."""
        
        hooks = intelligence.get("personalization_hooks", [])
        portfolio = intelligence.get("portfolio_analysis", {})
        thesis = intelligence.get("investment_thesis", "")
        
        prompt = f"""Write a personalized cold outreach email:
        
        INVESTOR PROFILE:
        - Name: {prospect.get('name')}
        - Type: {prospect.get('type')}
        - Focus: {prospect.get('focus')}
        - Investment Thesis: {thesis}
        
        PERSONALIZATION HOOKS:
        {json.dumps(hooks, indent=2)}
        
        PORTFOLIO ANALYSIS:
        {json.dumps(portfolio, indent=2)}
        
        CONVICURE DETAILS:
        - Tagline: {company_info.get('tagline')}
        - Stage: {company_info.get('stage')}
        - Raising: {company_info.get('fundraise', {}).get('target')} for {company_info.get('fundraise', {}).get('purpose')}
        - Science: {company_info.get('science', {}).get('approach')}
        - Founder: {company_info.get('science', {}).get('founder_credentials')}
        - Market Gap: {company_info.get('market', {}).get('unmet_need')}
        - Regulatory: {company_info.get('regulatory', {}).get('primary_pathway')}
        
        KEY DIFFERENTIATORS:
        {json.dumps(company_info.get('advantages', []), indent=2)}
        
        Write the email body following all guidelines. Be specific and show research."""
        
        try:
            body = self.call_claude(prompt, system_prompt=system_prompt, max_tokens=1000)
            
            # Add signature
            full_body = body.strip() + "\n\n" + signature
            
            # Validate length
            word_count = len(body.split())
            if word_count < 120 or word_count > 250:
                self.logger.warning(f"Draft length out of range: {word_count} words")
                
            return full_body
            
        except Exception as e:
            self.logger.error(f"Body generation error: {e}")
            return self._get_fallback_template(prospect)
            
    def _get_fallback_template(self, prospect: Dict) -> str:
        """Return a safe fallback template if generation fails"""
        signature = self.config.get("email", {}).get("signature", "")
        
        template = f"""Hi {prospect.get('name', 'there')},

I noticed your focus on early-stage life science companies and thought ConViCure might align with your investment thesis.

We're developing a first-in-class combination therapy for persistent Lyme disease—a condition affecting 100,000+ Americans annually with zero FDA-approved treatments. Our Stanford-affiliated founder discovered that our lead drug eliminates even the treatment-resistant forms of the bacteria.

We're raising $6.5M to reach IND clearance through an accelerated 505(b)(2) pathway. Would you be open to a brief conversation to explore if there's a fit?

{signature}"""
        
        return template
        
    def _save_draft(self, draft: Dict):
        """Save draft to file for review"""
        drafts_dir = self.config.get("paths", {}).get("drafts_dir", "data/drafts/")
        os.makedirs(drafts_dir, exist_ok=True)
        
        filename = f"{draft['prospect_id']}_{draft['created_date'][:10]}.json"
        filepath = os.path.join(drafts_dir, filename)
        
        self.save_json(draft, filepath)
        self.logger.debug(f"Draft saved: {filepath}")


if __name__ == "__main__":
    # Test the personalization engine
    engine = PersonalizationEngine()
    
    test_prospect = {
        "name": "Sarah Chen",
        "type": "VC Fund Partner",
        "focus": "Life science, drug repurposing",
        "match_score": 92,
        "intelligence": {
            "personalization_hooks": [
                "Portfolio: Compound Therapeutics - drug repurposing play",
                "Stanford connection - founder Dr. Jay Rajadas",
                "Investment thesis: infectious disease focus"
            ],
            "portfolio_analysis": {
                "relevant_companies": [
                    {"name": "Compound Therapeutics", "relevance": "Drug repurposing strategy"}
                ]
            },
            "investment_thesis": "Early-stage life science with focus on drug repurposing and infectious disease"
        }
    }
    
    draft = engine.create_draft(test_prospect)
    print("\n=== DRAFT EMAIL ===")
    print(f"To: {draft['prospect_name']}")
    print(f"Subject: {draft['subject']}")
    print(f"\n{draft['body']}")
