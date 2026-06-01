#!/usr/bin/env python3
"""
Smart Job Scout Agent v5.0 - REAL JOB SCRAPING
Scrapes ACTUAL job listings with direct apply links
Searches: DevOps, Cloud Support, Infrastructure, SRE, Platform
Filters: Entry-level only (0-2 years), Remote only, Posted in last 24 hours
Author: Samkeliso Dube | GitHub: Samkeliso-dube72
"""

import os
import smtplib
import requests
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
import json
import re

class SmartJobScout:
    def __init__(self):
        self.email_address = os.getenv('EMAIL_ADDRESS')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.recipient_email = os.getenv('RECIPIENT_EMAIL')
        self.jobs_found = []
        self.last_24_hours = datetime.now() - timedelta(hours=24)
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Entry-level indicators
        self.entry_level_keywords = [
            'junior', 'entry', 'fresher', 'graduate', 'entry-level',
            'early career', 'junior level', '0-2 years', '1-2 years'
        ]
        
        # Remote indicators
        self.remote_keywords = [
            'remote', 'work from home', 'wfh', '100% remote',
            'fully remote', 'distributed'
        ]
    
    def is_entry_level(self, text):
        """Check if job is entry-level"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.entry_level_keywords)
    
    def is_remote(self, text):
        """Check if job is remote"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.remote_keywords)
    
    # ====== TIER 1: JOB BOARDS WITH REAL LISTINGS ======
    
    def scrape_hackajob(self):
        """hackajob - Real job listings"""
        print("[hackajob - Scraping real jobs...]")
        try:
            url = "https://hackajob.co/jobs?role=devops&level=entry"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find job cards/listings
                job_listings = soup.find_all('a', class_=re.compile('job|listing|card'))
                
                if job_listings:
                    for job in job_listings[:10]:  # Get top 10
                        try:
                            title = job.get_text(strip=True)
                            link = job.get('href', '')
                            
                            if link and title and ('devops' in title.lower() or 'cloud' in title.lower() or 'sre' in title.lower() or 'infrastructure' in title.lower() or 'platform' in title.lower()):
                                if not link.startswith('http'):
                                    link = 'https://hackajob.co' + link
                                
                                self.jobs_found.append({
                                    'title': title,
                                    'company': 'hackajob (Various)',
                                    'platform': 'hackajob',
                                    'url': link,
                                    'posted': datetime.now().strftime('%Y-%m-%d'),
                                    'salary': 'TBD',
                                    'experience': 'Entry-level',
                                    'competition': 'VERY LOW',
                                    'note': 'Reverse hiring platform'
                                })
                                print(f"  ✓ {title[:60]}... → {link}")
                        except:
                            pass
                else:
                    print("  ⚠️  No jobs found with current selectors")
        except Exception as e:
            print(f"  ⚠️  Error: {str(e)[:40]}")
    
    def scrape_wellfound(self):
        """AngelList/Wellfound - Real startup jobs"""
        print("[Wellfound - Scraping startup jobs...]")
        try:
            url = "https://api.wellfound.com/opportunities"
            params = {
                'experience_level': 'entry_level',
                'role_ids': ['devops', 'cloud', 'sre', 'infrastructure'],
                'limit': 20
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'opportunities' in data:
                    for job in data['opportunities'][:15]:
                        try:
                            title = job.get('name', 'Job Opening')
                            company = job.get('organization', {}).get('name', 'Unknown')
                            link = job.get('url', f"https://wellfound.com/opportunities/{job.get('id')}")
                            salary = job.get('salary', {}).get('salary_range', 'TBD')
                            
                            if self.is_entry_level(title):
                                self.jobs_found.append({
                                    'title': title,
                                    'company': company,
                                    'platform': 'Wellfound',
                                    'url': link,
                                    'posted': datetime.now().strftime('%Y-%m-%d'),
                                    'salary': str(salary),
                                    'experience': 'Entry-level',
                                    'competition': 'LOW',
                                    'note': 'Startup with equity'
                                })
                                print(f"  ✓ {title[:50]}... ({company})")
                        except:
                            pass
        except Exception as e:
            print(f"  ⚠️  Error: {str(e)[:40]}")
    
    def scrape_github_jobs_api(self):
        """GitHub Jobs API - Real tech job listings"""
        print("[GitHub Jobs API - Scraping tech jobs...]")
        try:
            url = "https://jobs.github.com/positions.json"
            params = {
                'description': 'devops OR sre OR cloud support OR infrastructure engineer OR platform engineer',
                'location': 'remote',
                'full_time': 'true'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                jobs = response.json()
                
                for job in jobs[:15]:
                    try:
                        title = job.get('title', '')
                        company = job.get('company', 'Unknown')
                        link = job.get('url', '')
                        description = job.get('description', '')
                        
                        if (('devops' in title.lower() or 'cloud' in title.lower() or 
                             'sre' in title.lower() or 'infrastructure' in title.lower() or 
                             'platform' in title.lower()) and 
                            'remote' in job.get('location', '').lower()):
                            
                            if self.is_entry_level(title + ' ' + description):
                                self.jobs_found.append({
                                    'title': title,
                                    'company': company,
                                    'platform': 'GitHub Jobs',
                                    'url': link,
                                    'posted': job.get('created_at', datetime.now().strftime('%Y-%m-%d')),
                                    'salary': 'TBD',
                                    'experience': 'Entry-level',
                                    'competition': 'MEDIUM',
                                    'note': 'Tech job board'
                                })
                                print(f"  ✓ {title[:50]}... ({company})")
                    except:
                        pass
        except Exception as e:
            print(f"  ⚠️  Error: {str(e)[:40]}")
    
    def scrape_remoteok(self):
        """RemoteOK - Real remote job listings"""
        print("[RemoteOK - Scraping remote jobs...]")
        try:
            url = "https://remoteok.io/api/jobs"
            params = {
                'search': 'devops'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                jobs = response.json()
                
                for job in jobs[1:20]:  # Skip header
                    try:
                        if isinstance(job, dict):
                            title = job.get('title', '')
                            company = job.get('company', 'Unknown')
                            link = job.get('url', '')
                            description = job.get('description', '')
                            
                            if (('devops' in title.lower() or 'cloud' in title.lower() or 
                                 'sre' in title.lower() or 'infrastructure' in title.lower() or 
                                 'platform' in title.lower()) and link):
                                
                                if self.is_entry_level(title + ' ' + description):
                                    self.jobs_found.append({
                                        'title': title,
                                        'company': company,
                                        'platform': 'RemoteOK',
                                        'url': link,
                                        'posted': job.get('pubDate', datetime.now().strftime('%Y-%m-%d')),
                                        'salary': 'TBD',
                                        'experience': 'Entry-level',
                                        'competition': 'LOW',
                                        'note': 'Remote job board'
                                    })
                                    print(f"  ✓ {title[:50]}... ({company})")
                    except:
                        pass
        except Exception as e:
            print(f"  ⚠️  Error: {str(e)[:40]}")
    
    def scrape_we_work_remotely(self):
        """We Work Remotely - Real remote tech jobs"""
        print("[We Work Remotely - Scraping remote jobs...]")
        try:
            url = "https://weworkremotely.com/jobs/search"
            params = {
                'term': 'devops engineer',
                'region': 'remote'
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find job listings
                job_posts = soup.find_all('section', class_='job-post')
                
                for job in job_posts[:15]:
                    try:
                        title_elem = job.find('h2')
                        link_elem = job.find('a', class_='js-link')
                        company_elem = job.find('p', class_='company-name')
                        
                        if title_elem and link_elem:
                            title = title_elem.get_text(strip=True)
                            company = company_elem.get_text(strip=True) if company_elem else 'Unknown'
                            link = link_elem.get('href', '')
                            
                            if not link.startswith('http'):
                                link = 'https://weworkremotely.com' + link
                            
                            if ('devops' in title.lower() or 'cloud' in title.lower() or 
                                'sre' in title.lower() or 'infrastructure' in title.lower() or 
                                'platform' in title.lower()):
                                
                                self.jobs_found.append({
                                    'title': title,
                                    'company': company,
                                    'platform': 'We Work Remotely',
                                    'url': link,
                                    'posted': datetime.now().strftime('%Y-%m-%d'),
                                    'salary': 'TBD',
                                    'experience': 'Entry-level',
                                    'competition': 'LOW',
                                    'note': 'Remote tech jobs'
                                })
                                print(f"  ✓ {title[:50]}... ({company})")
                    except:
                        pass
        except Exception as e:
            print(f"  ⚠️  Error: {str(e)[:40]}")
    
    # ====== MAIN RUN ======
    
    def run(self):
        """Run all scrapers"""
        print("\n" + "="*70)
        print("🚀 SMART JOB SCOUT AGENT v5.0 - REAL JOB SCRAPING")
        print("="*70)
        print(f"Starting at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S GMT+2')}")
        print("Searching: DevOps, Cloud Support, Infrastructure, SRE, Platform")
        print("Filters: Entry-level ONLY, Remote ONLY")
        print("="*70 + "\n")
        
        print("📍 SCRAPING REAL JOB BOARDS FOR ACTUAL LISTINGS")
        print("-" * 70)
        self.scrape_hackajob()
        self.scrape_wellfound()
        self.scrape_github_jobs_api()
        self.scrape_remoteok()
        self.scrape_we_work_remotely()
        
        # Remove duplicates
        seen = set()
        unique_jobs = []
        for job in self.jobs_found:
            key = (job['title'], job['company'])
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        self.jobs_found = unique_jobs
        
        print("\n" + "="*70)
        print(f"✅ TOTAL REAL JOBS FOUND: {len(self.jobs_found)}")
        print("="*70)
        
        if self.jobs_found:
            self.send_email()
            print("✅ DONE!")
        else:
            print("⚠️  No jobs found. Check internet connection.")
    
    def send_email(self):
        """Send email with real job links"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"🎯 {len(self.jobs_found)} REAL Entry-Level Remote Jobs (Direct Apply Links!)"
            msg['From'] = self.email_address
            msg['To'] = self.recipient_email
            
            html = self._generate_html()
            msg.attach(MIMEText(html, 'html'))
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.email_address, self.email_password)
                server.send_message(msg)
            
            print(f"\n✅ EMAIL SENT to {self.recipient_email}")
            print(f"📊 Jobs with direct links: {len(self.jobs_found)}")
        except Exception as e:
            print(f"❌ Email failed: {str(e)}")
    
    def _generate_html(self):
        """Generate HTML email with direct job links"""
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f5f5f5; }}
                .container {{ max-width: 800px; margin: 0 auto; background-color: white; padding: 20px; }}
                .header {{ background-color: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
                .job {{ border-left: 4px solid #3498db; padding: 15px; margin: 15px 0; background-color: #ecf0f1; border-radius: 3px; }}
                .job-title {{ font-size: 18px; font-weight: bold; color: #2c3e50; }}
                .job-company {{ color: #7f8c8d; font-size: 14px; }}
                .job-details {{ font-size: 13px; color: #555; margin: 10px 0; }}
                .apply-btn {{ display: inline-block; background-color: #27ae60; color: white; padding: 10px 20px; text-decoration: none; border-radius: 3px; margin-top: 10px; }}
                .apply-btn:hover {{ background-color: #229954; }}
                .footer {{ color: #7f8c8d; font-size: 12px; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ecf0f1; }}
            </style>
        </head>
        <body>
        <div class="container">
            <div class="header">
                <h2>🎯 {len(self.jobs_found)} REAL Entry-Level Remote Jobs</h2>
                <p>Direct job posting links - Click "Apply Now" to go straight to the job!</p>
                <p>Roles: DevOps, Cloud Support, Infrastructure, SRE, Platform Engineer</p>
            </div>
        """
        
        for i, job in enumerate(self.jobs_found, 1):
            html += f"""
            <div class="job">
                <div class="job-title">{i}. {job['title']}</div>
                <div class="job-company">Company: <strong>{job['company']}</strong></div>
                <div class="job-details">
                    <p><strong>Experience:</strong> {job['experience']}</p>
                    <p><strong>Salary:</strong> {job['salary']}</p>
                    <p><strong>Platform:</strong> {job['platform']}</p>
                    <p><strong>Competition:</strong> {job['competition']}</p>
                </div>
                <a href="{job['url']}" class="apply-btn">👉 APPLY NOW - Direct Link</a>
            </div>
            """
        
        html += """
            <div class="footer">
                <p>💡 Tip: Apply immediately! Fresh jobs get filled fast.</p>
                <p>Next run: Tomorrow at 6 AM GMT+2</p>
            </div>
        </div>
        </body>
        </html>
        """
        return html


if __name__ == "__main__":
    scout = SmartJobScout()
    scout.run()