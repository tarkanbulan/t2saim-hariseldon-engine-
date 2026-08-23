import os
import sys
import pytest
import numpy as np

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from t2saim_crisis_engine.core.amnesia import AmnesiaFilter

def test_amnesia_deterministic_exponential_decay():
    """Amnesia filtresinin lambda=0.15 ile deterministik sönümleme yaptığını doğrular."""
    filter_engine = AmnesiaFilter(nominal_lambda=0.15)
    
    # 1. Tek bir büyük şok gönder
    m1 = filter_engine.update(1.0)
    assert m1 == 1.0
    
    # 2. Sıfır stresli takip eden 10 gün
    decay_series = []
    for _ in range(10):
        m = filter_engine.update(0.0)
        decay_series.append(m)
        
    # Her adımda bellek yükü (1 - lambda) = 0.85 oranında azalmalıdır
    for i in range(len(decay_series) - 1):
        assert decay_series[i+1] < decay_series[i]
        ratio = decay_series[i+1] / decay_series[i]
        assert abs(ratio - 0.85) < 1e-4

def test_amnesia_drift_acceleration():
    """ADWIN drift modunda eski şokun daha hızlı sönümlendiğini doğrular."""
    filter_nominal = AmnesiaFilter(nominal_lambda=0.15)
    filter_drift = AmnesiaFilter(nominal_lambda=0.15, drift_lambda=0.25)
    
    filter_nominal.update(1.0)
    filter_drift.update(1.0)
    
    filter_drift.set_drift_mode(True)
    
    # 5 gün sıfır stres uygulandığında drift modundaki bellek daha çok sönümlenir
    for _ in range(5):
        decay_nom = filter_nominal.update(0.0)
        decay_drf = filter_drift.update(0.0)
    
    assert decay_drf < decay_nom

def test_l6_phase_lock_gate():
    """L6 faz kilidinin eşiklerini doğrular."""
    filter_engine = AmnesiaFilter()
    
    assert filter_engine.compute_l6_phase_gate(sri_psy=0.55, sri_fin=0.50, sri_vol=0.52) is True
    assert filter_engine.compute_l6_phase_gate(sri_psy=0.45, sri_fin=0.50, sri_vol=0.52) is False
