#!/usr/bin/env python3
"""
FINAL COMPREHENSIVE TEST - iCloud Reminders Skill
Tests every feature with validation
"""
import subprocess
import json
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

CREDS = '-u "michaelwolfex@gmail.com" -p "*Mlkiop55*"'
CMD = f'python reminders.py {CREDS}'

def run(args, expect_success=True):
    """Run command and return parsed output"""
    full_cmd = f'{CMD} --json {args}'
    result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, cwd='skills/icloud-reminders')
    
    if result.returncode != 0 and expect_success:
        print(f"❌ FAILED: {args}")
        print(f"   Error: {result.stderr[:300]}")
        return None
    
    try:
        return json.loads(result.stdout) if result.stdout.strip() else {}
    except:
        return result.stdout

def run_text(args):
    """Run command and return text output"""
    full_cmd = f'{CMD} {args}'
    result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, cwd='skills/icloud-reminders')
    return result.stdout, result.returncode

print("=" * 70)
print("🦊 FINAL COMPREHENSIVE TEST - iCloud Reminders Skill")
print("=" * 70)

# Track created items for cleanup
created_ids = []
tests_passed = 0
tests_failed = 0

def test(name, condition, details=""):
    global tests_passed, tests_failed
    if condition:
        print(f"✅ {name}")
        if details:
            print(f"   {details}")
        tests_passed += 1
    else:
        print(f"❌ {name}")
        if details:
            print(f"   {details}")
        tests_failed += 1

# ============================================================
print("\n📊 TEST 1: Get baseline stats")
print("-" * 40)
before = run('summary')
test("Summary returns data", before is not None and 'total_pending' in before,
     f"Pending: {before.get('total_pending', '?')}, Overdue: {before.get('overdue', '?')}")

# ============================================================
print("\n📝 TEST 2: Create FULL-FEATURED reminder")
print("-" * 40)
# Using all options: list, due, time, alarm, flagged, priority, notes, url, tags, recurrence
create_result = run('create "Ultimate Fox Test 2026" --list Life --due 2026-02-15 --time 14:30 --alarm 30 --flagged --priority high --notes "This tests ALL features" --url "https://clawdhub.com" --tags "test,fox,ultimate" --recurrence weekly --recurrence-interval 2')

test("Create with all options", create_result and create_result.get('id'),
     f"ID: {create_result.get('id', '?')[:50]}...")

if create_result and create_result.get('id'):
    parent_id = create_result['id']
    created_ids.append(parent_id)
    
    test("Has alarm", create_result.get('has_alarm') == True)
    test("Has tags", create_result.get('has_tags') == True)
    test("Has recurrence", create_result.get('has_recurrence') == True)

# ============================================================
print("\n🔍 TEST 3: Verify creation via search")
print("-" * 40)
time.sleep(1)  # Let CloudKit sync
search_result = run('search "Ultimate Fox Test 2026"')
test("Search finds reminder", search_result and len(search_result) > 0,
     f"Found {len(search_result) if search_result else 0} matches")

if search_result and len(search_result) > 0:
    found = search_result[0]
    test("Title correct", "Ultimate Fox Test" in found.get('title', ''),
         f"Title: {found.get('title', '?')}")
    test("Flagged is True", found.get('flagged') == True)
    test("Priority is high (1)", found.get('priority') == 1,
         f"Priority value: {found.get('priority', '?')}")
    test("Has due date", found.get('due_date') is not None)
    test("Has notes", found.get('notes') is not None and 'ALL features' in str(found.get('notes', '')))

# ============================================================
print("\n📝 TEST 4: Create SUBTASK")
print("-" * 40)
if parent_id:
    subtask_result = run(f'create "Fox Subtask 2026" --list Life --parent "{parent_id}"')
    test("Subtask created", subtask_result and subtask_result.get('id'),
         f"ID: {subtask_result.get('id', '?')[:50]}...")
    test("Is marked as subtask", subtask_result.get('is_subtask') == True)
    
    if subtask_result and subtask_result.get('id'):
        subtask_id = subtask_result['id']
        created_ids.append(subtask_id)

