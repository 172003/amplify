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

from backend.job_factory import JobFactory
from backend.task_manager import TaskManager
from backend.executor import Executor


def build_jobs():

    # Activity 4: app.py never imports EmailJob/DataProcessingJob/PriorityJob
    # directly — it only knows type names and parameters, as if these came
    # from an API request or a config file. JobFactory hides the concrete
    # classes.
    return [

        JobFactory.create_job("email", job_id=1, recipient="user@example.com"),

        JobFactory.create_job("data_processing", job_id=2, dataset="dataset_A"),

        JobFactory.create_job("email", job_id=3, recipient="admin@example.com"),

        JobFactory.create_job("data_processing", job_id=4, dataset="dataset_B"),

        JobFactory.create_job("priority", job_id=5, description="Critical system alert", priority=10),

        JobFactory.create_job("priority", job_id=6, description="Routine cleanup task", priority=1),

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

        # Activity 5: duration is timed by Executor via job.start()/job.end().
        print(f"  Duration: {job.duration:.2f}s")