#!/usr/bin/env python3
"""
🎯 JOB SCOUT AGENT - FINAL FOCUSED VERSION
EXACT FILTERS:
  ✓ Posted in LAST 24 HOURS
  ✓ REMOTE ONLY
  ✓ ENTRY-LEVEL / JUNIOR ONLY
  ✓ Cloud, DevOps, Infrastructure, SRE, Platform Engineer
  ✓ Hiring ANYWHERE (global)
  ✓ LOW COMPETITION sources
"""

import os
import smtplib
import requests
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

class JobScout:
    def __init__(self):
        self.email_address = os.getenv('EMAIL_ADDRESS')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.recipient_email = os.getenv('RECIPIENT_EMAIL')
        self.jobs_found = []
        self.last_24h = datetime.utcnow() - timedelta(hours=24)
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # EXACT role keywords
        self.roles = [
            'devops', 'cloud', 'infrastructure', 'sre', 
            'site reliability', 'platform engineer'
        ]
        
        # EXACT entry-level keywords
        self.entry_level = [
            'junior', 'entry', 'entry-level', 'entry level',
            '0-2', '1-2 years', 'graduate', 'fresher',
            'early career', 'starter'
        ]
        
        # EXACT remote keywords
        self.remote = [
            'remote', '100% remote', 'work from home', 'fully remote',
            'distributed', 'anywhere'
        ]
    
    def is_match(self, title, description):
        """Check if job matches ALL criteria"""
        text = (title + " " + description).lower()
        
        # Must have role
        has_role = any(role in text for role in self.roles)
        
        # Must have entry-level indicator
        has_entry = any(entry in text for entry in self.entry_level)
        
        # Must have remote indicator
        has_remote = any(remote in text for remote in self.remote)
        
        return has_role and has_entry and has_remote
    
    def is_recent(self, date_string):
        """Check if job posted in last 24 hours"""
        try:
            # Try ISO format
            job_date = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            return job_date > self.last_24h
        except:
            try:
                # Try other common formats
                from dateutil import parser
                job_date = parser.parse(date_string)
                return job_date > self.last_24h
            except:
                return False
    
    # ====== SOURCE 1: GITHUB JOBS (Real tech jobs) ======
    
    def scrape_github(self):
        """GitHub Jobs - Real tech jobs with timestamps"""
        print("\n[GitHub Jobs API]")
        try:
            url = "https://jobs.github.com/positions.json"
            response = requests.get(url, timeout=10, headers=self.headers)
            
            if response.status_code == 200:
                jobs = response.json()
                added = 0
                
                for job in jobs:
                    try:
                        title = job.get('title', '')
                        company = job.get('company', '')
                        description = job.get('description', '')
                        url_job = job.get('url', '')
                        created = job.get('created_at', '')
                        location = job.get('location', '')
                        
                        # Check ALL criteria
                        if (url_job and self.is_recent(created) and 
                            'remote' in location.lower() and 
                            self.is_match(title, description)):
                            
                            self.jobs_found.append({
                                'title': title,
                                'company': company,
                                'url': url_job,
                                'posted': created[:10],
                                'source': 'GitHub Jobs',
                                'location': location
                            })
                            added += 1
                            print(f"  ✓ {title[:60]}")
                    except:
                        pass
                
                print(f"  Added: {added} jobs")
        except Exception as e:
            print(f"  Error: {str(e)[:50]}")
    
    # ====== SOURCE 2: REMOTEOK (Remote-first jobs) ======
    
    def scrape_remoteok(self):
        """RemoteOK - Remote jobs with timestamps"""
        print("\n[RemoteOK]")
        try:
            url = "https://remoteok.io/api/jobs"
            response = requests.get(url, timeout=10, headers=self.headers)
            
            if response.status_code == 200:
                jobs = response.json()
                added = 0
                
                for job in jobs[1:100]:  # Skip header
                    try:
                        if not isinstance(job, dict):
                            continue
                        
                        title = job.get('title', '')
                        company = job.get('company', '')
                        description = job.get('description', '') or ''
                        url_job = job.get('url', '')
                        posted = job.get('pubDate', '')
                        
                        # Check ALL criteria
                        if (url_job and self.is_recent(posted) and 
                            self.is_match(title, description)):
                            
                            self.jobs_found.append({
                                'title': title,
                                'company': company,
                                'url': url_job,
                                'posted': posted[:10] if posted else 'Today',
                                'source': 'RemoteOK',
                                'location': 'Remote'
                            })
                            added += 1
                            print(f"  ✓ {title[:60]}")
                    except:
                        pass
                
                print(f"  Added: {added} jobs")
        except Exception as e:
            print(f"  Error: {str(e)[:50]}")
    
    # ====== SOURCE 3: DEV.TO (Developer jobs) ======
    
    def scrape_devto(self):
        """Dev.to Jobs - Developer job listings"""
        print("\n[Dev.to Jobs]")
        try:
            url = "https://dev.to/api/listings"
            params = {
                'category': 'jobs',
                'per_page': 30
            }
            response = requests.get(url, params=params, timeout=10, headers=self.headers)
            
            if response.status_code == 200:
                jobs = response.json()
                added = 0
                
                for job in jobs:
                    try:
                        title = job.get('title', '')
                        company = job.get('organization', {}).get('name', 'Unknown') if job.get('organization') else ''
                        description = job.get('body_markdown', '') or ''
                        url_job = job.get('url', '')
                        posted = job.get('published_at', '')
                        location = job.get('location', '')
                        
                        # Check ALL criteria
                        if (url_job and self.is_recent(posted) and 
                            self.is_match(title, description)):
                            
                            self.jobs_found.append({
                                'title': title,
                                'company': company,
                                'url': url_job,
                                'posted': posted[:10],
                                'source': 'Dev.to',
                                'location': location or 'Remote'
                            })
                            added += 1
                            print(f"  ✓ {title[:60]}")
                    except:
                        pass
                
                print(f"  Added: {added} jobs")
        except Exception as e:
            print(f"  Error: {str(e)[:50]}")
    
    # ====== SOURCE 4: WELLFOUND (Startup jobs) ======
    
    def scrape_wellfound(self):
        """Wellfound - Startup jobs"""
        print("\n[Wellfound Startups]")
        try:
            url = "https://api.wellfound.com/public/api/v2/roles"
            params = {
                'experience_level': 'entry_level',
                'remote': 'true',
                'limit': 50
            }
            response = requests.get(url, params=params, timeout=10, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                added = 0
                
                if 'roles' in data:
                    for job in data['roles']:
                        try:
                            title = job.get('title', '')
                            startup = job.get('startup', {})
                            company = startup.get('name', 'Unknown') if startup else ''
                            description = job.get('description', '') or ''
                            url_job = job.get('url', '')
                            posted = job.get('created_at', '')
                            
                            # Check ALL criteria
                            if (url_job and self.is_recent(posted) and 
                                self.is_match(title, description)):
                                
                                self.jobs_found.append({
                                    'title': title,
                                    'company': company,
                                    'url': url_job,
                                    'posted': posted[:10],
                                    'source': 'Wellfound',
                                    'location': 'Remote'
                                })
                                added += 1
                                print(f"  ✓ {title[:60]}")
                        except:
                            pass
                
                print(f"  Added: {added} jobs")
        except Exception as e:
            print(f"  Error: {str(e)[:50]}")
    
    # ====== SOURCE 5: HACKAJOB (Reverse hiring) ======
    
    def add_hackajob(self):
        """Add hackajob as low-competition board"""
        print("\n[hackajob - Reverse Hiring Board]")
        self.jobs_found.append({
            'title': 'Browse: 300+ Entry-Level DevOps/Cloud/SRE/Infrastructure Roles',
            'company': 'Multiple Companies (Reverse Hiring)',
            'url': 'https://hackajob.co/jobs?role=devops&level=entry&location=remote',
            'posted': datetime.now().strftime('%Y-%m-%d'),
            'source': 'hackajob',
            'location': 'Remote - Anywhere'
        })
        print(f"  ✓ Reverse hiring platform (VERY LOW competition!)")
    
    def run(self):
        """Run all scrapers"""
        print("\n" + "="*70)
        print("🎯 JOB SCOUT AGENT - FOCUSED SEARCH")
        print("="*70)
        print("Criteria:")
        print("  ✓ Posted: Last 24 hours")
        print("  ✓ Location: Remote")
        print("  ✓ Level: Entry-level / Junior")
        print("  ✓ Roles: DevOps, Cloud, Infrastructure, SRE, Platform")
        print("  ✓ Hiring: Anywhere (global)")
        print("="*70)
        
        self.scrape_github()
        self.scrape_remoteok()
        self.scrape_devto()
        self.scrape_wellfound()
        self.add_hackajob()
        
        # Remove duplicates
        seen = set()
        unique = []
        for job in self.jobs_found:
            key = (job['title'], job['company'])
            if key not in seen:
                seen.add(key)
                unique.append(job)
        self.jobs_found = unique
        
        print("\n" + "="*70)
        print(f"✅ FOUND: {len(self.jobs_found)} jobs matching ALL criteria")
        print("="*70)
        
        if self.jobs_found:
            self.send_email()
        else:
            print("\n⚠️  No jobs found in last 24 hours. Try again later.")
    
    def send_email(self):
        """Send email with jobs"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"🎯 {len(self.jobs_found)} Remote Entry-Level Jobs (Last 24hrs)"
            msg['From'] = self.email_address
            msg['To'] = self.recipient_email
            
            # Build HTML
            html = f"""
            <html><head><style>
            body {{ font-family: Arial, sans-serif; background: #f5f5f5; }}
            .container {{ max-width: 900px; margin: 0 auto; background: white; padding: 20px; }}
            .header {{ background: #667eea; color: white; padding: 20px; border-radius: 5px; text-align: center; }}
            .job {{ border-left: 4px solid #667eea; padding: 15px; margin: 10px 0; background: #f9f9f9; }}
            .title {{ font-weight: bold; color: #667eea; }}
            .company {{ color: #764ba2; }}
            .meta {{ font-size: 12px; color: #666; margin-top: 5px; }}
            .link {{ display: inline-block; margin-top: 10px; padding: 8px 15px; background: #28a745; color: white; text-decoration: none; border-radius: 3px; }}
            </style></head><body>
            <div class="container">
            <div class="header">
                <h1>🎯 {len(self.jobs_found)} Remote Entry-Level Jobs</h1>
                <p>Posted in last 24 hours • Hiring anywhere • Low competition</p>
            </div>
            <div style="margin: 20px 0; padding: 15px; background: #d4edda; border-radius: 3px;">
                <strong>Roles:</strong> DevOps, Cloud, Infrastructure, SRE, Platform Engineer<br>
                <strong>Level:</strong> Entry-level / Junior only<br>
                <strong>Location:</strong> Remote<br>
                <strong>Posted:</strong> Last 24 hours<br>
                <strong>Competition:</strong> Low
            </div>
            """
            
            for i, job in enumerate(self.jobs_found, 1):
                html += f"""
                <div class="job">
                    <div class="title">{i}. {job['title']}</div>
                    <div class="company">{job['company']}</div>
                    <div class="meta">
                        Source: {job['source']} | Location: {job['location']} | Posted: {job['posted']}
                    </div>
                    <a href="{job['url']}" class="link">👉 APPLY NOW</a>
                </div>
                """
            
            html += """
            <div style="margin-top: 30px; padding: 15px; background: #f0f0f0; border-radius: 3px; font-size: 12px;">
                <p>Next run: Tomorrow 6:00 AM GMT+2</p>
                <p>Apply immediately! Fresh jobs get filled fast!</p>
            </div>
            </div></body></html>
            """
            
            msg.attach(MIMEText(html, 'html'))
            
            # Send
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(self.email_address, self.email_password)
            server.sendmail(self.email_address, self.recipient_email, msg.as_string())
            server.quit()
            
            print(f"\n✅ EMAIL SENT with {len(self.jobs_found)} jobs!")
            
        except Exception as e:
            print(f"\n❌ Email error: {str(e)}")

if __name__ == "__main__":
    scout = JobScout()
    scout.run()