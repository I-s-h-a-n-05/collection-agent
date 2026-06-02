# agent/logger.py
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'collection_log.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS communication_log (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id     TEXT NOT NULL,
            invoice_ref     TEXT NOT NULL,
            stage           TEXT NOT NULL,
            channel         TEXT NOT NULL,
            status          TEXT NOT NULL,
            message_text    TEXT,
            sent_at         TEXT NOT NULL,
            error_detail    TEXT
        );

        CREATE TABLE IF NOT EXISTS invoice_stage_tracker (
            customer_id     TEXT NOT NULL,
            invoice_ref     TEXT NOT NULL,
            stage           TEXT NOT NULL,
            completed_at    TEXT NOT NULL,
            PRIMARY KEY (customer_id, invoice_ref, stage)
        );
    """)

    conn.commit()
    conn.close()
    print("[DB] Tables initialized.")

def log_communication(customer_id, invoice_ref, stage, channel, status, message_text=None, error_detail=None):
    conn = get_connection()
    conn.execute("""
        INSERT INTO communication_log
            (customer_id, invoice_ref, stage, channel, status, message_text, sent_at, error_detail)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (customer_id, invoice_ref, stage, channel, status, message_text, datetime.utcnow().isoformat(), error_detail))
    conn.commit()
    conn.close()

def mark_stage_done(customer_id, invoice_ref, stage):
    conn = get_connection()
    conn.execute("""
        INSERT OR IGNORE INTO invoice_stage_tracker (customer_id, invoice_ref, stage, completed_at)
        VALUES (?, ?, ?, ?)
    """, (customer_id, invoice_ref, stage, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def is_stage_done(customer_id, invoice_ref, stage):
    conn = get_connection()
    row = conn.execute("""
        SELECT 1 FROM invoice_stage_tracker
        WHERE customer_id = ? AND invoice_ref = ? AND stage = ?
    """, (customer_id, invoice_ref, stage)).fetchone()
    conn.close()
    return row is not None

if __name__ == "__main__":
    init_db()