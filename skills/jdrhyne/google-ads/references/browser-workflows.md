# Google Ads Browser Automation Workflows

Detailed step-by-step browser automation for Google Ads UI.

## Table of Contents
1. [Navigation Basics](#navigation-basics)
2. [Campaign Performance](#campaign-performance)
3. [Keyword Analysis](#keyword-analysis)
4. [Bulk Actions](#bulk-actions)
5. [Report Downloads](#report-downloads)
6. [Conversion Tracking](#conversion-tracking)

---

## Navigation Basics

### URL Patterns
```
Base: https://ads.google.com/aw/
├── overview          # Account overview
├── campaigns         # All campaigns
├── adgroups          # All ad groups
├── keywords          # All keywords (search)
├── ads               # All ads
├── conversions       # Conversion actions
└── tools/conversions # Conversion settings
```

### Account Switcher
- Location: Top-right corner, account name dropdown
- Click to switch between accounts/MCCs

### Date Range Picker
- Location: Top-right, shows current date range
- Click → Select preset or custom range
- Always set before pulling data

---

## Campaign Performance

### View All Campaigns
```
1. browser:navigate → ads.google.com/aw/campaigns
2. browser:snapshot → Look for table with columns:
   - Campaign (name)
   - Status (Enabled/Paused/Removed)
   - Budget (daily)
   - Cost
   - Conversions
   - Cost/conv.
```

### Filter by Status
```
1. Click "Add filter" button (filter icon)
2. Select "Campaign status"
3. Choose: Enabled, Paused, or All
4. Click "Apply"
```

### Sort by Performance
```
1. Click column header (e.g., "Cost")
2. Click again to reverse sort
3. Descending = highest first
```

### Common Table Selectors
```
Table: [role="grid"] or table.ess-table
Rows: [role="row"] or tbody tr
Cells: [role="gridcell"] or td
Headers: [role="columnheader"] or th
```

---

## Keyword Analysis

### Find Zero-Conversion Keywords

**Manual Filter Method:**
```
1. Navigate: ads.google.com/aw/keywords
2. Click "Add filter"
3. Select "Conversions" → "Less than" → "1"
4. Click "Add filter" again
5. Select "Cost" → "Greater than" → "500" (or threshold)
6. Apply filters
7. Sort by Cost descending
8. Snapshot results
```

**Filter URL (faster):**
```
ads.google.com/aw/keywords?filter=metrics.conversions<1,metrics.cost_micros>500000000
```

### Keyword Match Type Analysis
```
Filter by match type:
- Broad: [match_type] = BROAD
- Phrase: [match_type] = PHRASE  
- Exact: [match_type] = EXACT
```

### Quality Score Check
```
1. Keywords view
2. Columns → Modify columns
3. Add: Quality Score, Expected CTR, Landing page exp., Ad relevance
4. Apply
5. Sort by Quality Score ascending (find low scores)
```

---

## Bulk Actions

### Pause Multiple Items
```
1. Check boxes next to items (checkbox in first column)
2. Click "Edit" button (appears in toolbar when items selected)
3. Select "Pause" from dropdown
4. Confirm if prompted
```

### Enable Paused Items
```
1. Filter: Status = Paused
2. Check boxes for items to enable
3. Edit → "Enable"
```

### Change Budgets
```
For campaigns:
1. Click on budget amount (it's editable)
2. Enter new value
3. Press Enter or click away to save

For bulk budget changes:
1. Select multiple campaigns
2. Edit → "Change budgets"
3. Choose: Set to, Increase by %, Decrease by %
4. Enter value, Apply
```

### Add Labels
```
1. Select items
2. Click "Labels" button
3. Choose existing label or create new
4. Apply
```

---

## Report Downloads

### Quick Export
```
1. Go to any view (campaigns, keywords, etc.)
2. Click download icon (↓) in toolbar above table
3. Select format:
   - .csv (recommended for data analysis)
   - .xlsx (Excel)
   - Google Sheets
4. File saves to Downloads
```

### Custom Reports
```
1. Navigate: Reports (left menu) → Reports
2. Click "+ Custom"
3. Drag dimensions/metrics to canvas
4. Set filters and date range
5. Run → Download
```

### Scheduled Reports
```
1. Create custom report
2. Click "Schedule" icon
3. Set frequency (daily/weekly/monthly)
4. Add email recipients
5. Save
```

---

## Conversion Tracking

### View Conversion Actions
```
1. Navigate: Goals → Conversions → Summary
   OR: ads.google.com/aw/conversions
2. Check status column:
   - "Recording conversions" = ✅ Working
   - "No recent conversions" = ⚠️ Check setup
   - "Inactive" = ❌ Needs fixing
```

### Check Conversion Settings
```
For each conversion action:
1. Click conversion name
2. Review:
   - Status (active/inactive)
   - Count (one/every)
   - Attribution model
   - Conversion window
   - Value settings
```

### Diagnose Tracking Issues
```
1. Tools & Settings → Conversions
2. Click specific conversion action
3. Look at "Recording status" timeline
4. Check "Last conversion" date
5. If stale: verify tag installation
```

---

## UI Element Patterns

### Buttons
```
Primary action: button[data-color="primary"]
Secondary: button[data-color="secondary"]  
Dropdown triggers: [aria-haspopup="listbox"]
```

### Tables
```
Data table: [role="grid"], table.ess-table
Checkbox column: First td/th in each row
Sortable header: th[aria-sort], th[role="columnheader"]
```

### Filters
```
Filter bar: [role="toolbar"]
Add filter button: Contains "Add filter" text
Filter chips: [role="listitem"] in filter bar
Clear filters: "Clear all" button
```

### Dialogs/Modals
```
Modal: [role="dialog"]
Close button: [aria-label="Close"]
Confirm: Primary button in modal
Cancel: Secondary button or close
```

---

## Tips for Reliable Automation

1. **Wait for table load**: Tables load async; wait for row count > 0
2. **Handle pagination**: Check for "Show more" or page controls
3. **Verify filters applied**: Check filter chips appear
4. **Date range matters**: Always confirm date range before reading data
5. **Account context**: Verify correct account selected (top-right)
