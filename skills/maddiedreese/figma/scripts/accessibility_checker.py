#!/usr/bin/env python3
"""
Figma Accessibility Checker - WCAG compliance validation
Specialized accessibility audit with detailed WCAG compliance checking.
"""

import os
import sys
import json
import math
import time
from typing import Dict, List, Optional, Union, Any, Tuple
import argparse

try:
    from figma_client import FigmaClient
except ImportError:
    # Handle case where script is run directly
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent))
    from figma_client import FigmaClient

class AccessibilityChecker:
    """WCAG-focused accessibility checker for Figma designs"""
    
    def __init__(self, figma_client: FigmaClient):
        self.client = figma_client
    
    def check_wcag_compliance(self, file_key: str, level: str = 'AA') -> Dict[str, Any]:
        """Comprehensive WCAG compliance check"""
        
        print(f"Checking WCAG {level} compliance for file: {file_key}")
        
        file_data = self.client.get_file(file_key)
        
        results = {
            'file_key': file_key,
            'file_name': file_data.get('name', 'Unknown'),
            'wcag_level': level,
            'timestamp': time.time(),
            'compliance_score': 0,
            'issues': [],
            'summary': {}
        }
        
        # Run all WCAG checks
        self._check_color_contrast(file_data, results, level)
        self._check_touch_targets(file_data, results)
        self._check_text_sizing(file_data, results)
        self._check_focus_indicators(file_data, results)
        
        # Calculate compliance score
        results['compliance_score'] = self._calculate_compliance_score(results)
        results['summary'] = self._generate_summary(results)
        
        return results
    
    def _check_color_contrast(self, file_data: Dict[str, Any], results: Dict[str, Any], level: str):
        """Check color contrast ratios against WCAG standards"""
        
        contrast_requirements = {
            'AA': {'normal_text': 4.5, 'large_text': 3.0, 'ui_components': 3.0},
            'AAA': {'normal_text': 7.0, 'large_text': 4.5, 'ui_components': 4.5}
        }
        
        requirements = contrast_requirements[level]
        
        def check_node_contrast(node):
            if node.get('type') == 'TEXT':
                # Get text color
                fills = node.get('fills', [])
                if not fills:
                    return
                
                text_color = fills[0].get('color', {})
                if not text_color:
                    return
                
                # Estimate background color (simplified - would need parent analysis)
                bg_color = {'r': 1, 'g': 1, 'b': 1}  # Assume white background
                
                contrast_ratio = self._calculate_contrast_ratio(text_color, bg_color)
                
                # Determine if text is large
                style = node.get('style', {})
                font_size = style.get('fontSize', 16)
                font_weight = style.get('fontWeight', 400)
                
                is_large_text = font_size >= 18 or (font_size >= 14 and font_weight >= 700)
                required_ratio = requirements['large_text'] if is_large_text else requirements['normal_text']
                
                if contrast_ratio < required_ratio:
                    results['issues'].append({
                        'type': 'color_contrast',
                        'severity': 'error' if level == 'AA' else 'warning',
                        'message': f'Insufficient contrast: {contrast_ratio:.1f}:1 (required: {required_ratio}:1)',
                        'node_id': node.get('id'),
                        'node_name': node.get('name', ''),
                        'wcag_criterion': '1.4.3' if level == 'AA' else '1.4.6',
                        'details': {
                            'contrast_ratio': contrast_ratio,
                            'required_ratio': required_ratio,
                            'text_color': self._rgb_to_hex(text_color),
                            'is_large_text': is_large_text
                        }
                    })
            
            # Check children
            for child in node.get('children', []):
                check_node_contrast(child)
        
        if 'document' in file_data:
            check_node_contrast(file_data['document'])
    
    def _check_touch_targets(self, file_data: Dict[str, Any], results: Dict[str, Any]):
        """Check minimum touch target sizes (WCAG 2.5.5)"""
        
        min_size = 44  # iOS/WCAG standard
        
        def check_node_size(node):
            # Look for interactive elements
            node_name = node.get('name', '').lower()
            node_type = node.get('type', '')
            
            is_interactive = (
                'button' in node_name or 
                'link' in node_name or 
                node_type in ['COMPONENT', 'INSTANCE'] and 
                any(keyword in node_name for keyword in ['btn', 'tap', 'click', 'interactive'])
            )
            
            if is_interactive:
                bounds = node.get('absoluteBoundingBox', {})
                width = bounds.get('width', 0)
                height = bounds.get('height', 0)
                
                if width < min_size or height < min_size:
                    results['issues'].append({
                        'type': 'touch_target',
                        'severity': 'warning',
                        'message': f'Touch target too small: {width:.0f}×{height:.0f}px (minimum: {min_size}×{min_size}px)',
                        'node_id': node.get('id'),
                        'node_name': node.get('name', ''),
                        'wcag_criterion': '2.5.5',
                        'details': {
                            'width': width,
                            'height': height,
                            'min_size': min_size
                        }
                    })
            
            # Check children
            for child in node.get('children', []):
                check_node_size(child)
        
        if 'document' in file_data:
            check_node_size(file_data['document'])
    
    def _check_text_sizing(self, file_data: Dict[str, Any], results: Dict[str, Any]):
        """Check minimum text sizes for readability"""
        
        min_size = 12  # Minimum readable size
        recommended_size = 16  # Recommended for body text
        
        def check_text_size(node):
            if node.get('type') == 'TEXT':
                style = node.get('style', {})
                font_size = style.get('fontSize', 16)
                
                if font_size < min_size:
                    results['issues'].append({
                        'type': 'text_size',
                        'severity': 'error',
                        'message': f'Text too small: {font_size}px (minimum: {min_size}px)',
                        'node_id': node.get('id'),
                        'node_name': node.get('name', ''),
                        'wcag_criterion': '1.4.4',
                        'details': {
                            'font_size': font_size,
                            'min_size': min_size,
                            'characters': node.get('characters', '')[:50]
                        }
                    })
                elif font_size < recommended_size:
                    results['issues'].append({
                        'type': 'text_size',
                        'severity': 'info',
                        'message': f'Text smaller than recommended: {font_size}px (recommended: {recommended_size}px)',
                        'node_id': node.get('id'),
                        'node_name': node.get('name', ''),
                        'wcag_criterion': '1.4.4',
                        'details': {
                            'font_size': font_size,
                            'recommended_size': recommended_size
                        }
                    })
            
            # Check children
            for child in node.get('children', []):
                check_text_size(child)
        
        if 'document' in file_data:
            check_text_size(file_data['document'])
    
    def _check_focus_indicators(self, file_data: Dict[str, Any], results: Dict[str, Any]):
        """Check for focus indicators on interactive elements"""
        
        def check_focus_states(node):
            node_name = node.get('name', '').lower()
            node_type = node.get('type', '')
            
            is_interactive = (
                'button' in node_name or 
                'link' in node_name or 
                'input' in node_name or
                node_type in ['COMPONENT', 'INSTANCE']
            )
            
            if is_interactive:
                # Check for focus-related effects or states
                effects = node.get('effects', [])
                has_focus_indicator = any(
                    'focus' in str(effect).lower() or
                    effect.get('type') == 'DROP_SHADOW'
                    for effect in effects
                )
                
                if not has_focus_indicator:
                    results['issues'].append({
                        'type': 'focus_indicator',
                        'severity': 'info',
                        'message': 'Interactive element may need focus indicator',
                        'node_id': node.get('id'),
                        'node_name': node.get('name', ''),
                        'wcag_criterion': '2.4.7',
                        'details': {
                            'suggestion': 'Add visible focus state for keyboard navigation'
                        }
                    })
            
            # Check children
            for child in node.get('children', []):
                check_focus_states(child)
        
        if 'document' in file_data:
            check_focus_states(file_data['document'])
    
    def _calculate_contrast_ratio(self, color1: Dict[str, float], color2: Dict[str, float]) -> float:
        """Calculate WCAG contrast ratio between two colors"""
        
        def get_luminance(color):
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
    
    def _calculate_compliance_score(self, results: Dict[str, Any]) -> int:
        """Calculate overall compliance score (0-100)"""
        
        error_count = len([i for i in results['issues'] if i['severity'] == 'error'])
        warning_count = len([i for i in results['issues'] if i['severity'] == 'warning'])
        info_count = len([i for i in results['issues'] if i['severity'] == 'info'])
        
        # Scoring: errors are -10 points, warnings -3 points, info -1 point
        penalty = error_count * 10 + warning_count * 3 + info_count * 1
        score = max(0, 100 - penalty)
        
        return score
    
    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary of accessibility results"""
        
        issues_by_type = {}
        issues_by_severity = {'error': 0, 'warning': 0, 'info': 0}
        
        for issue in results['issues']:
            issue_type = issue['type']
            severity = issue['severity']
            
            issues_by_type[issue_type] = issues_by_type.get(issue_type, 0) + 1
            issues_by_severity[severity] += 1
        
        compliance_level = 'FAIL'
        if issues_by_severity['error'] == 0:
            if issues_by_severity['warning'] == 0:
                compliance_level = 'AAA'
            elif issues_by_severity['warning'] <= 2:
                compliance_level = 'AA'
            else:
                compliance_level = 'A'
        
        return {
            'total_issues': len(results['issues']),
            'issues_by_type': issues_by_type,
            'issues_by_severity': issues_by_severity,
            'compliance_level': compliance_level,
            'score': results['compliance_score']
        }
    
    def generate_accessibility_report(self, results: Dict[str, Any], output_path: str = None) -> str:
        """Generate detailed accessibility report"""
        
        if not output_path:
            output_path = f"accessibility-report-{int(time.time())}.html"
        
        html_report = self._create_accessibility_html_report(results)
        
        with open(output_path, 'w') as f:
            f.write(html_report)
        
        print(f"Accessibility report generated: {output_path}")
        return output_path
    
    def _create_accessibility_html_report(self, results: Dict[str, Any]) -> str:
        """Create comprehensive HTML accessibility report"""
        
        # Color coding for compliance levels
        level_colors = {
            'AAA': '#28a745',
            'AA': '#17a2b8', 
            'A': '#ffc107',
            'FAIL': '#dc3545'
        }
        
        level_color = level_colors.get(results['summary']['compliance_level'], '#6c757d')
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Accessibility Report - {results['file_name']}</title>
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
            margin: 40px; 
            line-height: 1.6;
            color: #333;
        }}
        .header {{ 
            border-bottom: 3px solid {level_color}; 
            padding-bottom: 20px; 
            margin-bottom: 30px; 
        }}
        .compliance-badge {{
            display: inline-block;
            background: {level_color};
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            font-weight: bold;
            font-size: 18px;
            margin: 10px 0;
        }}
        .score {{
            font-size: 48px;
            font-weight: bold;
            color: {level_color};
        }}
        .summary {{ 
            background: #f8f9fa; 
            padding: 25px; 
            border-radius: 8px; 
            margin-bottom: 30px;
            border-left: 5px solid {level_color};
        }}
        .issue {{ 
            margin-bottom: 25px; 
            padding: 20px; 
            border-left: 4px solid #ddd;
            background: #fff;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .error {{ border-left-color: #dc3545; background: #f8d7da; }}
        .warning {{ border-left-color: #ffc107; background: #fff3cd; }}
        .info {{ border-left-color: #17a2b8; background: #d1ecf1; }}
        .wcag-criterion {{
            background: #e9ecef;
            padding: 4px 8px;
            border-radius: 4px;
            font-family: monospace;
            font-size: 12px;
        }}
        .node-info {{
            color: #6c757d;
            font-size: 14px;
            margin-top: 5px;
        }}
        .stats {{
            display: flex;
            gap: 20px;
            margin: 20px 0;
        }}
        .stat {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid #dee2e6;
        }}
        .stat-number {{
            font-size: 24px;
            font-weight: bold;
            color: {level_color};
        }}
        .recommendations {{
            background: #e7f3ff;
            border: 1px solid #b8daff;
            border-radius: 8px;
            padding: 20px;
            margin: 30px 0;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 Accessibility Report</h1>
        <p><strong>File:</strong> {results['file_name']}</p>
        <p><strong>WCAG Level:</strong> {results['wcag_level']}</p>
        <p><strong>Generated:</strong> {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(results['timestamp']))}</p>
        <div class="compliance-badge">
            WCAG {results['summary']['compliance_level']} Compliance
        </div>
    </div>
    
    <div class="summary">
        <h2>📊 Summary</h2>
        <div class="stats">
            <div class="stat">
                <div class="stat-number">{results['summary']['score']}</div>
                <div>Score</div>
            </div>
            <div class="stat">
                <div class="stat-number">{results['summary']['total_issues']}</div>
                <div>Total Issues</div>
            </div>
            <div class="stat">
                <div class="stat-number">{results['summary']['issues_by_severity']['error']}</div>
                <div>Errors</div>
            </div>
            <div class="stat">
                <div class="stat-number">{results['summary']['issues_by_severity']['warning']}</div>
                <div>Warnings</div>
            </div>
        </div>
    </div>
"""

        if results['issues']:
            html += "<h2>🐛 Issues Found</h2>\n"
            
            for issue in results['issues']:
                severity_class = issue['severity']
                html += f"""
    <div class="issue {severity_class}">
        <h3>{issue['type'].replace('_', ' ').title()}: {issue['message']}</h3>
        <span class="wcag-criterion">WCAG {issue['wcag_criterion']}</span>
        <div class="node-info">
            <strong>Element:</strong> {issue.get('node_name', 'N/A')} 
            (ID: {issue.get('node_id', 'N/A')})
        </div>
"""
                
                if 'details' in issue and issue['details']:
                    html += "<div style='margin-top: 10px;'><strong>Details:</strong><ul>"
                    for key, value in issue['details'].items():
                        html += f"<li><strong>{key.replace('_', ' ').title()}:</strong> {value}</li>"
                    html += "</ul></div>"
                
                html += "</div>\n"
        else:
            html += """
    <div class="recommendations">
        <h2>🎉 Excellent Work!</h2>
        <p>No accessibility issues found in this design. This indicates strong adherence to WCAG guidelines.</p>
    </div>
"""

        html += """
    <div class="recommendations">
        <h2>💡 Recommendations</h2>
        <ul>
            <li><strong>Manual Testing:</strong> Automated checks catch many issues, but manual testing with assistive technologies is still essential.</li>
            <li><strong>User Testing:</strong> Include users with disabilities in your testing process.</li>
            <li><strong>Regular Audits:</strong> Run accessibility checks throughout the design process, not just at the end.</li>
            <li><strong>Design System:</strong> Build accessibility into your component library to prevent issues.</li>
        </ul>
    </div>
    
    <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #dee2e6; color: #6c757d; font-size: 14px;">
        <p>Generated by Figma Accessibility Checker | Learn more about WCAG at <a href="https://www.w3.org/WAI/WCAG21/quickref/">WCAG Quick Reference</a></p>
    </div>
</body>
</html>"""
        
        return html

