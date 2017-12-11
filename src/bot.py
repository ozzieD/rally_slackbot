### MODULE IMPORTS
# 3rd-party imports
import os 
import time 
from slackclient import SlackClient 
from dotenv import load_dotenv, find_dotenv

# local source imports
import event 

# expose local environment constants
load_dotenv(find_dotenv())


class Bot(object):
    
    def __init__(self):
        """
            method constructor to initialize the Bot class
        """
        # collect service agent info
        self.BOT_NAME = os.environ.get('SLACK_BOT_NAME')
        self.BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
        
        self.slack_client = SlackClient(self.BOT_TOKEN)
        self.bot_name = self.BOT_NAME 
        self.bot_id = self.get_bot_id()

        if self.bot_id is None:
            exit("Error, could not locate " + self.bot_name)
        
        self.event = event.Event(self)
        self.listen()
    
    def get_bot_id(self):
        """
            collects the bot_id from the response from the 'members' endpoint
            obtained by an api call made to 'users.list'
        """
        api_call = self.slack_client.api_call('users.list')
        if api_call.get('ok'):
            # extract bot info from list of users
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == self.bot_name:
                    return '<@' + user.get('id') + '>'
            return None
    
    def listen(self):
        if self.slack_client.rtm_connect(with_team_state=False):
            print("CE Bot connected and listening in!")

            while True:
                self.event.wait_for_event()
                time.sleep(1)
            else:
                exit("Error: Connection Failed!!")

