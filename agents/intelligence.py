"""
Intelligence Agent
Performs deep research on qualified prospects to enable personalization
"""

import json
from typing import Dict, List
from agents.base_agent import BaseAgent


class IntelligenceAgent(BaseAgent):
    """Agent responsible for deep prospect intelligence gathering"""
    
    def analyze_prospect(self, prospect: Dict) -> Dict:
        """
        Perform deep analysis on a prospect
        
        Args:
            prospect: Basic prospect information
            
        Returns:
            Enhanced prospect dict with intelligence data
        """
        self.logger.info(f"Analyzing prospect: {prospect.get('name')}")
        
        # Gather intelligence from multiple sources
        intelligence = {
            "portfolio_analysis": self._analyze_portfolio(prospect),
            "investment_thesis": self._extract_thesis(prospect),
            "recent_activity": self._find_recent_activity(prospect),
            "connection_points": self._find_connections(prospect),
            "personalization_hooks": []
        }
        
        # Synthesize intelligence
        intelligence["personalization_hooks"] = self._identify_hooks(prospect, intelligence)
        
        # Update prospect with intelligence
        enhanced_prospect = {
            **prospect,
            "intelligence": intelligence,
            "status": "Researched",
            "analyzed_date": self.get_timestamp()
        }
        
        self.log_activity("intelligence_analysis", {
            "prospect": prospect.get("name"),
            "hooks_found": len(intelligence["personalization_hooks"])
        })
        
        return enhanced_prospect
        
    def _analyze_portfolio(self, prospect: Dict) -> Dict:
        """Analyze investor's portfolio for relevant companies"""
        system_prompt = """You are an expert at analyzing venture capital portfolios.
        Given an investor's information, identify portfolio companies that are relevant
        to ConViCure's positioning (infectious disease, drug repurposing, combination
        therapies, Stanford connections, etc.).
        
        Return JSON with:
        - relevant_companies: list of portfolio companies with relevance explanation
        - investment_patterns: observed patterns in their investments
        - stage_preference: preferred investment stages
        - check_size_range: typical investment amounts"""
        
        portfolio_companies = prospect.get("portfolio_companies", [])
        
        prompt = f"""Analyze this investor's portfolio for ConViCure relevance:
        
        INVESTOR: {prospect.get('name')}
        TYPE: {prospect.get('type')}
        FOCUS: {prospect.get('focus')}
        KNOWN PORTFOLIO COMPANIES: {json.dumps(portfolio_companies)}
        
        CONVICURE CONTEXT:
        - Preclinical infectious disease therapeutics
        - Drug repurposing (azlocillin + 3 others)
        - Combination therapy approach
        - Stanford founder (Dr. Jay Rajadas)
        - Lyme disease + coinfections
        - 505(b)(2) regulatory pathway
        
        Find connections and patterns. Return as JSON."""
        
        try:
            response = self.call_claude(prompt, system_prompt=system_prompt, max_tokens=2000)
            analysis = self._parse_json_response(response)
            return analysis
        except Exception as e:
            self.logger.error(f"Portfolio analysis error: {e}")
            return {}
            
    def _extract_thesis(self, prospect: Dict) -> str:
        """Extract investor's investment thesis"""
        system_prompt = """Extract and summarize an investor's investment thesis
        from available information. Focus on what types of companies they back,
        at what stages, and what they look for. Be concise."""
        
        prompt = f"""Based on this investor information, extract their investment thesis:
        
        NAME: {prospect.get('name')}
        FOCUS: {prospect.get('focus')}
        STAGE: {prospect.get('stage')}
        PORTFOLIO: {json.dumps(prospect.get('portfolio_companies', []))}
        
        Return a 2-3 sentence summary of their investment thesis."""
        
        try:
            thesis = self.call_claude(prompt, system_prompt=system_prompt, max_tokens=500)
            return thesis.strip()
        except Exception as e:
            self.logger.error(f"Thesis extraction error: {e}")
            return ""
            
    def _find_recent_activity(self, prospect: Dict) -> List[Dict]:
        """Find recent investment activity or news"""
        # This would ideally use real-time web search, but we'll simulate
        # In production, this would call web_search API
        
        self.logger.debug(f"Finding recent activity for {prospect.get('name')}")
        
        # Placeholder - in real implementation, use web search tool
        # For now, return empty list
        return []
        
    def _find_connections(self, prospect: Dict) -> Dict:
        """Find connection points to ConViCure"""
        warm_intro_networks = self.knowledge.get("warm_intro_networks", {})
        
        connections = {
            "stanford": self._check_stanford_connection(prospect),
            "lyme_community": self._check_lyme_connection(prospect),
            "mutual_investors": [],  # Placeholder for mutual portfolio companies
            "geographic": self._check_geographic_connection(prospect)
        }
        
        return connections
        
    def _check_stanford_connection(self, prospect: Dict) -> bool:
        """Check for Stanford affiliation"""
        name = prospect.get("name", "").lower()
        focus = prospect.get("focus", "").lower()
        location = prospect.get("location", "").lower()
        
        stanford_indicators = ["stanford", "palo alto", "menlo park"]
        return any(indicator in name + focus + location for indicator in stanford_indicators)
        
    def _check_lyme_connection(self, prospect: Dict) -> bool:
        """Check for Lyme disease or tick-borne illness interest"""
        text = (
            prospect.get("name", "") + " " +
            prospect.get("focus", "") + " " +
            str(prospect.get("portfolio_companies", []))
        ).lower()
        
        lyme_indicators = ["lyme", "tick", "infectious disease", "vector-borne"]
        return any(indicator in text for indicator in lyme_indicators)
        
    def _check_geographic_connection(self, prospect: Dict) -> str:
        """Determine geographic connection strength"""
        location = prospect.get("location", "").lower()
        
        if any(city in location for city in ["san francisco", "bay area", "palo alto", "menlo park"]):
            return "Bay Area - same region"
        elif "california" in location:
            return "California - same state"
        elif any(city in location for city in ["boston", "cambridge"]):
            return "Boston - biotech hub"
        else:
            return ""
            
    def _identify_hooks(self, prospect: Dict, intelligence: Dict) -> List[str]:
        """Identify personalization hooks for email outreach"""
        hooks = []
        
        # Portfolio-based hooks
        portfolio_analysis = intelligence.get("portfolio_analysis", {})
        relevant_companies = portfolio_analysis.get("relevant_companies", [])
        
        if relevant_companies:
            for company in relevant_companies[:2]:  # Top 2 most relevant
                if isinstance(company, dict):
                    hooks.append(f"Portfolio: {company.get('name', 'Unknown')} - {company.get('relevance', '')}")
                    
        # Connection-based hooks
        connections = intelligence.get("connection_points", {})
        
        if connections.get("stanford"):
            hooks.append("Stanford connection - founder Dr. Jay Rajadas")
            
        if connections.get("lyme_community"):
            hooks.append("Lyme disease community interest")
            
        if connections.get("geographic"):
            hooks.append(f"Geographic: {connections['geographic']}")
            
        # Thesis-based hooks
        thesis = intelligence.get("investment_thesis", "")
        if "drug repurposing" in thesis.lower():
            hooks.append("Investment thesis: drug repurposing alignment")
        if "infectious disease" in thesis.lower():
            hooks.append("Investment thesis: infectious disease focus")
            
        return hooks
        
    def _parse_json_response(self, response: str) -> Dict:
        """Parse JSON from Claude response, handling markdown blocks"""
        response = response.strip()
        
        # Remove markdown code blocks if present
        if response.startswith("```json"):
            response = response[7:]
        elif response.startswith("```"):
            response = response[3:]
            
        if response.endswith("```"):
            response = response[:-3]
            
        response = response.strip()
        
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON parse error: {e}")
            return {}


if __name__ == "__main__":
    # Test the intelligence agent
    agent = IntelligenceAgent()
    
    test_prospect = {
        "name": "LifeSci Ventures",
        "type": "VC Fund",
        "focus": "Early-stage life science companies, focus on drug repurposing",
        "stage": "Seed to Series A",
        "location": "Menlo Park, CA",
        "portfolio_companies": ["Compound Therapeutics", "Infectious Disease Solutions"]
    }
    
    enhanced = agent.analyze_prospect(test_prospect)
    print(json.dumps(enhanced, indent=2))
