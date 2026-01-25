#!/usr/bin/env python3
"""
Figma Style Auditor - Design system analysis and consistency checking
Analyzes files for brand compliance, accessibility, and design system health.
"""

import os
import sys
import json
import math
import time
from typing import Dict, List, Optional, Union, Any, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import argparse
import colorsys
try:
    from figma_client import FigmaClient
except ImportError:
    # Handle case where script is run directly
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent))
    from figma_client import FigmaClient

@dataclass
class AuditConfig:
    """Configuration for design system audits"""
    check_accessibility: bool = True
    check_brand_compliance: bool = True
    check_consistency: bool = True
    generate_report: bool = True
    min_contrast_ratio: float = 4.5  # WCAG AA standard
    min_touch_target: float = 44  # iOS/Material Design standard
    brand_colors: List[str] = field(default_factory=list)
    brand_fonts: List[str] = field(default_factory=list)

@dataclass
class AuditIssue:
    """Represents a design issue found during audit"""
    severity: str  # 'error', 'warning', 'info'
    category: str  # 'accessibility', 'brand', 'consistency'
    message: str
    node_id: str = None
    node_name: str = None
    suggestions: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)

class StyleAuditor:
    """Comprehensive design system auditor for Figma files"""
    
    def __init__(self, figma_client: FigmaClient, config: AuditConfig = None):
        self.client = figma_client
        self.config = config or AuditConfig()
        self.issues: List[AuditIssue] = []
    
    def audit_file(self, file_key: str) -> Dict[str, Any]:
        """Perform comprehensive audit of a Figma file"""
        
        print(f"Starting audit of file: {file_key}")
        self.issues.clear()
        
        # Get file data
        file_data = self.client.get_file(file_key)
        
        # Run audit checks
        if self.config.check_accessibility:
            self._audit_accessibility(file_data)
        
        if self.config.check_brand_compliance:
            self._audit_brand_compliance(file_data)
        
        if self.config.check_consistency:
            self._audit_consistency(file_data)
        
        # Generate summary
        summary = self._generate_summary()
        
        print(f"Audit completed: {len(self.issues)} issues found")
        return {
            'file_key': file_key,
            'file_name': file_data.get('name', 'Unknown'),
            'audit_timestamp': time.time(),
            'summary': summary,
            'issues': [self._issue_to_dict(issue) for issue in self.issues],
            'recommendations': self._generate_recommendations()
        }
    
    def audit_multiple_files(self, file_keys: List[str]) -> Dict[str, Any]:
        """Audit multiple files and generate comparative analysis"""
        
        all_results = {}
        aggregated_issues = []
        
        for file_key in file_keys:
            try:
                result = self.audit_file(file_key)
                all_results[file_key] = result
                aggregated_issues.extend(self.issues)
                print(f"✓ Audited {result['file_name']}: {len(result['issues'])} issues")
            except Exception as e:
                print(f"✗ Failed to audit {file_key}: {e}")
                all_results[file_key] = {'error': str(e)}
        
        # Generate cross-file analysis
        cross_file_analysis = self._analyze_cross_file_patterns(all_results)
        
        return {
            'individual_audits': all_results,
            'cross_file_analysis': cross_file_analysis,
            'total_files': len(file_keys),
            'successful_audits': len([r for r in all_results.values() if 'error' not in r])
        }
    
    def _audit_accessibility(self, file_data: Dict[str, Any]):
        """Check accessibility compliance (WCAG guidelines)"""
        
        def audit_node_accessibility(node):
            node_type = node.get('type', '')
            node_name = node.get('name', '')
            node_id = node.get('id', '')
            
            # Check text contrast
            if node_type == 'TEXT':
                self._check_text_contrast(node)
            
            # Check touch targets
            if node_type in ['COMPONENT', 'INSTANCE', 'FRAME'] and 'button' in node_name.lower():
                self._check_touch_target_size(node)
            
            # Check focus indicators
            if 'interactive' in node_name.lower() or 'button' in node_name.lower():
                self._check_focus_indicators(node)
            
            # Recursively check children
            for child in node.get('children', []):
                audit_node_accessibility(child)
        
        if 'document' in file_data:
            audit_node_accessibility(file_data['document'])
    
    def _audit_brand_compliance(self, file_data: Dict[str, Any]):
        """Check compliance with brand guidelines"""
        
        if not self.config.brand_colors and not self.config.brand_fonts:
            return  # Skip if no brand guidelines configured
        
        def audit_node_brand(node):
            # Check color compliance
            if 'fills' in node:
                self._check_brand_colors(node)
            
            # Check font compliance
            if node.get('type') == 'TEXT':
                self._check_brand_fonts(node)
            
            # Recursively check children
            for child in node.get('children', []):
                audit_node_brand(child)
        
        if 'document' in file_data:
            audit_node_brand(file_data['document'])
    
    def _audit_consistency(self, file_data: Dict[str, Any]):
        """Check internal consistency within the file"""
        
        # Collect all styles for analysis
        colors_used = []
        fonts_used = []
        spacing_used = []
        
        def collect_styles(node):
            # Collect colors
            if 'fills' in node:
                for fill in node.get('fills', []):
                    if fill.get('type') == 'SOLID':
                        color = fill.get('color', {})
                        if color:
                            colors_used.append({
                                'color': color,
                                'node_id': node.get('id'),
                                'node_name': node.get('name', '')
                            })
            
            # Collect fonts
            if node.get('type') == 'TEXT':
                style = node.get('style', {})
                if style:
                    fonts_used.append({
                        'font_family': style.get('fontFamily', ''),
                        'font_size': style.get('fontSize', 0),
                        'font_weight': style.get('fontWeight', 400),
                        'node_id': node.get('id'),
                        'node_name': node.get('name', '')
                    })
            
            # Collect spacing (approximation from layout)
            if 'children' in node and len(node['children']) > 1:
                # This would need more sophisticated analysis
                pass
            
            # Recursively collect from children
            for child in node.get('children', []):
                collect_styles(child)
        
        if 'document' in file_data:
            collect_styles(file_data['document'])
        
        # Analyze collected styles
        self._analyze_color_consistency(colors_used)
        self._analyze_typography_consistency(fonts_used)
    
    def _check_text_contrast(self, text_node: Dict[str, Any]):
        """Check if text has sufficient contrast against background"""
        
        # This is a simplified implementation
        # Real implementation would need to calculate actual contrast
        fills = text_node.get('fills', [])
        if not fills:
            return
        
        text_color = fills[0].get('color', {})
        if not text_color:
            return
        
        # For now, assume white background (would need parent background detection)
        bg_color = {'r': 1, 'g': 1, 'b': 1}  # White
        
        contrast_ratio = self._calculate_contrast_ratio(text_color, bg_color)
        
        if contrast_ratio < self.config.min_contrast_ratio:
            self.issues.append(AuditIssue(
                severity='error',
                category='accessibility',
                message=f'Insufficient color contrast: {contrast_ratio:.1f}:1 (minimum: {self.config.min_contrast_ratio}:1)',
                node_id=text_node.get('id'),
                node_name=text_node.get('name', ''),
                suggestions=[
                    'Darken text color or lighten background',
                    'Use high contrast color combinations',
                    'Test with accessibility tools'
                ],
                details={'contrast_ratio': contrast_ratio, 'text_color': text_color}
            ))
    
    def _check_touch_target_size(self, node: Dict[str, Any]):
        """Check if interactive elements meet minimum touch target size"""
        
        bounds = node.get('absoluteBoundingBox', {})
        if not bounds:
            return
        
        width = bounds.get('width', 0)
        height = bounds.get('height', 0)
        
        if width < self.config.min_touch_target or height < self.config.min_touch_target:
            self.issues.append(AuditIssue(
                severity='warning',
                category='accessibility',
                message=f'Touch target too small: {width}×{height}px (minimum: {self.config.min_touch_target}×{self.config.min_touch_target}px)',
                node_id=node.get('id'),
                node_name=node.get('name', ''),
                suggestions=[
                    f'Increase size to at least {self.config.min_touch_target}×{self.config.min_touch_target}px',
                    'Add padding around interactive elements',
                    'Consider user interaction patterns'
                ],
                details={'current_size': {'width': width, 'height': height}}
            ))
    
    def _check_focus_indicators(self, node: Dict[str, Any]):
        """Check if interactive elements have proper focus indicators"""
        
        # This would check for focus states, outlines, etc.
        # For now, just flag interactive elements that might need focus indicators
        
        effects = node.get('effects', [])
        has_focus_effect = any(
            effect.get('type') == 'DROP_SHADOW' and 
            'focus' in str(effect).lower() 
            for effect in effects
        )
        
        if not has_focus_effect:
            self.issues.append(AuditIssue(
                severity='info',
                category='accessibility',
                message='Interactive element may need focus indicator',
                node_id=node.get('id'),
                node_name=node.get('name', ''),
                suggestions=[
                    'Add focus state with visible outline',
                    'Use consistent focus indicator style',
                    'Test keyboard navigation'
                ]
            ))
    
    def _check_brand_colors(self, node: Dict[str, Any]):
        """Check if colors match brand guidelines"""
        
        if not self.config.brand_colors:
            return
        
        fills = node.get('fills', [])
        for fill in fills:
            if fill.get('type') == 'SOLID':
                color = fill.get('color', {})
                if color:
                    hex_color = self._rgb_to_hex(color)
                    
                    if hex_color not in self.config.brand_colors:
                        # Check if it's close to a brand color
                        closest_brand_color = self._find_closest_brand_color(hex_color)
                        
                        self.issues.append(AuditIssue(
                            severity='warning',
                            category='brand',
                            message=f'Non-brand color used: {hex_color}',
                            node_id=node.get('id'),
                            node_name=node.get('name', ''),
                            suggestions=[
                                f'Consider using brand color: {closest_brand_color}',
                                'Check brand color palette',
                                'Use design system colors'
                            ],
                            details={'used_color': hex_color, 'suggested_color': closest_brand_color}
                        ))
    
    def _check_brand_fonts(self, text_node: Dict[str, Any]):
        """Check if fonts match brand guidelines"""
        
        if not self.config.brand_fonts:
            return
        
        style = text_node.get('style', {})
        font_family = style.get('fontFamily', '')
        
        if font_family and font_family not in self.config.brand_fonts:
            self.issues.append(AuditIssue(
                severity='warning',
                category='brand',
                message=f'Non-brand font used: {font_family}',
                node_id=text_node.get('id'),
                node_name=text_node.get('name', ''),
                suggestions=[
                    f'Use brand fonts: {", ".join(self.config.brand_fonts)}',
                    'Check typography guidelines',
                    'Maintain font consistency'
                ],
                details={'used_font': font_family, 'brand_fonts': self.config.brand_fonts}
            ))
    
    def _analyze_color_consistency(self, colors_used: List[Dict[str, Any]]):
        """Analyze color usage patterns for consistency issues"""
        
        # Group similar colors
        color_groups = {}
        
        for color_data in colors_used:
            color = color_data['color']
            hex_color = self._rgb_to_hex(color)
            
            # Find similar colors (within tolerance)
            similar_group = None
            for group_color in color_groups.keys():
                if self._colors_are_similar(hex_color, group_color):
                    similar_group = group_color
                    break
            
            if similar_group:
                color_groups[similar_group].append(color_data)
            else:
                color_groups[hex_color] = [color_data]
        
        # Flag groups with multiple similar but not identical colors
        for base_color, group in color_groups.items():
            if len(group) > 1:
                unique_colors = set(self._rgb_to_hex(item['color']) for item in group)
                if len(unique_colors) > 1:
                    self.issues.append(AuditIssue(
                        severity='info',
                        category='consistency',
                        message=f'Multiple similar colors found: {", ".join(unique_colors)}',
                        suggestions=[
                            'Standardize similar colors',
                            'Use design system color tokens',
                            'Review color palette'
                        ],
                        details={'similar_colors': list(unique_colors), 'usage_count': len(group)}
                    ))
    
    def _analyze_typography_consistency(self, fonts_used: List[Dict[str, Any]]):
        """Analyze typography usage for consistency"""
        
        # Group by font family and size
        font_combinations = {}
        
        for font_data in fonts_used:
            key = f"{font_data['font_family']}-{font_data['font_size']}pt-{font_data['font_weight']}"
            if key not in font_combinations:
                font_combinations[key] = []
            font_combinations[key].append(font_data)
        
        # Look for too many font variations
        families = set(font['font_family'] for font in fonts_used)
        sizes = set(font['font_size'] for font in fonts_used)
        
        if len(families) > 3:
            self.issues.append(AuditIssue(
                severity='warning',
                category='consistency',
                message=f'Too many font families: {len(families)} ({", ".join(families)})',
                suggestions=[
                    'Reduce to 2-3 font families maximum',
                    'Establish typography hierarchy',
                    'Use consistent font pairing'
                ]
            ))
        
        if len(sizes) > 8:
            self.issues.append(AuditIssue(
                severity='info',
                category='consistency',
                message=f'Many font sizes used: {len(sizes)} different sizes',
                suggestions=[
                    'Create modular typography scale',
                    'Reduce to 6-8 standard sizes',
                    'Use consistent size progression'
                ]
            ))
    
    def _calculate_contrast_ratio(self, color1: Dict[str, float], color2: Dict[str, float]) -> float:
        """Calculate WCAG contrast ratio between two colors"""
        
        def get_luminance(color):
            """Calculate relative luminance"""
            def linearize(val):
                if val <= 0.03928:
                    return val / 12.92
                else:
                    return pow((val + 0.055) / 1.055, 2.4)
            
            r = linearize(color.get('r', 0))
            g = linearize(color.get('g', 0))  
            b = linearize(color.get('b', 0))
            
            return 0.2126 * r + 0.7152 * g + 0.0722 * b
        
        lum1 = get_luminance(color1)
        lum2 = get_luminance(color2)
        
        lighter = max(lum1, lum2)
        darker = min(lum1, lum2)
        
        return (lighter + 0.05) / (darker + 0.05)
    
    def _rgb_to_hex(self, color: Dict[str, float]) -> str:
        """Convert RGB color to hex string"""
        r = int(color.get('r', 0) * 255)
        g = int(color.get('g', 0) * 255)
        b = int(color.get('b', 0) * 255)
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _colors_are_similar(self, color1: str, color2: str, tolerance: int = 30) -> bool:
        """Check if two hex colors are similar within tolerance"""
        
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        rgb1 = hex_to_rgb(color1)
        rgb2 = hex_to_rgb(color2)
        
        distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)))
        return distance < tolerance
    
    def _find_closest_brand_color(self, hex_color: str) -> str:
        """Find the closest brand color to the given color"""
        
        if not self.config.brand_colors:
            return hex_color
        
        min_distance = float('inf')
        closest_color = self.config.brand_colors[0]
        
        for brand_color in self.config.brand_colors:
            if self._colors_are_similar(hex_color, brand_color, tolerance=255):  # Use max tolerance for distance calc
                distance = self._color_distance(hex_color, brand_color)
                if distance < min_distance:
                    min_distance = distance
                    closest_color = brand_color
        
        return closest_color
    
    def _color_distance(self, color1: str, color2: str) -> float:
        """Calculate Euclidean distance between two colors"""
        
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        rgb1 = hex_to_rgb(color1)
        rgb2 = hex_to_rgb(color2)
        
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)))
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate audit summary statistics"""
        
        summary = {
            'total_issues': len(self.issues),
            'by_severity': {
                'error': len([i for i in self.issues if i.severity == 'error']),
                'warning': len([i for i in self.issues if i.severity == 'warning']),
                'info': len([i for i in self.issues if i.severity == 'info'])
            },
            'by_category': {
                'accessibility': len([i for i in self.issues if i.category == 'accessibility']),
                'brand': len([i for i in self.issues if i.category == 'brand']),
                'consistency': len([i for i in self.issues if i.category == 'consistency'])
            }
        }
        
        # Calculate overall score (0-100)
        max_score = 100
        error_penalty = 10
        warning_penalty = 3
        info_penalty = 1
        
        penalty = (summary['by_severity']['error'] * error_penalty +
                  summary['by_severity']['warning'] * warning_penalty +
                  summary['by_severity']['info'] * info_penalty)
        
        summary['score'] = max(0, max_score - penalty)
        summary['grade'] = self._score_to_grade(summary['score'])
        
        return summary
    
    def _score_to_grade(self, score: int) -> str:
        """Convert numeric score to letter grade"""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
    
    def _generate_recommendations(self) -> List[str]:
        """Generate overall recommendations based on audit results"""
        
        recommendations = []
        
        error_count = len([i for i in self.issues if i.severity == 'error'])
        warning_count = len([i for i in self.issues if i.severity == 'warning'])
        
        if error_count > 0:
            recommendations.append(f"Fix {error_count} critical accessibility issues immediately")
        
        if warning_count > 5:
            recommendations.append("Review and address design consistency issues")
        
        brand_issues = len([i for i in self.issues if i.category == 'brand'])
        if brand_issues > 0:
            recommendations.append("Establish and enforce brand guidelines")
        
        consistency_issues = len([i for i in self.issues if i.category == 'consistency'])
        if consistency_issues > 3:
            recommendations.append("Create and apply design system standards")
        
        if not recommendations:
            recommendations.append("Great work! Consider periodic design system reviews")
        
        return recommendations
    
    def _analyze_cross_file_patterns(self, all_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze patterns across multiple files"""
        
        # This would analyze common issues across files
        # For now, return basic aggregation
        
        total_issues = 0
        common_issues = {}
        
        for file_key, result in all_results.items():
            if 'error' not in result:
                total_issues += result['summary']['total_issues']
                
                for issue in result['issues']:
                    issue_type = f"{issue['category']}:{issue['message'].split(':')[0]}"
                    common_issues[issue_type] = common_issues.get(issue_type, 0) + 1
        
        # Find most common issues
        most_common = sorted(common_issues.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total_issues_across_files': total_issues,
            'most_common_issues': most_common,
            'files_with_errors': len([r for r in all_results.values() if 'error' not in r and r['summary']['by_severity']['error'] > 0])
        }
    
    def _issue_to_dict(self, issue: AuditIssue) -> Dict[str, Any]:
        """Convert AuditIssue to dictionary for JSON serialization"""
        return {
            'severity': issue.severity,
            'category': issue.category,
            'message': issue.message,
            'node_id': issue.node_id,
            'node_name': issue.node_name,
            'suggestions': issue.suggestions,
            'details': issue.details
        }
    
    def generate_report(self, audit_results: Dict[str, Any], output_path: str = None) -> str:
        """Generate comprehensive audit report"""
        
        if not output_path:
            output_path = 'figma-audit-report.html'
        
        html_report = self._create_html_report(audit_results)
        
        with open(output_path, 'w') as f:
            f.write(html_report)
        
        print(f"Audit report generated: {output_path}")
        return output_path
    
    def _create_html_report(self, audit_results: Dict[str, Any]) -> str:
        """Create HTML audit report"""
        
        # This would generate a comprehensive HTML report
        # For now, return basic HTML structure
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Figma Design Audit Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 40px; }}
        .header {{ border-bottom: 2px solid #007AFF; padding-bottom: 20px; margin-bottom: 30px; }}
        .summary {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 30px; }}
        .issue {{ margin-bottom: 20px; padding: 15px; border-left: 4px solid #ddd; }}
        .error {{ border-color: #dc3545; background: #f8d7da; }}
        .warning {{ border-color: #ffc107; background: #fff3cd; }}
        .info {{ border-color: #17a2b8; background: #d1ecf1; }}
        .grade {{ font-size: 48px; font-weight: bold; color: #007AFF; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Figma Design Audit Report</h1>
        <p>File: {audit_results.get('file_name', 'Unknown')}</p>
        <p>Audit Date: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="summary">
        <h2>Summary</h2>
        <div style="display: flex; align-items: center; gap: 40px;">
            <div>
                <div class="grade">{audit_results['summary']['grade']}</div>
                <div>Score: {audit_results['summary']['score']}/100</div>
            </div>
            <div>
                <p><strong>Total Issues:</strong> {audit_results['summary']['total_issues']}</p>
                <p><strong>Errors:</strong> {audit_results['summary']['by_severity']['error']}</p>
                <p><strong>Warnings:</strong> {audit_results['summary']['by_severity']['warning']}</p>
                <p><strong>Info:</strong> {audit_results['summary']['by_severity']['info']}</p>
            </div>
        </div>
    </div>
    
    <h2>Issues Found</h2>
"""
        
        for issue in audit_results['issues']:
            severity_class = issue['severity']
            html += f"""
    <div class="issue {severity_class}">
        <h3>{issue['category'].title()}: {issue['message']}</h3>
        <p><strong>Node:</strong> {issue.get('node_name', 'N/A')} ({issue.get('node_id', 'N/A')})</p>
        <p><strong>Suggestions:</strong></p>
        <ul>
"""
            for suggestion in issue.get('suggestions', []):
                html += f"<li>{suggestion}</li>\n"
            
            html += "</ul></div>\n"
        
        html += """
    <h2>Recommendations</h2>
    <ul>
"""
        
        for rec in audit_results['recommendations']:
            html += f"<li>{rec}</li>\n"
        
        html += """
    </ul>
</body>
</html>"""
        
        return html

def main():
    """CLI interface for style auditing"""
    parser = argparse.ArgumentParser(description='Figma Style Auditor')
    parser.add_argument('command', choices=['audit-file', 'audit-multiple', 'audit-brand'])
    parser.add_argument('file_keys', help='File key(s) or path to file list')
    parser.add_argument('--output', help='Output file for audit report')
    parser.add_argument('--brand-colors', help='Comma-separated list of brand hex colors')
    parser.add_argument('--brand-fonts', help='Comma-separated list of brand fonts')
    parser.add_argument('--min-contrast', type=float, default=4.5, help='Minimum contrast ratio')
    parser.add_argument('--generate-html', action='store_true', help='Generate HTML report')
    
    args = parser.parse_args()
    
    try:
        client = FigmaClient()
        
        # Configure auditor
        config = AuditConfig(
            min_contrast_ratio=args.min_contrast,
            brand_colors=args.brand_colors.split(',') if args.brand_colors else [],
            brand_fonts=args.brand_fonts.split(',') if args.brand_fonts else [],
            generate_report=args.generate_html
        )
        
        auditor = StyleAuditor(client, config)
        
        if args.command == 'audit-file':
            file_key = client.parse_file_url(args.file_keys)
            result = auditor.audit_file(file_key)
            
        elif args.command == 'audit-multiple':
            # Parse file keys (could be comma-separated or from file)
            if os.path.isfile(args.file_keys):
                with open(args.file_keys) as f:
                    file_keys = [line.strip() for line in f if line.strip()]
            else:
                file_keys = args.file_keys.split(',')
            
            file_keys = [client.parse_file_url(key) for key in file_keys]
            result = auditor.audit_multiple_files(file_keys)
        
        # Output results
        output_content = json.dumps(result, indent=2)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output_content)
            print(f"Audit results saved to {args.output}")
        else:
            print(output_content)
        
        # Generate HTML report if requested
        if args.generate_html and args.command == 'audit-file':
            html_path = args.output.replace('.json', '.html') if args.output else 'audit-report.html'
            auditor.generate_report(result, html_path)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()