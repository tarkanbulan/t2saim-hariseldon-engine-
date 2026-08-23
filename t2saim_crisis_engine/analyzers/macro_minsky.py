#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM MACRO & MINSKY DEBT RESONANCE ANALYZER (PHI_MACRO)
Doktrin: Veritas Per Se · M2/NIR, REER Sarkaç, 191B$ Dış Borç ve DOLGAP Kapalıçarşı Makası
"""

import numpy as np
from ..core.schemas import TelemetryInput

class MacroMinskyAnalyzer:
    """
    Phi_Macro Hesaplayıcı:
    1. M2 / NIR (Net Uluslararası Rezerv) Oranı (Eşik > 15.0)
    2. Swap Hariç Net Rezerv Seviyesi (Kritik: < -40 Mr $)
    3. REER Sarkaç Aşırı Değerlenmesi (Eşik >= 68.0)
    4. DOLGAP Kapalıçarşı Kur Makası (%)
    """
    def analyze(self, data: TelemetryInput) -> float:
        # 1. M2 / NIR Stresi (10.0 normal, 20.0 aşırı kriz)
        m2_stress = np.clip((data.m2_nir_ratio - 10.0) / 10.0, 0.0, 1.0)
        
        # 2. Net Rezerv Erimesi (-60 Mr $ kriz, 0 Mr $ normal)
        nir_stress = np.clip((-data.net_nir_usd_billion) / 60.0, 0.0, 1.0)
        
        # 3. REER Sarkaç Tepesi (50.0 normal, 75.0 aşırı değerli patlama)
        reer_stress = np.clip((data.reer_cpi - 55.0) / 20.0, 0.0, 1.0)
        
        # 4. DOLGAP Kapalıçarşı Primi (%0 normal, %5.0 kriz)
        dolgap_stress = np.clip(data.dolgap_premium_pct / 4.0, 0.0, 1.0)

        # Ağırlıklı Phi_Macro
        phi = (0.35 * m2_stress) + (0.30 * nir_stress) + (0.20 * dolgap_stress) + (0.15 * reer_stress)
        return float(np.clip(phi, 0.0, 1.0))
