# ConViCure Fundraising System - Quick Start Guide

## 🎯 What This System Does

Helps ConViCure raise $6.5M by:
1. Finding qualified life science investors matching ConViCure's profile
2. Researching each investor deeply (portfolio, thesis, connections)
3. Generating personalized email drafts
4. Managing pipeline and follow-ups
5. **YOU review every email before it sends** - complete human control

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies

```bash
# Clone the repository
git clone <repository-url>
cd convicure-fundraising-system

# Install Python dependencies
pip install -r requirements.txt
```

### Step 2: Configure Credentials

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use any text editor
```

Fill in:
- **ANTHROPIC_API_KEY**: Get from https://console.anthropic.com/settings/keys
- **GMAIL_APP_PASSWORD**: Generate from https://myaccount.google.com/apppasswords

### Step 3: Configure System

```bash
# Copy configuration template
cp config/config.example.yaml config/config.yaml

# Edit config.yaml
nano config/config.yaml
```

Update:
- `email.from_address`: Your ConViCure email
- `email.daily_limit`: Max emails per day (default: 10)

### Step 4: Test the System

```bash
# Find 5 test prospects
python run.py research --count 5

# Analyze them
python run.py analyze

# Generate drafts
python run.py draft

# Review drafts (interactive)
python run.py review
```

## 📖 Daily Workflow

### Morning: Research & Draft

```bash
# Run the full pipeline (research → analyze → draft)
python run.py pipeline --count 10
```

This will:
1. Find 10 qualified investor prospects
2. Deep-research each one
3. Generate personalized email drafts
4. Save them for your review

**Time:** ~15-20 minutes (automated)

### Afternoon: Review & Send

```bash
# Review and approve drafts
python run.py review
```

Interactive review interface:
- Shows each draft with connection points
- You choose: **[A]pprove**, **[E]dit**, **[R]eject**, **[S]kip**
- Only approved emails are sent

**Time:** ~5-10 minutes (your review time)

### Check Progress

```bash
# View pipeline dashboard
python run.py dashboard
```

Shows:
- Prospects by stage
- Response rates
- Follow-ups due

## 🎨 Example Review Session

```
╔══════════════════════════════════════════════════════════════╗
║ DRAFT #1/5 - Review Required                                 ║
╚══════════════════════════════════════════════════════════════╝

Prospect: Sarah Chen, Partner @ LifeSci Ventures
Match Score: 92/100
Connection Points:
  • Portfolio: Compound Therapeutics - drug repurposing play
  • Stanford connection - founder Dr. Jay Rajadas
  • Investment thesis: infectious disease focus

──────────────────────────────────────────────────────────────
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

Best regards,
George Vincent
CEO, ConViCure, Inc.
george@convicure.com
──────────────────────────────────────────────────────────────

Actions: [A]pprove  [E]dit  [R]eject  [S]kip  [Q]uit
>
```

## 🚀 Advanced Usage

### Custom Research Queries

Edit `config/convicure_knowledge.yaml` to update:
- Investor criteria
- Search queries
- Email guidelines
- Prohibited content

### Follow-ups

The system automatically identifies prospects needing follow-up:

```bash
# View follow-ups due
python run.py dashboard
```

Follow-up timing:
- First follow-up: Day 5 (if no response)
- Second follow-up: Day 12 (if still no response)

### Pipeline Management

Track prospects through stages:
1. **Identified** - Found by research agent
2. **Researched** - Intelligence gathered
3. **Drafted** - Email created
4. **Sent** - Email delivered
5. **Responded** - Investor replied
6. **Meeting Scheduled** - Call booked
7. **Meeting Completed** - Call done
8. **Passed** - Not a fit
9. **Closed** - Investment secured

## ⚙️ Command Reference

```bash
# Research investors
python run.py research --count 10

# Analyze researched prospects
python run.py analyze

# Generate email drafts
python run.py draft

# Review and send
python run.py review

# View dashboard
python run.py dashboard

# Full pipeline (research + analyze + draft)
python run.py pipeline --count 10
```

## 🔒 Safety Features

### Daily Limits
- Maximum 10 emails per day (configurable)
- Prevents spam and protects sender reputation

### Human Review
- Every email requires your explicit approval
- Edit any draft before sending
- Reject drafts that don't feel right

### Content Filtering
Automatically enforces ConViCure guidelines:
- No specific drug molecule names
- No Stanford attribution claims  
- No TBI mentions
- No GJH INC references
- No spam language

### Warm-up Period
First 14 days: gradually increases volume to establish sender reputation

## 📊 Expected Results

**Per Day:**
- 10 prospects researched
- 5-10 emails sent (after your review)

**Per Week:**
- 50 prospects identified
- 25-50 personalized emails sent

**Per Month:**
- 200 prospects identified
- 100-200 quality outreach emails
- 10-20 investor meetings (5-10% response rate)
- 3-5 serious conversations

**To Close $6.5M:**
- Need ~5-10 investors
- Requires ~100-200 quality meetings
- This system helps you get those meetings

## 🆘 Troubleshooting

### "ANTHROPIC_API_KEY not found"
- Check `.env` file exists and has correct API key
- Make sure no spaces around the `=` sign

### "Gmail authentication failed"
- Use App Password, NOT your regular Gmail password
- Enable 2-Step Verification in Google Account first
- Generate new App Password if needed

### "No prospects found"
- Check search queries in `config/convicure_knowledge.yaml`
- Adjust `min_match_score` in `config/config.yaml` (lower = more results)

### "Drafts look generic"
- Run `python run.py analyze` again to enhance intelligence
- Check prospect data has portfolio companies listed
- Edit `config/convicure_knowledge.yaml` personalization hooks

## 📧 Support

For issues:
1. Check `data/analytics/system.log` for errors
2. Review `docs/TROUBLESHOOTING.md`
3. Contact technical support

---

**Remember:** This system is a tool to help you work efficiently. The quality of relationships you build with investors is what closes deals, not the quantity of emails. Use this system to be more thoughtful and personalized at scale, not to spam.
