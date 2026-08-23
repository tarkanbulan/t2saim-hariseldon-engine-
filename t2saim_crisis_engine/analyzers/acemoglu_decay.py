#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM DARON ACEMOĞLU INSTITUTIONAL DECAY & FORENSIC ANOMALY ANALYZER (PHI_ACEMOGLU)
Doktrin: Veritas Per Se · TR-DEI Ölü Ekonomi, KİK İhale HHI, Rant/İmalat ve LM 1-3 Adli Kanunları
"""

import numpy as np
from ..core.schemas import TelemetryInput

class AcemogluDecayAnalyzer:
    """
    Phi_Acemoglu Hesaplayıcı:
    1. TR-DEI Ölü Ekonomi İndeksi
    2. KİK Kamu İhale Yoğunlaşması (HHI > 2500 oligopol, > 4000 kilitlenme)
    3. 21/b Pazarlık Usulü Dağıtım Oranı
    4. Rant / İmalat Kredi Oranı (> 2.5x)
    5. LM-1 Caliper CV (Gece yarısı bürokrat azil ve kararnameleri zaman varyasyonu)
    """
    def analyze(self, data: TelemetryInput) -> float:
        # 1. TR-DEI Stresi
        tr_dei_stress = np.clip(data.tr_dei_score, 0.0, 1.0)
        
        # 2. İhale HHI Yoğunlaşması (1500 normal, 4500 tam kilitlenme)
        hhi_stress = np.clip((data.procurement_hhi - 1500.0) / 3000.0, 0.0, 1.0)
        
        # 3. KİK 21/b Pazarlık Oranı (%10 normal, %50 kriz)
        kik_stress = np.clip((data.kik_21b_ratio - 0.10) / 0.40, 0.0, 1.0)
        
        # 4. Rant / İmalat Kredi Oranı (1.2 normal, 3.0 aşırı balon)
        rent_stress = np.clip((data.rent_to_mfg_credit - 1.2) / 1.8, 0.0, 1.0)
        
        # 5. LM-1 Caliper CV (< 0.15 keyfilik tavanı)
        caliper_stress = np.clip((0.25 - data.lm1_caliper_cv) / 0.20, 0.0, 1.0)

        phi = (0.25 * tr_dei_stress) + (0.25 * hhi_stress) + (0.20 * kik_stress) + (0.15 * rent_stress) + (0.15 * caliper_stress)
        return float(np.clip(phi, 0.0, 1.0))
