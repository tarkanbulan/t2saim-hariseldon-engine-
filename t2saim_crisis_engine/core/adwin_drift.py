#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T2SAIM RIVER ADWIN CONCEPT DRIFT MANAGEMENT CORE
Doktrin: Veritas Per Se · Rejim ve Politika Kaymalarının Gerçek Zamanlı Tespiti
"""

try:
    from river import drift
    RIVER_AVAILABLE = True
except ImportError:
    RIVER_AVAILABLE = False

class ConceptDriftManager:
    """
    ADWIN (Adaptive Windowing) Akış Tabanlı Konsept Kayması Dedektörü:
    Türkiye regülasyon (KKM, faiz, zorunlu karşılık) değişimlerini yakalar.
    """
    def __init__(self, delta: float = 0.002):
        self.delta = delta
        if RIVER_AVAILABLE:
            self.detector = drift.ADWIN(delta=delta)
        else:
            self.detector = None
            self.window = []
            self.window_size = 30

    def update(self, value: float) -> bool:
        """
        Yeni bir veri noktası ekler ve rejim kayması (drift) olup olmadığını döndürür.
        """
        if RIVER_AVAILABLE and self.detector is not None:
            self.detector.update(value)
            return bool(self.detector.drift_detected)
        else:
            # Yedek adaptif varyans pencere algoritması
            self.window.append(value)
            if len(self.window) > self.window_size:
                self.window.pop(0)
            if len(self.window) == self.window_size:
                w1 = self.window[: self.window_size // 2]
                w2 = self.window[self.window_size // 2 :]
                mean_diff = abs(sum(w1)/len(w1) - sum(w2)/len(w2))
                return mean_diff > 0.25
            return False
