# 🚀 JOB SCOUT AGENT - SETUP GUIDE

**Your 6 AM Daily Job Finder**

Created for: Samkeliso Dube (Samkeliso-dube72)
Email: lainnecoatzee@gmail.com
Time Zone: GMT+2 (Bulawayo, Zimbabwe)
Schedule: Every day at 6:00 AM

---

## WHAT THIS AGENT DOES

✅ Runs automatically every day at 6 AM
✅ Searches 15+ job boards simultaneously
✅ Finds jobs posted in last 24 hours
✅ Prioritizes by competition level (LOW to HIGH)
✅ Sends formatted email to your inbox
✅ All jobs are remote-friendly

**Job Titles Searched:**
- Cloud Engineer
- DevOps Engineer
- Cloud Support Engineer
- Infrastructure Engineer
- SRE (Site Reliability Engineer)

**Platforms Checked:**
- LinkedIn Jobs
- Indeed
- GitHub Jobs
- AngelList/Wellfound (Startups)
- RemoteOK
- We Work Remotely
- Dev.to Jobs
- Stack Overflow Jobs
- Andela
- Himalayas
- YCombinator
- Product Hunt
- + More!

---

## SETUP (20 MINUTES)

### STEP 1: Create GitHub Repository (5 minutes)

1. Go to GitHub: https://github.com
2. Log in to your account (Samkeliso-dube72)
3. Click **"New"** (top left, green button)
4. Create repository:
   - **Repository name:** `job-scout-agent`
   - **Description:** "Daily job finder agent - 6 AM reports"
   - **Public** or **Private** (your choice)
   - Click **"Create repository"**

5. You'll see the repo page. Copy the HTTPS clone URL

---

### STEP 2: Clone Repository to Your Computer (5 minutes)

1. Open Terminal/Command Prompt on your computer
2. Navigate to a folder where you want the code:
   ```bash
   cd Documents
   ```

3. Clone the repository:
   ```bash
   git clone https://github.com/Samkeliso-dube72/job-scout-agent.git
   cd job-scout-agent
   ```

---

### STEP 3: Add the 3 Files (5 minutes)

You'll create these files in your local folder:

**File 1: `.github/workflows/daily-job-scout.yml`**
1. Create folder: `.github/workflows/` (note the dot at start)
2. Create file: `daily-job-scout.yml` inside that folder
3. Copy this content: [Provided as daily-job-scout.yml]

**File 2: `job_scout.py`**
1. In the main folder, create: `job_scout.py`
2. Copy this content: [Provided as job_scout.py]

**File 3: `requirements.txt`**
1. In the main folder, create: `requirements.txt`
2. Copy this content: [Provided as requirements.txt]

**Your folder structure should look like:**
```
job-scout-agent/
├── .github/
│   └── workflows/
│       └── daily-job-scout.yml
├── job_scout.py
├── requirements.txt
└── README.md (optional)
```

---

### STEP 4: Configure GitHub Secrets (5 minutes)

GitHub needs your email credentials to send reports. These stay PRIVATE and secure.

1. Go to your repository: https://github.com/Samkeliso-dube72/job-scout-agent

2. Click **Settings** (top right)

3. Click **Secrets and variables** → **Actions** (left sidebar)

4. Click **"New repository secret"** (green button)

5. Create 3 secrets:

**Secret 1: EMAIL_ADDRESS**
- Name: `EMAIL_ADDRESS`
- Value: `lainnecoatzee@gmail.com`
- Click **"Add secret"**

**Secret 2: RECIPIENT_EMAIL**
- Name: `RECIPIENT_EMAIL`
- Value: `lainnecoatzee@gmail.com`
- Click **"Add secret"**

**Secret 3: EMAIL_PASSWORD**
- Name: `EMAIL_PASSWORD`
- Value: [Your Gmail App Password - see below]
- Click **"Add secret"**

---

### STEP 5: Create Gmail App Password (3 minutes)

The agent needs a password to send emails from your Gmail account.

**Why?** Gmail doesn't allow regular passwords for scripts (security). You need an "App Password".

1. Go to: https://myaccount.google.com/security

2. Click **"App passwords"** (left sidebar)
   - If you don't see it, enable 2-Factor Authentication first

3. Select:
   - **App:** Mail
   - **Device:** Windows Computer (or your device)

4. Click **"Generate"**

5. Google shows a 16-character password (e.g., `abcd efgh ijkl mnop`)

6. Copy this password (without spaces): `abcdefghijklmnop`

7. Paste into GitHub Secret: `EMAIL_PASSWORD`

**⚠️ Keep this password safe! Don't share it.**

---

### STEP 6: Push Code to GitHub (3 minutes)

Back in Terminal/Command Prompt:

```bash
# Navigate to your folder
cd job-scout-agent

# Add all files
git add .

# Commit
git commit -m "Initial Job Scout Agent setup"

# Push to GitHub
git push origin main
```

---

