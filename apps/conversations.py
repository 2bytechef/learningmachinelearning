
# conversation
# loop to listen to user input
# checks for pending thoughts for bots and oracles each loop
# if there is a pending thoughts, and available threads, 
#   spin up a new thinking thread for the bot with the pending thought
#   after thinking threads return, queue actions
#   in conversations with lots of bots, avoid using bots with a lot of pending thoughts
# if conversation is open, allow an action thread to go through
#   for any bots with queued actions (actions)
#   when an action is triggered, notify other bots of the triggered action, this may start thinking threads for them
# if user inputs a command, process command
#   pause/resume actions, 
#   pause/resume thoughts,
#   speak - give commands
#      return text from speaking thread
#      analyze for bot names and send to most named bot to think

from apps.conversation_hosts.system_prompt_loader import ConversationRules


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
