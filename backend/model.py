"""
models.py
Defines the Job hierarchy (parent + child classes).
Polymorphism: each subclass implements its own execute().
"""

import time
from datetime import datetime
from typing import List, Optional


class Job:

    """Parent/base class shared by all job types."""

    def __init__(self, job_id: int, description: str) -> None:

        # Activity 3: attributes are private (name-mangled). External code
        # reads them only through the read-only properties below, and
        # writes to status only through the status.setter, which logs
        # every transition automatically.
        self.__job_id = job_id

        self.__description = description

        self.__status = "pending"

        self.__logs: List[str] = []

        # Activity 5: lifecycle timing, set by start()/end().
        self.__start_time: Optional[float] = None

        self.__end_time: Optional[float] = None

        self._log(f"Job created with status '{self.__status}'")


    @property
    def job_id(self) -> int:

        return self.__job_id


    @property
    def description(self) -> str:

        return self.__description


    @property
    def status(self) -> str:

        return self.__status


    @status.setter
    def status(self, new_status: str) -> None:

        self._log(f"Status changed: '{self.__status}' -> '{new_status}'")

        self.__status = new_status


    def _log(self, message: str) -> None:

        """Protected helper so this class and subclasses can add log entries."""

        timestamp = datetime.now().strftime("%H:%M:%S")

        self.__logs.append(f"[{timestamp}] {message}")


    def get_logs(self) -> List[str]:

        """Public read-only access to this job's internal logs."""

        return list(self.__logs)


    def start(self) -> None:

        """Marks the beginning of execution. Call once, before doing any work."""

        self.__start_time = time.monotonic()

        self._log("Job started")


    def end(self) -> None:

        """Marks the end of execution. Call once, after work finishes (success or failure)."""

        self.__end_time = time.monotonic()

        self._log(f"Job ended (duration: {self.duration:.2f}s)")


    @property
    def duration(self) -> float:

        """Elapsed seconds between start() and end(). 0.0 if either hasn't been called."""

        if self.__start_time is None or self.__end_time is None:

            return 0.0

        return self.__end_time - self.__start_time


    def execute(self) -> None:

        """Must be overridden by subclasses."""

        raise NotImplementedError("Each job must implement its own execution logic.")


    def mark_done(self) -> None:

        self.status = "completed"


    def __repr__(self) -> str:

        return f"<Job id={self.job_id} status={self.status} desc='{self.description}'>"



class EmailJob(Job):

    """Child class: sends an email."""

    def __init__(self, job_id: int, recipient: str) -> None:

        # super() calls parent constructor (DRY)

        super().__init__(job_id, f"Send email to {recipient}")

        self.recipient = recipient


    def execute(self) -> None:

        print(f"Sending email to {self.recipient}...")

        self._log(f"Sent email to {self.recipient}")

        # FIX (models.py): removed self.mark_done() here.
        # Previously mark_done() set job.status="completed" inside execute(),
        # so update_status() in executor.py searched the wrong bucket and
        # added a duplicate — causing Pending:4, Completed:4 in the summary.
        # Status is now managed exclusively by TaskManager.update_status().



class DataProcessingJob(Job):

    """Child class: processes a dataset."""

    def __init__(self, job_id: int, dataset: str) -> None:

        super().__init__(job_id, f"Process dataset {dataset}")

        self.dataset = dataset


    def execute(self) -> None:

        print(f"Processing dataset {self.dataset}...")

        self._log(f"Processed dataset {self.dataset}")

        # FIX (models.py): removed self.mark_done() here — same reason as EmailJob above.



class PriorityJob(Job):

    """Child class: a job with an execution priority. Higher priority runs first.

    Demonstrates extending Job with new behaviour (a priority field) without
    modifying the base class at all.
    """

    def __init__(self, job_id: int, description: str, priority: int = 0) -> None:

        super().__init__(job_id, description)

        self.priority = priority


    def execute(self) -> None:

        print(f"Running priority job (priority={self.priority}): {self.description}...")

        self._log(f"Ran priority job at priority={self.priority}")