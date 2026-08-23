#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM CRISIS ENGINE CONFIGURATION & SETTINGS
Doktrin: Veritas Per Se · Pydantic V2 SettingsConfigDict & Mühürlü Eşikler
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class CrisisEngineSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="T2SAIM_CRISIS_", case_sensitive=False)
    
    # Proje Yolları
    PROJECT_NAME: str = "T2SAIM_TURKIYE_CRISIS_ENGINE_V5"
    MCP_PORT: int = 39300
    
    # 5 Boyutlu Ağırlıklar: [Macro, Bank, Neuro, Gullini, Acemoglu]
    WEIGHT_MACRO: float = 0.25
    WEIGHT_BANK: float = 0.20
    WEIGHT_NEURO: float = 0.20
    WEIGHT_GULLINI: float = 0.20
    WEIGHT_ACEMOGLU: float = 0.15

    # Kalibrasyon ve Sönümleme
    AMNESIA_LAMBDA_NOMINAL: float = 0.15
    AMNESIA_LAMBDA_DRIFT: float = 0.25
    ADWIN_DELTA: float = 0.002
    ECE_TARGET: float = 0.0124
    UCI_CASH_GATE: float = 0.65
    
    # Minsky Tekillik Günü
    MINSKY_T_STAR: str = "2026-11-18"

@lru_cache()
def get_settings() -> CrisisEngineSettings:
    return CrisisEngineSettings()
