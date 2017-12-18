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
            "estimate": self._get_artifact_info,
            "name": self._get_artifact_info,
            "owner": self._get_artifact_info,
            "status": self._get_artifact_info,
            "state": self._get_artifact_info
        }
        self.COMMANDS_LIST = list(self.commands.keys())
        self.CREATOR = 'garth'

        self.hidden_commands = {
            "quit": self._quit
        }

##    
    def _find_command(self, usr_txt):
        lis = []
        fuzz_methods = [
            'ratio', 
            'partial_ratio', 
            'token_sort_ratio', 
            'partial_token_sort_ratio', 
            'token_set_ratio', 
            'partial_token_set_ratio'
            ]
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
            return f'No suitable match for: "{usr_txt}". Please rewrite your request.'

##    
    def _get_formatted_id(self, usr_txt):
        puncts = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
        for wrd in usr_txt.split():        
            for p in puncts:
                wrd = wrd.replace(p, '')

        if not wrd.isalpha():
            return wrd.upper()
        else:
            return f"No Rally IDs found in: {usr_txt}"        
##
    def _handle_command(self, user, usr_txt):
        response = '<@' + user + '> '
        _CMD = self._find_command(usr_txt)
        print(_CMD)
        _ID = self._get_formatted_id(usr_txt)
        print(_ID)

        if usr_txt in self.hidden_commands:
            response += self.hidden_commands[usr_txt]()
        elif _CMD in self.commands:
            if _CMD in ('estimate'):
                response += self.commands[_CMD](_ID, 'PE')
            elif _CMD in ('name'):
                response += self.commands[_CMD](_ID, 'N')
            elif _CMD in ('owner'):
                response += self.commands[_CMD](_ID, 'O')
            elif _CMD in ('state'):
                response += self.commands[_CMD](_ID, 'KSA')
            else:
                response += self.commands[_CMD]()
        else:
            response += "I do not understand the command: _*" + _CMD + "*_. " + self._get_help()        
        return response    

##
    def _get_artifact_info(self, formatted_id, _attribute):
        _artifact = self._get_artifact_type(formatted_id)
        _rallyresp = self.AYX._artifact_info(formatted_id, _artifact, _attribute)
        return _rallyresp['msg']
        
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
