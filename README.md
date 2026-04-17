# ConViCure Intelligent Fundraising System

**Reputation-First Investor Outreach for Biotech Fundraising**

## Overview

This multi-agent system assists ConViCure's $6.5M fundraising effort by researching qualified investors, generating personalized outreach emails, and managing the investor pipeline. Every email requires human review before sending.

**Design Principle:** Quality over quantity. 5-10 thoughtful, personalized emails per day beats 1000 generic spam messages.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    HUMAN OVERSIGHT LAYER                     │
│              (George reviews every email)                    │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────────────────────────────────────┐
│                   AGENT ORCHESTRATOR                         │
└─────────────────────────────────────────────────────────────┘
         │              │              │              │
    ┌────▼───┐    ┌────▼───┐    ┌────▼───┐    ┌────▼───┐
    │Research│    │Intel   │    │Personal│    │  CRM   │
    │Agent   │───▶│Agent   │───▶│-ization│───▶│Manager │
    └────────┘    └────────┘    │Engine  │    └────────┘
                                └────────┘
                                     │
                            ┌────────▼────────┐
                            │ Draft Queue     │
                            │ (Human Review)  │
                            └────────┬────────┘
                                     │
                            ┌────────▼────────┐
                            │ Gmail Sender    │
                            │ (Post-Approval) │
                            └─────────────────┘
```

## Agents

### 1. **Prospect Research Agent** (`agents/researcher.py`)
- Searches for investors matching ConViCure's profile
- Criteria: Life science focus, infectious disease interest, $1M-$10M check sizes
- Sources: Web search, PitchBook, Crunchbase, AngelList
- Output: 5-10 qualified prospects per day

### 2. **Intelligence Agent** (`agents/intelligence.py`)
- Deep research on each prospect
- Portfolio analysis, investment thesis, recent activity
- Identifies connection points (Lyme disease, Stanford, drug repurposing, etc.)
- Output: Detailed prospect profile

### 3. **Personalization Engine** (`agents/personalizer.py`)
- Generates custom email drafts using Claude API
- Incorporates: prospect's portfolio, thesis, recent investments, connection points
- Tone: Professional, warm, non-salesy
- Output: Personalized email draft + rationale

### 4. **CRM Manager** (`agents/crm.py`)
- Tracks investor pipeline stages
- Manages follow-up timing
- Stores conversation history
- Output: Pipeline status, next actions

### 5. **Review & Send Controller** (`agents/controller.py`)
- Presents drafts for human review
- Handles approval/edit/reject workflow
- Sends approved emails via Gmail API
- Logs all activity

## Setup Instructions

### Prerequisites
- Python 3.9+
- Gmail account with App Password enabled
- Anthropic API key (for Claude)
- Git installed

### Installation

```bash
# Clone repository
git clone <repo-url>
cd convicure-fundraising-system

# Install dependencies
pip install -r requirements.txt

# Configure credentials
cp config/config.example.yaml config/config.yaml
# Edit config.yaml with your API keys and email settings
```

### Configuration

Edit `config/config.yaml`:

```yaml
# ConViCure company profile
company:
  name: "ConViCure, Inc."
  stage: "Preclinical"
  raise_amount: "$6.5M"
  use_case: "IND clearance for four-drug Lyme disease combination therapy"
  
# Email settings
email:
  from_address: "george@convicure.com"
  from_name: "George Vincent"
  daily_limit: 10
  
# API credentials (use environment variables)
anthropic_api_key: "${ANTHROPIC_API_KEY}"
gmail_app_password: "${GMAIL_APP_PASSWORD}"
```

## Usage

### Daily Workflow

```bash
# Step 1: Research new prospects (runs automatically or on-demand)
python run.py research --count 10

# Step 2: Generate intelligence profiles
python run.py analyze

# Step 3: Create personalized drafts
python run.py draft

# Step 4: Review drafts (interactive)
python run.py review

