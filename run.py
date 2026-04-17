#!/usr/bin/env python3
"""
ConViCure Fundraising System - Main Orchestrator
Coordinates all agents for intelligent investor outreach
"""

import sys
import argparse
from rich.console import Console
from rich.table import Table

from agents.researcher import ProspectResearcher
from agents.intelligence import IntelligenceAgent
from agents.personalizer import PersonalizationEngine
from agents.crm import CRMManager
from agents.controller import ReviewController


console = Console()


class FundraisingOrchestrator:
    """Main orchestrator for the fundraising system"""
    
    def __init__(self):
        self.researcher = ProspectResearcher()
        self.intelligence = IntelligenceAgent()
        self.personalizer = PersonalizationEngine()
        self.crm = CRMManager()
        self.controller = ReviewController()
        
    def run_research(self, count: int = 10):
        """Run prospect research"""
        console.print(f"\n[bold blue]🔍 Researching {count} investor prospects...[/bold blue]\n")
        
        try:
            prospects = self.researcher.research_prospects(count=count)
            
            if prospects:
                console.print(f"[green]✓ Found {len(prospects)} qualified prospects[/green]\n")
                
                # Display results
                table = Table(title="Qualified Prospects")
                table.add_column("Name", style="cyan")
                table.add_column("Type", style="magenta")
                table.add_column("Match Score", style="green")
                table.add_column("Focus", style="yellow")
                
                for p in prospects:
                    table.add_row(
                        p.get("name", ""),
                        p.get("type", ""),
                        str(p.get("match_score", 0)),
                        p.get("focus", "")[:50] + "..." if len(p.get("focus", "")) > 50 else p.get("focus", "")
                    )
                    
                console.print(table)
            else:
                console.print("[yellow]No qualified prospects found[/yellow]\n")
                
        except Exception as e:
            console.print(f"[red]✗ Research error: {e}[/red]\n")
            
    def run_analysis(self):
        """Run intelligence analysis on researched prospects"""
        console.print("\n[bold blue]🔬 Analyzing prospects...[/bold blue]\n")
        
        try:
            # Get prospects that need analysis
            prospects_data = self.researcher.load_json(
                self.researcher.prospects_db_path
            ) or []
            
            to_analyze = [
                p for p in prospects_data
                if p.get("status") == "Identified"
            ]
            
            if not to_analyze:
                console.print("[yellow]No prospects need analysis[/yellow]\n")
                return
                
            console.print(f"Analyzing {len(to_analyze)} prospects...\n")
            
            for prospect in to_analyze:
                console.print(f"  → {prospect.get('name')}")
                enhanced = self.intelligence.analyze_prospect(prospect)
                
                # Update in database
                for i, p in enumerate(prospects_data):
                    if p.get("name") == prospect.get("name"):
                        prospects_data[i] = enhanced
                        break
                        
            # Save updated prospects
            self.researcher.save_json(prospects_data, self.researcher.prospects_db_path)
            
            console.print(f"\n[green]✓ Analysis complete for {len(to_analyze)} prospects[/green]\n")
            
        except Exception as e:
            console.print(f"[red]✗ Analysis error: {e}[/red]\n")
            
    def run_drafting(self):
        """Generate email drafts for analyzed prospects"""
        console.print("\n[bold blue]✍️  Drafting personalized emails...[/bold blue]\n")
        
        try:
            # Get prospects ready for drafting
            prospects_data = self.researcher.load_json(
                self.researcher.prospects_db_path
            ) or []
            
            to_draft = [
                p for p in prospects_data
                if p.get("status") == "Researched"
            ]
            
            if not to_draft:
                console.print("[yellow]No prospects ready for drafting[/yellow]\n")
                return
                
            console.print(f"Creating drafts for {len(to_draft)} prospects...\n")
            
            for prospect in to_draft:
                console.print(f"  → {prospect.get('name')}")
                draft = self.personalizer.create_draft(prospect)
                
                # Update prospect status
                for i, p in enumerate(prospects_data):
                    if p.get("name") == prospect.get("name"):
                        prospects_data[i]["status"] = "Drafted"
                        break
                        
            # Save updated prospects
            self.researcher.save_json(prospects_data, self.researcher.prospects_db_path)
            
            console.print(f"\n[green]✓ Created {len(to_draft)} email drafts[/green]\n")
            console.print("[cyan]Next step: Run 'python run.py review' to review and approve[/cyan]\n")
            
        except Exception as e:
            console.print(f"[red]✗ Drafting error: {e}[/red]\n")
            
    def run_review(self):
        """Run interactive draft review"""
        console.print("\n[bold blue]📋 Starting draft review...[/bold blue]\n")
        
        try:
            self.controller.review_drafts_interactive()
        except Exception as e:
            console.print(f"[red]✗ Review error: {e}[/red]\n")
            
    def run_dashboard(self):
        """Display pipeline dashboard"""
        console.print("\n[bold blue]📊 Pipeline Dashboard[/bold blue]\n")
        
        try:
            dashboard = self.crm.generate_dashboard()
            console.print(dashboard)
        except Exception as e:
            console.print(f"[red]✗ Dashboard error: {e}[/red]\n")
            
    def run_full_pipeline(self, count: int = 5):
        """Run the complete pipeline: research → analyze → draft"""
        console.print("\n[bold blue]🚀 Running full pipeline...[/bold blue]\n")
        
        self.run_research(count=count)
        self.run_analysis()
        self.run_drafting()
        
        console.print("\n[green]✓ Pipeline complete. Ready for review.[/green]\n")
        console.print("[cyan]Run 'python run.py review' to approve emails[/cyan]\n")


def main():
    parser = argparse.ArgumentParser(
        description="ConViCure Intelligent Fundraising System"
    )
    
    parser.add_argument(
        "command",
        choices=["research", "analyze", "draft", "review", "dashboard", "pipeline"],
        help="Command to run"
    )
    
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of prospects to research (default: 10)"
    )
    
    args = parser.parse_args()
    
    orchestrator = FundraisingOrchestrator()
    
    if args.command == "research":
        orchestrator.run_research(count=args.count)
    elif args.command == "analyze":
        orchestrator.run_analysis()
    elif args.command == "draft":
        orchestrator.run_drafting()
    elif args.command == "review":
        orchestrator.run_review()
    elif args.command == "dashboard":
        orchestrator.run_dashboard()
    elif args.command == "pipeline":
        orchestrator.run_full_pipeline(count=args.count)


if __name__ == "__main__":
    main()
