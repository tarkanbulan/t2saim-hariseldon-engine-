#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM CRISIS ENGINE DUCKDB & PARQUET STORAGE LAYER
Doktrin: Veritas Per Se · Kriz Zaman Serileri & Walk-Forward Veri Deposu
"""

import os
import duckdb
import pandas as pd
from datetime import datetime
from typing import Optional
from ..core.schemas import TelemetryInput, CrisisOutput

class CrisisDuckDBStore:
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            db_dir = os.path.join(base_dir, "data_lakehouse")
            os.makedirs(db_dir, exist_ok=True)
            self.db_path = os.path.join(db_dir, "turkey_crisis_telemetry.duckdb")
        else:
            self.db_path = db_path
        self._init_db()

    def get_connection(self) -> duckdb.DuckDBPyConnection:
        return duckdb.connect(self.db_path)

    def _init_db(self):
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS crisis_outputs (
                    timestamp TIMESTAMP NOT NULL,
                    uci_score DOUBLE NOT NULL,
                    p0 DOUBLE NOT NULL,
                    p1 DOUBLE NOT NULL,
                    phi_macro DOUBLE NOT NULL,
                    phi_bank DOUBLE NOT NULL,
                    phi_neuro DOUBLE NOT NULL,
                    phi_gullini DOUBLE NOT NULL,
                    phi_acemoglu DOUBLE NOT NULL,
                    tactical_state VARCHAR(64) NOT NULL,
                    strategic_state VARCHAR(64) NOT NULL,
                    recommended_action VARCHAR(64) NOT NULL,
                    quarter_kelly DOUBLE NOT NULL
                );
            """)

    def save_crisis_output(self, output: CrisisOutput):
        with self.get_connection() as conn:
            conn.execute("""
                INSERT INTO crisis_outputs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, [
                output.timestamp,
                output.uci_score,
                output.confidence_interval_p0,
                output.confidence_interval_p1,
                output.phi_macro,
                output.phi_bank,
                output.phi_neuro,
                output.phi_gullini,
                output.phi_acemoglu,
                output.tactical_state_d14,
                output.strategic_state_m3,
                output.recommended_action,
                output.quarter_kelly_fraction
            ])
