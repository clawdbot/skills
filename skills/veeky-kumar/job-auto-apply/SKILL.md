---
name: job-auto-apply
description: Automated job search and application system for Clawdbot. Use when the user wants to search for jobs and automatically apply to positions matching their criteria. Handles job searching across LinkedIn, Indeed, Glassdoor, ZipRecruiter, and Wellfound, generates tailored cover letters, fills application forms, and tracks application status. Use when user says things like "find and apply to jobs", "auto-apply for [job title]", "search for [position] jobs and apply", or "help me apply to multiple jobs automatically".
---

# Job Auto-Apply Skill

Automate job searching and application submission across multiple job platforms using Clawdbot.

## Overview

This skill enables automated job search and application workflows. It searches for jobs matching user criteria, analyzes compatibility, generates tailored cover letters, and submits applications automatically or with user confirmation.

**Supported Platforms:**
- LinkedIn (including Easy Apply)
- Indeed
- Glassdoor
- ZipRecruiter
- Wellfound (AngelList)

## Quick Start

### 1. Set Up User Profile

First, create a user profile using the template:

```bash
# Copy the profile template
cp profile_template.json ~/job_profile.json

# Edit with user's information
# Fill in: name, email, phone, resume path, skills, preferences
```

### 2. Run Job Search and Apply

```bash
# Basic usage - search and apply (dry run)
python job_search_apply.py \
  --title "Software Engineer" \
  --location "San Francisco, CA" \
  --remote \
  --max-applications 10 \
  --dry-run

# With profile file
python job_search_apply.py \
  --profile ~/job_profile.json \
  --title "Backend Engineer" \
  --platforms linkedin,indeed \
  --auto-apply

# Production mode (actual applications)
python job_search_apply.py \
  --profile ~/job_profile.json \
  --title "Senior Developer" \
  --no-dry-run \
  --require-confirmation
```

## Workflow Steps

### Step 1: Profile Configuration

Load the user's profile from the template or create programmatically:

```python
from job_search_apply import ApplicantProfile

profile = ApplicantProfile(
    full_name="Jane Doe",
    email="jane@example.com",
    phone="+1234567890",
    resume_path="~/Documents/resume.pdf",
    linkedin_url="https://linkedin.com/in/janedoe",
    years_experience=5,
    authorized_to_work=True,
    requires_sponsorship=False
)
```

### Step 2: Define Search Parameters

```python
from job_search_apply import JobSearchParams, JobPlatform

search_params = JobSearchParams(
    title="Software Engineer",
    location="Remote",
    remote=True,
    experience_level="mid",
    job_type="full-time",
    salary_min=100000,
    platforms=[JobPlatform.LINKEDIN, JobPlatform.INDEED]
)
```

### Step 3: Run Automated Application

```python
from job_search_apply import auto_apply_workflow

results = auto_apply_workflow(
    search_params=search_params,
    profile=profile,
    max_applications=10,
    min_match_score=0.75,
    dry_run=False,
    require_confirmation=True
)
```

## Integration with Clawdbot

### Using as a Clawdbot Tool

When installed as a Clawdbot skill, invoke via natural language:

**Example prompts:**
- "Find and apply to Python developer jobs in San Francisco"
- "Search for remote backend engineer positions and apply to the top 5 matches"
- "Auto-apply to senior software engineer roles with 100k+ salary"
- "Apply to jobs at tech startups on Wellfound"

The skill will:
1. Parse the user's intent and extract search parameters
2. Load the user's profile from saved configuration
3. Search across specified platforms
4. Analyze job compatibility
5. Generate tailored cover letters
6. Submit applications (with confirmation if enabled)
7. Report results and track applications

### Configuration in Clawdbot

Add to your Clawdbot configuration:

```json
{
  "skills": {
    "job-auto-apply": {
      "enabled": true,
      "profile_path": "~/job_profile.json",
      "default_platforms": ["linkedin", "indeed"],
      "max_daily_applications": 10,
      "require_confirmation": true,
      "dry_run": false
    }
  }
}
```

## Features

### 1. Multi-Platform Search
- Searches across all major job platforms
- Uses official APIs when available
- Falls back to web scraping for platforms without APIs

### 2. Smart Matching
- Analyzes job descriptions for requirement matching
- Calculates compatibility scores
- Filters jobs based on minimum match threshold

### 3. Application Customization
- Generates tailored cover letters per job
- Customizes resume emphasis based on job requirements
- Handles platform-specific application forms

### 4. Safety Features
- **Dry Run Mode**: Test without submitting applications
- **Manual Confirmation**: Review each application before submission
- **Rate Limiting**: Prevents overwhelming platforms
- **Application Logging**: Tracks all submissions for reference

### 5. Form Automation
Automatically fills common application fields:
- Personal information
- Work authorization status
- Education and experience
- Skills and certifications
- Screening questions (using AI when needed)

## Advanced Usage

### Custom Cover Letter Templates

Create a template with placeholders:

```text
Dear Hiring Manager at {company},

I am excited to apply for the {position} role. With {years} years of 
experience in {skills}, I believe I would be an excellent fit.

{custom_paragraph}

I look forward to discussing how I can contribute to {company}'s success.

Best regards,
{name}
```

### Application Tracking

Results are automatically saved in JSON format with details on each application submitted, including timestamps, match scores, and status.

## Bundled Resources

### Scripts
- `job_search_apply.py` - Main automation script with search, matching, and application logic

### References
- `platform_integration.md` - Technical documentation for API integration, web scraping, form automation, and platform-specific details

### Assets
- `profile_template.json` - Comprehensive profile template with all required and optional fields

## Safety and Ethics

### Important Guidelines

1. **Truthfulness**: Never misrepresent qualifications or experience
2. **Genuine Interest**: Only apply to jobs you're actually interested in
3. **Rate Limiting**: Respect platform limits and terms of service
4. **Manual Review**: Consider enabling confirmation mode for quality control
5. **Privacy**: Secure storage of personal information and credentials

### Best Practices

- Start with dry-run mode to verify behavior
- Set reasonable limits (5-10 applications per day)
- Use high match score thresholds (0.75+)
- Enable confirmation for important applications
- Track results to optimize strategy
