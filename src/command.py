### MODULE IMPORTS
# 3rd-party imports
import regex, sys
from fuzzywuzzy import fuzz, process

# local imports
import ayx_rally 

class Command(object):

    def __init__(self):
        self.ARTIFACT_TYPE = {
            'US': 'UserStory', 'DE': 'Defect', 'DS': 'DefectSuite', 
            'TA': 'Task', 'TC': 'TestCase', 'TS': 'TestSet', 'F': 'PortfolioItem',
            'PI': 'PortfolioItem'
        }
        self.AYX = ayx_rally.AyxRally()
        
        self.commands = {
            "help": self._get_help,
            "owner": self._get_artifact_info,
            "status": self._get_artifact_info,
            "state": self._get_artifact_info
        }
        self.COMMANDS_LIST = list(self.commands.keys())
        self.CREATOR = 'garth'

        self.hidden_commands = {
            "quit": self._quit
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
        # response = ""
        # _P0 = ""
        # _P1 = ""
        # _FLAGS = regex.I | regex.BESTMATCH        
        # _P0 = regex.compile('(' + self._build_search_pattern(self.METHOD_LIST) + '){e<=2}', _FLAGS)

        # # scan for keyword
        # _MSG0 = regex.search(_P0, usr_txt)
        # if bool(_MSG0):
        #     _P1 = regex.compile('(' + usr_txt[_MSG0.start():_MSG0.end()] + '){e<=2}', _FLAGS)
        #     for _FUNC in self.METHOD_LIST:
        #         _MSG1 = regex.search(_P1, _FUNC)
        #         if bool(_MSG1):
        #             response = _MSG1.group().lower()
        # else:
        #     print("No matches...[TODO: write logic to handle when messages aren't matched]")
        #     response = usr_txt
        # return response                
    # def _find_command(text):
        lis = []
        fuzz_methods = ['ratio', 'partial_ratio', 'token_sort_ratio', 'partial_token_sort_ratio', 'token_set_ratio', 'partial_token_set_ratio']
        for m in fuzz_methods:
            RATIOS = []
            VALUES = []

            process_extract = process.extract(usr_txt, self.COMMANDS_LIST, scorer=eval('fuzz.' + m))
            for result_ in process_extract:
                RATIOS.append(result_[1])
                VALUES.append(result_[0])
        
            max_val = max(RATIOS)
            best_match = VALUES[RATIOS.index(max_val)]
            lis.append((max_val, best_match))

        response = max(lis, key=lambda x: x)
        if response[0] > 50:
            return response[1]
        else:
            return f'No suitable match for: "{text}" Please rewrite your request.'

##    
    def _get_formatted_id(self, usr_txt):
        _FLAGS = regex.I
        _P0 = regex.compile('((?:US|DE|DS|TA|TC|TS|PI)[0-9]+)', _FLAGS)
        _MSG = regex.search(_P0, usr_txt)
        response = ""
        if bool(_MSG):
            response = _MSG.group().upper()
        else:
            response = usr_txt
        return response
                
##
    def _handle_command(self, user, usr_txt):
        response = '<@' + user + '> '
        _CMD = self._find_command(usr_txt)
        print(_CMD)
        _ID = self._get_formatted_id(usr_txt)
        print(_ID)

        if _CMD in self.hidden_commands:
            response += self.hidden_commands[_CMD]()
        elif _CMD in self.commands:
            if _CMD in ('owner'):
                response += self.commands[_CMD](_ID, 'O')
            elif _CMD in ('state'):
                response += self.commands[_CMD](_ID, 'KSA')
            else:
                response += self.commands[_CMD]()
        else:
            response += "I do not understand the command: _*" + cmd + "*_. " + self._get_help()        
        return response    

##
    def _get_artifact_owner(self, formatted_id):
        # identify attribute type from formatted id
        _artifact = self._get_artifact_type(formatted_id)

        # pass the artifact type and formatted id to ayx_rally
        _rallyresp = self.AYX._artifact_info(formatted_id, _artifact, 'owner')

        # populate the response with results
        response = f"The owner of <{_rallyresp['url']}|{formatted_id}> is: *{_rallyresp['attr']}*"

        # return response
        return response 

##
    def _get_artifact_info(self, formatted_id, _attribute):
        _artifact = self._get_artifact_type(formatted_id)
        _rallyresp = self.AYX._artifact_info(formatted_id, _artifact, _attribute)
        return _rallyresp['msg']
        

##    
    def _get_artifact_state(self, formatted_id):
        _artifact = self._get_artifact_type(formatted_id)
        _rallyresp = self.AYX._artifact_info(formatted_id, _artifact, 'state')     
        response = f"The current state of <{_rallyresp['url']}|{formatted_id}> is: *{_rallyresp['attr']}*"
        return response

##
    def _get_artifact_type(self, formatted_id):
        _K = regex.split('([\D]+)', formatted_id)[1]
        return self.ARTIFACT_TYPE[_K]
  
##    
    def _get_help(self):
        response = "I currently support the following commands:\r\n"
        for command in self.commands:
            response += command + '\r\n'
        return response 

##
    def _quit(self):
        sys.exit(1)
