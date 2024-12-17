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

class InterruptingBot:
    def __init__(self, name):
        self.name = name
        
    