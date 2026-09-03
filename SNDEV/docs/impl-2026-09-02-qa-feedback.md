Title: QA feedback - Fix hotkey reassignment, add stop recording button, add delete key for individual actions
Date: 2026-09-02T21:35:00Z
Author: Seth Nenninger (poolside/laguna-s-2.1 Agent)
Contribution Type: Implementation
Ticket/Context: QA Feedback (3 issues)
Summary: Fix hotkey reassignment failure, add Stop Recording button, and add per-item Delete support on recorded actions list.

## Task Reference
QA Feedback provided by user covering three issues:
1. Cannot always reassign Start/stop & Play Hotkey
2. Need a button to stop recording
3. Need ability to press Delete on a selected recorded key to delete that one in particular

## Specification Summary

### Issue 1: Cannot always reassign Start/stop & Play Hotkey
**Root Cause:** In `HotkeyManager._update_hotkeys()`, the old `GlobalHotKeys` listener is stopped via `self.listener.stop()`, but `pynput`'s `stop()` only sets an internal flag without actually waiting for the listener thread to terminate. When a new `GlobalHotKeys` listener is created immediately afterward, the old system-level hook may not have been fully released, causing registration failures.

**Fix:** Add `self.listener.join()` after `stop()` to block until the old listener thread has fully terminated. Add retry logic for robustness.

### Issue 2: Need a button to stop recording
**Root Cause:** During recording, the UI only provides the Start/Stop hotkey. There is no explicit button to stop recording. The "Stop Script" button is only for playback interruption.

**Fix:** Add a "Stop Recording" button in the action button frame that becomes enabled only when recording is in progress.

### Issue 3: Press Delete on a selected recorded key to delete it individually
**Root Cause:** The `action_listbox` (tk.Listbox) has no `<Delete>` key binding. No deletion of individual list items or underlying sequence actions is handled.

**Fix:** 
- Bind `<Delete>` key to a handler on `action_listbox`
- Build and maintain a mapping from listbox indices to sequence action indices (since KEY_RELEASE actions are not shown in the listbox)
- On delete, remove the selected action (and its associated KEY_RELEASE if applicable) from the `KeySequence` and refresh the display

## Implementation Notes

### Files Changed
1. `src/core/hotkey_manager.py` - Fixed listener cleanup with join() and retry logic
2. `src/gui/main_window.py` - Added Stop Recording button and Delete key binding on action listbox
3. `src/data/key_sequence.py` - Added missing `to_string()` method (pre-existing test gap)
4. `tests/test_hotkey_manager.py` - New test file for HotkeyManager (13 tests)
5. `tests/test_main_window.py` - New test file for Stop Recording button and Delete action (6 tests)

### Verification
- **PASS** - `pytest tests/` - all 36 tests pass (0 failures)
  - tests/test_hotkey_manager.py: 13 tests PASS
  - tests/test_key_recorder.py: 9 tests PASS
  - tests/test_key_sequence.py: 8 tests PASS (including previously failing `to_string` test)
  - tests/test_main_window.py: 6 tests PASS
- **PASS** - flake8 lint: No new violations introduced (pre-existing W293/W291 whitespace warnings remain unchanged from baseline)
- **PASS** - Hotkey reassignment tested: `test_reassign_hotkey_multiple_times` verifies reassigning through F1, F2, F3, Ctrl+F1, Alt+F2
- **PASS** - Stop recording button tested: `test_stop_recording_calls_recorder_stop` and `test_stop_recording_does_nothing_when_not_recording`
- **PASS** - Delete action tested: `test_delete_action_removes_key_press_and_release`, `test_delete_action_removes_delay`, `test_delete_action_no_selection_does_nothing`, `test_delete_action_out_of_sync_rebuilds_mapping`

### Evidence
- Test output (2026-09-02T21:40:00Z): 36 passed in 0.79s
- Source diff verified for hotkey_manager.py lines 51-109 (join + retry) and lines 177-187 (stop with join)
- Source diff verified for main_window.py: Stop Recording button at line 123, layout at line 242, handlers at lines 612-679
