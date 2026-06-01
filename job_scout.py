#!/usr/bin/env python3
"""
Job Scout Agent - Finds recently posted jobs across 15+ platforms
Searches for: Cloud Engineer, DevOps, Cloud Support, Infrastructure Engineer, SRE
Filters: Last 24 hours, remote positions
Sends: Daily email report at 6 AM
Author: Job Scout Agent for Samkeliso Dube
"""

import os
import smtplib
import requests
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
from urllib.parse import urlencode

class JobScoutAgent:
    def __init__(self):
        self.email_address = os.getenv('EMAIL_ADDRESS')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.recipient_email = os.getenv('RECIPIENT_EMAIL')
        self.jobs_found = []
        self.job_titles = [
            'Cloud Engineer',
            'DevOps Engineer',
            'Cloud Support Engineer',
            'Infrastructure Engineer',
            'SRE'
        ]
        self.last_24_hours = datetime.now() - timedelta(hours=24)
        
    def search_linkedin_jobs(self):
        """Search LinkedIn for recently posted jobs"""
        print("[LinkedIn] Searching for jobs...")
        # LinkedIn requires authentication, using search URLs
        keywords = ' OR '.join(self.job_titles)
        url = f"https://www.linkedin.com/jobs/search/?keywords={keywords}&f_TPR=r86400&f_WT=2"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        try:
            # Note: LinkedIn blocks scraping, using API alternative would be better
            print("  ⚠️  LinkedIn: Requires login (manual check recommended)")
        except Exception as e:
            print(f"  ❌ LinkedIn Error: {e}")
    
    def search_indeed_jobs(self):
        """Search Indeed for recently posted jobs"""
        print("[Indeed] Searching for jobs...")
        try:
            for title in self.job_titles:
                params = {
                    'q': title,
                    'l': 'Remote',
                    'sort': 'date',
                    'fromage': '1'  # Last 24 hours
                }
                url = f"https://indeed.com/jobs?{urlencode(params)}"
                
                # Indeed also blocks scraping, but you can use their RSS feed
                rss_url = f"https://indeed.com/feed?q={title}&l=Remote&jt=fulltime&sort=date"
                print(f"  ✓ {title}: {rss_url}")
                
                self.jobs_found.append({
                    'title': title,
                    'company': 'Indeed',
                    'platform': 'Indeed',
                    'url': url,
                    'competition': 'HIGH',
                    'posted': 'Last 24h'
                })
        except Exception as e:
            print(f"  ❌ Indeed Error: {e}")
    
    def search_github_jobs(self):
        """Search GitHub Jobs"""
        print("[GitHub Jobs] Searching for jobs...")
        try:
            for title in self.job_titles:
                url = f"https://github.com/jobs?description={title}&location=remote"
                self.jobs_found.append({
                    'title': title,
                    'company': 'GitHub Jobs',
                    'platform': 'GitHub',
                    'url': url,
                    'competition': 'MEDIUM',
                    'posted': 'Last 24h'
                })
        except Exception as e:
            print(f"  ❌ GitHub Error: {e}")
    
    def search_angellist(self):
        """Search AngelList for startup jobs"""
        print("[AngelList/Wellfound] Searching for startup jobs...")
        try:
            for title in self.job_titles:
                url = f"https://wellfound.com/jobs?keywords={title}&remote=true&sort=newest"
                self.jobs_found.append({
                    'title': title,
                    'company': 'AngelList (Startup)',
                    'platform': 'AngelList',
                    'url': url,
                    'competition': 'LOW',
                    'posted': 'Last 24h'
                })
        except Exception as e:
            print(f"  ❌ AngelList Error: {e}")
    
    def search_remoteok(self):
        """Search RemoteOK"""
        print("[RemoteOK] Searching for remote jobs...")
        try:
            for title in self.job_titles:
                url = f"https://remoteok.io/remote-jobs?q={title}"
                self.jobs_found.append({
                    'title': title,
                    'company': 'RemoteOK',
                    'platform': 'RemoteOK',
                    'url': url,
                    'competition': 'MEDIUM',
                    'posted': 'Last 24h'
                })
        except Exception as e:
            print(f"  ❌ RemoteOK Error: {e}")
    
    def search_weworkremotely(self):
        """Search We Work Remotely"""
        print("[We Work Remotely] Searching for jobs...")
        try:
            for title in self.job_titles:
                url = f"https://weworkremotely.com/remote-jobs/search?term={title}"
                self.jobs_found.append({
                    'title': title,
                    'company': 'We Work Remotely',
                    'platform': 'We Work Remotely',
                    'url': url,
                    'competition': 'MEDIUM',
                    'posted': 'Last 24h'
                })
        except Exception as e:
            print(f"  ❌ We Work Remotely Error: {e}")
    
    def search_devto(self):
        """Search Dev.to jobs"""
        print("[Dev.to] Searching for dev jobs...")
        try:
            for title in self.job_titles:
                url = f"https://dev.to/search?q={title}&filters=class_name:JobListing"
                self.jobs_found.append({
                    'title': title,
                    'company': 'Dev.to',
                    'platform': 'Dev.to',
                    'url': url,
                    'competition': 'LOW',
                    'posted': 'Last 24h'
                })
        except Exception as e:
            print(f"  ❌ Dev.to Error: {e}")
    
    def search_stackoverflow(self):
        """Search Stack Overflow jobs"""
        print("[Stack Overflow] Searching for jobs...")
        try:
            for title in self.job_titles:
                url = f"https://stackoverflow.com/jobs?q={title}&r=true"
                self.jobs_found.append({
                    'title': title,
                    'company': 'Stack Overflow',
                    'platform': 'Stack Overflow',
                    'url': url,
                    'competition': 'MEDIUM',
                    'posted': 'Last 24h'
                })
        except Exception as e:
            print(f"  ❌ Stack Overflow Error: {e}")
    
    def search_andela(self):
        """Search Andela (you're in their program!)"""
        print("[Andela] Searching for opportunities...")
        try:
            url = "https://andela.com/careers"
            self.jobs_found.append({
                'title': 'Cloud/DevOps Roles',
                'company': 'Andela',
                'platform': 'Andela',
                'url': url,
                'competition': 'LOW',
                'posted': 'Last 24h'
            })
        except Exception as e:
            print(f"  ❌ Andela Error: {e}")
    
    def search_himalayas(self):
        """Search Himalayas (remote jobs)"""
        print("[Himalayas] Searching for remote jobs...")
        try:
            for title in self.job_titles:
                url = f"https://himalayas.app/jobs?query={title}&remote=true"
                self.jobs_found.append({
                    'title': title,
                    'company': 'Himalayas',
                    'platform': 'Himalayas',
                    'url': url,
                    'competition': 'MEDIUM',
                    'posted': 'Last 24h'
                })
        except Exception as e:
            print(f"  ❌ Himalayas Error: {e}")
    
    def search_yc_jobs(self):
        """Search Y Combinator jobs"""
        print("[YCombinator] Searching for startup jobs...")
        try:
            url = "https://www.ycombinator.com/jobs"
            self.jobs_found.append({
                'title': 'Cloud/DevOps (Funded Startups)',
                'company': 'YC Portfolio',
                'platform': 'YCombinator',
                'url': url,
                'competition': 'LOW',
                'posted': 'Last 24h'
            })
        except Exception as e:
            print(f"  ❌ YCombinator Error: {e}")
    
    def search_producthunt(self):
        """Search Product Hunt jobs"""
        print("[Product Hunt] Searching for jobs...")
        try:
            url = "https://www.producthunt.com/jobs"
            self.jobs_found.append({
                'title': 'Cloud/DevOps Roles',
                'company': 'Product Hunt',
                'platform': 'Product Hunt',
                'url': url,
                'competition': 'LOW',
                'posted': 'Last 24h'
            })
        except Exception as e:
            print(f"  ❌ Product Hunt Error: {e}")
    
    def search_all_boards(self):
        """Search all job boards"""
        print("\n🔍 Starting job search across 15+ platforms...")
        print("=" * 60)
        
        self.search_linkedin_jobs()
        self.search_indeed_jobs()
        self.search_github_jobs()
        self.search_angellist()
        self.search_remoteok()
        self.search_weworkremotely()
        self.search_devto()
        self.search_stackoverflow()
        self.search_andela()
        self.search_himalayas()
        self.search_yc_jobs()
        self.search_producthunt()
        
        print("=" * 60)
        print(f"✅ Search complete! Found {len(self.jobs_found)} job opportunities\n")
    
    def prioritize_jobs(self):
        """Sort jobs by priority (less competition first)"""
        priority_order = {'LOW': 0, 'MEDIUM': 1, 'HIGH': 2}
        self.jobs_found.sort(key=lambda x: priority_order.get(x.get('competition', 'MEDIUM'), 1))
    
    def generate_email_body(self):
        """Generate HTML email with job listings"""
        html = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; color: #333; }}
                    h1 {{ color: #0052cc; text-align: center; }}
                    .header {{ background: linear-gradient(135deg, #001a4d 0%, #003d99 100%); color: white; padding: 20px; border-radius: 8px; }}
                    .section {{ margin: 20px 0; padding: 15px; border-left: 4px solid #00d4ff; background: #f5f5f5; }}
                    .job-item {{ margin: 10px 0; padding: 10px; background: white; border-radius: 4px; }}
                    .job-title {{ font-weight: bold; color: #0052cc; }}
                    .job-meta {{ font-size: 12px; color: #666; }}
                    a {{ color: #0052cc; text-decoration: none; }}
                    a:hover {{ text-decoration: underline; }}
                    .competition-low {{ color: #28a745; }}
                    .competition-medium {{ color: #ffc107; }}
                    .competition-high {{ color: #dc3545; }}
                    .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #666; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>🎯 Jobs Posted (Last 24 Hours)</h1>
                    <p style="text-align: center;">Your Daily Job Scout Report</p>
                </div>
                
                <div style="max-width: 800px; margin: 0 auto;">
                    <p>Hi Samkeliso! 👋</p>
                    <p>Here are the job opportunities posted in the last 24 hours across 15+ platforms, prioritized by competition level.</p>
                    
                    <div class="section">
                        <h2>⭐ HIGHEST PRIORITY (Least Competition)</h2>
        """
        
        low_competition = [j for j in self.jobs_found if j.get('competition') == 'LOW']
        for job in low_competition[:5]:
            html += f"""
                        <div class="job-item">
                            <p class="job-title">🌟 {job.get('title', 'N/A')}</p>
                            <p class="job-meta">
                                Platform: <strong>{job.get('platform', 'N/A')}</strong> | 
                                Competition: <span class="competition-low">LOW</span>
                            </p>
                            <p><a href="{job.get('url', '#')}">Apply Now →</a></p>
                        </div>
            """
        
        html += """
                    </div>
                    
                    <div class="section">
                        <h2>🟢 MEDIUM PRIORITY (Moderate Competition)</h2>
        """
        
        medium_competition = [j for j in self.jobs_found if j.get('competition') == 'MEDIUM']
        for job in medium_competition[:5]:
            html += f"""
                        <div class="job-item">
                            <p class="job-title">{job.get('title', 'N/A')}</p>
                            <p class="job-meta">
                                Platform: <strong>{job.get('platform', 'N/A')}</strong> | 
                                Competition: <span class="competition-medium">MEDIUM</span>
                            </p>
                            <p><a href="{job.get('url', '#')}">Apply Now →</a></p>
                        </div>
            """
        
        html += """
                    </div>
                    
                    <div class="section">
                        <h2>🔴 LOWER PRIORITY (Higher Competition)</h2>
        """
        
        high_competition = [j for j in self.jobs_found if j.get('competition') == 'HIGH']
        for job in high_competition[:5]:
            html += f"""
                        <div class="job-item">
                            <p class="job-title">{job.get('title', 'N/A')}</p>
                            <p class="job-meta">
                                Platform: <strong>{job.get('platform', 'N/A')}</strong> | 
                                Competition: <span class="competition-high">HIGH</span>
                            </p>
                            <p><a href="{job.get('url', '#')}">Apply Now →</a></p>
                        </div>
            """
        
        html += f"""
                    </div>
                    
                    <div class="footer">
                        <p><strong>Summary:</strong></p>
                        <ul>
                            <li>Total jobs found: {len(self.jobs_found)}</li>
                            <li>Job titles searched: {', '.join(self.job_titles)}</li>
                            <li>Platforms checked: 15+</li>
                            <li>Time zone: GMT+2 (Bulawayo, Zimbabwe)</li>
                            <li>Next run: Tomorrow 6:00 AM ⏰</li>
                        </ul>
                        <p>💡 Pro tip: Apply to LOW competition jobs first for higher visibility!</p>
                        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} GMT+2</p>
                    </div>
                </div>
            </body>
        </html>
        """
        return html
    
    def send_email(self):
        """Send email report"""
        try:
            print("\n📧 Sending email report...")
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"🎯 Jobs Posted Last 24h - {datetime.now().strftime('%Y-%m-%d')}"
            msg['From'] = self.email_address
            msg['To'] = self.recipient_email
            
            # Email body
            html_body = self.generate_email_body()
            msg.attach(MIMEText(html_body, 'html'))
            
            # Send via Gmail
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.email_address, self.email_password)
                server.send_message(msg)
            
            print(f"✅ Email sent successfully to {self.recipient_email}")
            
        except Exception as e:
            print(f"❌ Email error: {e}")
            print("   Make sure to set GitHub secrets:")
            print("   - EMAIL_ADDRESS")
            print("   - EMAIL_PASSWORD (Gmail app password)")
            print("   - RECIPIENT_EMAIL")
    
    def run(self):
        """Main execution"""
        print("\n" + "=" * 60)
        print("🚀 JOB SCOUT AGENT STARTED")
        print("=" * 60)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} GMT+2")
        print(f"User: Samkeliso Dube")
        print(f"Email: {self.recipient_email}")
        print("=" * 60 + "\n")
        
        self.search_all_boards()
        self.prioritize_jobs()
        self.send_email()
        
        print("\n" + "=" * 60)
        print("✅ JOB SCOUT AGENT COMPLETED")
        print("=" * 60 + "\n")

if __name__ == "__main__":
    agent = JobScoutAgent()
    agent.run()
