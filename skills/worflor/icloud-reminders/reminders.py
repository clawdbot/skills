#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iCloud Reminders - iOS 13+ CloudKit API

iOS 13+ moved reminders from CalDAV to CloudKit. This script accesses
the real data via the com.apple.reminders CloudKit container.

Commands:
    lists       - Show all reminder lists (with hierarchy)
    all         - Show all reminders (grouped by list)
    pending     - Show only incomplete reminders
    today       - Show reminders due today
    overdue     - Show overdue reminders
    flagged     - Show flagged reminders
    search      - Search reminders by title
    tags        - Show all hashtags
    summary     - Quick summary (for heartbeats)
    create      - Create a new reminder with full metadata
    
Usage:
    python reminders.py -u EMAIL -p PASSWORD lists
    python reminders.py -u EMAIL -p PASSWORD pending
    python reminders.py -u EMAIL -p PASSWORD search "grocery"
    
Create examples:
    # Basic reminder
    python reminders.py -u EMAIL -p PASS create "Buy groceries"
    
    # With list and flag
    python reminders.py -u EMAIL -p PASS create "Important task" --list Work --flagged
    
    # With due date (all-day)
    python reminders.py -u EMAIL -p PASS create "Pay bills" --due 2026-02-01
    
    # With due date and time
    python reminders.py -u EMAIL -p PASS create "Meeting" --due 2026-02-01 --time 14:30
    
    # Full metadata
    python reminders.py -u EMAIL -p PASS create "Project deadline" \\
        --list Work --due 2026-03-15 --time 09:00 \\
        --priority high --flagged --notes "Final submission"
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import argparse
import json
import base64
import gzip
import re
import uuid
import time
import requests
from datetime import datetime, timedelta, timezone
from pyicloud import PyiCloudService

import urllib3
urllib3.disable_warnings()

JSON_MODE = False


def decode_title(b64_str):
    """Decode ENCRYPTED_BYTES title field (base64 → gzip → extract text)"""
    if not b64_str:
        return '?'
    try:
        decoded = base64.b64decode(b64_str)
        decompressed = gzip.decompress(decoded)
        text = decompressed.decode('utf-8', errors='replace')
        # Extract readable ASCII strings (the title is in there)
        readable = re.findall(r'[\x20-\x7e]{3,}', text)
        return readable[0] if readable else '?'
    except Exception:
        return '?'


def varint_encode(n):
    """Encode integer as protobuf varint."""
    parts = []
    while n >= 128:
        parts.append((n & 0x7f) | 0x80)
        n >>= 7
    parts.append(n)
    return bytes(parts)


def encode_title(text):
    """
    Encode title as Apple's TitleDocument protobuf format.
    
    Structure matches real iOS reminders exactly:
    - Field 1: varint 0
    - Field 2: length-delimited message containing styled text
    """
    title_bytes = text.encode('utf-8')
    title_len = len(title_bytes)
    
    # Fixed suffix pattern (styled text attributes from working reminders)
    suffix = bytes([
        0x1a, 0x10, 0x0a, 0x04, 0x08, 0x00, 0x10, 0x00, 0x10, 0x00, 
        0x1a, 0x04, 0x08, 0x00, 0x10, 0x00, 0x28, 0x01,
        0x1a, 0x10, 0x0a, 0x04, 0x08, 0x01, 0x10, 0x00, 0x10
    ])
    suffix += varint_encode(title_len)
    suffix += bytes([0x1a, 0x04, 0x08, 0x01, 0x10, 0x00, 0x28, 0x02])
    suffix += bytes([
        0x1a, 0x16, 0x0a, 0x08, 0x08, 0x00, 0x10, 0xff, 0xff, 0xff, 0xff, 0x0f, 0x10, 0x00,
        0x1a, 0x08, 0x08, 0x00, 0x10, 0xff, 0xff, 0xff, 0xff, 0x0f
    ])
    
    # UUID for attributed string
    attr_uuid = uuid.uuid4().bytes
    suffix += bytes([0x22, 0x1c, 0x0a, 0x1a, 0x0a, 0x10])
    suffix += attr_uuid
    suffix += bytes([0x12, 0x02, 0x08])
    suffix += varint_encode(title_len)
    suffix += bytes([0x12, 0x02, 0x08, 0x01, 0x2a, 0x02, 0x08])
    suffix += varint_encode(title_len)
    
    # Build field 3: title string + attributes
    field3_content = bytes([0x12]) + varint_encode(title_len) + title_bytes + suffix
    
    # Build field 2: nested structure
    field3_len = varint_encode(len(field3_content))
    field2_content = bytes([0x08, 0x00, 0x10, 0x00, 0x1a]) + field3_len + field3_content
    
    # Build full message
    field2_len = varint_encode(len(field2_content))
    full = bytes([0x08, 0x00, 0x12]) + field2_len + field2_content
    
    compressed = gzip.compress(full)
    return base64.b64encode(compressed).decode('ascii')


def ts_to_datetime(ts_ms):
    """Convert CloudKit timestamp (ms) to datetime"""
    if not ts_ms:
        return None
    try:
        return datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc)
    except:
        return None


