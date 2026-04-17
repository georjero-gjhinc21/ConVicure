"""
Prospect Research Agent
Finds and qualifies investors matching ConViCure's profile
"""

import json
from typing import List, Dict
from agents.base_agent import BaseAgent


class ProspectResearcher(BaseAgent):
    """Agent responsible for finding and qualifying investor prospects"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        super().__init__(config_path)
        self.prospects_db_path = self.config.get("paths", {}).get(
            "prospects_db", "data/prospects/prospects.json"
        )
        
    def research_prospects(self, count: int = 10) -> List[Dict]:
        """
        Research new investor prospects
        
        Args:
            count: Number of prospects to find
            
        Returns:
            List of qualified prospect dictionaries
        """
        self.logger.info(f"Starting prospect research (target: {count} prospects)")
        
        # Load existing prospects to avoid duplicates
        existing = self._load_existing_prospects()
        existing_names = {p.get("name", "").lower() for p in existing}
        
        # Generate search queries based on ConViCure criteria
        search_queries = self._generate_search_queries()
        
        prospects = []
        for query in search_queries:
            if len(prospects) >= count:
                break
                
            self.logger.info(f"Searching: {query}")
            results = self._search_investors(query)
            
            for result in results:
                if len(prospects) >= count:
                    break
                    
                # Skip duplicates
                if result.get("name", "").lower() in existing_names:
                    continue
                    
                # Qualify the prospect
                qualified = self._qualify_prospect(result)
                if qualified:
                    prospects.append(qualified)
                    existing_names.add(qualified["name"].lower())
                    
        self.logger.info(f"Research complete: {len(prospects)} qualified prospects found")
        
        # Save new prospects
        self._save_prospects(prospects)
        
        # Log activity
        self.log_activity("prospect_research", {
            "count_targeted": count,
            "count_found": len(prospects),
            "queries_used": len(search_queries)
        })
        
        return prospects
        
    def _generate_search_queries(self) -> List[str]:
        """Generate search queries based on investor criteria"""
        queries = [
            "life science venture capital infectious disease",
            "biotech seed investors drug repurposing",
            "lyme disease therapeutics investors",
            "stanford affiliated venture capital life science",
            "infectious disease early stage investors",
            "orphan disease venture capital",
            "antibiotic resistance startup investors",
            "preclinical biotech investors bay area",
            "combination therapy drug development investors",
            "rare disease venture capital seed stage"
        ]
        return queries
        
    def _search_investors(self, query: str) -> List[Dict]:
        """
        Search for investors using Claude + web search
        
        Args:
            query: Search query string
            
        Returns:
            List of potential investor matches
        """
        system_prompt = """You are an expert at identifying venture capital investors 
        and angel investors in the life science and biotech space. Given a search query, 
        identify specific investors, funds, or individuals who match the criteria.
        
        Return your response as valid JSON array of objects with these fields:
        - name: Investor or fund name
        - type: "VC Fund" or "Angel Investor"
        - focus: Brief description of investment focus
        - stage: Preferred stage (Seed, Series A, etc.)
        - location: Geographic location
        - portfolio_companies: List of 1-3 relevant portfolio companies
        - linkedin: LinkedIn URL if known
        - website: Website URL if known
        
        Only return JSON, no other text."""
        
        prompt = f"""Find investors matching this search query: "{query}"
        
        Focus on:
        - Life science / biotech investors
        - Infectious disease or drug development focus
        - Seed to Series A stage
        - US-based or US-investing
        - Active in last 2 years
        
        Return 3-5 high-quality matches as JSON array."""
        
        try:
            response = self.call_claude(prompt, system_prompt=system_prompt)
            
            # Parse JSON response
            # Claude might wrap in ```json blocks, so clean it
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            investors = json.loads(response)
            return investors if isinstance(investors, list) else []
            
        except Exception as e:
            self.logger.error(f"Search error for query '{query}': {e}")
            return []
            
    def _qualify_prospect(self, prospect: Dict) -> Dict:
        """
        Qualify a prospect against ConViCure criteria
        
        Args:
            prospect: Raw prospect data
            
        Returns:
            Qualified prospect dict with match score, or None if disqualified
        """
        criteria = self.knowledge.get("investor_criteria", {})
        
        # Build qualification prompt
        system_prompt = """You are an expert at qualifying investor prospects for 
        biotech fundraising. Analyze if an investor is a good fit for a company based 
        on their profile and the company's needs.
        
        Return valid JSON with these fields:
        - qualified: boolean (true if good fit)
        - match_score: integer 0-100
        - fit_reasons: list of reasons why they're a fit
        - concerns: list of potential concerns
        - recommended_approach: suggested outreach strategy
        """
        
        prompt = f"""Qualify this investor prospect for ConViCure:
        
        PROSPECT:
        {json.dumps(prospect, indent=2)}
        
        CONVICURE PROFILE:
        - Stage: Preclinical biotech
        - Raising: $6.5M for IND clearance
        - Focus: Four-drug combination therapy for persistent Lyme disease
        - Approach: Drug repurposing via 505(b)(2) pathway
        - Founder: Stanford-affiliated, 14,600+ citations
        - Market: Infectious disease with zero approved treatments
        
        IDEAL INVESTOR CRITERIA:
        {json.dumps(criteria, indent=2)}
        
        Assess the fit and return qualification decision as JSON."""
        
        try:
            response = self.call_claude(prompt, system_prompt=system_prompt)
            
            # Clean and parse JSON
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            qualification = json.loads(response)
            
            # Check qualification threshold
            min_score = self.config.get("research", {}).get("min_match_score", 70)
            
            if qualification.get("qualified") and qualification.get("match_score", 0) >= min_score:
                # Merge qualification data with prospect data
                qualified_prospect = {
                    **prospect,
                    "match_score": qualification["match_score"],
                    "fit_reasons": qualification.get("fit_reasons", []),
                    "concerns": qualification.get("concerns", []),
                    "recommended_approach": qualification.get("recommended_approach", ""),
                    "status": "Identified",
                    "added_date": self.get_timestamp(),
                    "source": "research_agent"
                }
                
                self.logger.info(
                    f"✓ Qualified: {prospect.get('name')} (score: {qualification['match_score']})"
                )
                return qualified_prospect
            else:
                self.logger.debug(
                    f"✗ Disqualified: {prospect.get('name')} (score: {qualification.get('match_score', 0)})"
                )
                return None
                
        except Exception as e:
            self.logger.error(f"Qualification error for {prospect.get('name')}: {e}")
            return None
            
    def _load_existing_prospects(self) -> List[Dict]:
        """Load existing prospects from database"""
        existing = self.load_json(self.prospects_db_path)
        return existing if existing else []
        
    def _save_prospects(self, new_prospects: List[Dict]):
        """Save new prospects to database"""
        existing = self._load_existing_prospects()
        combined = existing + new_prospects
        self.save_json(combined, self.prospects_db_path)
        self.logger.info(f"Saved {len(new_prospects)} new prospects (total: {len(combined)})")


if __name__ == "__main__":
    # Test the researcher
    researcher = ProspectResearcher()
    prospects = researcher.research_prospects(count=5)
    
    print(f"\n✓ Found {len(prospects)} qualified prospects:")
    for p in prospects:
        print(f"  - {p['name']} (Score: {p['match_score']})")
