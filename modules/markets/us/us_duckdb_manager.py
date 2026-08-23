#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM US MARKET DUCKDB LAKEHOUSE MANAGER (TICKET-US-01)
Doktrin: Veritas Per Se · ABD Piyasaları Veri Gölü, SPY/QQQ Pusulası & Deterministik Zaman Pencereleri
"""

import os
import sys
import duckdb
import pandas as pd
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional

# Root path resolution
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from modules.common.t2saim_logger import get_logger

logger = get_logger("US_DUCKDB_MANAGER")

class USCandleRecord(BaseModel):
    timestamp: datetime
    symbol: str = Field(..., description="Hisse/ETF Sembolü: NVDA, PLTR, VST, CEG, LLY, SPY, QQQ, VIX")
    open: float = Field(..., gt=0.0)
    high: float = Field(..., gt=0.0)
    low: float = Field(..., gt=0.0)
    close: float = Field(..., gt=0.0)
    volume: float = Field(..., ge=0.0)
    sector: str = Field(default="GENERAL")
    vix_level: float = Field(default=15.0, ge=0.0)

class USDuckDBManager:
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            lakehouse_dir = os.path.join(PROJECT_ROOT, "data_lakehouse")
            os.makedirs(lakehouse_dir, exist_ok=True)
            self.db_path = os.path.join(lakehouse_dir, "us_market.duckdb")
        else:
            self.db_path = db_path
            
        self._init_tables()

    def _init_tables(self):
        conn = duckdb.connect(self.db_path)
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS us_candles (
                    timestamp TIMESTAMP NOT NULL,
                    symbol VARCHAR(16) NOT NULL,
                    open DOUBLE NOT NULL,
                    high DOUBLE NOT NULL,
                    low DOUBLE NOT NULL,
                    close DOUBLE NOT NULL,
                    volume DOUBLE NOT NULL,
                    sector VARCHAR(32) NOT NULL,
                    vix_level DOUBLE NOT NULL,
                    PRIMARY KEY (timestamp, symbol)
                );
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS us_alpha_signals (
                    timestamp TIMESTAMP NOT NULL,
                    symbol VARCHAR(16) NOT NULL,
                    hurst_exponent DOUBLE NOT NULL,
                    sector VARCHAR(32) NOT NULL,
                    vix_state VARCHAR(32) NOT NULL,
                    composite_score DOUBLE NOT NULL,
                    is_vetoed BOOLEAN NOT NULL,
                    veto_reason VARCHAR(128)
                );
            """)
            logger.info("US DuckDB Lakehouse tabloları başarıyla hazırlandı.")
        finally:
            conn.close()

    def insert_us_candles(self, records: List[USCandleRecord]):
        if not records:
            return
        data = [
            (
                r.timestamp,
                r.symbol,
                r.open,
                r.high,
                r.low,
                r.close,
                r.volume,
                r.sector,
                r.vix_level
            )
            for r in records
        ]
        conn = duckdb.connect(self.db_path)
        try:
            conn.executemany("""
                INSERT OR REPLACE INTO us_candles 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, data)
            logger.info(f"{len(records)} adet ABD mumu DuckDB'ye yazıldı.")
        finally:
            conn.close()

    def get_causal_us_window(
        self,
        symbol: str,
        target_date: datetime,
        lookback_days: int = 60
    ) -> pd.DataFrame:
        query = """
            SELECT * FROM us_candles
            WHERE symbol = ? AND timestamp <= ?
            ORDER BY timestamp DESC
            LIMIT ?;
        """
        conn = duckdb.connect(self.db_path)
        try:
            df = conn.execute(query, [symbol, target_date, lookback_days]).df()
            if not df.empty:
                df = df.sort_values(by="timestamp").reset_index(drop=True)
            return df
        finally:
            conn.close()
