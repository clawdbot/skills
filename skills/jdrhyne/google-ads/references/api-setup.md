# Google Ads API Setup

Complete guide for setting up Google Ads API access.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [OAuth Setup](#oauth-setup)
3. [Configuration File](#configuration-file)
4. [Common Queries](#common-queries)
5. [Mutation Operations](#mutation-operations)

---

## Prerequisites

### What You Need
1. **Google Ads account** (or MCC access)
2. **Developer token** - Apply at developers.google.com/google-ads/api/docs/first-call/dev-token
3. **OAuth 2.0 credentials** - Create in Google Cloud Console
4. **Python 3.8+** with `google-ads` package

### Install SDK
```bash
pip install google-ads
# Or with venv
python -m venv google-ads-venv
source google-ads-venv/bin/activate
pip install google-ads
```

---

## OAuth Setup

### 1. Create OAuth Credentials
```
1. Go to console.cloud.google.com
2. Create project (or select existing)
3. Enable "Google Ads API"
4. APIs & Services → Credentials
5. Create Credentials → OAuth Client ID
6. Application type: Desktop app
7. Download JSON (client_secret_*.json)
```

### 2. Generate Refresh Token
```python
# oauth_setup.py
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/adwords']

flow = InstalledAppFlow.from_client_secrets_file(
    'client_secret.json', scopes=SCOPES)

# Opens browser for consent
credentials = flow.run_local_server(port=8080)

print(f"Refresh token: {credentials.refresh_token}")
```

### 3. Get Login Customer ID
```
- For single account: Your 10-digit account ID
- For MCC: The MCC account ID (for API auth)
- Customer ID: The account you're querying (can differ from login)
```

---

## Configuration File

### google-ads.yaml
```yaml
developer_token: YOUR_DEVELOPER_TOKEN
client_id: YOUR_CLIENT_ID.apps.googleusercontent.com
client_secret: YOUR_CLIENT_SECRET
refresh_token: YOUR_REFRESH_TOKEN
login_customer_id: YOUR_MCC_ID  # Optional, for MCC accounts

# Optional settings
# use_proto_plus: True
# logging:
#   version: 1
#   handlers:
#     default:
#       class: logging.StreamHandler
#   loggers:
#     "":
#       level: WARNING
```

### Location Options
```
1. ~/.google-ads.yaml (default)
2. ./google-ads.yaml (project directory)
3. Environment variables:
   - GOOGLE_ADS_DEVELOPER_TOKEN
   - GOOGLE_ADS_CLIENT_ID
   - GOOGLE_ADS_CLIENT_SECRET
   - GOOGLE_ADS_REFRESH_TOKEN
   - GOOGLE_ADS_LOGIN_CUSTOMER_ID
```

---

## Common Queries

### Initialize Client
```python
from google.ads.googleads.client import GoogleAdsClient

# From file
client = GoogleAdsClient.load_from_storage("./google-ads.yaml")

# Or from env
client = GoogleAdsClient.load_from_env()

ga_service = client.get_service("GoogleAdsService")
```

### Campaign Performance
```python
CUSTOMER_ID = "1234567890"  # No dashes

query = """
    SELECT 
        campaign.id,
        campaign.name,
        campaign.status,
        campaign_budget.amount_micros,
        metrics.cost_micros,
        metrics.conversions,
        metrics.cost_per_conversion
    FROM campaign
    WHERE segments.date DURING LAST_30_DAYS
      AND campaign.status != 'REMOVED'
    ORDER BY metrics.cost_micros DESC
    LIMIT 50
"""

response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

for row in response:
    cost = row.metrics.cost_micros / 1_000_000
    conv = row.metrics.conversions
    cpa = row.metrics.cost_per_conversion / 1_000_000 if conv > 0 else 0
    print(f"{row.campaign.name}: ${cost:.2f} | {conv:.1f} conv | ${cpa:.2f} CPA")
```

### Zero-Conversion Keywords
```python
query = """
    SELECT 
        ad_group_criterion.criterion_id,
        ad_group_criterion.keyword.text,
        ad_group_criterion.keyword.match_type,
        campaign.name,
        ad_group.name,
        metrics.cost_micros,
        metrics.clicks,
        metrics.impressions
    FROM keyword_view
    WHERE metrics.conversions = 0
      AND metrics.cost_micros > 500000000
      AND segments.date DURING LAST_90_DAYS
      AND ad_group_criterion.status = 'ENABLED'
    ORDER BY metrics.cost_micros DESC
    LIMIT 100
"""
```

### Ad Group Status Check
```python
query = """
    SELECT 
        ad_group.id,
        ad_group.name,
        ad_group.status,
        campaign.name,
        metrics.cost_micros
    FROM ad_group
    WHERE ad_group.status = 'ENABLED'
      AND segments.date DURING LAST_30_DAYS
"""

# Check for ad groups with no ads
query_ads = """
    SELECT 
        ad_group.id,
        ad_group.name,
        ad_group_ad.ad.id
    FROM ad_group_ad
    WHERE ad_group.status = 'ENABLED'
      AND ad_group_ad.status = 'ENABLED'
"""
```

### Conversion Actions
```python
query = """
    SELECT 
        conversion_action.id,
        conversion_action.name,
        conversion_action.status,
        conversion_action.category,
        conversion_action.counting_type,
        metrics.conversions,
        metrics.all_conversions
    FROM conversion_action
"""
```

---

## Mutation Operations

### Pause Campaigns
```python
from google.ads.googleads.client import GoogleAdsClient

client = GoogleAdsClient.load_from_storage()
campaign_service = client.get_service("CampaignService")

def pause_campaigns(customer_id, campaign_ids):
    operations = []
    for campaign_id in campaign_ids:
        operation = client.get_type("CampaignOperation")
        campaign = operation.update
        campaign.resource_name = campaign_service.campaign_path(
            customer_id, campaign_id
        )
        campaign.status = client.enums.CampaignStatusEnum.PAUSED
        client.copy_from(
            operation.update_mask,
            protobuf_helpers.field_mask(None, campaign._pb)
        )
        operations.append(operation)
    
    response = campaign_service.mutate_campaigns(
        customer_id=customer_id,
        operations=operations
    )
    return response
```

### Pause Keywords
```python
ad_group_criterion_service = client.get_service("AdGroupCriterionService")

def pause_keywords(customer_id, keyword_resource_names):
    operations = []
    for resource_name in keyword_resource_names:
        operation = client.get_type("AdGroupCriterionOperation")
        criterion = operation.update
        criterion.resource_name = resource_name
        criterion.status = client.enums.AdGroupCriterionStatusEnum.PAUSED
        # Set field mask
        client.copy_from(
            operation.update_mask,
            protobuf_helpers.field_mask(None, criterion._pb)
        )
        operations.append(operation)
    
    response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id,
        operations=operations
    )
    return response
```

### Update Budget
```python
campaign_budget_service = client.get_service("CampaignBudgetService")

def update_budget(customer_id, budget_id, new_amount_micros):
    operation = client.get_type("CampaignBudgetOperation")
    budget = operation.update
    budget.resource_name = campaign_budget_service.campaign_budget_path(
        customer_id, budget_id
    )
    budget.amount_micros = new_amount_micros
    
    client.copy_from(
        operation.update_mask,
        protobuf_helpers.field_mask(None, budget._pb)
    )
    
    response = campaign_budget_service.mutate_campaign_budgets(
        customer_id=customer_id,
        operations=[operation]
    )
    return response
```

---

## Error Handling

### Common Errors
```python
from google.ads.googleads.errors import GoogleAdsException

try:
    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)
except GoogleAdsException as ex:
    for error in ex.failure.errors:
        print(f"Error: {error.message}")
        print(f"Code: {error.error_code}")
        if error.location:
            for field_path_element in error.location.field_path_elements:
                print(f"  Field: {field_path_element.field_name}")
```

### Rate Limits
- Standard: 15,000 operations/day (mutate)
- Query: Generally unlimited but be reasonable
- Retry with exponential backoff on RESOURCE_EXHAUSTED
