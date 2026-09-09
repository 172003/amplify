"""
test_backend.py
Deterministic unit tests for the job scheduler backend, used by CI
(Activity 7). Randomness is pinned (failure_rate=0.0/1.0) so results
are reproducible instead of depending on the Executor's random delays
and failures.
"""

import pytest

from backend.errors import JobExecutionError
from backend.job_factory import JobFactory
from backend.model import DataProcessingJob, EmailJob, PriorityJob, RetryableJob
from backend.task_manager import TaskManager


def test_email_job_execute_and_logs():
    job = EmailJob(1, "user@example.com")
    assert job.status == "pending"

    job.execute()

    assert any("Sent email" in entry for entry in job.get_logs())


def test_job_attributes_are_read_only():
    job = EmailJob(1, "user@example.com")

    with pytest.raises(AttributeError):
        job.job_id = 999

    with pytest.raises(AttributeError):
        job.description = "changed"


def test_status_setter_logs_transition():
    job = DataProcessingJob(2, "dataset_A")

    job.status = "completed"

    assert job.status == "completed"
    assert any("pending' -> 'completed'" in entry for entry in job.get_logs())


def test_priority_job_defaults_and_execute():
    job = PriorityJob(3, "Critical alert", priority=10)

    assert job.priority == 10

    job.execute()

    assert any("priority=10" in entry for entry in job.get_logs())


def test_task_manager_add_and_update_status():
    manager = TaskManager()
    job = EmailJob(1, "user@example.com")

    manager.add_job(job)
    assert job in manager.get_jobs_by_status("pending")

    manager.update_status(job, "completed")
    assert job in manager.get_jobs_by_status("completed")
    assert job not in manager.get_jobs_by_status("pending")
    assert job.status == "completed"


def test_job_factory_creates_correct_types():
    email_job = JobFactory.create_job("email", job_id=1, recipient="user@example.com")
    data_job = JobFactory.create_job("data_processing", job_id=2, dataset="A")
    priority_job = JobFactory.create_job("priority", job_id=3, description="x", priority=5)
    retryable_job = JobFactory.create_job("retryable", job_id=4, description="x")

    assert isinstance(email_job, EmailJob)
    assert isinstance(data_job, DataProcessingJob)
    assert isinstance(priority_job, PriorityJob)
    assert isinstance(retryable_job, RetryableJob)


def test_job_factory_unknown_type_raises():
    with pytest.raises(ValueError):
        JobFactory.create_job("unknown_type", job_id=1)


def test_job_lifecycle_timing():
    job = EmailJob(1, "user@example.com")
    assert job.duration == 0.0

    job.start()
    job.end()

    assert job.duration >= 0.0


def test_retryable_job_succeeds_without_failure():
    job = RetryableJob(1, "Reliable task", max_retries=3, failure_rate=0.0)

    job.execute()  # should not raise

    assert job.attempts == 1
    assert any("Succeeded on attempt 1" in entry for entry in job.get_logs())


def test_retryable_job_exhausts_retries_when_always_failing():
    job = RetryableJob(1, "Always fails", max_retries=3, failure_rate=1.0, backoff_seconds=0)

    with pytest.raises(JobExecutionError):
        job.execute()

    assert job.attempts == 3
    assert any("All retry attempts exhausted" in entry for entry in job.get_logs())