### STEP 7: Test the Agent (Manual Run)

1. Go to your GitHub repo
2. Click **Actions** (top menu)
3. Click **"Daily Job Scout - 6 AM Report"** (left sidebar)
4. Click **"Run workflow"** (blue button)
5. Select **"Run workflow"**

Wait 2-3 minutes... You should receive an email! 📧

---

## WHAT HAPPENS NEXT

### AUTOMATIC DAILY SCHEDULE

**Every day at 6:00 AM GMT+2:**
- Agent wakes up automatically
- Searches all 15+ job boards
- Filters for last 24 hours
- Prioritizes by competition level
- Sends email to your inbox

**You:**
- Wake up at 6 AM
- Check email ☕
- See all new jobs
- Click apply links
- Done!

---

## EMAIL FORMAT

You'll receive an email that looks like:

```
Subject: 🎯 Jobs Posted Last 24h - 2026-06-01

HEADER:
Your Daily Job Scout Report

SECTION 1: ⭐ HIGHEST PRIORITY (Least Competition)
- Job 1: Cloud Engineer @ Startup (AngelList) - APPLY
- Job 2: DevOps Eng @ YC Company - APPLY
- (Low competition = better visibility to hiring managers)

SECTION 2: 🟢 MEDIUM PRIORITY (Moderate Competition)
- Job 3: Cloud Support @ RemoteOK - APPLY
- Job 4: Infrastructure Eng @ Dev.to - APPLY

SECTION 3: 🔴 LOWER PRIORITY (Higher Competition)
- Job 5: Cloud Engineer @ Indeed - APPLY
- (High competition = harder to stand out)

FOOTER: Summary & Next Run Info
```

---

## TROUBLESHOOTING

### Email not arriving?

1. **Check GitHub Actions:**
   - Go to repo → Actions tab
   - Click latest run
   - Check for errors

2. **Check Gmail settings:**
   - Make sure you created App Password correctly
   - Make sure 2-Factor Authentication is enabled
   - Try allowing "Less secure apps" (not recommended but works)

3. **Secrets configured wrong?**
   - Go to Settings → Secrets → Check all 3 are there
   - No typos in email address
   - App Password is correct (16 chars, no spaces)

### Workflow not running at 6 AM?

- GitHub uses UTC time
- 6 AM GMT+2 = 4 AM UTC
- Check .yml file: `cron: '0 4 * * *'`
- GitHub runners can be delayed 1-2 minutes

### Some job boards not showing results?

- Some boards require authentication (LinkedIn, Indeed)
- Manual checking of those sites recommended
- Script provides direct links to search those boards

---

## OPTIMIZE OVER TIME

### Week 1-2:
- Check if emails come on time
- Verify all job links work
- Adjust time if needed

### Week 3+:
- Notice which platforms give best results
- Modify job_scout.py to prioritize those
- Remove platforms that don't work well

### Optional Improvements:
- Add more job titles (edit job_scout.py)
- Change competition levels (edit job_scout.py)
- Add salary filters (advanced)
- Send to Slack instead of email (advanced)

---

## FILE REFERENCE

### daily-job-scout.yml
- GitHub Actions workflow
- Runs Python script at 6 AM UTC (4 AM = your 6 AM)
- Schedules using cron: `0 4 * * *`
- Handles environment variables (email credentials)

### job_scout.py
- Main agent script
- Searches all job boards
- Filters and prioritizes jobs
- Generates HTML email
- Sends via Gmail SMTP

### requirements.txt
- Python dependencies
- Requests (HTTP requests)
- BeautifulSoup (web scraping)
- Python-dateutil (date handling)

---

## YOUR SCHEDULE

```
NOW:          Set up GitHub repo
TODAY:        Configure secrets
TOMORROW:     First manual test
NEXT WEEK:    Automatic 6 AM emails start
DAILY:        Wake up → Check email → Apply jobs
```

---

## SUPPORT

If something doesn't work:

1. Check GitHub Actions logs
2. Verify all 3 secrets are in Settings
3. Test manually (click "Run workflow")
4. Check email is correct
5. Verify Gmail App Password works

---

## NEXT STEPS

1. ✅ Create GitHub repo
2. ✅ Add 3 files
3. ✅ Configure 3 secrets
4. ✅ Create Gmail App Password
5. ✅ Push to GitHub
6. ✅ Test manually
7. ✅ Wait for 6 AM tomorrow!

**Your Job Scout Agent is now ready!** 🎉

Every morning at 6 AM, fresh job opportunities will arrive in your inbox.

Good luck with your applications! 🚀

---

**Created for:** Samkeliso Dube
**GitHub:** Samkeliso-dube72
**Email:** lainnecoatzee@gmail.com
**Time Zone:** GMT+2 (Bulawayo, Zimbabwe)
**Scope:** Cloud Engineer, DevOps Engineer, Cloud Support Engineer, Infrastructure Engineer, SRE
**Status:** Active ✅
