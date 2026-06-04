# conftest.py
import sys
import os
import tempfile
import atexit
import pytest

# 1. Project root on path — must be before any agent imports
sys.path.insert(0, os.path.dirname(__file__))

# 2. Override DB path before agent.logger is imported anywhere
_tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
_tmp.close()
os.environ["COLLECTION_DB_PATH"] = _tmp.name

# 3. Clean up temp DB file when pytest process exits
atexit.register(
    lambda: os.unlink(_tmp.name) if os.path.exists(_tmp.name) else None
)

# 4. Safe to import now — DB_PATH will resolve to temp file
from agent.logger import get_connection, init_db


@pytest.fixture(autouse=True)
def fresh_db():
    """
    Runs automatically before every test function.
    Drops and recreates all tables → guaranteed clean state.
    Defined here (not in test files) so it applies to all test modules.
    """
    conn = get_connection()
    conn.executescript("""
        DROP TABLE IF EXISTS communication_log;
        DROP TABLE IF EXISTS invoice_stage_tracker;
    """)
    conn.close()
    init_db()