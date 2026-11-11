# -*- coding: utf-8 -*-
"""连续批处理：多请求合并成 batch 统一调度（静态分批）。"""
from __future__ import annotations


class BatchScheduler:
    """静态连续批处理：按 batch_size 收集请求并调度。"""

    def __init__(self, max_batch_size: int = 16):
        self.max_batch_size = max_batch_size
        self.queue = []

    def submit(self, job):
        self.queue.append(job)

    def drain(self):
        """取出最多 max_batch_size 个请求。"""
        batch = self.queue[:self.max_batch_size]
        self.queue = self.queue[self.max_batch_size:]
        return batch

    def pending(self):
        return len(self.queue)
