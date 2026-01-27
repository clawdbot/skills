# Job Platform Integration Reference

This document provides technical details for integrating with various job platforms.

## Platform APIs

### LinkedIn Jobs API
- **Documentation**: https://developer.linkedin.com/docs/v2/jobs
- **Authentication**: OAuth 2.0
- **Rate Limits**: 100 requests per day (free tier)
- **Easy Apply**: Available through API for partner integrations
- **Required Scopes**: `r_basicprofile`, `r_emailaddress`, `w_member_social`

### Indeed API
- **Documentation**: https://opensource.indeedeng.io/api-documentation/
- **Authentication**: API Key
- **Rate Limits**: 1000 requests per day
- **Application Method**: Redirect to Indeed's application page
- **Job Search**: Supports advanced filters

### Glassdoor API
- **Documentation**: https://www.glassdoor.com/developer/index.htm
- **Authentication**: API Key + Partner ID
- **Rate Limits**: Varies by partnership tier
- **Features**: Job listings, company reviews, salary data

### ZipRecruiter API
- **Documentation**: Contact ZipRecruiter for partner API access
- **Authentication**: API Key
- **Features**: Job posting, applicant tracking integration

### Wellfound (AngelList)
- **Documentation**: https://docs.wellfound.com/
- **Authentication**: OAuth 2.0
- **Focus**: Startup and tech jobs
- **Easy Apply**: Built-in quick apply feature

## Web Scraping Approach

When APIs are not available or limited, use web scraping with these tools:

### Selenium Setup
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=options)
```

### Playwright (Recommended)
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://linkedin.com/jobs')
```

## Application Form Automation

### Common Form Fields
1. **Personal Information**
   - Full name
   - Email address
   - Phone number
   - Location/Address
   
2. **Professional Information**
   - Resume/CV upload
   - Cover letter (text or upload)
   - LinkedIn profile URL
   - Portfolio/Website URL
   - GitHub/GitLab profile
   
3. **Work Authorization**
   - Authorized to work in [country]?
   - Require visa sponsorship?
   - Willing to relocate?
   
4. **Experience & Education**
   - Years of experience
   - Highest education level
   - Degree field
   - University name
   
5. **Screening Questions**
   - Custom questions (vary by employer)
   - Multiple choice or text answers
   - Skills assessments

### Form Field Selectors

#### LinkedIn Easy Apply
```python
LINKEDIN_SELECTORS = {
    "easy_apply_button": "button[aria-label*='Easy Apply']",
    "phone": "input[name='phoneNumber']",
    "resume_upload": "input[type='file'][name*='resume']",
    "submit": "button[aria-label='Submit application']",
}
```

#### Indeed
```python
INDEED_SELECTORS = {
    "apply_button": "button[id*='apply']",
    "name": "input[name='applicant.name']",
    "email": "input[name='applicant.emailAddress']",
    "phone": "input[name='applicant.phoneNumber']",
    "resume": "input[type='file'][name='resume']",
}
```

## Best Practices

### Rate Limiting
- Add delays between applications (2-5 seconds minimum)
- Respect platform rate limits
- Use exponential backoff for retries

### Error Handling
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def submit_application(job_url):
    # Application logic
    pass
```

### Session Management
- Maintain authenticated sessions
- Handle cookie persistence
- Refresh tokens before expiration

### Captcha Handling
- Use 2Captcha or Anti-Captcha services
- Implement manual intervention fallback
- Detect captcha presence early

## Compliance & Ethics

### Important Considerations
1. **Terms of Service**: Review each platform's ToS regarding automation
2. **Rate Limiting**: Don't overwhelm platforms with requests
3. **Truthfulness**: Never misrepresent information in applications
4. **Privacy**: Securely store and handle personal data
5. **Authenticity**: Each application should be genuine interest

### Recommended Approach
- Use official APIs when available
- Implement reasonable delays
- Add manual review checkpoints
- Maintain application logs
- Allow user confirmation before submission

## Profile Management

### Resume Tailoring
Use AI to customize resumes per job:
```python
def tailor_resume(resume_text, job_description):
    """Customize resume to highlight relevant skills"""
    # Use LLM to analyze job requirements
    # Reorder/emphasize matching experience
    # Return tailored resume
    pass
```

### Cover Letter Generation
Generate personalized cover letters:
```python
def generate_cover_letter(job, profile, company_research):
    """Create personalized cover letter"""
    # Research company culture
    # Match skills to requirements
    # Generate authentic, personalized letter
    pass
```

## Tracking & Analytics

### Application Tracker
```python
APPLICATION_SCHEMA = {
    "job_id": str,
    "company": str,
    "position": str,
    "applied_date": str,
    "platform": str,
    "status": str,  # applied, rejected, interview, offer
    "match_score": float,
    "follow_up_date": str,
    "notes": str
}
```

### Success Metrics
- Application-to-response rate
- Interview conversion rate
- Best performing platforms
- Most successful job titles/companies
- Time to hire statistics

## Security

### Credential Storage
```python
from cryptography.fernet import Fernet
import keyring

# Store credentials securely
keyring.set_password("job_automation", "linkedin", encrypted_password)
```

### Data Encryption
- Encrypt stored resumes and personal data
- Use environment variables for API keys
- Implement secure file permissions

## Troubleshooting

### Common Issues
1. **Session Expiration**: Implement token refresh logic
2. **DOM Changes**: Use flexible selectors, have fallbacks
3. **Captcha Blocks**: Reduce frequency, use residential proxies
4. **Form Variations**: Detect form type, adjust strategy
5. **Upload Failures**: Verify file formats, check size limits

### Debug Mode
Enable verbose logging to troubleshoot issues:
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
```
