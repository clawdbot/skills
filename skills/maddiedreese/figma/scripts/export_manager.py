#!/usr/bin/env python3
"""
Figma Export Manager - Batch asset export with intelligent organization
Handles multiple formats, naming conventions, and export workflows.
"""

import os
import sys
import json
import asyncio
import aiohttp
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor
import argparse
import time
try:
    from figma_client import FigmaClient
except ImportError:
    # Handle case where script is run directly
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent))
    from figma_client import FigmaClient

@dataclass
class ExportConfig:
    """Configuration for export operations"""
    formats: List[str] = field(default_factory=lambda: ['png'])
    scales: List[float] = field(default_factory=lambda: [1.0])
    output_dir: str = './figma-exports'
    naming_pattern: str = '{name}_{id}.{format}'
    create_manifest: bool = True
    skip_existing: bool = False
    max_concurrent: int = 5
    organize_by_format: bool = True

class ExportManager:
    """Professional-grade Figma asset export manager"""
    
    def __init__(self, figma_client: FigmaClient, config: ExportConfig = None):
        self.client = figma_client
        self.config = config or ExportConfig()
        
        # Create output directory
        Path(self.config.output_dir).mkdir(parents=True, exist_ok=True)
    
    def export_frames(self, file_key: str, frame_ids: List[str] = None, 
                     frame_names: List[str] = None) -> Dict[str, Any]:
        """Export all frames or specific frames from a file"""
        
        # Get file data to identify frames
        file_data = self.client.get_file(file_key)
        
        if not frame_ids and not frame_names:
            # Export all frames
            frame_nodes = self._find_frames(file_data)
        else:
            # Filter specific frames
            all_frames = self._find_frames(file_data)
            frame_nodes = []
            
            for frame in all_frames:
                if frame_ids and frame['id'] in frame_ids:
                    frame_nodes.append(frame)
                elif frame_names and frame['name'] in frame_names:
                    frame_nodes.append(frame)
        
        if not frame_nodes:
            print("No frames found to export")
            return {'exported': 0, 'files': []}
        
        print(f"Found {len(frame_nodes)} frames to export")
        return self._export_nodes(file_key, frame_nodes)
    
    def export_components(self, file_key: str, component_names: List[str] = None) -> Dict[str, Any]:
        """Export all components or specific components from a file"""
        
        file_data = self.client.get_file(file_key)
        component_nodes = self._find_components(file_data)
        
        if component_names:
            component_nodes = [c for c in component_nodes if c['name'] in component_names]
        
        if not component_nodes:
            print("No components found to export")
            return {'exported': 0, 'files': []}
        
        print(f"Found {len(component_nodes)} components to export")
        return self._export_nodes(file_key, component_nodes)
    
    def export_pages(self, file_key: str, page_names: List[str] = None) -> Dict[str, Any]:
        """Export all pages or specific pages as complete images"""
        
        file_data = self.client.get_file(file_key)
        
        pages = []
        for child in file_data.get('document', {}).get('children', []):
            if child.get('type') == 'CANVAS':
                if not page_names or child.get('name') in page_names:
                    pages.append(child)
        
        if not pages:
            print("No pages found to export")
            return {'exported': 0, 'files': []}
        
        print(f"Found {len(pages)} pages to export")
        return self._export_nodes(file_key, pages)
    
    def export_custom_selection(self, file_key: str, node_ids: List[str]) -> Dict[str, Any]:
        """Export specific nodes by ID"""
        
        # Get node information
        nodes_data = self.client.get_file_nodes(file_key, node_ids)
        
        if 'nodes' not in nodes_data:
            print("No nodes found with provided IDs")
            return {'exported': 0, 'files': []}
        
        nodes = []
        for node_id, node_info in nodes_data['nodes'].items():
            if 'document' in node_info:
                node = node_info['document']
                node['id'] = node_id  # Ensure ID is present
                nodes.append(node)
        
        print(f"Found {len(nodes)} nodes to export")
        return self._export_nodes(file_key, nodes)
    
    def export_design_tokens(self, file_key: str, output_format: str = 'json') -> str:
        """Export design tokens (colors, typography, effects) in various formats"""
        
        file_data = self.client.get_file(file_key)
        
        # Extract design tokens
        tokens = {
            'colors': self._extract_color_tokens(file_data),
            'typography': self._extract_typography_tokens(file_data),
            'effects': self._extract_effect_tokens(file_data),
            'spacing': self._extract_spacing_tokens(file_data)
        }
        
        # Format output
        if output_format == 'css':
            output_content = self._tokens_to_css(tokens)
            output_file = Path(self.config.output_dir) / 'design-tokens.css'
        elif output_format == 'scss':
            output_content = self._tokens_to_scss(tokens)
            output_file = Path(self.config.output_dir) / 'design-tokens.scss'
        elif output_format == 'js':
            output_content = self._tokens_to_js(tokens)
            output_file = Path(self.config.output_dir) / 'design-tokens.js'
        else:  # json
            output_content = json.dumps(tokens, indent=2)
            output_file = Path(self.config.output_dir) / 'design-tokens.json'
        
        # Write output file
        with open(output_file, 'w') as f:
            f.write(output_content)
        
        print(f"Design tokens exported to {output_file}")
        return str(output_file)
    
    def create_client_package(self, file_key: str, package_name: str = None) -> str:
        """Create a complete client delivery package with all assets"""
        
        if not package_name:
            file_data = self.client.get_file(file_key)
            package_name = file_data.get('name', 'figma-package').replace(' ', '-').lower()
        
        package_dir = Path(self.config.output_dir) / package_name
        package_dir.mkdir(parents=True, exist_ok=True)
        
        # Export all asset types
        results = {}
        
        # 1. Export all frames
        self.config.output_dir = str(package_dir / 'frames')
        Path(self.config.output_dir).mkdir(exist_ok=True)
        results['frames'] = self.export_frames(file_key)
        
        # 2. Export all components
        self.config.output_dir = str(package_dir / 'components')
        Path(self.config.output_dir).mkdir(exist_ok=True)
        results['components'] = self.export_components(file_key)
        
        # 3. Export design tokens
        self.config.output_dir = str(package_dir)
        results['tokens'] = {
            'json': self.export_design_tokens(file_key, 'json'),
            'css': self.export_design_tokens(file_key, 'css'),
            'scss': self.export_design_tokens(file_key, 'scss')
        }
        
        # 4. Create documentation
        doc_file = package_dir / 'README.md'
        self._create_package_documentation(file_key, doc_file, results)
        
        print(f"Client package created at {package_dir}")
        return str(package_dir)
    
    def _export_nodes(self, file_key: str, nodes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Export nodes with all configured formats and scales"""
        
        exported_files = []
        total_exports = len(nodes) * len(self.config.formats) * len(self.config.scales)
        current_export = 0
        
        for node in nodes:
            node_id = node['id']
            node_name = self._sanitize_filename(node.get('name', 'untitled'))
            
            for format in self.config.formats:
                for scale in self.config.scales:
                    current_export += 1
                    print(f"Exporting {current_export}/{total_exports}: {node_name} ({format} @ {scale}x)")
                    
                    # Get export URLs from Figma
                    try:
                        export_data = self.client.export_images(
                            file_key, [node_id], 
                            format=format, scale=scale
                        )
                        
                        if 'images' in export_data and node_id in export_data['images']:
                            image_url = export_data['images'][node_id]
                            
                            if image_url:
                                # Generate filename
                                filename = self.config.naming_pattern.format(
                                    name=node_name,
                                    id=node_id,
                                    format=format,
                                    scale=f'{scale}x' if scale != 1.0 else ''
                                )
                                
                                # Organize by format if configured
                                if self.config.organize_by_format:
                                    format_dir = Path(self.config.output_dir) / format
                                    format_dir.mkdir(exist_ok=True)
                                    output_path = format_dir / filename
                                else:
                                    output_path = Path(self.config.output_dir) / filename
                                
                                # Skip if file exists and skip_existing is True
                                if self.config.skip_existing and output_path.exists():
                                    print(f"  Skipping existing file: {output_path}")
                                    continue
                                
                                # Download the image
                                self.client.download_image(str(image_url), str(output_path))
                                
                                exported_files.append({
                                    'path': str(output_path),
                                    'node_id': node_id,
                                    'node_name': node_name,
                                    'format': format,
                                    'scale': scale,
                                    'url': image_url
                                })
                                
                                print(f"  Saved: {output_path}")
                            else:
                                print(f"  Warning: No image URL returned for {node_name}")
                    
                    except Exception as e:
                        print(f"  Error exporting {node_name}: {e}")
                        continue
                    
                    # Rate limiting
                    time.sleep(0.5)
        
        # Create manifest file
        if self.config.create_manifest:
            manifest_path = Path(self.config.output_dir) / 'export-manifest.json'
            manifest_data = {
                'exported_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'file_key': file_key,
                'total_files': len(exported_files),
                'config': {
                    'formats': self.config.formats,
                    'scales': self.config.scales,
                    'naming_pattern': self.config.naming_pattern
                },
                'files': exported_files
            }
            
            with open(manifest_path, 'w') as f:
                json.dump(manifest_data, f, indent=2)
            
            print(f"Manifest created: {manifest_path}")
        
        return {
            'exported': len(exported_files),
            'files': exported_files
        }
    
    def _find_frames(self, file_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find all frames in the file"""
        frames = []
        
        def traverse_node(node):
            if node.get('type') == 'FRAME':
                frames.append(node)
            
            for child in node.get('children', []):
                traverse_node(child)
        
        if 'document' in file_data:
            traverse_node(file_data['document'])
        
        return frames
    
    def _find_components(self, file_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find all components in the file"""
        components = []
        
        def traverse_node(node):
            if node.get('type') == 'COMPONENT':
                components.append(node)
            
            for child in node.get('children', []):
                traverse_node(child)
        
        if 'document' in file_data:
            traverse_node(file_data['document'])
        
        return components
    
    def _extract_color_tokens(self, file_data: Dict[str, Any]) -> Dict[str, str]:
        """Extract color design tokens from file styles"""
        colors = {}
        
        for style_id, style in file_data.get('styles', {}).items():
            if style.get('styleType') == 'FILL':
                name = style.get('name', '').replace('/', '-').lower()
                # This would need to be enhanced with actual color values
                # from the style definition
                colors[name] = f"#{style_id[:6]}"  # Placeholder
        
        return colors
    
    def _extract_typography_tokens(self, file_data: Dict[str, Any]) -> Dict[str, Dict]:
        """Extract typography design tokens"""
        typography = {}
        
        for style_id, style in file_data.get('styles', {}).items():
            if style.get('styleType') == 'TEXT':
                name = style.get('name', '').replace('/', '-').lower()
                typography[name] = {
                    'fontSize': '16px',  # Placeholder - would need actual values
                    'fontWeight': '400',
                    'lineHeight': '1.5',
                    'fontFamily': 'Inter'
                }
        
        return typography
    
    def _extract_effect_tokens(self, file_data: Dict[str, Any]) -> Dict[str, str]:
        """Extract effect design tokens (shadows, etc.)"""
        effects = {}
        
        for style_id, style in file_data.get('styles', {}).items():
            if style.get('styleType') == 'EFFECT':
                name = style.get('name', '').replace('/', '-').lower()
                effects[name] = "0 2px 4px rgba(0,0,0,0.1)"  # Placeholder
        
        return effects
    
    def _extract_spacing_tokens(self, file_data: Dict[str, Any]) -> Dict[str, str]:
        """Extract spacing tokens from layout patterns"""
        # This would analyze common spacing patterns in the design
        return {
            'xs': '4px',
            'sm': '8px', 
            'md': '16px',
            'lg': '24px',
            'xl': '32px'
        }
    
    def _tokens_to_css(self, tokens: Dict[str, Any]) -> str:
        """Convert tokens to CSS custom properties"""
        css_content = ":root {\n"
        
        # Colors
        for name, value in tokens['colors'].items():
            css_content += f"  --color-{name}: {value};\n"
        
        # Typography
        for name, values in tokens['typography'].items():
            for prop, value in values.items():
                css_content += f"  --{name}-{prop.lower()}: {value};\n"
        
        # Effects
        for name, value in tokens['effects'].items():
            css_content += f"  --effect-{name}: {value};\n"
        
        # Spacing
        for name, value in tokens['spacing'].items():
            css_content += f"  --spacing-{name}: {value};\n"
        
        css_content += "}\n"
        return css_content
    
    def _tokens_to_scss(self, tokens: Dict[str, Any]) -> str:
        """Convert tokens to SCSS variables"""
        scss_content = "// Design Tokens\n\n"
        
        # Colors
        scss_content += "// Colors\n"
        for name, value in tokens['colors'].items():
            scss_content += f"${name.replace('-', '_')}: {value};\n"
        
        scss_content += "\n// Typography\n"
        for name, values in tokens['typography'].items():
            for prop, value in values.items():
                scss_content += f"${name.replace('-', '_')}_{prop.lower()}: {value};\n"
        
        return scss_content
    
    def _tokens_to_js(self, tokens: Dict[str, Any]) -> str:
        """Convert tokens to JavaScript/JSON module"""
        return f"export const designTokens = {json.dumps(tokens, indent=2)};\n\nexport default designTokens;\n"
    
    def _sanitize_filename(self, name: str) -> str:
        """Convert name to safe filename"""
        # Remove/replace invalid characters
        safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_'))
        safe_name = safe_name.strip().replace(' ', '-').lower()
        return safe_name or 'untitled'
    
    def _create_package_documentation(self, file_key: str, doc_path: Path, results: Dict[str, Any]):
        """Create documentation for the exported package"""
        
        file_data = self.client.get_file(file_key)
        
        doc_content = f"""# {file_data.get('name', 'Figma Export')}
        
Exported from Figma on {time.strftime('%Y-%m-%d %H:%M:%S')}

## File Information
- **File Key**: {file_key}
- **Last Modified**: {file_data.get('lastModified', 'Unknown')}
- **Version**: {file_data.get('version', 'Unknown')}

## Package Contents

### Frames ({results.get('frames', {}).get('exported', 0)} files)
All page frames exported in configured formats
Location: `./frames/`

### Components ({results.get('components', {}).get('exported', 0)} files)
All reusable components exported for development handoff
Location: `./components/`

### Design Tokens
Design system tokens in multiple formats:
- `design-tokens.json` - Raw token data
- `design-tokens.css` - CSS custom properties
- `design-tokens.scss` - SCSS variables

## Usage

### Web Development
```css
/* Import CSS tokens */
@import './design-tokens.css';

.my-component {{
  color: var(--color-primary);
  font-size: var(--typography-body-fontsize);
}}
```

### React/JavaScript
```javascript
import tokens from './design-tokens.js';

const MyComponent = () => (
  <div style={{{{color: tokens.colors.primary}}}}>
    Content
  </div>
);
```

## Support
For questions about this export or design implementation, contact your design team.
"""
        
        with open(doc_path, 'w') as f:
            f.write(doc_content)

def main():
    """CLI interface for export operations"""
    parser = argparse.ArgumentParser(description='Figma Export Manager')
    parser.add_argument('command', choices=[
        'export-frames', 'export-components', 'export-pages', 'export-nodes',
        'export-tokens', 'client-package'
    ])
    parser.add_argument('file_key', help='Figma file key or URL')
    parser.add_argument('node_ids', nargs='?', help='Comma-separated node IDs for export-nodes')
    parser.add_argument('--formats', default='png', help='Export formats (comma-separated)')
    parser.add_argument('--scales', default='1.0', help='Export scales (comma-separated)')
    parser.add_argument('--output-dir', default='./figma-exports', help='Output directory')
    parser.add_argument('--token-format', default='json', choices=['json', 'css', 'scss', 'js'])
    parser.add_argument('--package-name', help='Name for client package')
    parser.add_argument('--frame-names', help='Specific frame names to export (comma-separated)')
    parser.add_argument('--component-names', help='Specific component names to export (comma-separated)')
    
    args = parser.parse_args()
    
    try:
        client = FigmaClient()
        file_key = client.parse_file_url(args.file_key)
        
        # Configure export settings
        config = ExportConfig(
            formats=args.formats.split(','),
            scales=[float(s) for s in args.scales.split(',')],
            output_dir=args.output_dir
        )
        
        manager = ExportManager(client, config)
        
        if args.command == 'export-frames':
            frame_names = args.frame_names.split(',') if args.frame_names else None
            result = manager.export_frames(file_key, frame_names=frame_names)
            
        elif args.command == 'export-components':
            component_names = args.component_names.split(',') if args.component_names else None
            result = manager.export_components(file_key, component_names=component_names)
            
        elif args.command == 'export-pages':
            result = manager.export_pages(file_key)
            
        elif args.command == 'export-nodes':
            if not args.node_ids:
                parser.error('node_ids required for export-nodes command')
            result = manager.export_custom_selection(file_key, args.node_ids.split(','))
            
        elif args.command == 'export-tokens':
            result = manager.export_design_tokens(file_key, args.token_format)
            print(f"Design tokens exported: {result}")
            return
            
        elif args.command == 'client-package':
            result = manager.create_client_package(file_key, args.package_name)
            print(f"Client package created: {result}")
            return
        
        print(f"Export completed: {result['exported']} files exported")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()