# Resend Email Setup Guide for ConViCure

This guide explains how to configure the ConViCure fundraising system to send emails via **info@convicure.com** using Resend + Cloudflare.

---

## Overview

**Your Email Architecture:**
- **Email Address:** info@convicure.com
- **Send/Receive:** Configured through Resend API
- **DNS Management:** Cloudflare
- **Domain:** convicure.com

**Why Resend?**
- ✅ Built for transactional emails (better than Gmail for automation)
- ✅ Professional sender reputation
- ✅ Better deliverability and tracking
- ✅ No App Password complexity
- ✅ Detailed analytics dashboard

---

## Prerequisites

Your domain **convicure.com** should already be:
1. Configured in Resend
2. DNS records set up in Cloudflare
3. Email routing enabled

If not yet configured, see **"Initial Domain Setup"** below.

---

## Quick Setup (5 Minutes)

### Step 1: Get Your Resend API Key

1. **Log into Resend**
   - Go to: https://resend.com/login
   - Use your Resend account credentials

2. **Navigate to API Keys**
   - Click on **"API Keys"** in the left sidebar
   - Or go directly to: https://resend.com/api-keys

3. **Create New API Key**
   - Click **"Create API Key"**
   - Name: `ConViCure Fundraising System`
   - Permissions: **Full Access** (or minimum: Send Emails)
   - Click **"Create"**

4. **Copy the API Key**
   - Copy the key that starts with `re_...`
   - **Important:** You can only see this once!
   - Store it securely

### Step 2: Configure the System

1. **Create .env file**
   ```bash
   cd convicure-fundraising-system
   cp .env.example .env
   nano .env  # or use any text editor
   ```

2. **Add your API keys**
   ```bash
   # Anthropic API Key
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   
   # Resend API Key (paste the key you just copied)
   RESEND_API_KEY=re_your_resend_key_here
   
   # Email Configuration
   FROM_EMAIL=info@convicure.com
   FROM_NAME=George Vincent
   ```

3. **Save and close**

### Step 3: Verify Domain Configuration

Run the verification script:

```bash
cd convicure-fundraising-system
python -c "from agents.resend_emailer import ResendEmailer; e = ResendEmailer(); print(e.verify_domain())"
```

**Expected output:**
```
{
  'verified': True,
  'status': 'verified',
  'domain': 'convicure.com'
}
```

If you see `'verified': True`, you're good to go!

If you see `'verified': False`, proceed to **"Domain Verification"** section below.

### Step 4: Test Email Sending

Send a test email to yourself:

```bash
python agents/resend_emailer.py
```

Edit the file first to uncomment the test email section and add your test email address.

---

## Domain Verification (If Needed)

If `verify_domain()` returned `False`, your domain needs to be verified in Resend.

### Check DNS Records in Cloudflare

Your **convicure.com** domain needs these DNS records (should already be configured):

1. **SPF Record** (TXT)
   - Name: `@` or `convicure.com`
   - Value: `v=spf1 include:_spf.resend.com ~all`

2. **DKIM Record** (TXT)
   - Name: `resend._domainkey` (provided by Resend)
   - Value: DKIM public key (provided by Resend)

3. **DMARC Record** (TXT)
   - Name: `_dmarc`
   - Value: `v=DMARC1; p=none; rua=mailto:info@convicure.com`

### To Verify in Resend:

1. Go to https://resend.com/domains
2. Find `convicure.com`
3. Check verification status
4. If not verified, click **"Verify Domain"**
5. Follow instructions to add/update DNS records in Cloudflare

**DNS Propagation:** Can take 24-48 hours, but usually within minutes.

---

## Initial Domain Setup (If Starting Fresh)

If **convicure.com** is not yet in Resend:

### 1. Add Domain to Resend

1. Go to https://resend.com/domains
2. Click **"Add Domain"**
3. Enter: `convicure.com`
4. Click **"Add Domain"**

### 2. Configure DNS Records in Cloudflare

Resend will provide you with DNS records to add. In Cloudflare:

1. Go to https://dash.cloudflare.com
2. Select **convicure.com** domain
3. Navigate to **DNS** → **Records**
4. Add each record provided by Resend:
   - SPF (TXT record)
   - DKIM (TXT record)
   - DMARC (TXT record - optional but recommended)

### 3. Verify Domain

After adding DNS records:
1. Return to Resend
2. Click **"Verify Domain"**
3. Wait for verification (can take a few minutes)

### 4. Configure Email Routing (Optional)

To receive emails at info@convicure.com:

**In Cloudflare:**
1. Go to **Email** → **Email Routing**
2. Enable Email Routing
3. Add destination address (where you want emails forwarded)
4. Set up routing rule: `info@convicure.com` → your personal email

**In Resend:**
- No additional configuration needed - Resend handles sending only

---

## Email Sending Configuration

### System Configuration

The system is configured to send from **info@convicure.com** by default.

**In `config/config.yaml`:**
```yaml
email:
  from_address: "info@convicure.com"
  from_name: "George Vincent"
  daily_limit: 10
  hourly_limit: 3
```

### Email Signature

Default signature in all emails:
```
Best regards,
George Vincent
CEO, ConViCure, Inc.
info@convicure.com
```

To customize, edit `config/config.yaml`:
```yaml
email:
  signature: |
    Best regards,
    George Vincent
    CEO, ConViCure, Inc.
    info@convicure.com
    (650) 456-1744  # Optional phone number
```

---

## Monitoring & Deliverability

