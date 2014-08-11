import requests
import common
import util
import sys
import os

class Wiki(object):
  """A class of Wiki enquiry
  """
  
  WIKIAPI       = "http://api.sl.se/api2/realtimedepartures.json"
  WIKIAPI_FLAGS = {
    "key"          : "86564990d30b4fc496406e1b93c12686",
    "timewindow"   : "30",
  }

  def __init__(self, siteid):
    """Constructor of the Wiki enquiry
    @param titles titles to be searched
    """
    ## titles to be searched
    self.siteid = siteid
    ## XML raw results
    self.raw_results = None
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
    self.keywords = "siteid=%d" % self.siteid
    return

  def get_content(self):
    """Get the content of the wiki enquiry
    """
    formatted_url = common.format_url(self.WIKIAPI, self.WIKIAPI_FLAGS, self.keywords);
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
    
    self.results = self.form_results_text(all_traffic)
    return
  
  def form_results_text(self, all_traffic):
    seq = [transport["ExpectedDateTime"] for transport in all_traffic]
    
    return min(seq)
  
  def format_a_traffic(self, traffic):
    return 
    
def main():
    sys.argv.pop(0)
    #wiki = Wiki(sys.argv[1])
    wiki = Wiki(4634)
    print wiki.get_results()

if __name__ == "__main__":
    main()
