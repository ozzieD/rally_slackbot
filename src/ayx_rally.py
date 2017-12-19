### MODULE IMPORTS
# 3rd-party imports
import os
from pyral import Rally, rallyWorkset
from dotenv import load_dotenv, find_dotenv

# local imports
import command

# expose local environment constants
load_dotenv(find_dotenv())

class AyxRally:
    
    def __init__(self):

        self.RALLYREST_KEYS = {
            'B': 'Blocked',  'BR': 'BlockedReason','D': 'Description', 'F': 'PortfolioItem', 
            'I': 'Iteration', 'ID': 'FormattedID', 'KSA': 'c_KanbanStateAlteryxSuperset', 
            'LU': 'LastUpdateDate', 'N': 'Name', 'O': 'Owner', 'OID': 'ObjectID', 
            'PE': 'PlanEstimate', 'RDY': 'Ready',  'REL': 'Release', 'SS': 'ScheduleState'
        }
        # collect service agent info
        RALLY_SERVER = os.environ.get('RALLY_SERVER')
        RALLY_USER = os.environ.get('RALLY_USER')
        RALLY_PASSWORD = os.environ.get('RALLY_PASSWORD')
        RALLY_APIKEY = os.environ.get('RALLY_APIKEY')
        RALLY_PROJECT = 'Content Engineering'
        options = RALLY_SERVER, RALLY_USER, RALLY_PASSWORD, RALLY_APIKEY, RALLY_PROJECT
        rallyWorkset(options)
        
        self.rally = Rally(RALLY_SERVER, RALLY_USER, RALLY_PASSWORD, apikey=RALLY_APIKEY, project=RALLY_PROJECT)
        rally_project = self.rally.get("Project", fetch=True, query=f'Name = "{RALLY_PROJECT}"').content['QueryResult']['Results'][0]
        rally_project_id = rally_project.get('ObjectID')
        self.rally_url = f"https://rally1.rallydev.com/#/{rally_project_id}"
    
    def _rally_get(self, _artifact, _query):
        response = self.rally.get(_artifact, fetch=True, query=_query).content['QueryResult']['Results'][0]
        return response 

    def _prune_rally_obj(self, _object):
        RALLY_ITEMS = [self.RALLYREST_KEYS[k] for k in self.RALLYREST_KEYS]
        response = {
            (_k if _k else _k): (_object[_k].get('_refObjectName') 
            if isinstance(_object[_k], dict) else _object[_k]) for _k in RALLY_ITEMS
            }
        return response             
            

    def _artifact_info(self, _id, _artifact, _attrib):

        _query = f'FormattedID = "{_id}"'
        _rallyresp = self._rally_get(_artifact, _query)
        _rallyresp = self._prune_rally_obj(_rallyresp)

        response = {
            "id": _id,
            "attr": _rallyresp[self.RALLYREST_KEYS[_attrib]],
            "url": self.rally_url + f'/detail/{_artifact.lower()}/' + str(_rallyresp[self.RALLYREST_KEYS['OID']])
            }
        
        if _attrib in ('KSA'): 
            # Kanban State
            response['msg'] = f"The current state of <{response['url']}|{_id}> is: *{response['attr']}*"
        elif _attrib in ('N'): 
            # Name
            response['msg'] = f"The {_artifact} name for <{response['url']}|{_id}> is:\r\n&gt;_*{response['attr']}*_"    
        elif _attrib in ('O'):
            # Owner
            response['msg'] = f"The owner of <{response['url']}|{_id}> is: *{response['attr']}*"
        elif _attrib in ('PE'):
            # Plan Estimate
            response['msg'] = f"The plan estimate for <{response['url']}|{_id}> is: *{response['attr']}*"            
        
        return response

    def _artifact_type(self, _id, _artifact):
        pass
