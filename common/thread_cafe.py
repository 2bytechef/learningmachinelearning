
import threading

from common.jobs import Job


class ThreadCafe:
    class ThreadCounter:
        def __init__(self):
            self.queue_condition = threading.Condition()
            self._thought_thread_count = 0
            self._action_thread_count = 0
            self._notification_thread_count = 0
            
        def add_thread(self, job_type: Job.JobType):
            with self.queue_condition:
                if job_type == Job.JobType.THOUGHT:
                    self._thought_thread_count += 1
                elif job_type == Job.JobType.ACTION:
                    self._action_thread_count += 1
                elif job_type == Job.JobType.NOTIFICATION:
                    self._notification_thread_count += 1
                else:
                    raise ValueError("Invalid JobType")
            
        def remove_thread(self, job_type: Job.JobType):
            with self.queue_condition:
                if job_type == Job.JobType.THOUGHT:
                    self._thought_thread_count -= 1
                elif job_type == Job.JobType.ACTION:
                    self._action_thread_count -= 1
                elif job_type == Job.JobType.NOTIFICATION:
                    self._notification_thread_count -= 1
                else:
                    raise ValueError("Invalid JobType")
            
        def get_thread_count(self, job_type: Job.JobType):
            with self.queue_condition:
                if job_type == Job.JobType.THOUGHT:
                    return self._thought_thread_count
                elif job_type == Job.JobType.ACTION:
                    return self._action_thread_count
                elif job_type == Job.JobType.NOTIFICATION:
                    return self._notification_thread_count
                else:
                    raise ValueError("Invalid JobType")
            
        def get_all_threads_count(self):
            with self.queue_condition:
                return self._thought_thread_count + self._action_thread_count + self._notification_thread_count
    
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
    
    def work(self, job: Job):
        try:
            # Execute the action's function
            if self.check_job_clearance(job):
                self.thread_shelf.add_thread(job.type)
                
                # interrupt will stop all jobs of the same type
                # TODO: interrupts should only stop jobs of the same class once classes are implemented
                if job.priority == Job.Priority.INTERRUPT:
                    
                    
                
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
