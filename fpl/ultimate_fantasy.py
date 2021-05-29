"""
End-to-end automated fantasy script
"""

#Import libraries
import requests
import json
from datetime import datetime
import pandas as pd
#from selenium import webdriver

#Define classes 
class fpl_endpoints:
    """
    Define all endpoints available for fantasy premier league api
    """
    def __init__(self, endpoint, element=None, event=None, user=None, league=None):
        """
        Define fixed variables for class
        """
        self.endpoint = endpoint
        self.element = element
        self.event = event
        self.user = user
        self.league = league
    
    def _get_url(self):
        """
        Define url endpoint to use 
        """
        if self.endpoint=='players':
            url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
        elif self.endpoint=='fixtures':
            url = 'https://fantasy.premierleague.com/api/fixtures/'
        elif self.endpoint=='detailed' and self.element!=None:
            url = 'https://fantasy.premierleague.com/api/element-summary/{}/'.format(self.element)
        elif self.endpoint=='live' and self.event!=None:
            url = 'https://fantasy.premierleague.com/api/event/{}/live/'.format(self.event)
        elif self.endpoint=='user' and self.user!=None:
            url = 'https://fantasy.premierleague.com/api/entry/{}/'.format(self.user)
        elif self.endpoint=='league' and self.league!=None:
            url = 'https://fantasy.premierleague.com/api/leagues-classic/{}/standings'.format(self.league)
        elif self.endpoint=='team' and self.user!=None:
            url = 'https://fantasy.premierleague.com/api/my-team/{}/'.format(self.user)
        else:
            url = None
        return url
    
    def _get_data(self):
        """
        Get data fro api endpoint
        """
        url = self._get_url()
        get_data = requests.get(url).text
        data = json.loads(get_data)
        return data
            
    
class fpl_players:
    """
    Define all endpoints related to players endpoint
    """
    
    def __init__(self):
        """
        Define fixed variables for class
        """
        self.data = fpl_endpoints(endpoint='players')._get_data()
        self.events = self.data['events']
        self.players = self.data['elements']
    
    def _get_current_gweek(self):
        """
        Get the id for the current gameweek (if in a gameweek)
        """
        current = None
        for week in self.events:
            if week['is_current'] == True:
                current = week['id']
        return current
    
    def _get_next_gweek(self):
        """
        Get the id for the next gameweek
        """
        nxt = None
        for week in self.events:
            if week['is_next'] == True:
                nxt = week['id']
        return nxt
    
    def _get_deadline(self):
        """
        Get the deadline for the next gameweek
        """
        gameweek = self._get_next_gweek()
        for event in self.events:
            if event['id'] == gameweek:
                deadline = event['deadline_time']
        deadline = deadline.replace('Z','')
        deadline = deadline.replace('T', ' ')
        deadline = datetime.strptime(deadline,'%Y-%m-%d %H:%M:%S')
        return deadline
    
    def _player_data(self):
        df = pd.DataFrame(data=self.players)
        df = df.set_index('id')
        df = df.sort_index(ascending=True)
        return df
    
    def _get_column(self, column):
        df = self._player_data().filter(['id', 'first_name', 'second_name', column], axis=1)
        return df
    
    def _get_points(self):
        return self._get_column(column='total_points')
    
    def _get_max_points(self):
        df = self._get_points()
        df = df.sort_values(by=['total_points'], ascending=False)
        return df
    
    def _get_ppc(self):
        df = self._player_data().filter(['id', 'first_name', 'second_name', 'total_points', 'now_cost'], axis=1)
        df['ppc'] = df.apply(lambda x: x['total_points'] / x['now_cost'], axis=1)
        df = df.drop(['total_points', 'now_cost'], axis=1)
        df = df.sort_values(by=['ppc'], ascending=False)
        return df
    
    def _get_player_attribute(self, player, attribute):
        """
        Where you type in the players last name for player
        """
        df = self._player_data()
        att = df[df['second_name']==player][attribute].values[0]
        return att
    
    def _get_position(self):
        return self._get_column(column='element_type')
    
    def _get_cost(self):
        return self._get_column(column='now_cost')
    
    def _get_play_chance(self):
        return self._get_column(column='chance_of_playing_this_round')
    
    def _get_team(self):
        return self._get_column(column='team')
    
    def _get_news(self):
        return self._get_column(column='news')
            
class fpl_fixtures:
    """
    Get the fixture information
    """
    
    def __init__(self):
        self.data = fpl_endpoints(endpoint='fixtures')._get_data() 

class fpl_detailed:
    """
    Get the detailed info about a specified player
    """
    
    def __init__(self, element):
        self.data = fpl_endpoints(endpoint='detailed', element=element)._get_data()
        
class fpl_live:
    """
    Get the live gameweek data
    """
    
    def __init__(self, event):
        self.data = fpl_endpoints(endpoint='live', event=event)._get_data()

class fpl_user:
    """
    Get info about a fpl user/manager
    """
    
    def __init__(self, user):
        self.data = fpl_endpoints(endpoint='user', user=user)._get_data()
        
class fpl_league:
    """
    Get info about a fpl league
    """
    
    def __init__(self, league):
        self.data = fpl_endpoints(endpoint='league', league=league)._get_data()

class fpl_my_team:
    """
    Get my team - requires authorisation
    """
    
    def __init__(self, user):
        self.data = fpl_endpoints(endpoint='team', user=user)._get_data()
    
        
    
class transfer_reminder:
    """
    Email notification of the next gameweek deadline
    """
    
    def __init__(self):
        pass

class make_trasfers:
    """
    Class to make transfers automatically
    """
    
    def __init__(self):
        pass
        
class create_team:
    
    def __init__(self):
        pass


user = ''
p = fpl_players()
