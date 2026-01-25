#!/usr/bin/env python3
"""
Figma API Client - Complete wrapper for Figma REST API
Handles authentication, rate limiting, and all major endpoints.
"""

import os
import sys
import json
import time
import requests
from typing import Dict, List, Optional, Union, Any
from urllib.parse import urlencode
import argparse
from dataclasses import dataclass

@dataclass
class FigmaConfig:
    """Configuration for Figma API client"""
    access_token: str
    base_url: str = "https://api.figma.com/v1"
    rate_limit_delay: float = 0.5
    max_retries: int = 3

class FigmaClient:
    """Professional-grade Figma API client with rate limiting and error handling"""
    
    def __init__(self, access_token: str = None):
        self.config = FigmaConfig(
            access_token=access_token or os.getenv('FIGMA_ACCESS_TOKEN')
        )
        
        if not self.config.access_token:
            raise ValueError("Figma access token required. Set FIGMA_ACCESS_TOKEN env var or pass token.")
            
        self.session = requests.Session()
        self.session.headers.update({
            'X-Figma-Token': self.config.access_token,
            'Content-Type': 'application/json'
        })
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make authenticated request with rate limiting and retry logic"""
        url = f"{self.config.base_url}/{endpoint.lstrip('/')}"
        
        for attempt in range(self.config.max_retries):
            try:
                # Rate limiting
                time.sleep(self.config.rate_limit_delay)
                
                response = self.session.request(method, url, **kwargs)
                response.raise_for_status()
                
                return response.json()
                
            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:  # Rate limited
                    wait_time = 2 ** attempt
                    print(f"Rate limited. Waiting {wait_time}s before retry {attempt + 1}/{self.config.max_retries}")
                    time.sleep(wait_time)
                    continue
                elif response.status_code == 403:
                    raise ValueError("Access denied. Check your Figma token permissions.")
                elif response.status_code == 404:
                    raise ValueError(f"File or resource not found: {url}")
                else:
                    raise
            except requests.exceptions.RequestException as e:
                if attempt == self.config.max_retries - 1:
                    raise
                print(f"Request failed, retrying {attempt + 1}/{self.config.max_retries}: {e}")
                time.sleep(2 ** attempt)
    
    # ========== FILE OPERATIONS ==========
    
    def get_file(self, file_key: str, **params) -> Dict[str, Any]:
        """Get complete file data including components and styles"""
        return self._request('GET', f'/files/{file_key}', params=params)
    
    def get_file_nodes(self, file_key: str, node_ids: Union[str, List[str]], **params) -> Dict[str, Any]:
        """Get specific nodes from a file"""
        if isinstance(node_ids, list):
            node_ids = ','.join(node_ids)
        
        params['ids'] = node_ids
        return self._request('GET', f'/files/{file_key}/nodes', params=params)
    
    def get_file_versions(self, file_key: str) -> Dict[str, Any]:
        """Get version history for a file"""
        return self._request('GET', f'/files/{file_key}/versions')
    
    def get_file_components(self, file_key: str) -> Dict[str, Any]:
        """Get all components in a file"""
        return self._request('GET', f'/files/{file_key}/components')
    
    def get_file_styles(self, file_key: str) -> Dict[str, Any]:
        """Get all styles in a file"""
        return self._request('GET', f'/files/{file_key}/styles')
    
    # ========== IMAGE EXPORTS ==========
    
    def export_images(self, file_key: str, node_ids: Union[str, List[str]], 
                     format: str = 'png', scale: float = 1.0, **params) -> Dict[str, Any]:
        """Export nodes as images"""
        if isinstance(node_ids, list):
            node_ids = ','.join(node_ids)
            
        params.update({
            'ids': node_ids,
            'format': format,
            'scale': scale
        })
        
        return self._request('GET', f'/images/{file_key}', params=params)
    
    def get_image_fills(self, file_key: str) -> Dict[str, Any]:
        """Get image fill metadata from a file"""
        return self._request('GET', f'/files/{file_key}/images')
    
    # ========== TEAM & PROJECT OPERATIONS ==========
    
    def get_team_projects(self, team_id: str) -> Dict[str, Any]:
        """Get projects for a team"""
        return self._request('GET', f'/teams/{team_id}/projects')
    
    def get_project_files(self, project_id: str) -> Dict[str, Any]:
        """Get files in a project"""
        return self._request('GET', f'/projects/{project_id}/files')
    
    # ========== COMPONENT & STYLE OPERATIONS ==========
    
    def get_team_components(self, team_id: str, **params) -> Dict[str, Any]:
        """Get team component library"""
        return self._request('GET', f'/teams/{team_id}/components', params=params)
    
    def get_component(self, component_key: str) -> Dict[str, Any]:
        """Get individual component metadata"""
        return self._request('GET', f'/components/{component_key}')
    
    def get_team_styles(self, team_id: str, **params) -> Dict[str, Any]:
        """Get team style library"""
        return self._request('GET', f'/teams/{team_id}/styles', params=params)
    
    def get_style(self, style_key: str) -> Dict[str, Any]:
        """Get individual style metadata"""
        return self._request('GET', f'/styles/{style_key}')
    
    # ========== UTILITY METHODS ==========
    
    def parse_file_url(self, url: str) -> str:
        """Extract file key from Figma URL"""
        # https://www.figma.com/file/ABC123/File-Name
        if '/file/' in url:
            return url.split('/file/')[1].split('/')[0]
        return url  # Assume it's already a file key
    
    def get_user_info(self) -> Dict[str, Any]:
        """Get current user information"""
        return self._request('GET', '/me')
    
    def download_image(self, image_url: str, output_path: str) -> str:
        """Download image from Figma CDN"""
        response = requests.get(image_url)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        return output_path
    
    # ========== ANALYSIS HELPERS ==========
    
    def extract_colors(self, file_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract all colors used in a file"""
        colors = []
        
        def traverse_node(node):
            if 'fills' in node:
                for fill in node.get('fills', []):
                    if fill.get('type') == 'SOLID':
                        color = fill.get('color', {})
                        if color:
                            colors.append({
                                'r': color.get('r', 0),
                                'g': color.get('g', 0), 
                                'b': color.get('b', 0),
                                'a': color.get('a', 1),
                                'node_id': node.get('id'),
                                'node_name': node.get('name', '')
                            })
            
            for child in node.get('children', []):
                traverse_node(child)
        
        if 'document' in file_data:
            traverse_node(file_data['document'])
        
        return colors
    
    def extract_text_styles(self, file_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract all text styles used in a file"""
        text_styles = []
        
        def traverse_node(node):
            if node.get('type') == 'TEXT':
                style = node.get('style', {})
                if style:
                    text_styles.append({
                        'font_family': style.get('fontFamily', ''),
                        'font_size': style.get('fontSize', 0),
                        'font_weight': style.get('fontWeight', 400),
                        'line_height': style.get('lineHeightPx', 0),
                        'letter_spacing': style.get('letterSpacing', 0),
                        'node_id': node.get('id'),
                        'node_name': node.get('name', ''),
                        'text': node.get('characters', '')
                    })
            
            for child in node.get('children', []):
                traverse_node(child)
        
        if 'document' in file_data:
            traverse_node(file_data['document'])
        
        return text_styles

def main():
    """CLI interface for Figma operations"""
    parser = argparse.ArgumentParser(description='Figma API Client')
    parser.add_argument('command', choices=[
        'get-file', 'export-images', 'get-components', 'get-styles',
        'extract-colors', 'extract-typography', 'user-info'
    ])
    parser.add_argument('file_key', nargs='?', help='Figma file key or URL')
    parser.add_argument('--node-ids', help='Comma-separated node IDs')
    parser.add_argument('--format', default='png', choices=['png', 'svg', 'pdf'])
    parser.add_argument('--scale', type=float, default=1.0)
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--token', help='Figma access token (overrides env var)')
    
    args = parser.parse_args()
    
    try:
        client = FigmaClient(access_token=args.token)
        
        if args.command == 'get-file':
            if not args.file_key:
                parser.error('file_key required for get-file command')
            
            file_key = client.parse_file_url(args.file_key)
            result = client.get_file(file_key)
            
        elif args.command == 'export-images':
            if not args.file_key or not args.node_ids:
                parser.error('file_key and --node-ids required for export-images command')
            
            file_key = client.parse_file_url(args.file_key)
            result = client.export_images(
                file_key, 
                args.node_ids.split(','),
                format=args.format,
                scale=args.scale
            )
            
        elif args.command == 'get-components':
            if not args.file_key:
                parser.error('file_key required for get-components command')
                
            file_key = client.parse_file_url(args.file_key)
            result = client.get_file_components(file_key)
            
        elif args.command == 'get-styles':
            if not args.file_key:
                parser.error('file_key required for get-styles command')
                
            file_key = client.parse_file_url(args.file_key)
            result = client.get_file_styles(file_key)
            
        elif args.command == 'extract-colors':
            if not args.file_key:
                parser.error('file_key required for extract-colors command')
                
            file_key = client.parse_file_url(args.file_key)
            file_data = client.get_file(file_key)
            result = client.extract_colors(file_data)
            
        elif args.command == 'extract-typography':
            if not args.file_key:
                parser.error('file_key required for extract-typography command')
                
            file_key = client.parse_file_url(args.file_key)
            file_data = client.get_file(file_key)
            result = client.extract_text_styles(file_data)
            
        elif args.command == 'user-info':
            result = client.get_user_info()
        
        # Output result
        output = json.dumps(result, indent=2)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Output saved to {args.output}")
        else:
            print(output)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()