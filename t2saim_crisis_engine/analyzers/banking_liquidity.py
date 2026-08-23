#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM BANKING & LIQUIDITY LOCKDOWN ANALYZER (PHI_BANK)
Doktrin: Veritas Per Se · LDR, Hayalet Krediler (NPL_real), TED Spread ve 4 Finansal Boğulma Eğrisi
"""

import numpy as np
from ..core.schemas import TelemetryInput

class BankingLiquidityAnalyzer:
    """
    Phi_Bank Hesaplayıcı:
    1. Kredi / Mevduat Oranı (LDR > 1.15)
    2. Hayalet / Ötelenen Krediler (NPL_real / NPL_official >= 2.0)
    3. TED Spread (Tahvil - Mevduat Faizi Makası)
    4. 4 Boğulma Eğrisi (UYAP İcra, Karşılıksız Çek)
    """
    def analyze(self, data: TelemetryInput) -> float:
        # 1. LDR Stresi (0.90 normal, 1.25 kritik)
        ldr_stress = np.clip((data.ldr_ratio - 0.95) / 0.30, 0.0, 1.0)
        
        # 2. NPL Makası (Real vs Official)
        npl_ratio = data.npl_real_ratio / max(0.5, data.npl_official_ratio)
        npl_stress = np.clip((npl_ratio - 1.0) / 2.0, 0.0, 1.0)
        
        # 3. TED Spread Stresi (%0 normal, %8 kriz)
        ted_stress = np.clip(data.ted_spread_pct / 7.0, 0.0, 1.0)
        
        # 4. UYAP İcra & Çek Boğulma Eğrisi
        uyap_stress = np.clip((data.uyap_active_cases_million - 20.0) / 15.0, 0.0, 1.0)

        phi = (0.30 * ldr_stress) + (0.30 * npl_stress) + (0.25 * ted_stress) + (0.15 * uyap_stress)
        return float(np.clip(phi, 0.0, 1.0))
