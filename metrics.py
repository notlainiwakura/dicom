# compass_perf/metrics.py

"""
Thread-safe metrics collection for performance tests including latency, success rates, and error tracking.
"""

from __future__ import annotations

import statistics
import threading
import time
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Sample:
    """One message's timing and status."""

    start_time: float
    end_time: float
    success: bool
    status_code: Optional[int] = None
    error: Optional[str] = None

    @property
    def latency_ms(self) -> float:
        return (self.end_time - self.start_time) * 1000.0


@dataclass
class PerfMetrics:
    """Aggregated, thread-safe metrics."""

    _samples: List[Sample] = field(default_factory=list)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def record(self, sample: Sample) -> None:
        with self._lock:
            self._samples.append(sample)

    @property
    def samples(self) -> List[Sample]:
        with self._lock:
            return list(self._samples)

    @property
    def total(self) -> int:
        return len(self.samples)

    @property
    def successes(self) -> int:
        return sum(1 for s in self.samples if s.success)

    @property
    def failures(self) -> int:
        return sum(1 for s in self.samples if not s.success)

    @property
    def error_rate(self) -> float:
        if self.total == 0:
            return 0.0
        return self.failures / float(self.total)

    def _latencies(self) -> List[float]:
        return [s.latency_ms for s in self.samples if s.success]

    @property
    def min_latency_ms(self) -> Optional[float]:
        lat = self._latencies()
        return min(lat) if lat else None

    @property
    def avg_latency_ms(self) -> Optional[float]:
        lat = self._latencies()
        return statistics.mean(lat) if lat else None

    @property
    def p95_latency_ms(self) -> Optional[float]:
        lat = sorted(self._latencies())
        if not lat:
            return None
        k = int(len(lat) * 0.95) - 1
        k = max(0, min(k, len(lat) - 1))
        return lat[k]

    def throughput_per_second(self, window_seconds: Optional[float] = None) -> float:
        """
        Compute average throughput over all samples or the last N seconds.
        """
        samples = self.samples
        if not samples:
            return 0.0

        end_time = max(s.end_time for s in samples)
        if window_seconds is None:
            start_time = min(s.start_time for s in samples)
        else:
            start_time = end_time - window_seconds

        duration = max(end_time - start_time, 1e-9)
        count = sum(1 for s in samples if s.start_time >= start_time)
        return count / duration

    def snapshot(self) -> dict:
        """
        Small JSON-serializable snapshot for logging or exporting to dashboards.
        """
        return {
            "total": self.total,
            "successes": self.successes,
            "failures": self.failures,
            "error_rate": self.error_rate,
            "min_latency_ms": self.min_latency_ms,
            "avg_latency_ms": self.avg_latency_ms,
            "p95_latency_ms": self.p95_latency_ms,
            "throughput_per_second": self.throughput_per_second(),
            "timestamp": time.time(),
        }