class iCloudReminders:
    """iCloud Reminders via CloudKit API (iOS 13+)"""
    
    def __init__(self, username, password):
        self.api = PyiCloudService(username, password)
        self.session = self.api.session
        self.params = self.api.params
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        self.ck_url = self.api.get_webservice_url('ckdatabasews')
        self.container = 'com.apple.reminders'
        
        # Get the correct zone ID (must fetch dynamically)
        self.zone_id = self._get_reminders_zone()
        
        # Cache
        self._all_records = None
        self._by_type = None
    
    def _get_reminders_zone(self):
        """Fetch the actual Reminders zone with correct ownerRecordName"""
        r = self.session.post(
            f'{self.ck_url}/database/1/{self.container}/production/private/zones/list',
            params=self.params,
            json={},
            headers=self.headers
        )
        
        if r.status_code != 200:
            raise Exception(f"Failed to get zones: {r.status_code}")
        
        for zone in r.json().get('zones', []):
            zone_id = zone.get('zoneID', {})
            if zone_id.get('zoneName') == 'Reminders':
                return zone_id
        
        raise Exception("Reminders zone not found")
    
    def _fetch_all_records(self):
        """Fetch all records from CloudKit Reminders zone"""
        if self._all_records is not None:
            return self._all_records
        
        all_records = []
        sync_token = None
        
        while True:
            payload = {'zoneID': self.zone_id}
            if sync_token:
                payload['syncToken'] = sync_token
            
            r = self.session.post(
                f'{self.ck_url}/database/1/{self.container}/production/private/records/changes',
                params=self.params,
                json=payload,
                headers=self.headers
            )
            
            if r.status_code != 200:
                raise Exception(f"CloudKit error: {r.status_code} - {r.text[:200]}")
            
            data = r.json()
            records = data.get('records', [])
            all_records.extend(records)
            
            if not data.get('moreComing') or not records:
                break
            
            sync_token = data.get('syncToken')
        
        self._all_records = all_records
        
        # Group by type
        self._by_type = {}
        for rec in all_records:
            rt = rec.get('recordType', 'unknown')
            self._by_type.setdefault(rt, []).append(rec)
        
        return all_records
    
    def _get_by_type(self, record_type):
        """Get records of a specific type"""
        self._fetch_all_records()
        return self._by_type.get(record_type, [])
    
    def get_lists(self):
        """Get all reminder lists with hierarchy"""
        lists = []
        for rec in self._get_by_type('List'):
            fields = rec.get('fields', {})
            
            if fields.get('Deleted', {}).get('value', 0):
                continue
            
            parent_ref = fields.get('ParentList', {}).get('value')
            
            lists.append({
                'id': rec.get('recordName'),
                'name': fields.get('Name', {}).get('value', '?'),
                'is_group': bool(fields.get('IsGroup', {}).get('value', 0)),
                'parent_id': parent_ref.get('recordName') if parent_ref else None,
                'color': self._parse_color(fields.get('Color', {}).get('value', '{}')),
            })
        
        return lists
    
    def _parse_color(self, color_str):
        """Parse color JSON to get symbolic name"""
        try:
            data = json.loads(color_str) if isinstance(color_str, str) else color_str
            return data.get('daSymbolicColorName', data.get('ckSymbolicColorName', 'default'))
        except:
            return 'default'
    
    def get_reminders(self, include_completed=True):
        """Get all reminders"""
        reminders = []
        
        for rec in self._get_by_type('Reminder'):
            fields = rec.get('fields', {})
            
            if fields.get('Deleted', {}).get('value', 0):
                continue
            
            is_completed = bool(fields.get('Completed', {}).get('value', 0))
            if not include_completed and is_completed:
                continue
            
            list_ref = fields.get('List', {}).get('value', {})
            due_ts = fields.get('DueDate', {}).get('value')
            
            reminders.append({
                'id': rec.get('recordName'),
                'title': decode_title(fields.get('TitleDocument', {}).get('value', '')),
                'notes': decode_title(fields.get('NotesDocument', {}).get('value', '')),
                'completed': is_completed,
                'flagged': bool(fields.get('Flagged', {}).get('value', 0)),
                'priority': fields.get('Priority', {}).get('value', 0),
                'due_date': ts_to_datetime(due_ts),
                'all_day': bool(fields.get('AllDay', {}).get('value', 0)),
                'list_id': list_ref.get('recordName') if list_ref else None,
            })
        
        return reminders
    
    def get_hashtags(self):
        """Get all unique hashtags"""
        tags = set()
        for rec in self._get_by_type('Hashtag'):
            fields = rec.get('fields', {})
            if fields.get('Deleted', {}).get('value', 0):
                continue
            name = fields.get('Name', {}).get('value', '')
            if name:
                tags.add(name)
        return sorted(tags)
    
    def get_smart_lists(self):
        """Get smart lists"""
        smart_lists = []
        for rec in self._get_by_type('SmartList'):
            fields = rec.get('fields', {})
            if fields.get('Deleted', {}).get('value', 0):
                continue
            
            sl_type = fields.get('SmartListType', {}).get('value', '')
            name = fields.get('Name', {}).get('value', '') or sl_type.split('.')[-1]
            
            smart_lists.append({
                'type': sl_type,
                'name': name,
            })
        return smart_lists
    
    def get_list_by_name(self, name):
        """Find a list by name (case-insensitive)"""
        name_lower = name.lower()
        for lst in self.get_lists():
            if lst['name'].lower() == name_lower:
                return lst
        return None
    
    def create_reminder(self, title, list_name=None, flagged=False, due_date=None, 
                        notes=None, priority=0, all_day=True, url=None,
                        alarm_minutes=None, parent_id=None, tags=None, recurrence=None):
        """
        Create a new reminder with full metadata support.
        
        Args:
            title: Reminder title (required)
            list_name: Target list name (default: first available list)
            flagged: Mark as flagged (default: False)
            due_date: Due date as datetime object (default: None)
            notes: Notes/description text (default: None)
            priority: 0=none, 1=high, 5=medium, 9=low (default: 0)
            all_day: True for all-day, False for specific time (default: True)
            url: Associated URL (default: None)
            alarm_minutes: Minutes before due date to alert (e.g., 0, 15, 60) (default: None)
            parent_id: Parent reminder ID for subtask (default: None)
            tags: List of hashtag strings without # (default: None)
            recurrence: Dict with frequency ('daily','weekly','monthly','yearly'), 
                       interval (int), end_date (datetime), count (int) (default: None)
        
        Note: Location-based alarms require device-level encryption and cannot be
        created via the CloudKit API. Use the iOS Reminders app for location alarms.
        
        Returns:
            dict with id, title, list info
        """
        # Find the target list
        if list_name:
            lst = self.get_list_by_name(list_name)
            if not lst:
                raise ValueError(f"List '{list_name}' not found")
            list_id = lst['id']
        else:
            # Use first non-group list as default
            lists = self.get_lists()
            default_list = next((l for l in lists if not l['is_group']), None)
            if not default_list:
                raise ValueError("No lists available")
            list_id = default_list['id']
            list_name = default_list['name']
        
        # Generate unique ID
        reminder_uuid = str(uuid.uuid4()).upper()
        record_name = f"Reminder/{reminder_uuid}"
        now_ms = int(time.time() * 1000)
        
        # Build fields with full metadata
        fields = {
            'TitleDocument': {'value': encode_title(title), 'type': 'ENCRYPTED_BYTES'},
            'Completed': {'value': 0, 'type': 'NUMBER_INT64'},
            'Flagged': {'value': 1 if flagged else 0, 'type': 'NUMBER_INT64'},
            'Priority': {'value': priority, 'type': 'NUMBER_INT64'},
            'AllDay': {'value': 1 if all_day else 0, 'type': 'NUMBER_INT64'},
            'Deleted': {'value': 0, 'type': 'NUMBER_INT64'},
            'Imported': {'value': 0, 'type': 'NUMBER_INT64'},
            'CreationDate': {'value': now_ms, 'type': 'TIMESTAMP'},
            'LastModifiedDate': {'value': now_ms, 'type': 'TIMESTAMP'},
            'List': {
                'value': {
                    'recordName': list_id,
                    'action': 'NONE',
                    'zoneID': self.zone_id
                },
                'type': 'REFERENCE'
            },
        }
        
        if notes:
            fields['NotesDocument'] = {'value': encode_title(notes), 'type': 'ENCRYPTED_BYTES'}
        
        if due_date:
            fields['DueDate'] = {'value': int(due_date.timestamp() * 1000), 'type': 'TIMESTAMP'}
            # Add timezone for non-all-day reminders
            if not all_day:
                fields['TimeZone'] = {'value': 'America/Toronto', 'type': 'STRING'}
        
        if url:
            fields['URL'] = {'value': url, 'type': 'STRING'}
        
        # Subtask support - link to parent reminder
        if parent_id:
            fields['ParentReminder'] = {
                'value': {
                    'recordName': parent_id if parent_id.startswith('Reminder/') else f'Reminder/{parent_id}',
                    'action': 'VALIDATE',
                    'zoneID': self.zone_id
                },
                'type': 'REFERENCE'
            }
        
        # Build operations list - may include alarm and hashtag records
        operations = []
        
        # Alarm support - create Alarm + AlarmTrigger records
        alarm_uuid = None
        if alarm_minutes is not None and due_date:
            alarm_uuid = str(uuid.uuid4()).upper()
            trigger_uuid = str(uuid.uuid4()).upper()
            alarm_name = f"Alarm/{alarm_uuid}"
            trigger_name = f"AlarmTrigger/{trigger_uuid}"
            
            # Calculate alarm time
            alarm_time = due_date - timedelta(minutes=alarm_minutes)
            
            # DateComponentsData for trigger
            date_components = base64.b64encode(json.dumps({
                "minute": alarm_time.minute,
                "hour": alarm_time.hour,
                "day": alarm_time.day,
                "month": alarm_time.month,
                "year": alarm_time.year,
                "second": 0,
                "timeZone": {"identifier": "America/Toronto"}
            }).encode()).decode()
            
            fields['AlarmIDs'] = {'value': [alarm_uuid], 'type': 'STRING_LIST'}
            
            # AlarmTrigger record
            operations.append({
                'operationType': 'create',
                'record': {
                    'recordName': trigger_name,
                    'recordType': 'AlarmTrigger',
                    'fields': {
                        'Type': {'value': 'Date', 'type': 'STRING'},
                        'DateComponentsData': {'value': date_components, 'type': 'BYTES'},
                        'Deleted': {'value': 0, 'type': 'NUMBER_INT64'},
                        'Imported': {'value': 0, 'type': 'NUMBER_INT64'},
                    }
                }
            })
            
            # Alarm record (references trigger and will reference reminder)
            operations.append({
                'operationType': 'create',
                'record': {
                    'recordName': alarm_name,
                    'recordType': 'Alarm',
                    'fields': {
                        'AlarmUID': {'value': alarm_uuid, 'type': 'STRING'},
                        'TriggerID': {'value': trigger_uuid, 'type': 'STRING'},
                        'Deleted': {'value': 0, 'type': 'NUMBER_INT64'},
                        'Imported': {'value': 0, 'type': 'NUMBER_INT64'},
                    }
                }
            })
        
        # Note: Location-based alarms are NOT supported via CloudKit API
        # They require device-level encryption keys (isEncrypted fields)
        # Use iOS Reminders app for location-based reminders
        
        # Hashtag support - create Hashtag records
        hashtag_ids = []
        if tags:
            for tag in tags:
                tag_clean = tag.lstrip('#')
                tag_uuid = str(uuid.uuid4()).upper()
                tag_name = f"Hashtag/{tag_uuid}"
                hashtag_ids.append(tag_uuid)
                
                operations.append({
                    'operationType': 'create',
                    'record': {
                        'recordName': tag_name,
                        'recordType': 'Hashtag',
                        'fields': {
                            'Name': {'value': tag_clean, 'type': 'STRING'},
                            'Type': {'value': 0, 'type': 'NUMBER_INT64'},
                            'CreationDate': {'value': now_ms, 'type': 'TIMESTAMP'},
                            'Deleted': {'value': 0, 'type': 'NUMBER_INT64'},
                            'Imported': {'value': 0, 'type': 'NUMBER_INT64'},
                        }
                    }
                })
            
            fields['HashtagIDs'] = {'value': hashtag_ids, 'type': 'STRING_LIST'}
        
        # Recurrence support - create RecurrenceRule record
        if recurrence and due_date:
            freq_map = {'daily': 0, 'weekly': 1, 'monthly': 2, 'yearly': 3}
            freq = freq_map.get(recurrence.get('frequency', 'daily').lower(), 0)
            interval = recurrence.get('interval', 1)
            
            rule_uuid = str(uuid.uuid4()).upper()
            rule_name = f"RecurrenceRule/{rule_uuid}"
            
            rule_fields = {
                'Frequency': {'value': freq, 'type': 'NUMBER_INT64'},
                'Interval': {'value': interval, 'type': 'NUMBER_INT64'},
                'Deleted': {'value': 0, 'type': 'NUMBER_INT64'},
                'Imported': {'value': 0, 'type': 'NUMBER_INT64'},
            }
            
            if recurrence.get('end_date'):
                rule_fields['EndDate'] = {'value': int(recurrence['end_date'].timestamp() * 1000), 'type': 'TIMESTAMP'}
            if recurrence.get('count'):
                rule_fields['OccurrenceCount'] = {'value': recurrence['count'], 'type': 'NUMBER_INT64'}
            
            operations.append({
                'operationType': 'create',
                'record': {
                    'recordName': rule_name,
                    'recordType': 'RecurrenceRule',
                    'fields': rule_fields
                }
            })
            
            fields['RecurrenceRuleIDs'] = {'value': [rule_uuid], 'type': 'STRING_LIST'}
        
        # Create the reminder record
        new_reminder = {
            'recordName': record_name,
            'recordType': 'Reminder',
            'fields': fields
        }
        operations.append({'operationType': 'create', 'record': new_reminder})
        
        # Now update Alarm to reference the Reminder (circular reference issue)
        # We need to create alarm first, then update it with reminder reference
        
        r = self.session.post(
            f'{self.ck_url}/database/1/{self.container}/production/private/records/modify',
            params=self.params,
            json={
                'zoneID': self.zone_id,
                'operations': operations
            },
            headers=self.headers
        )
        
        if r.status_code != 200:
            raise Exception(f"Failed to create reminder: {r.status_code} - {r.text[:200]}")
        
        resp = r.json()
        records = resp.get('records', [])
        
        # Find the reminder record in response
        reminder_rec = None
        for rec in records:
            if rec.get('recordName', '').startswith('Reminder/'):
                if not rec.get('serverErrorCode'):
                    reminder_rec = rec
                else:
                    raise Exception(f"Failed to create reminder: {rec.get('serverErrorCode')}")
        
        if reminder_rec:
            # If we created a time-based alarm, update it to reference the reminder
            if alarm_uuid:
                alarm_name = f"Alarm/{alarm_uuid}"
                alarm_rec = next((r for r in records if r.get('recordName') == alarm_name), None)
                if alarm_rec and not alarm_rec.get('serverErrorCode'):
                    alarm_tag = alarm_rec.get('recordChangeTag')
                    # Update alarm with reminder reference
                    self.session.post(
                        f'{self.ck_url}/database/1/{self.container}/production/private/records/modify',
                        params=self.params,
                        json={
                            'zoneID': self.zone_id,
                            'operations': [{
                                'operationType': 'update',
                                'record': {
                                    'recordName': alarm_name,
                                    'recordType': 'Alarm',
                                    'recordChangeTag': alarm_tag,
                                    'fields': {
                                        'Reminder': {
                                            'value': {'recordName': record_name, 'action': 'NONE', 'zoneID': self.zone_id},
                                            'type': 'REFERENCE'
                                        }
                                    }
                                }
                            }]
                        },
                        headers=self.headers
                    )
            
            # If we created hashtags, update them to reference the reminder
            if hashtag_ids:
                for tag_uuid in hashtag_ids:
                    tag_name = f"Hashtag/{tag_uuid}"
                    tag_rec = next((r for r in records if r.get('recordName') == tag_name), None)
                    if tag_rec and not tag_rec.get('serverErrorCode'):
                        tag_tag = tag_rec.get('recordChangeTag')
                        self.session.post(
                            f'{self.ck_url}/database/1/{self.container}/production/private/records/modify',
                            params=self.params,
                            json={
                                'zoneID': self.zone_id,
                                'operations': [{
                                    'operationType': 'update',
                                    'record': {
                                        'recordName': tag_name,
                                        'recordType': 'Hashtag',
                                        'recordChangeTag': tag_tag,
                                        'fields': {
                                            'Reminder': {
                                                'value': {'recordName': record_name, 'action': 'NONE', 'zoneID': self.zone_id},
                                                'type': 'REFERENCE'
                                            }
                                        }
                                    }
                                }]
                            },
                            headers=self.headers
                        )
            
            # If we created recurrence rule, update it to reference the reminder
            if recurrence:
                rule_name = f"RecurrenceRule/{rule_uuid}"
                rule_rec = next((r for r in records if r.get('recordName') == rule_name), None)
                if rule_rec and not rule_rec.get('serverErrorCode'):
                    rule_tag = rule_rec.get('recordChangeTag')
                    self.session.post(
                        f'{self.ck_url}/database/1/{self.container}/production/private/records/modify',
                        params=self.params,
                        json={
                            'zoneID': self.zone_id,
                            'operations': [{
                                'operationType': 'update',
                                'record': {
                                    'recordName': rule_name,
                                    'recordType': 'RecurrenceRule',
                                    'recordChangeTag': rule_tag,
                                    'fields': {
                                        'Reminder': {
                                            'value': {'recordName': record_name, 'action': 'NONE', 'zoneID': self.zone_id},
                                            'type': 'REFERENCE'
                                        }
                                    }
                                }
                            }]
                        },
                        headers=self.headers
                    )
            
            return {
                'id': reminder_rec.get('recordName'),
                'title': title,
                'list': list_name or 'default',
                'has_alarm': alarm_uuid is not None,
                'has_tags': len(hashtag_ids) > 0,
                'has_recurrence': recurrence is not None,
                'is_subtask': parent_id is not None
            }
        else:
            raise Exception("Failed to create reminder: no reminder record in response")
    
    def _get_reminder_by_id(self, reminder_id):
        """Get a reminder record by ID"""
        for rec in self._get_by_type('Reminder'):
            if rec.get('recordName') == reminder_id:
                return rec
        return None
    
    def _get_reminder_by_title(self, title_search):
        """Find a reminder by title (partial match)"""
        title_lower = title_search.lower()
        for rec in self._get_by_type('Reminder'):
            fields = rec.get('fields', {})
            if fields.get('Deleted', {}).get('value', 0):
                continue
            title_doc = fields.get('TitleDocument', {}).get('value', '')
            title = decode_title(title_doc).lower()
            if title_lower in title:
                return rec
        return None
    
    def delete_reminder(self, identifier):
        """
        Delete a reminder by ID or title search.
        Also deletes related Alarm and AlarmTrigger records.
        
        Args:
            identifier: Reminder ID (Reminder/xxx) or title search string
        
        Returns:
            dict with deleted reminder info
        """
        # Find the reminder
        if identifier.startswith('Reminder/'):
            rec = self._get_reminder_by_id(identifier)
        else:
            rec = self._get_reminder_by_title(identifier)
        
        if not rec:
            raise ValueError(f"Reminder not found: {identifier}")
        
        record_name = rec.get('recordName')
        record_tag = rec.get('recordChangeTag')
        title = decode_title(rec.get('fields', {}).get('TitleDocument', {}).get('value', ''))
        
        # Find related Alarms and AlarmTriggers to delete first
        operations = []
        
        # Get alarm IDs from the reminder
        alarm_ids = rec.get('fields', {}).get('AlarmIDs', {}).get('value', [])
        
        # Find and queue deletion of Alarm and AlarmTrigger records
        for alarm_rec in self._get_by_type('Alarm'):
            alarm_uid = alarm_rec.get('fields', {}).get('AlarmUID', {}).get('value', '')
            # Check if this alarm belongs to our reminder
            reminder_ref = alarm_rec.get('fields', {}).get('Reminder', {}).get('value', {})
            if reminder_ref.get('recordName') == record_name:
                # Delete any related triggers first
                trigger_id = alarm_rec.get('fields', {}).get('TriggerID', {}).get('value', '')
                for trigger_rec in self._get_by_type('AlarmTrigger'):
                    trigger_alarm_ref = trigger_rec.get('fields', {}).get('Alarm', {}).get('value', {})
                    if trigger_alarm_ref.get('recordName') == alarm_rec.get('recordName'):
                        operations.append({
                            'operationType': 'delete',
                            'record': {
                                'recordName': trigger_rec.get('recordName'),
                                'recordChangeTag': trigger_rec.get('recordChangeTag')
                            }
                        })
                # Then delete the alarm
                operations.append({
                    'operationType': 'delete',
                    'record': {
                        'recordName': alarm_rec.get('recordName'),
                        'recordChangeTag': alarm_rec.get('recordChangeTag')
                    }
                })
        
        # Finally delete the reminder itself
        operations.append({
            'operationType': 'delete',
            'record': {
                'recordName': record_name,
                'recordChangeTag': record_tag
            }
        })
        
        # Execute all deletions
        r = requests.post(
            f'{self.ck_url}/database/1/{self.container}/production/private/records/modify',
            params=self.params,
            cookies=dict(self.session.cookies),
            headers={**dict(self.session.headers), **self.headers},
            json={
                'zoneID': self.zone_id,
                'operations': operations
            },
            verify=False
        )
        
        if r.status_code != 200:
            raise Exception(f"Failed to delete: {r.status_code}")
        
        resp = r.json()
        # Check if reminder was deleted (last operation)
        reminder_result = resp.get('records', [])[-1] if resp.get('records') else {}
        if reminder_result.get('deleted'):
            deleted_count = len([r for r in resp.get('records', []) if r.get('deleted')])
            return {'id': record_name, 'title': title, 'deleted': True, 'related_deleted': deleted_count - 1}
        elif reminder_result.get('serverErrorCode'):
            raise Exception(f"Delete failed: {reminder_result.get('reason')}")
        else:
            raise Exception("Delete failed: unexpected response")
    
    def complete_reminder(self, identifier):
        """
        Mark a reminder as complete.
        
        Args:
            identifier: Reminder ID or title search string
        
        Returns:
            dict with completed reminder info
        """
        # Find the reminder
        if identifier.startswith('Reminder/'):
            rec = self._get_reminder_by_id(identifier)
        else:
            rec = self._get_reminder_by_title(identifier)
        
        if not rec:
            raise ValueError(f"Reminder not found: {identifier}")
        
        record_name = rec.get('recordName')
        record_tag = rec.get('recordChangeTag')
        title = decode_title(rec.get('fields', {}).get('TitleDocument', {}).get('value', ''))
        
        now_ms = int(time.time() * 1000)
        
        # Update to mark complete
        r = self.session.post(
            f'{self.ck_url}/database/1/{self.container}/production/private/records/modify',
            params=self.params,
            json={
                'zoneID': self.zone_id,
                'operations': [{
                    'operationType': 'update',
                    'record': {
                        'recordName': record_name,
                        'recordType': 'Reminder',
                        'recordChangeTag': record_tag,
                        'fields': {
                            'Completed': {'value': 1, 'type': 'NUMBER_INT64'},
                            'CompletionDate': {'value': now_ms, 'type': 'TIMESTAMP'},
                            'LastModifiedDate': {'value': now_ms, 'type': 'TIMESTAMP'},
                        }
                    }
                }]
            },
            headers=self.headers
        )
        
        if r.status_code != 200:
            raise Exception(f"Failed to complete: {r.status_code} - {r.text[:200]}")
        
        resp = r.json()
        if resp.get('records') and not resp['records'][0].get('serverErrorCode'):
            return {'id': record_name, 'title': title, 'completed': True}
        else:
            error = resp['records'][0].get('serverErrorCode', 'Unknown') if resp.get('records') else 'No response'
            raise Exception(f"Complete failed: {error}")
    
    def update_reminder(self, identifier, title=None, flagged=None, due_date=None, 
                        notes=None, priority=None, list_name=None):
        """
        Update an existing reminder.
        
        Args:
            identifier: Reminder ID or title search string
            title: New title (optional)
            flagged: New flagged state (optional)
            due_date: New due date as datetime (optional)
            notes: New notes (optional)
            priority: New priority 0/1/5/9 (optional)
            list_name: Move to different list (optional)
        
        Returns:
            dict with updated reminder info
        """
        # Find the reminder
        if identifier.startswith('Reminder/'):
            rec = self._get_reminder_by_id(identifier)
        else:
            rec = self._get_reminder_by_title(identifier)
        
        if not rec:
            raise ValueError(f"Reminder not found: {identifier}")
        
        record_name = rec.get('recordName')
        record_tag = rec.get('recordChangeTag')
        old_title = decode_title(rec.get('fields', {}).get('TitleDocument', {}).get('value', ''))
        
        now_ms = int(time.time() * 1000)
        
        # Build fields to update
        fields = {
            'LastModifiedDate': {'value': now_ms, 'type': 'TIMESTAMP'},
        }
        
        if title is not None:
            fields['TitleDocument'] = {'value': encode_title(title), 'type': 'ENCRYPTED_BYTES'}
        
        if flagged is not None:
            fields['Flagged'] = {'value': 1 if flagged else 0, 'type': 'NUMBER_INT64'}
        
        if due_date is not None:
            fields['DueDate'] = {'value': int(due_date.timestamp() * 1000), 'type': 'TIMESTAMP'}
        
        if notes is not None:
            fields['NotesDocument'] = {'value': encode_title(notes), 'type': 'ENCRYPTED_BYTES'}
        
        if priority is not None:
            fields['Priority'] = {'value': priority, 'type': 'NUMBER_INT64'}
        
        if list_name is not None:
            lst = self.get_list_by_name(list_name)
            if not lst:
                raise ValueError(f"List '{list_name}' not found")
            fields['List'] = {
                'value': {'recordName': lst['id'], 'action': 'NONE', 'zoneID': self.zone_id},
                'type': 'REFERENCE'
            }
        
        r = self.session.post(
            f'{self.ck_url}/database/1/{self.container}/production/private/records/modify',
            params=self.params,
            json={
                'zoneID': self.zone_id,
                'operations': [{
                    'operationType': 'update',
                    'record': {
                        'recordName': record_name,
                        'recordType': 'Reminder',
                        'recordChangeTag': record_tag,
                        'fields': fields
                    }
                }]
            },
            headers=self.headers
        )
        
        if r.status_code != 200:
            raise Exception(f"Failed to update: {r.status_code} - {r.text[:200]}")
        
        resp = r.json()
        if resp.get('records') and not resp['records'][0].get('serverErrorCode'):
            return {
                'id': record_name, 
                'title': title or old_title, 
                'updated': True,
                'fields_changed': [k for k in fields.keys() if k != 'LastModifiedDate']
            }
        else:
            error = resp['records'][0].get('serverErrorCode', 'Unknown') if resp.get('records') else 'No response'
            raise Exception(f"Update failed: {error}")
    
    def create_list(self, name, color='blue', parent_name=None):
        """
        Create a new reminder list.
        
        Args:
            name: List name
            color: Color name (blue, red, green, orange, purple, yellow)
            parent_name: Parent list/group name for hierarchy (optional)
        
        Returns:
            dict with id, name
        """
        # Color map
        colors = {
            'blue': {"ckSymbolicColorName": "blue", "daHexString": "#007AFF"},
            'red': {"ckSymbolicColorName": "red", "daHexString": "#FF3B30"},
            'green': {"ckSymbolicColorName": "green", "daHexString": "#34C759"},
            'orange': {"ckSymbolicColorName": "orange", "daHexString": "#FF9500"},
            'purple': {"ckSymbolicColorName": "purple", "daHexString": "#AF52DE"},
            'yellow': {"ckSymbolicColorName": "yellow", "daHexString": "#FFCC00"},
        }
        color_data = colors.get(color.lower(), colors['blue'])
        
        # Find parent if specified
        parent_id = None
        if parent_name:
            for lst in self.get_lists():
                if lst['name'].lower() == parent_name.lower():
                    parent_id = lst['id']
                    break
        
        list_uuid = str(uuid.uuid4()).upper()
        record_name = f"List/{list_uuid}"
        
        # Minimal fields that work - server auto-handles encryption
        fields = {
            'Name': {'value': name, 'type': 'STRING'},
            'Deleted': {'value': 0, 'type': 'NUMBER_INT64'},
            'Imported': {'value': 0, 'type': 'NUMBER_INT64'},
        }
        
        if parent_id:
            fields['ParentList'] = {
                'value': {'recordName': parent_id, 'action': 'NONE', 'zoneID': self.zone_id},
                'type': 'REFERENCE'
            }
        
        r = requests.post(
            f'{self.ck_url}/database/1/{self.container}/production/private/records/modify',
            params=self.params,
            cookies=dict(self.session.cookies),
            headers={**dict(self.session.headers), **self.headers},
            json={
                'zoneID': self.zone_id,
                'operations': [{'operationType': 'create', 'record': {
                    'recordName': record_name,
                    'recordType': 'List',
                    'fields': fields
                }}]
            },
            verify=False
        )
        
        if r.status_code != 200:
            raise Exception(f"Failed to create list: {r.status_code}")
        
        resp = r.json()
        if resp.get('records') and not resp['records'][0].get('serverErrorCode'):
            return {'id': record_name, 'name': name, 'color': color}
        else:
            error = resp['records'][0].get('reason', 'Unknown') if resp.get('records') else 'No response'
            raise Exception(f"Create list failed: {error}")


