#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM TURKEY MARKET DUCKDB LAKEHOUSE MANAGER (TICKET-TR-01)
Doktrin: Veritas Per Se · Mekanik Amnezi ve Sıfır Sızıntı (Zero Leakage)
"""

import os
import duckdb
import pandas as pd
from datetime import datetime, date
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator

from modules.common.t2saim_logger import get_logger, log_audit_event

logger = get_logger("TR_DUCKDB_MANAGER")

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DEFAULT_DB_PATH = os.path.join(PROJECT_ROOT, "data_lakehouse", "tr_market.duckdb")

# =====================================================================
# PYDANTIC V2 VERİ MODELLERİ (TİP VE DEĞER DOĞRULAYICILAR)
# =====================================================================

class BISTCandleRecord(BaseModel):
    timestamp: datetime
    symbol: str = Field(..., max_length=10)
    sector: str = Field(..., max_length=30)
    open: float = Field(..., gt=0.0)
    high: float = Field(..., gt=0.0)
    low: float = Field(..., gt=0.0)
    close: float = Field(..., gt=0.0)
    volume: float = Field(..., ge=0.0)
    c_takas: float = Field(default=0.0, ge=0.0, le=1.0, description="Takasbank Konsantrasyonu")
    r_cancel: float = Field(default=0.0, ge=0.0, le=1.0, description="Sahte Emir İptal Oranı")
    vpin: float = Field(default=0.0, ge=0.0, le=1.0, description="Emir Toksisite Endeksi")

    @field_validator("high")
    @classmethod
    def validate_high(cls, v, info):
        low = info.data.get("low")
        if low is not None and v < low:
            raise ValueError(f"High ({v}) Low'dan ({low}) küçük olamaz!")
        return v

class TRMacroTelemetryRecord(BaseModel):
    timestamp: datetime
    usd_try: float = Field(..., gt=0.0)
    cbrt_policy_rate: float = Field(..., ge=0.0)
    cds_5y: float = Field(..., ge=0.0)
    viop_squeeze_index: float = Field(default=0.0, ge=0.0, le=1.0)
    a_load: float = Field(default=0.0, ge=0.0, le=1.0)
    pfc_control: float = Field(default=1.0, ge=0.0, le=1.0)
    psi_decay: float = Field(default=0.0, ge=0.0)

class CompassAssetRecord(BaseModel):
    timestamp: datetime
    asset_type: str = Field(..., description="'CRYPTO_SUB2000' veya 'SUPER_COMMODITY'")
    symbol: str = Field(..., max_length=15)
    price: float = Field(..., gt=0.0)
    funding_rate: float = Field(default=0.0)
    wash_trading_score: float = Field(default=0.0, ge=0.0, le=1.0)
    physical_premium: float = Field(default=0.0)

class TRSignalRecord(BaseModel):
    signal_id: str
    timestamp: datetime
    symbol: str
    horizon_days: int
    nominal_expected_roi: float
    real_expected_roi: float
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    fraud_risk_score: float = Field(..., ge=0.0, le=1.0)
    captain_approval: str = Field(default="PENDING")
    sha256_hash: str

# =====================================================================
# DUCKDB LAKEHOUSE YÖNETİCİ ÇEKİRDEĞİ
# =====================================================================

class TRDuckDBManager:
    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_tables()

    def _get_connection(self) -> duckdb.DuckDBPyConnection:
        """DuckDB bağlantısını WAL modu ve bellek optimizasyonu ile açar."""
        con = duckdb.connect(self.db_path)
        con.execute("PRAGMA threads=4;")
        con.execute("PRAGMA memory_limit='1GB';")
        return con

    def init_tables(self):
        """T2SAIM Türkiye Podu'nun 4 ana tablosunu oluşturur."""
        con = self._get_connection()
        try:
            # 1. BIST Günlük Fiyat ve Mikro-Yapı Tablosu
            con.execute("""
            CREATE TABLE IF NOT EXISTS bist_daily_candles (
                timestamp TIMESTAMP,
                symbol VARCHAR(10),
                sector VARCHAR(30),
                open DOUBLE,
                high DOUBLE,
                low DOUBLE,
                close DOUBLE,
                volume DOUBLE,
                c_takas DOUBLE,
                r_cancel DOUBLE,
                vpin DOUBLE,
                PRIMARY KEY (timestamp, symbol)
            );
            """)

            # 2. Türkiye Makro, Kur ve Kriz Göstergeleri
            con.execute("""
            CREATE TABLE IF NOT EXISTS tr_macro_crisis_telemetry (
                timestamp TIMESTAMP PRIMARY KEY,
                usd_try DOUBLE,
                cbrt_policy_rate DOUBLE,
                cds_5y DOUBLE,
                viop_squeeze_index DOUBLE,
                a_load DOUBLE,
                pfc_control DOUBLE,
                psi_decay DOUBLE
            );
            """)

            # 3. Pusula Varlıklar (<$2000 Kripto & 30Y Süper Emtialar)
            con.execute("""
            CREATE TABLE IF NOT EXISTS compass_assets_daily (
                timestamp TIMESTAMP,
                asset_type VARCHAR(20),
                symbol VARCHAR(15),
                price DOUBLE,
                funding_rate DOUBLE,
                wash_trading_score DOUBLE,
                physical_premium DOUBLE,
                PRIMARY KEY (timestamp, symbol)
            );
            """)

            # 4. Ex-Ante Tahminler ve Kaptan Onay Kütüğü
            con.execute("""
            CREATE TABLE IF NOT EXISTS tr_signals_ledger (
                signal_id VARCHAR(64) PRIMARY KEY,
                timestamp TIMESTAMP,
                symbol VARCHAR(15),
                horizon_days INTEGER,
                nominal_expected_roi DOUBLE,
                real_expected_roi DOUBLE,
                confidence_score DOUBLE,
                fraud_risk_score DOUBLE,
                captain_approval VARCHAR(10),
                sha256_hash VARCHAR(64)
            );
            """)
            logger.info("DuckDB Lakehouse tabloları başarıyla doğrulandı/kuruldu.")
        finally:
            con.close()

    def insert_bist_candles(self, records: List[BISTCandleRecord]):
        """BIST mum kayıtlarını toplu (bulk) olarak ekler."""
        if not records:
            return
        con = self._get_connection()
        try:
            data = [
                (r.timestamp, r.symbol, r.sector, r.open, r.high, r.low, r.close, r.volume, r.c_takas, r.r_cancel, r.vpin)
                for r in records
            ]
            con.executemany("""
            INSERT OR REPLACE INTO bist_daily_candles 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, data)
            logger.info(f"{len(records)} adet BIST mumu DuckDB'ye yazıldı.")
            log_audit_event("DUCKDB_INSERT_BIST", {"count": len(records), "sample_symbol": records[0].symbol})
        finally:
            con.close()

    def insert_macro_telemetry(self, record: TRMacroTelemetryRecord):
        """Türkiye makro telemetri kaydını ekler."""
        con = self._get_connection()
        try:
            con.execute("""
            INSERT OR REPLACE INTO tr_macro_crisis_telemetry 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record.timestamp, record.usd_try, record.cbrt_policy_rate,
                record.cds_5y, record.viop_squeeze_index, record.a_load,
                record.pfc_control, record.psi_decay
            ))
            logger.info(f"TR Makro Telemetrisi mühürlendi: USD/TRY={record.usd_try}, CDS={record.cds_5y}")
        finally:
            con.close()

    def get_causal_bist_window(self, symbol: str, target_date: datetime, lookback_days: int = 60) -> pd.DataFrame:
        """Mekanik Amnezi Kuralı: target_date'den SONRAKİ hiçbir veriyi getirmez."""
        con = self._get_connection()
        try:
            query = """
            SELECT * FROM bist_daily_candles
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

    def get_latest_macro(self, target_date: Optional[datetime] = None) -> Optional[Dict[str, Any]]:
        """Hedef tarihe en yakın geçerli makro kriz durumunu döner."""
        con = self._get_connection()
        try:
            if target_date:
                query = "SELECT * FROM tr_macro_crisis_telemetry WHERE timestamp <= ? ORDER BY timestamp DESC LIMIT 1"
                res = con.execute(query, (target_date,)).df()
            else:
                query = "SELECT * FROM tr_macro_crisis_telemetry ORDER BY timestamp DESC LIMIT 1"
                res = con.execute(query).df()
            if not res.empty:
                return res.iloc[0].to_dict()
            return None
        finally:
            con.close()
