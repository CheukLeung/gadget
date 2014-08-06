import common
import util
import sys
import os

class Wiki(object):
  """A class of Wiki enquiry
  """
  WIKIAPI       = "http://api.sl.se/api2/realtimedepartures.xml"
  WIKIAPI_FLAGS = {
    "key"          : "86564990d30b4fc496406e1b93c12686",
    "timewindow"   : "30",
  }

  def __init__(self, titles):
    """Constructor of the Wiki enquiry
    @param titles titles to be searched
    """
    ## titles to be searched
    self.titles = titles
    ## keywords
    self.keywords = None
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
    formatted_titles = common.format_texts(self.titles);
    self.keywords = "siteid=" + formatted_titles
    return

  def get_content(self):
    """Get the content of the wiki enquiry
    """
    formatted_url = common.format_url(self.WIKIAPI, self.WIKIAPI_FLAGS, self.keywords);
    self.raw_results = common.get_url_content(formatted_url)
    return
    
  def format_results(self):
    """Extract the results from a wiki XML content
    """  
    metro_results = util.get_contents(self.raw_results, 'Metros')
    bus_results = util.get_contents(self.raw_results, 'Buses')
    train_results = util.get_contents(self.raw_results, 'Trains')
    tram_results = util.get_contents(self.raw_results, 'Trams')
    self.results = self.form_results_text(metro_results, bus_results, train_results, tram_results)
    return
  
  def form_results_text(self, metros, buses, trains, tram):
    return len(buses)
    
def main():
    sys.argv.pop(0)
    wiki = Wiki(sys.argv)
    print wiki.get_results()

if __name__ == "__main__":
    main()
