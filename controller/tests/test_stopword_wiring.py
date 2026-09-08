"""The stop classifier must kill playback without starting another turn."""

from pathlib import Path


CONTROLLER = Path(__file__).resolve().parents[1]
SOURCE = (CONTROLLER / "em_controller.py").read_text()


def test_stop_is_armed_only_during_playback_and_after_warmup():
    watcher = SOURCE[SOURCE.index("async def _barge_watcher"):]
    watcher = watcher[:watcher.index("\n\nasync def _run_post_turn_playback")]
    assert "if in_playback and stop_pred_key" in watcher
    assert "if stop_fired and trusted" in watcher


def test_stop_flushes_audio_and_records_its_own_reason():
    watcher = SOURCE[SOURCE.index("async def _barge_watcher"):]
    watcher = watcher[:watcher.index("\n\nasync def _run_post_turn_playback")]
    assert 'send_control({"type": "speaker_flush"})' in watcher
    assert 'reason="stopped"' in watcher
    assert "device.stop_word_detected = True" in watcher


def test_stop_path_exits_before_continuation_without_rearming_mic():
    start = SOURCE.index("if device.stop_word_detected:")
    block = SOURCE[start:SOURCE.index("if should_continue", start)]
    assert "break" in block
    assert "mic_start" not in block
    assert "continue" not in block
