from conversation_hosts.chatbots import Chatbot


class Oracle:
    def __init__(self, name: str):
        self.name = name
        
# oracle abilities
# human oracle:
#  should have flag to trigger AI based stt comprehension (for triggereing actions)
#  speak and analyze to make text
#  analyze speech using other bot to see if any thoughts for bots should triggered
#  Speaking is an ACTION, we can also analyze whether the oracle is interrupting or not
#  speech logs should be sent to bots 
class HumanOracle(Oracle):
    def __init__(self, name: str, should_comprehend_speech: bool = False):
        super().__init__(name)
        self.comprehend_speech = should_comprehend_speech
        
    def speak(self, text: str):
        pass
    

# chatbot oracle:
#  has all the abilities of a human oracle and chatbot
#  the difference between the chatbots and chatbot oracle is that the 
#    chatbot oracle can directly give actions to other chatbots, and bypass their thinking
class ChatbotOracle(Oracle, Chatbot):
    pass
    # pass
    