# Step 5: Send approved emails
python run.py send
```

### Review Interface

```
╔══════════════════════════════════════════════════════════════╗
║ DRAFT #3/8 - Review Required                                 ║
╚══════════════════════════════════════════════════════════════╝

Prospect: Sarah Chen, Partner @ LifeSci Ventures
Match Score: 92/100
Connection Points:
  • Invested in 2 infectious disease companies (2024-2025)
  • Stanford-affiliated fund
  • Portfolio includes drug repurposing play (Compound Therapeutics)

───────────────────────────────────────────────────────────────
SUBJECT: Stanford research → Lyme disease breakthrough

Hi Sarah,

I noticed LifeSci Ventures' recent investment in Compound 
Therapeutics and your focus on drug repurposing strategies in 
infectious disease. We're doing something similar at ConViCure.

Our founder, Dr. Jay Rajadas (Stanford, 14,600+ citations), 
discovered that azlocillin eliminates even the drug-resistant 
persister forms of Borrelia. We're combining it with three other 
FDA-established drugs to create the first treatment for persistent 
Lyme disease—a condition affecting 100,000+ Americans annually 
with zero approved therapies.

We're raising $6.5M to reach IND clearance through the 505(b)(2) 
pathway. Given LifeSci's thesis on repurposed drugs and infectious 
disease focus, would you be open to a brief conversation?

Best,
George Vincent
CEO, ConViCure, Inc.
───────────────────────────────────────────────────────────────

Actions:
  [A]pprove  [E]dit  [R]eject  [S]kip  [Q]uit
>
```

## Safety Features

✅ **Rate Limiting**: Maximum 10 emails per day (configurable)  
✅ **Human Review**: Every email requires explicit approval  
✅ **Domain Protection**: Validates sender domain health before sending  
✅ **Spam Prevention**: Checks against common spam triggers  
✅ **Blacklist Management**: Tracks unsubscribes and bounces  
✅ **Warm-up Mode**: Gradually increases volume over 2 weeks  

## Data Storage

All data stored locally in `data/` directory:
- `prospects.json` - Investor database
- `pipeline.json` - CRM tracking
- `drafts/` - Email drafts pending review
- `sent/` - Sent email log
- `analytics.json` - Campaign metrics

**No external databases required.**

## ConViCure-Specific Features

### Investor Qualification Criteria
1. **Investment Focus**: Life science, infectious disease, or drug repurposing
2. **Stage Fit**: Seed/Series A in preclinical-to-Phase 1 biotech
3. **Check Size**: $500K - $5M
4. **Geographic**: US-based or investing in US companies
5. **Portfolio Signals**: Stanford affiliations, Lyme disease interest, combination therapies

### Warm Introduction Detection
System identifies mutual connections:
- Stanford network (Jay's affiliations)
- Bay Area Lyme Foundation contacts
- SheppardMullin law firm network
- Existing ConViCure relationships

### Prohibited Practices
- ❌ No mass BCC emails
- ❌ No generic "Dear Investor" templates
- ❌ No misleading subject lines
- ❌ No false urgency tactics
- ❌ No sending without explicit approval

## Monitoring & Analytics

Track key metrics:
- Prospects researched vs. qualified
- Email open rates (if tracking enabled)
- Response rates
- Meeting conversion
- Pipeline velocity

```bash
# View dashboard
python run.py dashboard
```

## Troubleshooting

See `docs/TROUBLESHOOTING.md` for common issues:
- Gmail authentication errors
- API rate limits
- Email deliverability problems
- Agent failures

## License

Proprietary - ConViCure, Inc. Internal Use Only

## Support

For issues or questions:
- Technical: Review `docs/` directory
- Strategic: Consult fundraising strategy document
- Legal: Contact SheppardMullin before bulk outreach

---

**Remember:** This system assists fundraising—it doesn't replace relationship-building, warm introductions, and strategic partnerships that close deals.