def cmd_lists(rem):
    """Show all lists with hierarchy"""
    lists = rem.get_lists()
    
    if JSON_MODE:
        print(json.dumps(lists, indent=2, default=str))
        return
    
    # Build hierarchy
    groups = [l for l in lists if l['is_group']]
    children = [l for l in lists if not l['is_group']]
    
    print("📋 REMINDER LISTS")
    print("=" * 40)
    
    # Get reminder counts per list
    reminders = rem.get_reminders(include_completed=False)
    counts = {}
    for r in reminders:
        lid = r['list_id']
        counts[lid] = counts.get(lid, 0) + 1
    
    for group in groups:
        print(f"\n📁 {group['name']} ({group['color']})")
        for child in children:
            if child['parent_id'] == group['id']:
                count = counts.get(child['id'], 0)
                print(f"   📋 {child['name']} — {count} pending")
    
    # Orphan lists (no parent)
    orphans = [c for c in children if not c['parent_id'] or not any(g['id'] == c['parent_id'] for g in groups)]
    if orphans:
        print("\n📋 Other Lists")
        for child in orphans:
            count = counts.get(child['id'], 0)
            print(f"   📋 {child['name']} — {count} pending")


def cmd_pending(rem):
    """Show pending reminders"""
    reminders = rem.get_reminders(include_completed=False)
    lists = {l['id']: l['name'] for l in rem.get_lists()}
    
    if JSON_MODE:
        print(json.dumps(reminders, indent=2, default=str))
        return
    
    print(f"📌 PENDING REMINDERS ({len(reminders)})")
    print("=" * 40)
    
    # Group by list
    by_list = {}
    for r in reminders:
        list_name = lists.get(r['list_id'], 'Unknown')
        by_list.setdefault(list_name, []).append(r)
    
    for list_name, items in sorted(by_list.items()):
        print(f"\n📋 {list_name}")
        for r in items:
            flag = ' 🚩' if r['flagged'] else ''
            due = ''
            if r['due_date']:
                due_str = r['due_date'].strftime('%b %d') if r['all_day'] else r['due_date'].strftime('%b %d %H:%M')
                due = f' 📅 {due_str}'
            print(f"  • {r['title']}{flag}{due}")


