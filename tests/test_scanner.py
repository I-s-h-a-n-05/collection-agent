# tests/test_scanner.py
from agent.logger import mark_stage_done
from agent.scanner import days_delta, get_pending_stage, STAGES


def test_days_delta_future():
    assert days_delta("2099-01-01") < 0


def test_days_delta_past():
    assert days_delta("2000-01-01") > 0

def test_no_stage_too_early():
    result = get_pending_stage(-30, "CUST001", "CUST001_2099-01-01")
    assert result is None


def test_pre_7_fires():
    result = get_pending_stage(-7, "CUST_T", "CUST_T_REF")
    assert result == "pre_7"


def test_pre_3_fires_skips_pre_7_if_done():
    mark_stage_done("CUST_T", "CUST_T_REF", "pre_7")
    result = get_pending_stage(-3, "CUST_T", "CUST_T_REF")
    assert result == "pre_3"


def test_most_recent_stage_wins():
    # delta=8: pre_7/pre_3/pre_1/post_1/post_7 all reached, none sent → post_7 wins
    result = get_pending_stage(8, "CUST_NEW", "CUST_NEW_REF")
    assert result == "post_7"


def test_escalation_at_30_days():
    result = get_pending_stage(30, "CUST_ESC", "CUST_ESC_REF")
    assert result == "post_30"


def test_all_stages_done_returns_none():
    for stage_id, _ in STAGES:
        mark_stage_done("CUST_DONE", "CUST_DONE_REF", stage_id)
    result = get_pending_stage(30, "CUST_DONE", "CUST_DONE_REF")
    assert result is None