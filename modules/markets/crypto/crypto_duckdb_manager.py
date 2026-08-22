#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM CRYPTO MARKET DUCKDB LAKEHOUSE MANAGER (TICKET-CRYPTO-01)
Doktrin: Veritas Per Se · <$2000 Asimetrik Kripto Varlıkları ve Mekanik Amnezi
"""

import os
import duckdb
import pandas as pd
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator

from modules.common.t2saim_logger import get_logger, log_audit_event

logger = get_logger("CRYPTO_DUCKDB_MANAGER")

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DEFAULT_CRYPTO_DB_PATH = os.path.join(PROJECT_ROOT, "data_lakehouse", "crypto_market.duckdb")

# =====================================================================
# PYDANTIC V2 VERİ MODELLERİ
# =====================================================================

class CryptoCandleRecord(BaseModel):
    timestamp: datetime
    symbol: str = Field(..., max_length=15)
    open: float = Field(..., gt=0.0)
    high: float = Field(..., gt=0.0)
    low: float = Field(..., gt=0.0)
    close: float = Field(..., gt=0.0)
    volume: float = Field(..., ge=0.0)
    funding_rate: float = Field(default=0.0, description="8 Saatlik Fonlama Oranı")
    open_interest: float = Field(default=0.0, ge=0.0)
    wash_trading_score: float = Field(default=0.0, ge=0.0, le=1.0)

    @field_validator("high")
    @classmethod
    def validate_high(cls, v, info):
        low = info.data.get("low")
        if low is not None and v < low:
            raise ValueError(f"High ({v}) Low'dan ({low}) küçük olamaz!")
        return v

class CryptoSignalRecord(BaseModel):
    signal_id: str
    timestamp: datetime
    symbol: str
    macro_trend_regime: str
    funding_arbitrage_annual_pct: float
    expected_roi_pct: float
    real_roi_usd_pct: float
    wash_trading_risk: float = Field(..., ge=0.0, le=1.0)
    captain_approval: str = Field(default="PENDING")
    sha256_hash: str

# =====================================================================
# KRİPTO DUCKDB GÖL YÖNETİCİSİ
# =====================================================================

class CryptoDuckDBManager:
    def __init__(self, db_path: str = DEFAULT_CRYPTO_DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_tables()

    def _get_connection(self) -> duckdb.DuckDBPyConnection:
        con = duckdb.connect(self.db_path)
        con.execute("PRAGMA threads=4;")
        con.execute("PRAGMA memory_limit='1GB';")
        return con

    def init_tables(self):
        """Kripto Podu için DuckDB tablolarını oluşturur."""
        con = self._get_connection()
        try:
            # 1. Kripto Fiyat ve Türev Metrikleri Tablosu
            con.execute("""
            CREATE TABLE IF NOT EXISTS crypto_candles (
                timestamp TIMESTAMP,
                symbol VARCHAR(15),
                open DOUBLE,
                high DOUBLE,
                low DOUBLE,
                close DOUBLE,
                volume DOUBLE,
                funding_rate DOUBLE,
                open_interest DOUBLE,
                wash_trading_score DOUBLE,
                PRIMARY KEY (timestamp, symbol)
            );
            """)

            # 2. Makro Kripto Rejim ve TAS-GNN Logları
            con.execute("""
            CREATE TABLE IF NOT EXISTS crypto_regime_telemetry (
                timestamp TIMESTAMP PRIMARY KEY,
                btc_dominance DOUBLE,
                eth_btc_ratio DOUBLE,
                macro_regime VARCHAR(30),
                total_oi_usd DOUBLE,
                liquidation_cascade_risk DOUBLE
            );
            """)

            # 3. Kripto Sinyalleri ve İcra Kütüğü
            con.execute("""
            CREATE TABLE IF NOT EXISTS crypto_signals_ledger (
                signal_id VARCHAR(64) PRIMARY KEY,
                timestamp TIMESTAMP,
                symbol VARCHAR(15),
                macro_trend_regime VARCHAR(30),
                funding_arbitrage_annual_pct DOUBLE,
                expected_roi_pct DOUBLE,
                real_roi_usd_pct DOUBLE,
                wash_trading_risk DOUBLE,
                captain_approval VARCHAR(10),
                sha256_hash VARCHAR(64)
            );
            """)
            logger.info("Crypto DuckDB Lakehouse tabloları başarıyla hazırlandı.")
        finally:
            con.close()

    def insert_crypto_candles(self, records: List[CryptoCandleRecord]):
        """Kripto mumlarını toplu olarak yazar."""
        if not records:
            return
        con = self._get_connection()
        try:
            data = [
                (r.timestamp, r.symbol, r.open, r.high, r.low, r.close, r.volume, r.funding_rate, r.open_interest, r.wash_trading_score)
                for r in records
            ]
            con.executemany("""
            INSERT OR REPLACE INTO crypto_candles 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, data)
            logger.info(f"{len(records)} adet Kripto mumu DuckDB'ye yazıldı.")
            log_audit_event("DUCKDB_INSERT_CRYPTO", {"count": len(records), "sample": records[0].symbol})
        finally:
            con.close()

    def get_causal_crypto_window(self, symbol: str, target_date: datetime, lookback_days: int = 60) -> pd.DataFrame:
        """Gelecek sızıntısını engelleyen nedensellik penceresi."""
        con = self._get_connection()
        try:
            query = """
            SELECT * FROM crypto_candles
            WHERE symbol = ? AND timestamp <= ?
            ORDER BY timestamp DESC
            LIMIT ?
            """
            df = con.execute(query, (symbol, target_date, lookback_days)).df()
            if not df.empty:
                df = df.sort_values("timestamp").reset_index(drop=True)
            return df
        finally:
            con.close()
