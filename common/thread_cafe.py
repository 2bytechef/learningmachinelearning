
import threading
from collections import defaultdict

from common.jobs import Job


class ThreadCafe:
    class ThreadCounter:
        def __init__(self):
            self.queue_condition = threading.Condition()
            self._thread_counts = defaultdict(lambda: 0)
            self._thread_stops = defaultdict(lambda: threading.Event())
    
        @property
        def compatible_job_types(self):
            return [Job.JobType.THOUGHT, Job.JobType.ACTION, Job.JobType.NOTIFICATION]
            
        def add_thread(self, job: Job):
            with self.queue_condition:
                if job.type in self.compatible_job_types:
                    self._thread_counts[job.type] += 1
                else:
                    raise ValueError(f"Invalid `{job.type.__class__.__name__}`")
            
        def remove_thread(self, job: Job):
            with self.queue_condition:
                if job.type in self.compatible_job_types:
                    self._thread_counts[job.type] += 1
                else:
                    raise ValueError(f"Invalid `{job.type.__class__.__name__}`")
            
        def get_thread_count(self, job: Job):
            with self.queue_condition:
                if job.type in self.compatible_job_types:
                    return self._thread_counts[job.type]
                else:
                    raise ValueError(f"Invalid `{job.type.__class__.__name__}`")
            
        def get_all_threads_count(self):
            with self.queue_condition:
                return sum(self._thread_counts.values())
            
        def stop_thread(self, job: Job):
            # with self.queue_condition:
            if job.type in self.compatible_job_types:
                self._thread_stops[job.type].set()
            else:
                raise ValueError(f"Invalid `{job.type.__class__.__name__}`")
            
        def check_stop_thread(self, job: Job):
            # with self.queue_condition:
            if job.type in self.compatible_job_types:
                return self._thread_stops[job.type].is_set()
            else:
                raise ValueError(f"Invalid `{job.type.__class__.__name__}`")
            
        
    def __init__(self, max_threads: int):
        self.max_threads = max_threads
        self.thread_shelf = ThreadCafe.ThreadCounter()
        
    def check_job_clearance(self, job: Job) -> bool:
        if job.priority == Job.Priority.INTERRUPT:
            return (
                self.thread_shelf.get_thread_count(job.type) > 0
                or self.thread_shelf.get_all_threads_count() < self.max_threads
            )
        elif job.is_synchronous:
            return self.thread_shelf.get_all_threads_count() < self.max_threads
        else:
            return self.thread_shelf.get_thread_count(job.type) == 0
    
    # def check_thread_stop(self, job: Job) -> bool:
        
    
    def work(self, job: Job):
        try:
            # Execute the action's function
            if self.check_job_clearance(job):
                
                # interrupt will stop all jobs of the same type
                # TODO: interrupts should only stop jobs of the same class once classes are implemented
                if job.priority == Job.Priority.INTERRUPT:
                    self.thread_shelf.stop_thread(job)
                    
                
                self.thread_shelf.add_thread(job.type)
                # job.execute_fn()
            # with self.queue_condition:
            # job.execute_fn()
        finally:
            # Queue a new action if needed
                # running_actions.remove(action.action_type)
                # new_action = generate_new_action(action)
                # if new_action:
                #     action_queue.put(new_action)
                # queue_condition.notify_all()  # Notify that a thread has finished