def cmd_today(rem):
    """Show reminders due today"""
    reminders = rem.get_reminders(include_completed=False)
    today = datetime.now(timezone.utc).date()
    
    due_today = [r for r in reminders if r['due_date'] and r['due_date'].date() == today]
    
    if JSON_MODE:
        print(json.dumps(due_today, indent=2, default=str))
        return
    
    print(f"📅 DUE TODAY ({len(due_today)})")
    print("=" * 40)
    
    for r in due_today:
        flag = ' 🚩' if r['flagged'] else ''
        time_str = '' if r['all_day'] else f" @ {r['due_date'].strftime('%H:%M')}"
        print(f"  • {r['title']}{flag}{time_str}")
    
    if not due_today:
        print("  Nothing due today! 🎉")


def cmd_overdue(rem):
    """Show overdue reminders"""
    reminders = rem.get_reminders(include_completed=False)
    now = datetime.now(timezone.utc)
    
    overdue = [r for r in reminders if r['due_date'] and r['due_date'] < now]
    
    if JSON_MODE:
        print(json.dumps(overdue, indent=2, default=str))
        return
    
    print(f"⚠️ OVERDUE ({len(overdue)})")
    print("=" * 40)
    
    for r in sorted(overdue, key=lambda x: x['due_date']):
        flag = ' 🚩' if r['flagged'] else ''
        days_ago = (now - r['due_date']).days
        print(f"  • {r['title']}{flag} — {days_ago}d overdue")
    
    if not overdue:
        print("  All caught up! 🎉")


