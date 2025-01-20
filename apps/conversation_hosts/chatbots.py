# Interrupting bots have the ability to interrupt other bots and be interrupted
# ChatGPT will be told the list of bots in it's system prompt
# It will direct certain statements to [ALL] or to [BOT_NAME]
# "[BOT_NAME -> ALL]" | "[BOT_NAME -> BOT_NAME]" followed by text
# Ex. [BOT_NAME -> ALL] - I think we should use javascript. It is superior to php.

# Responses will be given to other bots before text is sent to tts
# Other bots have the choice to interrupt or wait.
# If all other bots choose to wait, the next chatbot is chosen by who was addressed the most:
# - If [ALL] was addressed, the next speaker is randomly chosen
# If a bot chooses to interrupt, the text is sent to tts and the interrupting bot is given the floor at the sentence it chose to interrupt
#     [INTERRUPT: BOT_NAME -> ALL] - I disagree. PHP is better than javascript.

# If a bot is interrupted, it's response is cut off, and we give the interrupted agent the chance to keep speaking and interrupt back or stop
# interrupted agents who stop talking are immediately given the floor after interrupting bot is done

# If multiple bots choose to interrupt, they are both given the floor and given the choice to keep speaking or stop


import threading
import queue
import time
import json
import openai
from typing import Any, List, Dict, Optional

from apps.conversation_hosts.jobs import Speak
from apps.conversation_hosts.system_prompt_loader import ConversationRules, Personality, SystemPromptLoader
from common.timers import Timer
from common.actors import Actor
from common.triggers import Trigger


# ConversationRules Class
# class ConversationRules:
#     MESSAGE_TAGS = ['{INTERRUPTING}', '{WAIT}', '{CONTINUE}', '{STOP}']

#     @staticmethod
#     def parse_message_tag(message: str) -> Optional[Dict[str, str]]:
#         import re
#         pattern = r"\[(.*?)\]\s*\{(.*?)\}(?:\s*->\s*`(.*?)`)?"
#         match = re.search(pattern, message)
#         if match:
#             bot_name, action, target = match.groups()
#             return {
#                 'bot_name': bot_name.strip(),
#                 'action': action.strip(),
#                 'target': target.strip() if target else None
#             }
#         return None

# Chatbot Class
# bot abilities
# thinking includes reading actions, submitting prompts and adding actions to action queue

class Chatbot(Actor):
    def __init__(
        self, 
        bot_name: str, 
        personality: Personality,
        conversation_kwargs: Dict[str, Any] = {},
        history_log_path: Optional[str] = None,
        timers: List[Timer] = [],
        *args: Any,
        **kwargs: Dict[str, Any] = {},
    ):#, other_bots: List[str]):
        conversation_rules = conversation_kwargs.pop("conversation_rules", None)
        formatting_instructions = conversation_kwargs.pop("formatting_instructions", None)
        scenario = conversation_kwargs.pop("scenario", None)
        
        prompt = SystemPromptLoader.load_prompt(
            conversation_rules=conversation_rules,
            formatting_instructions=formatting_instructions,
            scenario=scenario,
            personality=personality,
            history_log_path=history_log_path,
            bot_name=bot_name,
            **conversation_kwargs,
        )
        self.system_prompt = prompt.format(bot_name=bot_name, **conversation_kwargs)
        # self.timers = timers
        
        # if 'other_bots' in kwargs:
        #     self.other_bots = kwargs['other_bots']
        # self.other_bots = other_bots
        # self.conversation_history = []  # Persistent conversation file
        # self.message_queue = queue.Queue()
        # self.thinking_thread = threading.Thread(target=self._think)
        # self.speaking_thread = threading.Thread(target=self._speak)
        # self._stop_event = threading.Event()
        # self.lock = threading.Lock()
        # self.thinking_thread.start()
        # self.speaking_thread.start()
        
        return super().__init__(name=bot_name, timers=timers, *args, **kwargs)


    def _generate_response(self) -> str:
        prompt = self.system_prompt + '\n' + '\n'.join(self.conversation_history)
        # Call OpenAI's API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}]
        )
        return response['choices'][0]['message']['content']



    def _generate_speech(self, text: str):
        # get speech output from OpenAPI
        pass
        # print(f"{self.name} is sending TTS for: {text}")
        # Placeholder for OpenAPI TTS call

    def _speak(self):
        # send to audio_out
        pass
        # while not self._stop_event.is_set():
        #     try:
        #         message = self.message_queue.get(timeout=1)
        #         self._generate_speech(message)
        #     except queue.Empty:
        #         continue

    # notify of action -> starts notification thread
    #   will process an action performed by another bot or oracle
    #   if it's a conversation, bot appends to conversation log
    #   depending on the action, if thinking is not paused the bot may start a thinking thread
    #   or directly perform an action if actions are not paused
    def notify_of_action(self, action):
        pass
        # self.message_queue.put(message)
        
    # update log
    def _save_to_history(self, message: str):
        with self.lock:
            self.conversation_history.append(message)
            with open(f"{self.name}_history.txt", 'a') as file:
                file.write(message + '\n')

    # def stop(self):
    #     self._stop_event.set()
    #     self.thinking_thread.join()
    #     self.speaking_thread.join()
    
    def stop_thoughts(self):
        pass
        # self.thinking_thread.join()
        
    def stop_actions(self):
        pass
        # self.speaking_thread.join()
        

class InterruptingBot:
    def __init__(self, name):
        self.name = name

    #     self, 
    #     bot_name: str, 
    #     personality: Personality,
    #     conversation_kwargs: Dict[str, Any] = {},
    #     history_log_path: Optional[str] = None,
    #     timers: List[Timer] = [],
    #     *args: Any,
    #     **kwargs: Dict[str, Any] = {},
    # ):#, other_bots: List[str]):

class SamBot(Chatbot):
    def __init__(
        self, *args, **kwargs: Dict[str, Any]
        # bot_name,
        # conversation_kwargs: Dict
    ):#, system_prompt, conversation_kwargs):
        timers = [
            Timer(10, Speak()),
        ]
        
        super().__init__(timers=timers, *args, **kwargs)
        
    
    
    