# ============================================================
print("\n✏️ TEST 5: Update reminder")
print("-" * 40)
update_result = run('update "Ultimate Fox Test 2026" --title "Updated Fox Test 2026" --unflag --priority medium --notes "Updated notes here"')
test("Update succeeded", update_result and update_result.get('updated') == True,
     f"Changed: {update_result.get('fields_changed', [])}")

# Verify update
time.sleep(1)
verify_update = run('search "Updated Fox Test 2026"')
if verify_update and len(verify_update) > 0:
    updated = verify_update[0]
    test("Title updated", "Updated Fox Test 2026" in updated.get('title', ''))
    test("Unflagged", updated.get('flagged') == False)
    test("Priority changed to medium (5)", updated.get('priority') == 5,
         f"Priority: {updated.get('priority', '?')}")

# ============================================================
print("\n✅ TEST 6: Complete reminder")
print("-" * 40)
complete_result = run('complete "Updated Fox Test 2026"')
test("Complete succeeded", complete_result and complete_result.get('completed') == True)

# Verify completion
time.sleep(1)
all_reminders = run('all')
if all_reminders:
    # Check if it's in completed
    found_completed = False
    for r in all_reminders:
        if 'Updated Fox Test 2026' in r.get('title', '') and r.get('completed'):
            found_completed = True
            break
    test("Verified as completed", found_completed)

# ============================================================
print("\n📋 TEST 7: Lists and Tags")
print("-" * 40)
lists_result = run('lists')
test("Lists retrieved", lists_result and len(lists_result) > 0,
     f"Found {len(lists_result) if lists_result else 0} lists")

tags_result = run('tags')
test("Tags retrieved", tags_result and len(tags_result) > 0,
     f"Tags: {', '.join(tags_result[:5]) if tags_result else 'none'}...")

# ============================================================
print("\n📅 TEST 8: Date queries")
print("-" * 40)
overdue_result = run('overdue')
test("Overdue query works", overdue_result is not None,
     f"Found {len(overdue_result) if overdue_result else 0} overdue")

today_result = run('today')
test("Today query works", today_result is not None,
     f"Found {len(today_result) if today_result else 0} due today")

flagged_result = run('flagged')
test("Flagged query works", flagged_result is not None,
     f"Found {len(flagged_result) if flagged_result else 0} flagged")

# ============================================================
print("\n🗑️ TEST 9: Delete with cascade")
print("-" * 40)
# Delete subtask first
if len(created_ids) > 1:
    delete_sub = run(f'delete "{created_ids[1]}"')
    test("Subtask deleted", delete_sub and delete_sub.get('deleted') == True)

# Delete parent (should cascade alarms)
if created_ids:
    delete_parent = run(f'delete "{created_ids[0]}"')
    test("Parent deleted", delete_parent and delete_parent.get('deleted') == True,
         f"Related deleted: {delete_parent.get('related_deleted', 0)}")

# Verify deletion
time.sleep(1)
verify_delete = run('search "Fox Test 2026"')
test("Verified deleted (not found)", verify_delete is None or len(verify_delete) == 0)

# ============================================================
print("\n📊 TEST 10: Final stats comparison")
print("-" * 40)
after = run('summary')
test("Summary still works", after is not None and 'total_pending' in after,
     f"Pending: {after.get('total_pending', '?')}")

# ============================================================
print("\n" + "=" * 70)
print(f"🦊 FINAL RESULTS: {tests_passed} passed, {tests_failed} failed")
print("=" * 70)

if tests_failed == 0:
    print("\n✨ ALL TESTS PASSED - SKILL IS READY FOR CLAWDHUB! ✨")
else:
    print(f"\n⚠️ {tests_failed} tests failed - review above")
