#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM NEURO-FINANCE & AMYGDALA PANIC ANALYZER (PHI_NEURO)
Doktrin: Veritas Per Se · A_load, PFC Kontrolü, v_run Mevduat Kaçışı ve Kuramoto Sürü Kilitlenmesi
"""

import numpy as np
from ..core.schemas import TelemetryInput

class NeuroAmygdalaAnalyzer:
    """
    Phi_Neuro Hesaplayıcı:
    1. A_load (Amigdala Yükü)
    2. PFC_control (Prefrontal Korteks Denetimi)
    3. v_run (Mevduat Kaçış Hızı)
    4. H_herd (Kuramoto Sürü Kilitlenmesi)
    5. Fatalism Buffer (Tevekkül Tamponu Sönümlemesi)
    """
    def __init__(self, chi_sigma: float = 0.25, kappa_p: float = 5.0464, theta_panic: float = 0.70):
        self.chi_sigma = chi_sigma
        self.kappa_p = kappa_p
        self.theta_panic = theta_panic

    def analyze(self, data: TelemetryInput) -> float:
        # 1. A_load Hesabı
        a_load = np.clip(0.3 + (data.sigma_20_60_ratio - 1.0) * self.chi_sigma, 0.1, 1.0)
        
        # 2. PFC Kontrolü (Amigdala arttıkça PFC çöker)
        pfc_control = 1.0 / (1.0 + np.exp(self.kappa_p * (a_load - self.theta_panic)))
        
        # 3. v_run Mevduat Kaçış Hızı (0.0 - 1.0)
        v_run = data.v_run
        
        # 4. Kuramoto Sürü Kilitlenmesi (H_herd)
        h_herd = data.h_herd

        # 5. Tevekkül Tamponu Sönümlemesi (Fatalism Buffer)
        buffer_dampener = max(0.5, min(1.5, data.fatalism_buffer))

        # Ham Nöro Gerilim
        raw_neuro = (0.35 * a_load) + (0.30 * (1.0 - pfc_control)) + (0.20 * v_run) + (0.15 * h_herd)
        
        # Tevekkül tamponu ile sönümlenmiş / geciktirilmiş patlama gerilimi
        phi = raw_neuro / buffer_dampener
        return float(np.clip(phi, 0.0, 1.0))