def cmd_flagged(rem):
    """Show flagged reminders"""
    reminders = rem.get_reminders(include_completed=False)
    flagged = [r for r in reminders if r['flagged']]
    
    if JSON_MODE:
        print(json.dumps(flagged, indent=2, default=str))
        return
    
    print(f"🚩 FLAGGED ({len(flagged)})")
    print("=" * 40)
    
    for r in flagged:
        due = ''
        if r['due_date']:
            due = f" 📅 {r['due_date'].strftime('%b %d')}"
        print(f"  • {r['title']}{due}")


def cmd_search(rem, query):
    """Search reminders by title"""
    reminders = rem.get_reminders(include_completed=True)
    query_lower = query.lower()
    
    matches = [r for r in reminders if query_lower in r['title'].lower()]
    
    if JSON_MODE:
        print(json.dumps(matches, indent=2, default=str))
        return
    
    print(f"🔍 SEARCH: '{query}' ({len(matches)} matches)")
    print("=" * 40)
    
    for r in matches:
        status = '✓' if r['completed'] else '•'
        flag = ' 🚩' if r['flagged'] else ''
        print(f"  {status} {r['title']}{flag}")


def cmd_tags(rem):
    """Show all hashtags"""
    tags = rem.get_hashtags()
    
    if JSON_MODE:
        print(json.dumps(tags, indent=2))
        return
    
    print(f"#️⃣ HASHTAGS ({len(tags)})")
    print("=" * 40)
    print(f"  #{' #'.join(tags)}")


