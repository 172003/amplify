"""
job_factory.py
Factory pattern for creating Job instances from a type name + parameters.
Decouples job creation from concrete Job subclasses (Activity 4: Abstraction).
"""

from typing import Any, Dict, Type

from backend.model import DataProcessingJob, EmailJob, Job, PriorityJob, RetryableJob


class JobFactory:

    """Creates Job instances from a type string, hiding concrete classes from callers.

    Callers only need to know a type name (e.g. from an API request or a
    config file) and its parameters — never the concrete Job subclass.
    """

    _job_types: Dict[str, Type[Job]] = {
        "email": EmailJob,
        "data_processing": DataProcessingJob,
        "priority": PriorityJob,
        "retryable": RetryableJob,
    }

    @classmethod
    def create_job(cls, job_type: str, **kwargs: Any) -> Job:

        job_class = cls._job_types.get(job_type)

        if job_class is None:

            raise ValueError(
                f"Unknown job type: '{job_type}'. Available types: {list(cls._job_types)}"
            )

        return job_class(**kwargs)


    @classmethod
    def register_job_type(cls, name: str, job_class: Type[Job]) -> None:

        """Allows new job types to be added without modifying this factory's code."""

        cls._job_types[name] = job_class
