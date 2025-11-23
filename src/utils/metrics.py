"""Metrics collection utility"""

from typing import Dict, Any
from collections import defaultdict
from datetime import datetime


class MetricsCollector:
    """Collect and track bot performance metrics"""

    def __init__(self):
        self.task_metrics = defaultdict(list)
        self.error_counts = defaultdict(int)

    def record_task(self, task_name: str, duration: float, result: Dict[str, Any]):
        """Record task execution metrics"""
        self.task_metrics[task_name].append({
            "timestamp": datetime.now(),
            "duration": duration,
            "success": result.get("success", False),
        })

    def record_error(self, task_name: str, error: str):
        """Record error occurrence"""
        self.error_counts[f"{task_name}:{error}"] += 1

    def get_stats(self) -> Dict[str, Any]:
        """Get aggregated statistics"""
        return {
            "total_tasks": sum(len(v) for v in self.task_metrics.values()),
            "task_counts": {k: len(v) for k, v in self.task_metrics.items()},
            "error_counts": dict(self.error_counts),
        }
