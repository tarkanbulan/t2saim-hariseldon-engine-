#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM COMMODITY DUCKDB LAKEHOUSE MANAGER (TICKET-COMMODITY-01)
Doktrin: Veritas Per Se · 30 Yıllık Süper Emtialar Veri Gölü & Deterministik Zaman Pencereleri
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

logger = get_logger("COMMODITY_DUCKDB_MANAGER")

class CommodityCandleRecord(BaseModel):
    timestamp: datetime
    symbol: str = Field(..., description="Emtia Sembolü: SILVER, COCOA, URANIUM, COFFEE, COPPER, ALTIN.S1, GOLD_COMPASS, OIL_COMPASS")
    spot_price: float = Field(..., gt=0.0)
    front_month_futures: float = Field(..., gt=0.0)
    next_month_futures: float = Field(..., gt=0.0)
    roll_yield_pct: float = Field(default=0.0, description="Vadeli Taşıma / Roll Getirisi (Backwardation > 0, Contango < 0)")
    physical_deficit_score: float = Field(default=0.5, ge=0.0, le=1.0, description="Fiziksel Arz Açığı Skoru (0.0-1.0)")
    volume: float = Field(default=0.0, ge=0.0)

class CommodityDuckDBManager:
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            lakehouse_dir = os.path.join(PROJECT_ROOT, "data_lakehouse")
            os.makedirs(lakehouse_dir, exist_ok=True)
            self.db_path = os.path.join(lakehouse_dir, "commodity_market.duckdb")
        else:
            self.db_path = db_path
            
        self._init_tables()

    def _init_tables(self):
        conn = duckdb.connect(self.db_path)
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS commodity_candles (
                    timestamp TIMESTAMP NOT NULL,
                    symbol VARCHAR(32) NOT NULL,
                    spot_price DOUBLE NOT NULL,
                    front_month_futures DOUBLE NOT NULL,
                    next_month_futures DOUBLE NOT NULL,
                    roll_yield_pct DOUBLE NOT NULL,
                    physical_deficit_score DOUBLE NOT NULL,
                    volume DOUBLE NOT NULL,
                    PRIMARY KEY (timestamp, symbol)
                );
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS commodity_super_cycle_signals (
                    timestamp TIMESTAMP NOT NULL,
                    symbol VARCHAR(32) NOT NULL,
                    hurst_exponent DOUBLE NOT NULL,
                    contango_state VARCHAR(32) NOT NULL,
                    super_cycle_score DOUBLE NOT NULL,
                    is_vetoed BOOLEAN NOT NULL,
                    veto_reason VARCHAR(128)
                );
            """)
            logger.info("Commodity DuckDB Lakehouse tabloları başarıyla hazırlandı.")
        finally:
            conn.close()

    def insert_commodity_candles(self, records: List[CommodityCandleRecord]):
        if not records:
            return
        data = [
            (
                r.timestamp,
                r.symbol,
                r.spot_price,
                r.front_month_futures,
                r.next_month_futures,
                r.roll_yield_pct,
                r.physical_deficit_score,
                r.volume
            )
            for r in records
        ]
        conn = duckdb.connect(self.db_path)
        try:
            conn.executemany("""
                INSERT OR REPLACE INTO commodity_candles 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, data)
            logger.info(f"{len(records)} adet Emtia mumu DuckDB'ye yazıldı.")
        finally:
            conn.close()

    def get_causal_commodity_window(
        self,
        symbol: str,
        target_date: datetime,
        lookback_days: int = 60
    ) -> pd.DataFrame:
        query = """
            SELECT * FROM commodity_candles
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

if __name__ == "__main__":
    mgr = CommodityDuckDBManager()
    print("Commodity DuckDB Manager hazır:", mgr.db_path)
