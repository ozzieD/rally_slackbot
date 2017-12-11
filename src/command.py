### MODULE IMPORTS
# 3rd-party imports
import os, regex

# local source imports
import ayx_rally 

class Command(object):

    def __init__(self):
        self.ARTIFACT_TYPE = {
            'US': 'UserStory', 'DE': 'Defect', 'DS': 'DefectSuite', 
            'TA': 'Task', 'TC': 'TestCase', 'TS': 'TestSet', 
            'PI': 'PortfolioItem'
        }
        self.ayx = ayx_rally.AyxRally()
        self.commands = {
            "echo": self._echo_usr,
            "help": self._get_help,
            "quit": self._quit,
            "state": self._get_state
        }      
        self.METHOD_LIST = list(getattr(self, "commands").keys())
        
##
    def _build_search_pattern(self, list_arry):
        response = ""
        for _M in list_arry:
            response += _M + '|'
        return response.strip('|')

##    
    def _find_command(self, usr_txt):
        response = ""; _P0 = ""; _P1 = ""
        _FLAGS = regex.I | regex.BESTMATCH        
        _P0 = regex.compile('(' + self._build_search_pattern(self.METHOD_LIST) + '){e}', _FLAGS)

        # scan for keyword
        _MSG0 = regex.search(_P0, usr_txt)
        if bool(_MSG0):
            _P1 = regex.compile('(' + usr_txt[_MSG0.start():_MSG0.end()] + '){e<=2}', _FLAGS)
        else:
            print("No matches...[TODO: write logic to handle when messages aren't matched]")
        
        for _FUNC in self.METHOD_LIST:
            _MSG1 = regex.search(_P1, _FUNC)
            if bool(_MSG1):
                response = _MSG1.group()
        return response                
    
##    
    def _get_formatted_id(self, usr_txt):
        _FLAGS = regex.I
        _P0 = regex.compile('((?:US|DE|DS|TA|TC|TS|PI)[0-9]+)', _FLAGS)
        _MSG = regex.search(_P0, usr_txt)
        response = ""
        if bool(_MSG):
            response = _MSG.group().upper()
        else:
            response = "Something is screwy. " + self._echo_usr(usr_txt)
        return response
                
##
    def _handle_command(self, user, usr_txt):
        response = '<@' + user + '> '
        cmd = self._find_command(usr_txt)
        txt = self._get_formatted_id(usr_txt)

        if cmd in self.commands:
            if cmd in ('echo', 'state'):
                response += self.commands[cmd](txt)
            else:
                response += self.commands[cmd]()
        else:
            response += "I do not understand the command: " + command + ". " + self.help()        
        return response
    
##    
    def _echo_usr(self, usr_txt):
        if bool(usr_txt):
            response = usr_txt
        else:
            response = "All you sent me was the " + text + " command." 
        return response 
    
##    
    def _get_help(self):
        response = "I currently support the following commands:\r\n"
        for command in self.commands:
            response += command + '\r\n'
        return response 

##    
    def _get_state(self, formatted_id):
        _artifact_key = regex.split('([\D]+)', formatted_id)[1]
        _artifact = self.ARTIFACT_TYPE[_artifact_key]
        _rallyresp = self.ayx._query_state(formatted_id, _artifact)        
        response = f"The current state of *{formatted_id}* is: *{_rallyresp}*"
        return response
    
##
    def _quit(self):
        os.exit(1)

    
