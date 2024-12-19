
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
