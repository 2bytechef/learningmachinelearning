from pathlib import Path
import threading
import time
import random
from typing import List

from conversation_hosts.chatbots import Chatbot
from conversation_hosts.system_prompt_loader import FormattingInstructions, Personality, Scenario, SystemPromptLoader, ConversationRules
from conversation_hosts.oracles import HumanOracle, Oracle

# Shared event for signaling the interrupt
interrupt_event = threading.Event()

# Simulated function for playing audio
def audio_playback(response, playback_id):
    print(f"Thread-{playback_id}: Starting audio playback: '{response}'")
    for i, word in enumerate(response.split()):
        if interrupt_event.is_set():  # Check if interrupt event is triggered
            print(f"Thread-{playback_id}: Interrupted at word '{word}'!")
            interrupt_event.clear()  # Reset the interrupt
            return
        print(f"Thread-{playback_id}: Playing word: '{word}'")
        time.sleep(0.5)  # Simulate audio playback time
    print(f"Thread-{playback_id}: Playback complete.")

# Simulated function for predicting an interrupt point
def predictor(response, playback_id, trigger_word):
    print(f"Interruptor: Monitoring playback-{playback_id}...")
    words = response.split()
    # Predict when to send an interrupt
    for i, word in enumerate(words):
        if word == trigger_word:
            print(f"Interruptor: Interrupt predicted at word '{word}'!")
            time.sleep(i * 0.5)  # Wait until that point in playback
            interrupt_event.set()  # Trigger the interrupt
            return
    print("Interruptor: No trigger word found, no interrupt sent.")

# Thread for audio input simulation (listening to audio)
def audio_listener():
    print("Listener: Listening to audio input...")
    while True:
        time.sleep(random.uniform(1, 3))  # Simulate random listening events
        print("Listener: Heard something interesting!")

# Main function to simulate the threading
def main():
    # Sample responses from ChatGPT
    responses = [
        "Hello there how are you doing today",
        "The quick brown fox jumps over the lazy dog",
        "Python is a versatile programming language"
    ]
    trigger_word = "jumps"  # Word at which the interrupt occurs
    
    # Start the audio listener thread
    listener_thread = threading.Thread(target=audio_listener, daemon=True)
    listener_thread.start()

    # Start the audio playback threads with interrupt prediction
    for i, response in enumerate(responses):
        playback_thread = threading.Thread(target=audio_playback, args=(response, i))
        predictor_thread = threading.Thread(target=predictor, args=(response, i, trigger_word))
        
        playback_thread.start()
        predictor_thread.start()
        
        playback_thread.join()
        predictor_thread.join()

if __name__ == "__main__":
    main()


# Conversation Class
class Conversation:
    def __init__(self, bots: List[Chatbot], oracle: Oracle):
        self.bots = {bot.name: bot for bot in bots}
        self.oracle = oracle
        # self.speaking_queue = queue.Queue()
        # self.current_speaker = None

    def start(self):
        while True:
            # 
            
            
            # self._next_speaker()
            # time.sleep(0.5)

    def _next_speaker(self):
        if self.speaking_queue.empty():
            return
        speaker_name = self.speaking_queue.get()
        self.current_speaker = self.bots.get(speaker_name)
        if self.current_speaker:
            response = self.current_speaker._generate_response()
            self._handle_response(response)

    def _handle_response(self, response: str):
        parsed_tag = ConversationRules.parse_message_tag(response)
        if not parsed_tag:
            return

        action = parsed_tag['action']
        target = parsed_tag.get('target')
        bot_name = parsed_tag['bot_name']

        if action == 'INTERRUPTING':
            self.speaking_queue.queue.clear()
            self.speaking_queue.put(bot_name)
        elif action == 'WAIT':
            if target:
                self.speaking_queue.put(target)
        elif action == 'CONTINUE':
            self.speaking_queue.put(bot_name)
        elif action == 'STOP':
            pass

    def send_message(self, message: str):
        for bot in self.bots.values():
            bot.receive_message(message)

    def stop_all(self):
        for bot in self.bots.values():
            bot.stop()

# Example Usage
if __name__ == "__main__":
    sam_prompt = SystemPromptLoader.load_prompt(
        conversation_rules=ConversationRules.PERSONAL_ASSISTANT,
        formatting_instructions=None,
        scenario=Scenario.CODING_HELP,
        personality=Personality.PERSONAL_ASSISTANT,
        # history_log_path=Path("./chatbots/chat_history.log")
    )

    is_streaming = False

    ross = HumanOracle("ROSS")
    sam = Chatbot(
        "SAM",
        sam_prompt,
        conversation_kwargs={"oracle_name": "ROSS"},    
        history_log_path=Path("./chatbots/chat_history.log")
    )

    conv = Conversation([sam], oracle_name="ROSS")
    # try:
    #     conv.send_message("[TONY] {INTERRUPTING} -> `ALEX` Let's discuss this issue.")
    #     conv.start()
    # except KeyboardInterrupt:
    #     conv.stop_all()
