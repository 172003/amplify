"""
app.py
Build a few jobs, register them, run them, print a summary.
"""

import os
import sys

if __package__ in (None, ""):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

from backend.model import DataProcessingJob, EmailJob, PriorityJob
from backend.task_manager import TaskManager
from backend.executor import Executor


def build_jobs():

    return [

        EmailJob(1, "user@example.com"),

        DataProcessingJob(2, "dataset_A"),

        EmailJob(3, "admin@example.com"),

        DataProcessingJob(4, "dataset_B"),

        PriorityJob(5, "Critical system alert", priority=10),

        PriorityJob(6, "Routine cleanup task", priority=1),

    ]


if __name__ == "__main__":

    jobs = build_jobs()


    manager = TaskManager()

    for job in jobs:

        manager.add_job(job)  # all start as 'pending'


    # FIX (app.py): pass 'manager' to Executor so it can update statuses.
    # Previously Executor(jobs).run() had no manager reference — statuses never changed.
    Executor(jobs, manager).run()


    print("\n=== SUMMARY ===")

    print(f"Pending:   {len(manager.get_jobs_by_status('pending'))}")

    print(f"Completed: {len(manager.get_jobs_by_status('completed'))}")

    # FIX (app.py): added 'failed' count to summary so failures are visible.
    print(f"Failed:    {len(manager.get_jobs_by_status('failed'))}")

    # Activity 3: each job keeps its own private log, exposed only via
    # get_logs(). Printing them here demonstrates encapsulation in action.
    print("\n=== JOB LOGS ===")

    for job in jobs:

        print(f"Job {job.job_id} ({job.description}):")

        for entry in job.get_logs():

            print(f"  {entry}")