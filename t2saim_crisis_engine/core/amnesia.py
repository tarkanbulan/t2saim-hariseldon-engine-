#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM BTF-AMNESIA EXPONENTIAL FORGETTING CORE
Doktrin: Veritas Per Se · M_t = S_t + (1 - lambda) M_{t-1}, Sıfır Gelecek Sızıntısı & Travma Sönümlemesi
"""

import numpy as np

class AmnesiaFilter:
    """
    BTF-Amnesia Sönümleme Çekirdeği:
    Eski şokları sönümlerken kriz öncesi 3 aylık birikimi korur (lambda = 0.15).
    Formül: M_t = S_t + (1.0 - lambda) * M_{t-1}
    Normalize Bellek: lambda * M_t in [0.0, 1.0]
    """
    def __init__(self, nominal_lambda: float = 0.15, drift_lambda: float = 0.25):
        self.nominal_lambda = nominal_lambda
        self.drift_lambda = drift_lambda
        self.current_lambda = nominal_lambda
        self.memory_state: float = 0.0
        self.is_initialized: bool = False

    def set_drift_mode(self, is_drift: bool):
        """Konsept kayması (ADWIN drift) anında sönümlemeyi hızlandırır."""
        self.current_lambda = self.drift_lambda if is_drift else self.nominal_lambda

    def update(self, raw_stress_signal: float) -> float:
        stress = float(np.clip(raw_stress_signal, 0.0, 1.0))
        
        if not self.is_initialized:
            self.memory_state = stress / self.current_lambda
            self.is_initialized = True
        else:
            self.memory_state = stress + (1.0 - self.current_lambda) * self.memory_state
        
        normalized_load = float(np.clip(self.current_lambda * self.memory_state, 0.0, 1.0))
        return normalized_load

    def reset(self):
        self.memory_state = 0.0
        self.is_initialized = False
        self.current_lambda = self.nominal_lambda

    def compute_l6_phase_gate(
        self,
        sri_psy: float,
        sri_fin: float,
        sri_vol: float
    ) -> bool:
        """
        L6 Faz Kilidi (L6_gate):
        L6_gate = 1 <=> (SRI_psy > 0.50) & (SRI_fin > 0.45) & (SRI_vol > 0.50)
        """
        return (sri_psy > 0.50) and (sri_fin > 0.45) and (sri_vol > 0.50)
