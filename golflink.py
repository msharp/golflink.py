__author__="max"
__date__ ="$11/08/2009 09:10:33$"

import re
from google.appengine.api import urlfetch
from modules.BeautifulSoup import BeautifulSoup

DEFAULT_CLUB_NUMBER = "30001"

class GolflinkHandicap():
    """
    golflink website details
    """
    def __init__(self,gl=None):
        self.golflink_no = None
        self.exact_handicap = ""
        self.playing_handicap = None
        self.handicap_status = "not found"
        self.home_club = ""
        if gl:
            self.golflink_no = GolflinkNumber(gl)
            self.get_golflink_details()
    
    def get_golflink_details(self):
        if self.golflink_no:
            try:
                glpage = urlfetch.Fetch("http://www.golflink.com.au/HandicapHistory.aspx?golflink_no=" + self.golflink_no.golflink_no_for_golflink()).content
            except:
                glpage = None
			
            if glpage != None:			
                soup = BeautifulSoup(glpage)
                try:
                    self.exact_handicap = soup.find("div",id="exactHandicap").string
                    self.playing_handicap = int(soup.find("div",id="playingHandicap").string)
                except:
                    self.exact_handicap = "n/a"
                    self.playing_handicap = None
			
            #TODO - get status
            self.handicap_status = ""
    
    def is_club_member(self):
    	if self.golflink_no.club_number == DEFAULT_CLUB_NUMBER:
    		return True
    	else:
    	    return False
        
    
class GolflinkNumber():
    """
    class for working with a golflink number
    when external club is not specified, assumes default
    """
    def __init__(self, gl):
        if gl is None:    
            _cn = ""
            _bn = ""
        elif self._is_complete_golflink_no(gl):
            _cn = gl[:5]
            _bn = gl[-5:]
        else:
            _cn = DEFAULT_CLUB_NUMBER
            _bn = self._golflink_club_number(gl)
        self.club_number = _cn
        self.badge_number = _bn
	
    def golflink_no_for_golflink(self):
        ret = str(self.club_number) +'-'+ str(self.badge_number)
        if self._is_complete_golflink_no(ret):
            return ret
        else:
            return ""

    def golflink_no(self):
        if len(self.badge_number) == 5:
            return self.club_number + self.badge_number

    def _golflink_club_number(self,gl):
        bigstr = '00000'+str(gl)
        return bigstr[-5:]

    def _is_complete_golflink_no(self,gl):
        glre = re.compile("^[\d]{5}(-)?[\d]{5}$")
        if glre.match(gl):
            return True
        else:
        	return False