def cmd_summary(rem):
    """Quick summary for heartbeats"""
    reminders = rem.get_reminders(include_completed=False)
    now = datetime.now(timezone.utc)
    today = now.date()
    
    overdue = [r for r in reminders if r['due_date'] and r['due_date'] < now]
    due_today = [r for r in reminders if r['due_date'] and r['due_date'].date() == today]
    flagged = [r for r in reminders if r['flagged']]
    
    if JSON_MODE:
        print(json.dumps({
            'total_pending': len(reminders),
            'overdue': len(overdue),
            'due_today': len(due_today),
            'flagged': len(flagged),
        }, indent=2))
        return
    
    print(f"📊 REMINDERS SUMMARY")
    print(f"  Pending: {len(reminders)}")
    print(f"  Overdue: {len(overdue)}")
    print(f"  Due today: {len(due_today)}")
    print(f"  Flagged: {len(flagged)}")
    
    if overdue:
        print(f"\n⚠️ Overdue:")
        for r in overdue[:3]:
            print(f"  • {r['title']}")
        if len(overdue) > 3:
            print(f"  ... and {len(overdue) - 3} more")


def cmd_all(rem):
    """Show all reminders grouped by list"""
    reminders = rem.get_reminders(include_completed=True)
    lists = {l['id']: l['name'] for l in rem.get_lists()}
    
    if JSON_MODE:
        print(json.dumps(reminders, indent=2, default=str))
        return
    
    pending = [r for r in reminders if not r['completed']]
    completed = [r for r in reminders if r['completed']]
    
    print(f"📋 ALL REMINDERS ({len(pending)} pending, {len(completed)} completed)")
    print("=" * 40)
    
    # Group pending by list
    by_list = {}
    for r in pending:
        list_name = lists.get(r['list_id'], 'Unknown')
        by_list.setdefault(list_name, []).append(r)
    
    for list_name, items in sorted(by_list.items()):
        print(f"\n📋 {list_name}")
        for r in items:
            flag = ' 🚩' if r['flagged'] else ''
            print(f"  • {r['title']}{flag}")
    
    print(f"\n✓ Completed: {len(completed)} items")


