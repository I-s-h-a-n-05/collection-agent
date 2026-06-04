# tests/test_logger.py
from agent.logger import log_communication, mark_stage_done, is_stage_done, get_connection


def test_stage_not_done_by_default():
    assert is_stage_done("CUST001", "CUST001_2026-06-08", "pre_7") is False


def test_mark_and_check_stage_done():
    mark_stage_done("CUST001", "CUST001_2026-06-08", "pre_7")
    assert is_stage_done("CUST001", "CUST001_2026-06-08", "pre_7") is True


def test_mark_stage_idempotent():
    """Marking same stage twice must not raise or duplicate."""
    mark_stage_done("CUST001", "CUST001_2026-06-08", "pre_7")
    mark_stage_done("CUST001", "CUST001_2026-06-08", "pre_7")
    conn = get_connection()
    count = conn.execute(
        "SELECT COUNT(*) FROM invoice_stage_tracker "
        "WHERE customer_id='CUST001' AND stage='pre_7'"
    ).fetchone()[0]
    conn.close()
    assert count == 1


def test_log_communication_success():
    log_communication("CUST001", "CUST001_2026-06-08", "pre_7", "email", "sent", "Hello", None)
    conn = get_connection()
    row = conn.execute(
        "SELECT status, channel FROM communication_log WHERE customer_id='CUST001'"
    ).fetchone()
    conn.close()
    assert row["status"]  == "sent"
    assert row["channel"] == "email"


def test_log_communication_failure():
    log_communication("CUST002", "CUST002_2026-06-04", "pre_3", "whatsapp", "failed", None, "timeout")
    conn = get_connection()
    row = conn.execute(
        "SELECT error_detail FROM communication_log WHERE customer_id='CUST002'"
    ).fetchone()
    conn.close()
    assert row["error_detail"] == "timeout"


def test_different_stages_are_independent():
    mark_stage_done("CUST001", "CUST001_2026-06-08", "pre_7")
    assert is_stage_done("CUST001", "CUST001_2026-06-08", "pre_3") is False