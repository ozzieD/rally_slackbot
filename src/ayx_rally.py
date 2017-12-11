### MODULE IMPORTS
# 3rd-party imports
import os
from pyral import Rally, rallyWorkset
from dotenv import load_dotenv, find_dotenv

# local source imports
import command


# expose local environment constants
load_dotenv(find_dotenv())

"""
keys = 
    'Blocked', 'BlockedReason', 'c_KanbanStateAlteryxSuperset', 'Description', 
    'FormattedID', 'Feature', 'LastUpdateDate', 'Iteration', 'Name', 
    'Owner', 'PlanEstimate', 'Project', 'Ready', 'Release', 'RevisionHistory'

"""
class AyxRally:
    
    def __init__(self):
        self.RALLYREST_KEYS = {
            'AST': 'c_KanbanStateAlteryxSuperset', 
            'B': 'Blocked',  'BR': 'BlockedReason', 
            'D': 'Description', 
            'F': 'PortfolioItem', 
            'I': 'Iteration', 'ID': 'FormattedID', 
            'LU': 'LastUpdateDate', 
            'N': 'Name', 
            'O': 'Owner', 'OID': 'ObjectID',
            'PE': 'PlanEstimate', 
            'RDY': 'Ready',  'REL': 'Release', 
            'SS': 'ScheduleState',
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
                response[_k] = response[_k].get('_refObjectName')
        return response 

    def _query_artifact_state(self, _id, _artifact):
        _query = f'FormattedID = "{_id}"'
        _rallyget = self._rally_get(_artifact, _query)

        _rallystate = _rallyget['c_KanbanStateAlteryxSuperset']
        _rallyobjid = str(_rallyget['ObjectID'])
        _rallyrespobj = self.rally_url + '/detail/userstory/' + _rallyobjid
        _rallyrespkey = _rallyresp.get(_rallystate)

        response = [_rallyrespobj, _rallyrespkey]
        return response