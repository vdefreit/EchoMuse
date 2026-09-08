"""The bare stop kill word must be responsive without firing on one spike."""

import em_stopword


def test_clear_stop_fires_immediately():
    decision = em_stopword.decide(score=0.68, prev_score=0.0)
    assert decision.fired
    assert "score=" in decision.note


def test_borderline_stop_needs_two_adjacent_frames():
    assert not em_stopword.decide(score=0.66, prev_score=0.0).fired
    decision = em_stopword.decide(score=0.66, prev_score=0.67)
    assert decision.fired
    assert "two consecutive" in decision.note


def test_a_dip_breaks_borderline_confirmation():
    assert not em_stopword.decide(score=0.66, prev_score=0.2).fired


def test_threshold_itself_does_not_fire():
    assert not em_stopword.decide(score=em_stopword.STOP_THRESHOLD,
                                  prev_score=0.99).fired


def test_non_detection_has_no_reason():
    assert em_stopword.decide(score=0.1, prev_score=0.9).note == ""
