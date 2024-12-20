
# conversation
# loop to listen to user input
# checks for pending thoughts for bots and oracles each loop

import time
from typing import List

from apps.conversation_hosts.jobs import Action
from apps.conversation_hosts.chatbots import Chatbot
from apps.conversation_hosts.oracles import Oracle
from apps.conversation_hosts.system_prompt_loader import ConversationRules


class Conversation:
    is_conversation_paused = False
    are_actions_paused = False
    are_thoughts_paused = False
    
    action_queue: List[Action] = []
    
    def __init__(self, bots: List[Chatbot], oracle: Oracle):
        self.bots = {bot.name: bot for bot in bots}
        self.oracle = oracle
        # self.speaking_queue = queue.Queue()
        # self.current_speaker = None

    def start(self):
        while True:
            # check for pending thoughts for bots and oracles
            # if user inputs a command, process command
            #   pause/resume actions, 
            #   pause/resume thoughts,
            #   speak - give commands
            #      return text from speaking thread
            #      analyze for bot names and send to most named bot to think
            self.oracle.check_pending_actions()
            
            if self.is_conversation_paused:
                continue
            
            # if there is a pending thoughts, and available threads, 
            #   spin up a new thinking thread for the bot with the pending thought
            #   after thinking threads return, queue actions
            #   in conversations with lots of bots, avoid using bots with a lot of pending thoughts
            if not self.are_thoughts_paused:
                for bot in self.bots.values():
                    bot.check_pending_thoughts()
                    
            # if conversation is open, allow an action thread to go through
            #   for any bots with queued actions (actions)
            #   a bot may queue multiple actions
            #   Action queues are determined by previous actions
            #   If previous action expects a reciprocation from another bot that bot gets the next action
            
            #   A bot may pass on their action - this is a PASS action_type
            
            # when an action is triggered, notify other bots of the triggered action, this may start thinking threads for them
            # go through all actions and sort them by priority
            #    - interrupts go first
            #    - responses go next
            #    - waits go last
            # priority can be determined in multiple ways ->
            #   intterupt is passed in the message tag
            #   responses are actions that respond to directed actions
            #   all other actions are waits
            # actions can be synchronous
            # pull from the top of the priority list
            #    - if interrupt, remove all other actions of the same type
            #    - if response/wait, remove only the action from the list
            if not self.are_actions_paused:
                self.action_queue = sorted(self.action_queue, key=lambda x: x.priority)
                for action in self.action_queue:
                    self.
                    
                    # if no other actiosn are going, run action
                    # if other actions are going, only allow interrupting actions to go
                    if action.priority == 0:
                        action.execute()
                        self.action_queue = [a for a in self.action_queue if a.action_type != action.action_type]
                    else:
                        if no_actions_going or action.is_synchronous():
                            action.execute()
                            self.action_queue.remove(action)
                        else:
                            break
            
            time.sleep(0.1)

    # def _next_speaker(self):
    #     if self.speaking_queue.empty():
    #         return
    #     speaker_name = self.speaking_queue.get()
    #     self.current_speaker = self.bots.get(speaker_name)
    #     if self.current_speaker:
    #         response = self.current_speaker._generate_response()
    #         self._handle_response(response)

    # def _handle_response(self, response: str):
    #     parsed_tag = ConversationRules.parse_message_tag(response)
    #     if not parsed_tag:
    #         return

    #     action = parsed_tag['action']
    #     target = parsed_tag.get('target')
    #     bot_name = parsed_tag['bot_name']

    #     if action == 'INTERRUPTING':
    #         self.speaking_queue.queue.clear()
    #         self.speaking_queue.put(bot_name)
    #     elif action == 'WAIT':
    #         if target:
    #             self.speaking_queue.put(target)
    #     elif action == 'CONTINUE':
    #         self.speaking_queue.put(bot_name)
    #     elif action == 'STOP':
    #         pass

    # def send_message(self, message: str):
    #     for bot in self.bots.values():
    #         bot.receive_message(message)

    def stop_all(self):
        pass
        # for bot in self.bots.values():
        #     bot.stop()
