---
name: ai-pdf-builder
description: Generate professional PDFs from Markdown using Pandoc and LaTeX with AI-powered content generation. Creates whitepapers, term sheets, memos, agreements, SAFEs, NDAs, and more.
version: 1.1.0
---

# AI PDF Builder

Generate professional PDFs from Markdown with AI-powered content generation. Perfect for:
- Whitepapers & Litepapers
- Term Sheets
- SAFEs & NDAs
- Memos & Reports
- Legal Agreements

## What's New in v1.1.0

- **AI Content Generation** - Generate documents from prompts using Claude
- **`--company` Flag** - Inject company name directly via CLI
- **`enhance` Command** - Improve existing content with AI
- **`summarize` Command** - Generate executive summaries from documents
- **Content Sanitization** - Automatic cleanup of AI-generated content

## Requirements

**Option A: Local Generation (Free, Unlimited)**
```bash
# macOS
brew install pandoc
brew install --cask basictex
sudo tlmgr install collection-fontsrecommended fancyhdr titlesec enumitem xcolor booktabs longtable geometry hyperref graphicx setspace array multirow

# Linux
sudo apt-get install pandoc texlive-full
```

**Option B: Cloud API (Coming Soon)**
No install required. Get API key at ai-pdf-builder.com

**For AI Features:**
Set your Anthropic API key:
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

## Usage

### Check System
```bash
npx ai-pdf-builder check
```

### Generate via CLI
```bash
# From markdown file
npx ai-pdf-builder generate whitepaper ./content.md -o output.pdf

# With company name
npx ai-pdf-builder generate whitepaper ./content.md -o output.pdf --company "Acme Corp"

# Document types: whitepaper, memo, agreement, termsheet, safe, nda, report, proposal
```

### AI Content Generation (New!)
```bash
# Generate a whitepaper from a prompt
npx ai-pdf-builder ai whitepaper "Write a whitepaper about decentralized identity" -o identity.pdf

# Generate with company branding
npx ai-pdf-builder ai whitepaper "AI in healthcare" -o healthcare.pdf --company "HealthTech Inc"

# Generate other document types
npx ai-pdf-builder ai termsheet "Series A for a fintech startup" -o termsheet.pdf
npx ai-pdf-builder ai memo "Q4 strategy update" -o memo.pdf --company "TechCorp"
```

### Enhance Existing Content (New!)
```bash
# Improve and expand existing markdown
npx ai-pdf-builder enhance ./draft.md -o enhanced.md

# Enhance and convert to PDF in one step
npx ai-pdf-builder enhance ./draft.md -o enhanced.pdf --pdf
```

### Summarize Documents (New!)
```bash
# Generate executive summary
npx ai-pdf-builder summarize ./long-document.md -o summary.md

# Summarize as PDF
npx ai-pdf-builder summarize ./report.pdf -o summary.pdf --pdf
```

### Generate via Code
```typescript
import { generateWhitepaper, generateTermsheet, generateSAFE, aiGenerate, enhance, summarize } from 'ai-pdf-builder';

// AI-Generated Whitepaper
const aiResult = await aiGenerate('whitepaper', 
  'Write about blockchain scalability solutions',
  { company: 'ScaleChain Labs' }
);

// Whitepaper from content
const result = await generateWhitepaper(
  '# My Whitepaper\n\nContent here...',
  { title: 'Project Name', author: 'Your Name', version: 'v1.0', company: 'Acme Corp' }
);

if (result.success) {
  fs.writeFileSync('whitepaper.pdf', result.buffer);
}

// Enhance existing content
const enhanced = await enhance(existingMarkdown);

// Summarize a document
const summary = await summarize(longDocument);

// Term Sheet with company
const termsheet = await generateTermsheet(
  '# Series Seed Term Sheet\n\n## Investment Amount\n\n$500,000...',
  { title: 'Series Seed', subtitle: 'Your Company Inc.', company: 'Investor LLC' }
);

// SAFE
const safe = await generateSAFE(
  '# Simple Agreement for Future Equity\n\n...',
  { title: 'SAFE Agreement', subtitle: 'Your Company Inc.' }
);
```

## Document Types

| Type | Function | Best For |
|------|----------|----------|
| `whitepaper` | `generateWhitepaper()` | Technical docs, litepapers |
| `memo` | `generateMemo()` | Executive summaries |
| `agreement` | `generateAgreement()` | Legal contracts |
| `termsheet` | `generateTermsheet()` | Investment terms |
| `safe` | `generateSAFE()` | SAFE agreements |
| `nda` | `generateNDA()` | Non-disclosure agreements |
| `report` | `generateReport()` | Business reports |
| `proposal` | `generateProposal()` | Business proposals |

## Custom Branding

```typescript
const result = await generateWhitepaper(content, metadata, {
  customColors: {
    primary: '#E85D04',    // Signal Orange
    secondary: '#14B8A6',  // Coordinate Teal
    accent: '#0D0D0D'      // Frontier Dark
  },
  fontSize: 11,
  margin: '1in',
  paperSize: 'letter'
});
```

## Agent Instructions

When a user asks to generate a PDF:

1. Check what type of document they need (whitepaper, term sheet, memo, etc.)
2. Determine if they want AI generation or have existing content
3. Get the content - either from their message, a file, or use AI to generate
4. Ask for metadata if not provided (title, author, company name)
5. Use `--company` flag to inject company branding
6. Check if Pandoc is installed: `which pandoc`
7. If Pandoc missing, provide install instructions or suggest cloud API
8. Generate the PDF using the appropriate function
9. Send the PDF file to the user

**AI Commands Quick Reference:**
- `ai <type> "<prompt>"` - Generate new document from prompt
- `enhance <file>` - Improve existing content
- `summarize <file>` - Create executive summary
- `--company "Name"` - Add company branding to any command

## Links

- npm: https://www.npmjs.com/package/ai-pdf-builder
- GitHub: https://github.com/NextFrontierBuilds/ai-pdf-builder