def cmd_create(rem, title, list_name=None, flagged=False, due=None, due_time=None,
               notes=None, priority=None, url=None, alarm=None, parent=None, 
               tags=None, recurrence=None, recurrence_interval=1, recurrence_count=None):
    """Create a new reminder with full metadata"""
    from datetime import datetime
    
    # Parse due date/time
    due_date = None
    all_day = True
    
    if due:
        try:
            # Try various date formats
            for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d']:
                try:
                    due_date = datetime.strptime(due, fmt)
                    break
                except ValueError:
                    continue
            
            if not due_date:
                raise ValueError(f"Could not parse date: {due}")
            
            # Add time if provided
            if due_time:
                try:
                    time_parts = datetime.strptime(due_time, '%H:%M')
                    due_date = due_date.replace(hour=time_parts.hour, minute=time_parts.minute)
                    all_day = False
                except ValueError:
                    print(f"Warning: Could not parse time '{due_time}', using all-day")
            
            # Make timezone-aware
            due_date = due_date.replace(tzinfo=timezone.utc)
            
        except Exception as e:
            print(f"Warning: {e}, creating without due date")
            due_date = None
    
    # Map priority names to values
    priority_val = 0
    if priority:
        priority_map = {'high': 1, 'medium': 5, 'low': 9, 'none': 0}
        priority_val = priority_map.get(priority.lower(), 0)
    
    # Parse recurrence
    recurrence_dict = None
    if recurrence:
        recurrence_dict = {
            'frequency': recurrence,
            'interval': recurrence_interval,
        }
        if recurrence_count:
            recurrence_dict['count'] = recurrence_count
    
    # Parse tags
    tag_list = None
    if tags:
        tag_list = [t.strip().lstrip('#') for t in tags.split(',')]
    
    result = rem.create_reminder(
        title, 
        list_name=list_name, 
        flagged=flagged,
        due_date=due_date,
        notes=notes,
        priority=priority_val,
        all_day=all_day,
        url=url,
        alarm_minutes=alarm,
        parent_id=parent,
        tags=tag_list,
        recurrence=recurrence_dict
    )
    
    if JSON_MODE:
        print(json.dumps(result, indent=2, default=str))
        return
    
    print(f"✅ Created reminder:")
    print(f"  Title: {result['title']}")
    print(f"  List: {result['list']}")
    if due_date:
        if all_day:
            print(f"  Due: {due_date.strftime('%Y-%m-%d')}")
        else:
            print(f"  Due: {due_date.strftime('%Y-%m-%d %H:%M')}")
    if flagged:
        print(f"  Flagged: Yes")
    if priority_val:
        print(f"  Priority: {priority}")
    if result.get('has_alarm'):
        print(f"  Alarm: {alarm} min before")
    if result.get('has_tags'):
        print(f"  Tags: {tags}")
    if result.get('has_recurrence'):
        print(f"  Recurrence: {recurrence} (every {recurrence_interval})")
    if result.get('is_subtask'):
        print(f"  Parent: {parent}")
    print(f"  ID: {result['id']}")


def cmd_delete(rem, identifier):
    """Delete a reminder by ID or title"""
    result = rem.delete_reminder(identifier)
    
    if JSON_MODE:
        print(json.dumps(result, indent=2, default=str))
        return
    
    print(f"🗑️ Deleted reminder:")
    print(f"  Title: {result['title']}")
    print(f"  ID: {result['id']}")


def cmd_complete(rem, identifier):
    """Mark a reminder as complete"""
    result = rem.complete_reminder(identifier)
    
    if JSON_MODE:
        print(json.dumps(result, indent=2, default=str))
        return
    
    print(f"✅ Completed reminder:")
    print(f"  Title: {result['title']}")
    print(f"  ID: {result['id']}")