### Resend Dashboard

Monitor your emails at: https://resend.com/emails

**Metrics available:**
- Emails sent
- Delivery rate
- Bounce rate
- Open rate (if tracking enabled)
- Click rate (if tracking enabled)

### Best Practices for Deliverability

**1. Warm Up Your Domain**
- Start with 5-10 emails/day
- Gradually increase over 2 weeks
- System has built-in warmup period (14 days)

**2. Monitor Bounce Rates**
- Keep bounces < 5%
- Remove bounced emails from prospect list
- System tracks this automatically

**3. Check Spam Complaints**
- Keep complaints < 0.1%
- Include clear sender identification
- Add unsubscribe option (recommended for scale)

**4. Maintain Sender Reputation**
- Resend dashboard shows reputation score
- Aim for score > 80
- High engagement = better deliverability

---

## Troubleshooting

### "RESEND_API_KEY not found"
**Solution:**
- Check `.env` file exists in project root
- Verify `RESEND_API_KEY=re_...` line is present
- Ensure no spaces around `=` sign
- Restart terminal/IDE after editing `.env`

### "Domain not verified"
**Solution:**
- Check DNS records in Cloudflare dashboard
- Wait 24-48 hours for DNS propagation
- Run `dig TXT convicure.com` to check SPF record
- Contact Resend support if still failing

### "Email send failed: Invalid API key"
**Solution:**
- API key must start with `re_`
- Generate new key at https://resend.com/api-keys
- Copy entire key including `re_` prefix
- Update `.env` file with new key

### "Recipient email invalid"
**Solution:**
- Check prospect's email address format
- Remove any spaces or special characters
- Verify email exists (use email validation tool)

### "Rate limit exceeded"
**Solution:**
- Resend has rate limits (check your plan)
- System enforces daily limit (default: 10)
- Increase daily limit in `config/config.yaml` if needed
- Upgrade Resend plan for higher limits

### "Emails going to spam"
**Solution:**
- Verify SPF, DKIM, DMARC records
- Warm up domain gradually
- Improve email content (less spam trigger words)
- Check sender reputation in Resend dashboard
- Add physical address to signature (CAN-SPAM)

---

## Resend vs Gmail Comparison

| Feature | Resend (Your Setup) | Gmail (Alternative) |
|---------|-------------------|-------------------|
| Professional sender | ✅ info@convicure.com | ❌ Personal Gmail |
| API-first design | ✅ Built for automation | ⚠️ OAuth complexity |
| Deliverability | ✅ Excellent | ⚠️ Personal limits |
| Analytics | ✅ Detailed dashboard | ❌ Limited |
| Rate limits | ✅ Scalable | ❌ Strict (500/day) |
| Setup complexity | ✅ Simple API key | ⚠️ App Password + OAuth |
| Cost | ✅ Free tier generous | ✅ Free |
| Sender reputation | ✅ Dedicated IP option | ⚠️ Shared pool |

**Verdict:** Resend is the right choice for ConViCure's fundraising system.

---

## Advanced Configuration

### Custom Reply-To Address

If you want replies to go somewhere other than info@convicure.com:

**Edit `agents/resend_emailer.py`:**
```python
email_data = {
    "from": f"{from_name} <{from_email}>",
    "to": [to_email],
    "subject": subject,
    "text": body,
    "reply_to": "george@convicure.com"  # Custom reply-to
}
```

### Email Tracking

To enable open/click tracking:

**In Resend Dashboard:**
1. Go to https://resend.com/settings
2. Enable **"Track Opens"** and **"Track Clicks"**

**In System Config:**
```yaml
analytics:
  track_opens: true
  track_clicks: true
```

### HTML Emails (Optional)

System currently sends plain text emails (better for fundraising). To add HTML:

**Edit `agents/resend_emailer.py`:**
```python
email_data = {
    "from": f"{from_name} <{from_email}>",
    "to": [to_email],
    "subject": subject,
    "text": body,  # Plain text version
    "html": f"<html><body>{body}</body></html>"  # HTML version
}
```

---

## Support

### Resend Support
- Docs: https://resend.com/docs
- Support: support@resend.com
- Status: https://status.resend.com

### Cloudflare Support
- Docs: https://developers.cloudflare.com/email-routing/
- Community: https://community.cloudflare.com

### System Issues
- Check logs: `data/analytics/system.log`
- Review code: `agents/resend_emailer.py`
- Test script: `python agents/resend_emailer.py`

---

## Security Best Practices

**1. Protect Your API Key**
- Never commit `.env` to Git (already in `.gitignore`)
- Don't share API key in emails or Slack
- Rotate keys quarterly
- Use separate keys for dev/production

**2. Monitor Usage**
- Check Resend dashboard weekly
- Review sent emails for anomalies
- Alert on high bounce rates
- Track reputation score

**3. Secure Access**
- Enable 2FA on Resend account
- Restrict API key permissions
- Use read-only keys for monitoring scripts
- Revoke unused keys

---

## Quick Reference

```bash
# Verify domain configuration
python -c "from agents.resend_emailer import ResendEmailer; print(ResendEmailer().verify_domain())"

# Test email send (edit file first)
python agents/resend_emailer.py

# Check sent emails
# Visit: https://resend.com/emails

# View API keys
# Visit: https://resend.com/api-keys

# Check domain status
# Visit: https://resend.com/domains
```

---

**You're all set!** The system is now configured to send professional fundraising emails from **info@convicure.com** via Resend.
