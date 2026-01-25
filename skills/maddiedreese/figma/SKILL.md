---
name: figma
description: Professional Figma design analysis and asset export. Use for extracting design data, exporting assets in multiple formats, auditing accessibility compliance, analyzing design systems, and generating comprehensive design documentation. Read-only analysis of Figma files with powerful export and reporting capabilities.
---

# Figma Design Analysis & Export

Professional-grade Figma integration for design system analysis, asset export, and comprehensive design auditing.

## Core Capabilities

### 1. File Operations & Analysis
- **File inspection**: Get complete JSON representation of any Figma file
- **Component extraction**: List all components, styles, and design tokens
- **Asset export**: Batch export frames, components, or specific nodes as PNG/SVG/PDF
- **Version management**: Access specific file versions and branch information

**Example usage:**
- "Export all components from this design system file"
- "Get the JSON data for these specific frames"
- "Show me all the colors and typography used in this file"

### 2. Design System Management
- **Style auditing**: Analyze color usage, typography consistency, spacing patterns
- **Component analysis**: Identify unused components, measure usage patterns
- **Brand compliance**: Check adherence to brand guidelines across files
- **Design token extraction**: Generate CSS/JSON design tokens from Figma styles

**Example usage:**
- "Audit this design system for accessibility issues"
- "Generate CSS custom properties from these Figma styles"
- "Find all inconsistencies in our component library"

### 3. Bulk Asset Export
- **Multi-format exports**: Export assets as PNG, SVG, PDF, or WEBP
- **Platform-specific sizing**: Generate @1x, @2x, @3x assets for iOS/Android
- **Organized output**: Automatic folder organization by format or platform
- **Client packages**: Complete deliverable packages with documentation

**Example usage:**
- "Export all components in PNG and SVG formats"
- "Generate complete asset package for mobile app development"
- "Create client deliverable with all marketing assets"

### 4. Accessibility & Quality Analysis
- **Contrast checking**: Verify WCAG color contrast requirements
- **Font size analysis**: Ensure readable typography scales
- **Interactive element sizing**: Check touch target requirements
- **Focus state validation**: Verify keyboard navigation patterns

**Example usage:**
- "Check this design for WCAG AA compliance"
- "Analyze touch targets for mobile usability"
- "Generate an accessibility report for this app design"

## Quick Start

### Authentication Setup
```bash
# Set your Figma access token
export FIGMA_ACCESS_TOKEN="your-token-here"

# Or store in .env file
echo "FIGMA_ACCESS_TOKEN=your-token" >> .env
```

### Basic Operations
```bash
# Get file information and structure
python scripts/figma_client.py get-file "your-file-key"

# Export frames as images
python scripts/export_manager.py export-frames "file-key" --formats png,svg

# Analyze design system consistency
python scripts/style_auditor.py audit-file "file-key" --generate-html

# Check accessibility compliance
python scripts/accessibility_checker.py "file-key" --level AA --format html
```

## Workflow Patterns

### Design System Audit Workflow
1. **Extract file data** → Get components, styles, and structure
2. **Analyze consistency** → Check for style variations and unused elements
3. **Generate report** → Create detailed findings and recommendations
4. **Manual implementation** → Use findings to guide design improvements

### Asset Export Workflow
1. **Identify export targets** → Specify frames, components, or nodes
2. **Configure export settings** → Set formats, sizes, and naming conventions
3. **Batch process** → Export multiple assets simultaneously
4. **Organize output** → Structure files for handoff or implementation

### Analysis & Documentation Workflow
1. **Extract design data** → Pull components, styles, and design tokens
2. **Audit compliance** → Check accessibility and brand consistency  
3. **Generate documentation** → Create style guides and component specs
4. **Export deliverables** → Package assets for development or client handoff

## Resources

### scripts/
- `figma_client.py` - Complete Figma API wrapper with all REST endpoints
- `export_manager.py` - Professional asset export with multiple formats and scales
- `style_auditor.py` - Design system analysis and brand consistency checking
- `accessibility_checker.py` - Comprehensive WCAG compliance validation and reporting

### references/
- `figma-api-reference.md` - Complete API documentation and examples
- `design-patterns.md` - UI patterns and component best practices
- `accessibility-guidelines.md` - WCAG compliance requirements
- `export-formats.md` - Asset export options and specifications

### assets/
- `templates/design-system/` - Pre-built component library templates
- `templates/brand-kits/` - Standard brand guideline structures
- `templates/wireframes/` - Common layout patterns and flows

## Integration Examples

### With Development Workflows
```bash
# Generate design tokens for CSS
python scripts/export_manager.py export-tokens "file-key" --format css

# Create component documentation
python scripts/figma_client.py document-components "file-key" --output docs/
```

### With Brand Management
```bash
# Audit brand compliance in designs
python scripts/style_auditor.py audit-file "file-key" --brand-colors "#FF0000,#00FF00,#0000FF"

# Extract current brand colors for analysis
python scripts/figma_client.py extract-colors "file-key" --output brand-colors.json
```

### With Client Deliverables
```bash
# Generate client presentation assets
python scripts/export_manager.py client-package "file-key" --template presentation

# Create development handoff assets
python scripts/export_manager.py dev-handoff "file-key" --include-specs
```

## Limitations & Scope

### Read-Only Operations
This skill provides **read-only access** to Figma files through the REST API. It can:
- ✅ Extract data, components, and styles
- ✅ Export assets in multiple formats
- ✅ Analyze and audit design files
- ✅ Generate comprehensive reports

### What It Cannot Do
- ❌ **Modify existing files** (colors, text, components)
- ❌ **Create new designs** or components  
- ❌ **Batch update** multiple files
- ❌ **Real-time collaboration** features

For file modifications, you would need to develop a **Figma plugin** using the Plugin API.

## Technical Features

### API Rate Limiting
Built-in rate limiting and retry logic to handle Figma's API constraints gracefully.

### Error Handling
Comprehensive error handling with detailed logging and recovery suggestions.

### Multi-Format Support
Export assets in PNG, SVG, PDF, and WEBP with platform-specific sizing.