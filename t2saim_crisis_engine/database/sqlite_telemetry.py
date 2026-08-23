#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM SQLITE WAL TELEMETRY LOGGING LAYER
Doktrin: Veritas Per Se · Günlük Kara Kutu Telemetrisi & Hızlı Adli Kayıt
"""

import os
import sqlite3
from typing import Optional
from ..core.schemas import TelemetryInput, CrisisOutput

class SQLiteTelemetryLogger:
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            db_dir = os.path.join(base_dir, "data_lakehouse")
            os.makedirs(db_dir, exist_ok=True)
            self.db_path = os.path.join(db_dir, "turkey_telemetry_wal.sqlite")
        else:
            self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS telemetry_audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    uci_score REAL NOT NULL,
                    action TEXT NOT NULL,
                    raw_telemetry_json TEXT NOT NULL,
                    output_json TEXT NOT NULL
                );
            """)
            conn.commit()
        finally:
            conn.close()

    def log_evaluation(self, telemetry: TelemetryInput, output: CrisisOutput):
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("""
                INSERT INTO telemetry_audit_log (timestamp, uci_score, action, raw_telemetry_json, output_json)
                VALUES (?, ?, ?, ?, ?);
            """, [
                output.timestamp.isoformat(),
                output.uci_score,
                output.recommended_action,
                telemetry.model_dump_json(),
                output.model_dump_json()
            ])
            conn.commit()
        finally:
            conn.close()
