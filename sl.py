import requests
import common
import util
import sys
import os

class SLName(object):
  """A class of Wiki enquiry
  """
  SLNAMEAPI       = "http://api.sl.se/api2/typeahead.json"
  SLNAMEAPI_FLAGS = {
    "key"           : "a0c908774ff44caab2e553fd4bb9f609",
    "stationsonly"  : "True",
    "maxresults"    : "30"
  }
  
  def __init__(self, name):
    """Constructor of the Wiki enquiry
    @param titles titles to be searched
    """
    ## titles to be searched
    self.name = name
    ## Keyword to be searched
    self.keywords = None
    ## XML raw results
    self.raw_results = None
    ## Printable results
    self.results = None
    ##
    self.first_id = 0

  def get_results(self):
    """Get a formatted results
    """
    self.format_keywords()
    self.get_content()
    self.format_results()    
    return self.results
  
  def format_keywords(self):
    """Format the keywords
    """
    self.keywords = "searchstring=" + common.format_texts(self.name)
    return

  def get_content(self):
    """Get the content of the wiki enquiry
    """
    formatted_url = common.format_url(self.SLNAMEAPI, self.SLNAMEAPI_FLAGS, self.keywords);
    self.raw_results = requests.get(formatted_url)
    return

  def format_results(self):
    """Extract the results from a wiki XML content
    """  
    results = self.raw_results.json()["ResponseData"]
  
    output = "\n" 
    for result in results:
      output = output + '%-6s' % result["SiteId"] + result["Name"] + "\n"
    self.results = output
    self.first_id = results[0]["SiteId"]
    return

class SL(object):
  """A class of SL stop enquiry
  """
  
  SLAPI       = "http://api.sl.se/api2/realtimedepartures.json"
  SLAPI_FLAGS = {
    "key"          : "86564990d30b4fc496406e1b93c12686",
    "timewindow"   : "30",
  }

  def __init__(self, siteid, direction):
    """Constructor of the Wiki enquiry
    @param titles titles to be searched
    """
    ## titles to be searched
    self.siteid = siteid
    ## XML raw results
    self.raw_results = None
    ## 
    self.direction = int(direction)
    ## Printable results
    self.results = None

  def get_results(self):
    """Get a formatted results
    """
    self.format_keywords()
    self.get_content()
    self.format_results()    
    return self.results

  def format_keywords(self):
    """Format the keywords
    """
    self.keywords = "siteid=" + self.siteid
    return

  def get_content(self):
    """Get the content of the wiki enquiry
    """
    formatted_url = common.format_url(self.SLAPI, self.SLAPI_FLAGS, self.keywords);
    self.raw_results = requests.get(formatted_url)
    return
    
  def format_results(self):
    """Extract the results from a wiki XML content
    """  
    metro_results = self.raw_results.json()["ResponseData"]["Metros"]
    bus_results = self.raw_results.json()["ResponseData"]["Buses"]
    train_results = self.raw_results.json()["ResponseData"]["Trains"]
    tram_results = self.raw_results.json()["ResponseData"]["Trams"]
    
    all_traffic = []
    for metro in metro_results:
      all_traffic.append(metro)
    for bus in bus_results:
      all_traffic.append(bus)
    for train in train_results:
      all_traffic.append(train)
    for tram in tram_results:
      all_traffic.append(tram)
    
    output = "\n" + self.raw_results.json()["ResponseData"]["LatestUpdate"].replace("T", " ") + "\n\n"
    output = output + self.form_results_text(all_traffic)
    if self.raw_results.json()["Message"] != None:
      output = output + "\n" + self.raw_results.json()["Message"] + "\n"
    self.results = output
    return
  
  def form_results_text(self, all_traffic):
    output1=""
    output2=""
    for traffic in all_traffic:
      if traffic["JourneyDirection"] == 1:
        output1 = output1 + self.format_traffic(traffic)
      if traffic["JourneyDirection"] == 2:
        output2 = output2 + self.format_traffic(traffic)
    if self.direction == 1:
      output = output1
    elif self.direction == 2:
      output = output2
    elif self.direction == 3:
      output = output1 + "\n" + output2
    return output
  
  def format_traffic(self, traffic):
    text = '%-7s' % traffic["TransportMode"]
    text = text + '%-7s' % traffic["LineNumber"]
    text = text + '%-40s' % traffic["Destination"]
    text = text + '%-9s' % traffic["DisplayTime"]
    text = text + "\n"
    
    return text
    
def main():
    if len(sys.argv) < 4:
      sl = SL(sys.argv[1], sys.argv[2])
      print sl.get_results()
    elif sys.argv[3].isdigit():
      if len(sys.argv) > 4:
        sl = SL(sys.argv[3], sys.argv[4])
      else:
        sl = SL(sys.argv[3], 3)
      print sl.get_results()
    else:
      sys.argv.pop(0)
      sys.argv.pop(0)
      sys.argv.pop(0)
      slname = SLName(sys.argv)
      print slname.get_results()

if __name__ == "__main__":
    main()