def main():
    """CLI interface for accessibility checking"""
    parser = argparse.ArgumentParser(description='Figma Accessibility Checker')
    parser.add_argument('file_key', help='Figma file key or URL')
    parser.add_argument('--level', choices=['AA', 'AAA'], default='AA', help='WCAG compliance level')
    parser.add_argument('--output', help='Output file for accessibility report')
    parser.add_argument('--format', choices=['json', 'html'], default='json', help='Output format')
    
    args = parser.parse_args()
    
    try:
        client = FigmaClient()
        checker = AccessibilityChecker(client)
        
        file_key = client.parse_file_url(args.file_key)
        results = checker.check_wcag_compliance(file_key, args.level)
        
        if args.format == 'html':
            output_path = args.output or f"accessibility-report-{file_key}.html"
            checker.generate_accessibility_report(results, output_path)
        else:
            output_content = json.dumps(results, indent=2)
            
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(output_content)
                print(f"Accessibility results saved to {args.output}")
            else:
                print(output_content)
        
        # Print summary
        print(f"\n🔍 Accessibility Summary:")
        print(f"   Score: {results['summary']['score']}/100")
        print(f"   Compliance Level: WCAG {results['summary']['compliance_level']}")
        print(f"   Total Issues: {results['summary']['total_issues']}")
        print(f"   Errors: {results['summary']['issues_by_severity']['error']}")
        print(f"   Warnings: {results['summary']['issues_by_severity']['warning']}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()