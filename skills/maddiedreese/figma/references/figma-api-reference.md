# Figma API Reference

Complete reference for Figma REST API endpoints and Plugin API capabilities.

## Authentication

### Access Token Setup
1. Generate personal access token: Figma → Settings → Account → Personal Access Tokens
2. For team/organization usage: Create OAuth app for broader access
3. Set environment variable: `FIGMA_ACCESS_TOKEN=your_token_here`

### API Headers
```http
X-Figma-Token: your_access_token_here
Content-Type: application/json
```

## REST API Endpoints

### File Operations

#### GET /v1/files/:key
Get complete file data including document tree, components, and styles.

**Parameters:**
- `version` (optional): Specific version ID
- `ids` (optional): Comma-separated node IDs to limit scope
- `depth` (optional): How deep to traverse document tree
- `geometry` (optional): Set to "paths" for vector data
- `plugin_data` (optional): Plugin IDs to include plugin data

**Response includes:**
- Document tree with all nodes
- Components map with metadata
- Styles map with style definitions
- Version and file metadata

#### GET /v1/files/:key/nodes
Get specific nodes from a file.

**Parameters:**
- `ids` (required): Comma-separated node IDs
- `version`, `depth`, `geometry`, `plugin_data` (same as above)

#### GET /v1/images/:key
Export nodes as images.

**Parameters:**
- `ids` (required): Node IDs to export
- `scale` (optional): 1, 2, or 4 (default: 1)
- `format` (optional): jpg, png, svg, or pdf (default: png)
- `svg_include_id` (optional): Include node IDs in SVG
- `svg_simplify_stroke` (optional): Simplify strokes in SVG
- `use_absolute_bounds` (optional): Use absolute coordinates
- `version` (optional): Specific version to export

**Returns:** Map of node IDs to image URLs (URLs expire after 30 days)

#### GET /v1/files/:key/images
Get image fill metadata from a file.

### Component Operations

#### GET /v1/files/:key/components
Get all components in a file.

#### GET /v1/components/:key
Get component metadata by component key.

#### GET /v1/teams/:team_id/components
Get team component library.

**Parameters:**
- `page_size` (optional): Results per page (max 1000)
- `after` (optional): Pagination cursor

### Style Operations

#### GET /v1/files/:key/styles
Get all styles in a file.

#### GET /v1/styles/:key
Get style metadata by style key.

#### GET /v1/teams/:team_id/styles
Get team style library.

### Project Operations

#### GET /v1/teams/:team_id/projects
Get projects for a team.

#### GET /v1/projects/:project_id/files
Get files in a project.

### User Operations

#### GET /v1/me
Get current user information.

## Rate Limits

- 1000 requests per minute per access token
- Image exports: 100 requests per minute
- Use exponential backoff for 429 responses
- Monitor `X-RateLimit-*` headers

## Error Handling

### Common HTTP Status Codes
- `400 Bad Request`: Invalid parameters
- `401 Unauthorized`: Invalid or missing access token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: File or resource doesn't exist
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Figma server error

### Error Response Format
```json
{
  "status": 400,
  "err": "Bad request: Invalid file key"
}
```

## Node Types

### Document Structure
- `DOCUMENT` - Root document node
- `CANVAS` - Page/canvas node
- `FRAME` - Frame container
- `GROUP` - Group container
- `SECTION` - Section container

### Shape Nodes
- `RECTANGLE` - Rectangle shape
- `LINE` - Line shape
- `ELLIPSE` - Ellipse shape
- `POLYGON` - Polygon shape
- `STAR` - Star shape
- `VECTOR` - Vector shape

### Text and Components
- `TEXT` - Text node
- `COMPONENT` - Master component
- `COMPONENT_SET` - Component set (variants)
- `INSTANCE` - Component instance

### Special Nodes
- `BOOLEAN_OPERATION` - Boolean operation result
- `SLICE` - Export slice
- `STICKY` - Sticky note (FigJam)
- `CONNECTOR` - Connector line (FigJam)

## Plugin API Overview

The Plugin API allows creating, modifying, and analyzing design files through plugins.

### Key Capabilities
- **Create nodes**: Generate frames, shapes, text, components
- **Modify properties**: Update fills, strokes, effects, layout
- **Component management**: Create/update components and instances
- **Style operations**: Create and apply text/fill/effect styles
- **File operations**: Navigate pages, selection, document structure

### Plugin API Limitations
- Runs in browser sandbox environment
- Cannot directly access external APIs (use UI for HTTP requests)
- Limited file system access
- Must be installed/authorized by users

### Common Plugin Patterns

#### Creating Basic Shapes
```javascript
// Create rectangle
const rect = figma.createRectangle();
rect.resize(100, 100);
rect.fills = [{type: 'SOLID', color: {r: 1, g: 0, b: 0}}];

// Create text
const text = figma.createText();
await figma.loadFontAsync(text.fontName);
text.characters = "Hello World";
```

#### Working with Components
```javascript
// Create component
const component = figma.createComponent();
component.name = "Button";

// Create instance
const instance = component.createInstance();
```

#### Traversing Document Tree
```javascript
function traverse(node) {
  console.log(node.name, node.type);
  if ("children" in node) {
    for (const child of node.children) {
      traverse(child);
    }
  }
}

traverse(figma.root);
```

## Best Practices

### API Usage
1. **Batch operations**: Group multiple API calls when possible
2. **Cache results**: Store file data to minimize repeat requests
3. **Use specific node IDs**: Limit data transfer with `ids` parameter
4. **Handle rate limits**: Implement exponential backoff
5. **Version awareness**: Use version parameter for consistency

### Image Exports
1. **Choose appropriate format**: PNG for complex images, SVG for icons
2. **Optimize scale**: Use scale=1 unless high-DPI needed
3. **Batch exports**: Export multiple nodes in single request
4. **Cache URLs**: Store image URLs but remember 30-day expiration

### Plugin Development
1. **Minimize processing**: Keep operations fast to avoid timeouts
2. **Progress feedback**: Show progress for long operations
3. **Error handling**: Gracefully handle missing fonts, permissions
4. **Memory management**: Clean up large data structures
5. **User consent**: Request permissions appropriately

### Security
1. **Token protection**: Never expose access tokens in client-side code
2. **Scope principle**: Use minimal required permissions
3. **Input validation**: Validate all user inputs and API responses
4. **Audit logs**: Track API usage for compliance

## Common Use Cases

### Design System Automation
- Extract design tokens (colors, typography, spacing)
- Generate code from components
- Sync design systems across files
- Audit design consistency

### Asset Generation
- Export marketing assets in multiple formats
- Generate app icons and favicons
- Create social media templates
- Produce print-ready assets

### Workflow Integration
- Connect designs to development tools
- Automate handoff documentation
- Version control for design files
- Collaborative review processes

### Quality Assurance
- Accessibility compliance checking
- Brand guideline validation
- Consistency auditing across projects
- Performance optimization recommendations