def cmd_update(rem, identifier, title=None, flagged=None, unflag=False, due=None, 
               notes=None, priority=None, list_name=None):
    """Update an existing reminder"""
    from datetime import datetime
    
    # Parse due date
    due_date = None
    if due:
        for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d']:
            try:
                due_date = datetime.strptime(due, fmt).replace(tzinfo=timezone.utc)
                break
            except ValueError:
                continue
    
    # Handle flagged/unflag
    flag_value = None
    if flagged:
        flag_value = True
    elif unflag:
        flag_value = False
    
    # Map priority
    priority_val = None
    if priority:
        priority_map = {'high': 1, 'medium': 5, 'low': 9, 'none': 0}
        priority_val = priority_map.get(priority.lower())
    
    result = rem.update_reminder(
        identifier,
        title=title,
        flagged=flag_value,
        due_date=due_date,
        notes=notes,
        priority=priority_val,
        list_name=list_name
    )
    
    if JSON_MODE:
        print(json.dumps(result, indent=2, default=str))
        return
    
    print(f"✏️ Updated reminder:")
    print(f"  Title: {result['title']}")
    print(f"  Changed: {', '.join(result['fields_changed'])}")
    print(f"  ID: {result['id']}")


def cmd_create_list(rem, name, color='blue', parent=None):
    """Create a new reminder list (experimental - may not work reliably)"""
    try:
        result = rem.create_list(name, color=color, parent_name=parent)
        
        if JSON_MODE:
            print(json.dumps(result, indent=2, default=str))
            return
        
        print(f"📋 Created list:")
        print(f"  Name: {result['name']}")
        print(f"  Color: {result['color']}")
        print(f"  ID: {result['id']}")
    except Exception as e:
        print(f"❌ List creation failed: {e}")
        print("   Note: List creation via CloudKit API is inconsistent.")
        print("   Create lists manually in Reminders app instead.")


def main():
    global JSON_MODE
    
    parser = argparse.ArgumentParser(description='iCloud Reminders (iOS 13+ CloudKit)')
    parser.add_argument('-u', '--username', required=True, help='iCloud email')
    parser.add_argument('-p', '--password', required=True, help='App-specific password')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    subparsers.add_parser('lists', help='Show all lists')
    subparsers.add_parser('all', help='Show all reminders')
    subparsers.add_parser('pending', help='Show pending reminders')
    subparsers.add_parser('today', help='Show reminders due today')
    subparsers.add_parser('overdue', help='Show overdue reminders')
    subparsers.add_parser('flagged', help='Show flagged reminders')
    subparsers.add_parser('tags', help='Show all hashtags')
    subparsers.add_parser('summary', help='Quick summary')
    
    search_parser = subparsers.add_parser('search', help='Search reminders')
    search_parser.add_argument('query', help='Search query')
    
    create_parser = subparsers.add_parser('create', help='Create a reminder')
    create_parser.add_argument('title', help='Reminder title')
    create_parser.add_argument('--list', dest='list_name', help='List name (default: first available)')
    create_parser.add_argument('--flagged', action='store_true', help='Mark as flagged')
    create_parser.add_argument('--due', help='Due date (YYYY-MM-DD)')
    create_parser.add_argument('--time', dest='due_time', help='Due time (HH:MM, 24h format)')
    create_parser.add_argument('--notes', help='Notes/description')
    create_parser.add_argument('--priority', choices=['high', 'medium', 'low', 'none'], help='Priority level')
    create_parser.add_argument('--url', help='Associated URL')
    create_parser.add_argument('--alarm', type=int, help='Alert X minutes before due (e.g., 0, 15, 60)')
    create_parser.add_argument('--parent', help='Parent reminder ID for subtask')
    create_parser.add_argument('--tags', help='Comma-separated hashtags (e.g., "work,urgent")')
    create_parser.add_argument('--recurrence', choices=['daily', 'weekly', 'monthly', 'yearly'], 
                               help='Repeat frequency')
    create_parser.add_argument('--recurrence-interval', type=int, default=1, 
                               help='Repeat every N periods (default: 1)')
    create_parser.add_argument('--recurrence-count', type=int, help='Stop after N occurrences')
    # Note: Location-based alarms require device-level encryption and cannot be
    # created via CloudKit API. Use iOS Reminders app for location reminders.
    
    update_parser = subparsers.add_parser('update', help='Update an existing reminder')
    update_parser.add_argument('identifier', help='Reminder ID or title to search')
    update_parser.add_argument('--title', help='New title')
    update_parser.add_argument('--list', dest='list_name', help='Move to list')
    update_parser.add_argument('--flagged', action='store_true', help='Mark as flagged')
    update_parser.add_argument('--unflag', action='store_true', help='Remove flag')
    update_parser.add_argument('--due', help='New due date (YYYY-MM-DD)')
    update_parser.add_argument('--notes', help='New notes')
    update_parser.add_argument('--priority', choices=['high', 'medium', 'low', 'none'], help='Priority level')
    
    delete_parser = subparsers.add_parser('delete', help='Delete a reminder')
    delete_parser.add_argument('identifier', help='Reminder ID or title to search')
    
    complete_parser = subparsers.add_parser('complete', help='Mark a reminder as complete')
    complete_parser.add_argument('identifier', help='Reminder ID or title to search')
    
    createlist_parser = subparsers.add_parser('create-list', help='Create a new list')
    createlist_parser.add_argument('name', help='List name')
    createlist_parser.add_argument('--color', default='blue', 
                                   choices=['blue', 'red', 'green', 'orange', 'purple', 'yellow'],
                                   help='List color')
    createlist_parser.add_argument('--parent', help='Parent list/group name')
    
    args = parser.parse_args()
    JSON_MODE = args.json
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    rem = iCloudReminders(args.username, args.password)
    
    commands = {
        'lists': lambda: cmd_lists(rem),
        'all': lambda: cmd_all(rem),
        'pending': lambda: cmd_pending(rem),
        'today': lambda: cmd_today(rem),
        'overdue': lambda: cmd_overdue(rem),
        'flagged': lambda: cmd_flagged(rem),
        'tags': lambda: cmd_tags(rem),
        'summary': lambda: cmd_summary(rem),
        'search': lambda: cmd_search(rem, args.query),
        'create': lambda: cmd_create(rem, args.title, args.list_name, args.flagged,
                                     args.due, args.due_time, args.notes, args.priority, args.url,
                                     args.alarm, args.parent, args.tags, args.recurrence,
                                     args.recurrence_interval, args.recurrence_count),
        'update': lambda: cmd_update(rem, args.identifier, args.title, args.flagged, args.unflag,
                                     args.due, args.notes, args.priority, args.list_name),
        'delete': lambda: cmd_delete(rem, args.identifier),
        'complete': lambda: cmd_complete(rem, args.identifier),
        'create-list': lambda: cmd_create_list(rem, args.name, args.color, args.parent),
    }
    
    commands[args.command]()


if __name__ == '__main__':
    main()
