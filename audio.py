"""Audio measurements; these are technical metrics, not artistic quality scores."""
import io
import numpy as np
import soundfile as sf
from scipy.signal import resample_poly
from math import gcd


def decode_audio(data: bytes):
    if not data:
        raise ValueError('Empty audio file')
    samples, sample_rate = sf.read(io.BytesIO(data), dtype='float32', always_2d=True)
    if not len(samples) or sample_rate <= 0:
        raise ValueError('Invalid audio')
    if not np.isfinite(samples).all():
        raise ValueError('Non-finite audio samples')
    return samples.mean(axis=1), sample_rate


def measure_audio(samples, sample_rate):
    x = np.asarray(samples, dtype=np.float64)
    if x.ndim != 1 or not len(x) or sample_rate <= 0 or not np.isfinite(x).all():
        raise ValueError('Invalid samples or sample rate')
    peak = float(np.max(np.abs(x)))
    rms = float(np.sqrt(np.mean(x * x)))
    silence_fraction = float(np.mean(np.abs(x) < 0.001))
    return {
        'duration_s': round(len(x) / sample_rate, 2),
        'peak_dbfs': round(20 * np.log10(max(peak, 1e-12)), 2),
        'rms_dbfs': round(20 * np.log10(max(rms, 1e-12)), 2),
        'crest_db': round(20 * np.log10(max(peak, 1e-12) / max(rms, 1e-12)), 2),
        'silence_pct': round(100 * silence_fraction, 2),
        'sample_rate': int(sample_rate),
    }


def preview_wav(samples, sample_rate, max_seconds=30, target_rate=22050):
    """Create bounded mono preview without changing the original uploaded file."""
    x = np.asarray(samples[:int(sample_rate * max_seconds)], dtype=np.float32)
    d = gcd(sample_rate, target_rate)
    y = resample_poly(x, target_rate // d, sample_rate // d)
    buf = io.BytesIO()
    sf.write(buf, y, target_rate, format='WAV', subtype='PCM_16')
    return buf.getvalue()
