"""
executor.py
Runs jobs concurrently using threads to simulate a scheduler.
- Random delay: simulates work
- Random failure: exercises exception handling
"""


import threading

import time

import random

from datetime import datetime

from typing import List

from backend.errors import JobExecutionError
from backend.model import Job


class Executor:

    # FIX (executor.py): added 'manager' parameter so Executor can update
    # job statuses in TaskManager after each job succeeds or fails.
    # Previously Executor had no reference to manager, so statuses were never updated.
    def __init__(self, jobs: List[Job], manager) -> None:

        self.jobs = jobs

        self.manager = manager


    def _ts(self) -> str:

        return datetime.now().strftime("%H:%M:%S")


    def run_job(self, job: Job) -> None:

        # Activity 5: start()/end() bracket the whole attempt (including the
        # simulated delay and any failure) so duration reflects real elapsed
        # time. finally guarantees end() runs even when the job fails.
        job.start()

        try:

            print(f"[{self._ts()}] Executing job {job.job_id} ({job.description})...")

            time.sleep(random.uniform(1, 3))

            if random.random() < 0.2:  # ~20% simulated failure

                raise JobExecutionError(job.job_id)


            job.execute()

            # FIX (executor.py): update manager AFTER execute() succeeds,
            # so the job moves from "pending" -> "completed" in TaskManager.
            self.manager.update_status(job, "completed")

            print(f"[{self._ts()}] Completed job {job.job_id}.")

        except JobExecutionError as e:

            # FIX (executor.py): mark failed jobs in manager so they appear
            # in the summary under "failed" instead of staying as "pending".
            self.manager.update_status(job, "failed")

            print(f"[{self._ts()}] Error in job {e.job_id}: {e}")

        finally:

            job.end()

            print(f"[{self._ts()}] Job {job.job_id} duration: {job.duration:.2f}s")


    def run(self) -> None:

        threads: List[threading.Thread] = []

        # Activity 2: start higher-priority jobs first. Jobs without a
        # 'priority' attribute (EmailJob, DataProcessingJob) default to 0,
        # so this only affects PriorityJob instances. Since jobs still run
        # concurrently on separate threads, this controls start order, not
        # guaranteed completion order.
        ordered_jobs = sorted(self.jobs, key=lambda j: getattr(j, "priority", 0), reverse=True)

        for job in ordered_jobs:

            t = threading.Thread(target=self.run_job, args=(job,))

            threads.append(t)

            t.start()


        for t in threads:

            t.join()