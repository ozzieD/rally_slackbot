### MODULE IMPORTS
# 3rd-party imports
import os, re

# local source imports
import ayx_rally 

class Command(object):

    def __init__(self):
        """
        constructs a dictionary of functions that can be
        called to handle an event
        """
        self.ayx = ayx_rally.AyxRally()

        self.commands = {
            "echo": self.echo,
            "help": self.help,
            "state": self.state,
            "quit": self.quit
        }

    def handle_command(self, user, command):
        response = '<@' + user + '> '

        cmd_txt = self.parse_command_text(command)
        cmd = cmd_txt[0]
        txt = cmd_txt[1]
        print("command is: " + cmd, "\nmessage is: " + txt)

        if cmd in self.commands:
            if cmd in ('echo', 'state'):
                response += self.commands[cmd](txt)
            else:
                response += self.commands[cmd]()
        else:
            response += "I do not understand the command: " + command + ". " + self.help()
        
        return response 

    def parse_command_text(self, text):
        
        cmds = ''; cmd = ''; txt = ''
        for command in self.commands.keys():
            cmds += command + '|'
        cmds = cmds.strip('|')
        
        p = re.compile('(' + cmds.strip('|') + ')', re.IGNORECASE)
        msg = re.search(p, text)
        if msg is None:
            cmd = text
            txt = ""
        else:
            cmd = msg.group()
            txt = text.split(cmd)[1].strip()
        
        response = cmd, txt
        return response

    def echo(self, text):

        if bool(text):
            response = text
        else:
            response = "All you sent me was the " + text + " command." 
        return response 

    def help(self):
        response = "I currently support the following commands:\r\n"

        for command in self.commands:
            response += command + '\r\n'
        
        return response 
    
    def state(self, storyid):
        _id = storyid.upper()
        _attr = 'c_KanbanStateAlteryxSuperset'
        response = f"The current state of *{_id}* is: "

        if _id.startswith('US'):
            response += '*' + self.ayx.get_userstory_info(_id, _attr) + '*'
            
        return response

    def quit(self):
        os._exit(1)
