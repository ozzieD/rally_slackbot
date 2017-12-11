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

        # collect service agent info
        RALLY_SERVER = os.environ.get('RALLY_SERVER')
        RALLY_USER = os.environ.get('RALLY_USER')
        RALLY_PASSWORD = os.environ.get('RALLY_PASSWORD')
        RALLY_APIKEY = os.environ.get('RALLY_APIKEY')
        RALLY_PROJECT = 'Content Engineering'

        options = RALLY_SERVER, RALLY_USER, RALLY_PASSWORD, RALLY_APIKEY, RALLY_PROJECT
        rallyWorkset(options)
        self.rally = Rally(RALLY_SERVER, RALLY_USER, RALLY_PASSWORD, apikey=RALLY_APIKEY, project=RALLY_PROJECT)
        
    def get_userstory_info(self, storyid, attrib):
        _id = storyid.upper()
        _query = _query = f'FormattedID = "{_id}"'
        _attr = attrib

        response = self.rally.get("UserStory", fetch=True, query=_query).content['QueryResult']['Results'][0].get(_attr)
        return response

