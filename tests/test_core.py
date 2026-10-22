import numpy as np
import pytest
from audio import measure_audio
from ranking import elo_update


def test_silence():
    m = measure_audio(np.zeros(48000), 48000)
    assert m['duration_s'] == 1.0
    assert m['silence_pct'] == 100.0
    assert m['rms_dbfs'] <= -200


def test_sine():
    t = np.arange(48000) / 48000
    m = measure_audio(0.5 * np.sin(2 * np.pi * 440 * t), 48000)
    assert -6.1 < m['peak_dbfs'] < -5.9
    assert 2.9 < m['crest_db'] < 3.2


def test_elo_conservation():
    a,b = elo_update(1000,1000,'a')
    assert (a,b) == (1012,988)
    assert sum(elo_update(a,b,'tie')) == 2000


def test_bad_winner():
    with pytest.raises(ValueError):
        elo_update(1000,1000,'invalid')
