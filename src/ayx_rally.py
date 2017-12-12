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
        _rallyresp = self.rally.get(_artifact, fetch=True, query=_query).content['QueryResult']['Results'][0]
        response = {result: _rallyresp[result] for result in [self.RALLYREST_KEYS[k] for k in self.RALLYREST_KEYS]}
        for _k in response.keys():
            if isinstance(response[_k], dict):
                try:
                    response[_k] = response[_k].get('_refObjectName')
                except TypeError:
                    response[_k] = 'Unspecified'
        return response 

    def _artifact_info(self, _id, _artifact, _attrib):

        _query = f'FormattedID = "{_id}"'
        _rallyget = self._rally_get(_artifact, _query)

        response = {
            "id": _id,
            "url": self.rally_url + '/detail/userstory/' + str(_rallyget[self.RALLYREST_KEYS['OID']])
            }
        if _attrib in ('state'):
            response['attr'] = _rallyget[self.RALLYREST_KEYS['KSA']]
        elif _attrib in ('owner'):
            response['attr'] = _rallyget[self.RALLYREST_KEYS['O']]
        
        return response

    def _artifact_type(self, _id, _artifact):
        pass
