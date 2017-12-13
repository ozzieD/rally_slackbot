### MODULE IMPORTS
# local imports
import command 

class Event:
    
    def __init__(self, bot): 
        """
        this class constructor takes the 'bot' object as input
        and stores it in a variable so other methods can have 
        access to it
        """
        self.bot = bot
        self.bot_id = bot.bot_id
        self.command = command.Command()

    def wait_for_event(self):
        """
        waits to do something with the most recent event in
        the slack rtm queue
        """
        events = self.bot.slack_client.rtm_read()

        if events and len(events) > 0:
            for event in events:
                self.parse_event(event)
    
    def parse_event(self, event):
        """
        parses the text from slack rtm message
        """
        if event and 'text' in event and self.bot_id in event['text']:            
            usr = event['user']
            cmd = event['text'].split(self.bot_id)[1].strip().lower()
            chnnl = event['channel']

            self.handle_event(usr, cmd, chnnl)
    
    def handle_event(self, user, command, channel):
        if command and channel:
            response = self.command._handle_command(user, command)

            self.bot.slack_client.api_call('chat.postMessage', 
                channel=channel, 
                text=response, 
                as_user=True
                )



