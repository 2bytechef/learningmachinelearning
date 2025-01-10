from typing import List

from apps.conversation_hosts.timers import Timer
from common.jobs import Action, Job, Thought


class Actor:
    def __init__(self, name: str, timers: List[Timer] = []):
        self.name = name
        self.timers = timers
        # self.pending_thoughts = []
        # self.pending_actions = []
        
    # check for pending thoughts (time based processes) -> starts thinking thread
    # eg. check bluesky for tweets
    # read twitch chat (if streaming)
    # alarms, reminders, screen grabs etc
    # check video game screen
    # check for new emails
    # check for new discord messages
    def check_pending_timers(self):
        # check timer for thoughts
        for timer in self.timers:
            if timer.is_ready():
                self._work(timer.job)
                timer.reset()
                
    def _work(self, job: Job):
        if job.type == Job.JobType.OBSERVATION:
            self._observe(job)
        elif job.type == Job.JobType.THOUGHT:
            self._think(job)
        elif job.type == Job.JobType.ACTION:
            self._act(job)
        elif job.type == Job.JobType.NOTIFICATION:
            self._notify(job)
        else:
            raise ValueError(f"Invalid job type: {job.type}")
                
    def _think(self, thought: Thought):
        pass
        # while not self._stop_event.is_set():
        #     try:
        #         message = self.message_queue.get(timeout=1)
        #         self._save_to_history(message)
        #     except queue.Empty:
        #         continue
        
    
    # perform action -> starts action thread
    #   - speak
    #   - tweet (bluesky)
    #   - post to discord
    #   - send email
    #   - post on twitch chat (if streaming)
    #   - set an alarm
    #   - take a screen grab
    #   - set a reminder
    def _act(self, action: Action):
        pass
        # while not self._stop_event.is_set():
        #     response = self._generate_response()
        #     if response:
        #         print(f"{self.name}: {response}")
        #         self._speak_to_api(response)
        #         parsed_tag = ConversationRules.parse_message_tag(response)
        #         if parsed_tag and parsed_tag['action'] == 'INTERRUPTING':
        #             break
        #     time.sleep(0.5)  # Allow other threads to interact
