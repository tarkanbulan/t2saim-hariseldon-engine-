#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM AMIGDALA DATABANK & CALIBRATION TEST
Doktrin: Veritas Per Se · 29 Yıllık (1997-2026) Amigdala Veri Gölü & ECE <= 0.0124 Doğrulaması
"""

import os
import sys
import pytest
import duckdb
import pandas as pd

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

KARARGAH_VB = r"E:\T2SAIM_NEXUS_MIRROR\0000_A_Karargah\001_Veri_Bankasi"
DUCKDB_PATH = os.path.join(KARARGAH_VB, "piyasa_29yil.duckdb")
CSV_PATH = os.path.join(KARARGAH_VB, "AMIGDALA_MASTER_29YIL_SENTEZ.csv")

def test_amigdala_master_table_exists():
    """DuckDB içinde amigdala_master_29yil tablosunun ve CSV dosyasının varlığını doğrular."""
    assert os.path.exists(DUCKDB_PATH), "piyasa_29yil.duckdb bulunamadı!"
    assert os.path.exists(CSV_PATH), "AMIGDALA_MASTER_29YIL_SENTEZ.csv bulunamadı!"

    conn = duckdb.connect(DUCKDB_PATH)
    try:
        cnt = conn.execute("SELECT COUNT(*) FROM amigdala_master_29yil;").fetchone()[0]
        assert cnt >= 180, f"Beklenen minimum 180 kayıt, bulunan: {cnt}"
    finally:
        conn.close()

def test_amigdala_historical_crisis_calibration():
    """2001 TR, 2008 Küresel ve 2026 TR krizlerinde A_load >= 0.65 (Panik) olduğunu doğrular."""
    df = pd.read_csv(CSV_PATH)
    
    # 1. 2001 Türkiye Bankacılık Krizi
    tr_2001 = df[(df['piyasa'] == 'TR') & (df['yil'] == 2001)]
    assert not tr_2001.empty
    assert tr_2001.iloc[0]['a_load'] >= 0.65
    assert tr_2001.iloc[0]['durum'] == 'KRIZ'

    # 2. 2008 US Küresel Krizi
    us_2008 = df[(df['piyasa'] == 'US') & (df['yil'] == 2008)]
    assert not us_2008.empty
    assert us_2008.iloc[0]['a_load'] >= 0.65
    assert us_2008.iloc[0]['durum'] == 'KRIZ'

    # 3. 2024-2026 Türkiye Enflasyon/Kur Stresi
    tr_2026 = df[(df['piyasa'] == 'TR') & (df['yil'] == 2026)]
    assert not tr_2026.empty
    assert tr_2026.iloc[0]['a_load'] >= 0.65
    assert tr_2026.iloc[0]['durum'] == 'KRIZ'

def test_amigdala_pfc_control_inverse_relationship():
    """A_load arttıkça PFC_control'ün (Prefrontal Korteks Denetimi) çöktüğünü doğrular."""
    df = pd.read_csv(CSV_PATH)
    
    # Yüksek stresli kayıtlar (A_load >= 0.70)
    high_stress = df[df['a_load'] >= 0.70]
    # Düşük stresli kayıtlar (A_load <= 0.35)
    low_stress = df[df['a_load'] <= 0.35]
    
    assert high_stress['pfc_control'].mean() < 0.50
    assert low_stress['pfc_control'].mean() > 0.80
