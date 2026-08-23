#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM CRISIS ENGINE CORE SCHEMAS & MODELS
Doktrin: Veritas Per Se · Pydantic V2 TelemetryInput & CrisisOutput Modelleri
"""

from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class TelemetryInput(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # 1. Makroekonomik & Minsky Göstergeleri
    m2_nir_ratio: float = Field(..., description="M2 Para Arzı / Net Rezerv (Swap Hariç)")
    net_nir_usd_billion: float = Field(..., description="Swap hariç net rezerv ($ Mr)")
    reer_cpi: float = Field(..., description="TÜFE Bazlı Reel Efektif Döviz Kuru")
    ext_debt_service_1y_billion: float = Field(default=191.0)
    dolgap_premium_pct: float = Field(..., description="Kapalıçarşı döviz makası (%)")
    
    # 2. Bankacılık & Likidite Göstergeleri
    ldr_ratio: float = Field(..., description="Kredi / Mevduat Oranı")
    npl_real_ratio: float = Field(..., description="Gerçek / Ötelenen Takipteki Kredi Oranı (%)")
    npl_official_ratio: float = Field(default=1.8, description="Resmi NPL Oranı (%)")
    ted_spread_pct: float = Field(..., description="Gösterge Tahvil - Mevduat Faiz Makası (%)")
    uyap_active_cases_million: float = Field(default=24.5, description="Aktif UYAP icra dosya sayısı (Milyon)")
    bounced_checks_billion_tl: float = Field(default=65.0, description="Karşılıksız çek hacmi (Mr TL)")
    
    # 3. Nörofinans & Toplumsal Kaçış Göstergeleri
    sigma_20_60_ratio: float = Field(default=1.2, description="20 günlük / 60 günlük oynaklık oranı")
    v_run: float = Field(..., ge=0.0, le=1.0, description="Mevduat Kaçış Hızı (0.0-1.0)")
    h_herd: float = Field(..., ge=0.0, le=1.0, description="Kuramoto Sürü Senkronizasyonu (0.0-1.0)")
    fatalism_buffer: float = Field(default=0.85, ge=0.0, le=1.5, description="Tevekkül Tamponu (0.0-1.5)")
    
    # 4. Gullini Ekonofizik Göstergeleri
    cds_5y: float = Field(default=265.0, description="Türkiye 5 Yıllık CDS Primi")
    tcmb_trust_deficit: float = Field(default=0.60, ge=0.0, le=1.0, description="TCMB İtibar Açığı (0.0-1.0)")
    
    # 5. Acemoğlu Kurumsal Çürüme & Adli Göstergeler
    procurement_hhi: float = Field(default=2800.0, description="KİK İhale Yoğunlaşması (0-10000)")
    kik_21b_ratio: float = Field(default=0.32, description="Pazarlık usulü ihale oranı (0.0-1.0)")
    rent_to_mfg_credit: float = Field(default=2.4, description="İnşaat / İmalat Kredi Oranı")
    lm1_caliper_cv: float = Field(default=0.12, description="Gece yarısı atama varyasyon katsayısı")
    tr_dei_score: float = Field(default=0.65, ge=0.0, le=1.0, description="TR-DEI Ölü Ekonomi İndeksi")

class SHAPFactor(BaseModel):
    factor_name: str
    weight_pct: float
    contribution_score: float

class CrisisOutput(BaseModel):
    timestamp: datetime
    uci_score: float = Field(..., ge=0.0, le=1.0, description="Unified Crisis Index (0.0-1.0)")
    confidence_interval_p0: float = Field(..., ge=0.0, le=1.0)
    confidence_interval_p1: float = Field(..., ge=0.0, le=1.0)
    phi_macro: float
    phi_bank: float
    phi_neuro: float
    phi_gullini: float
    phi_acemoglu: float
    tactical_state_d14: str = Field(..., description="NORMAL, ELEVATED_TENSION, TACTICAL_CRISIS_ALARM")
    strategic_state_m3: str = Field(..., description="SUSTAINABLE, STRUCTURAL_DECAY, MINSKY_SINGULARITY_LOCK")
    recommended_action: str = Field(..., description="FULL_EQUITY, DEFENSIVE_50, CASH_100_VIOP_HEDGE, ABSTENTION")
    quarter_kelly_fraction: float
    top_shap_factors: List[SHAPFactor]
    is_concept_drift_detected: bool
