import requests
import common
import util
import sys
import os
import random
from bs4 import BeautifulSoup

class SvD(object):
  """A class of Wiki enquiry
  """
  SvDAPI       = "http://www.svd.se/search.do"
  SvDAPI_FLAGS = {
    "output"    : "json",
    "section1"  : "Nyheter"
  }
  
  def __init__(self, interested=-1):
    """Constructor of the Wiki enquiry
    @param titles titles to be searched
    """
    ## titles to be searched
    self.interested = interested
    ## XML raw results
    self.raw_results = None
    ## Printable results
    self.results = None


  def get_results(self):
    """Get a formatted results
    """
    self.get_content()
    self.format_results()    
    return self.results

  def get_content(self):
    """Get the content of the wiki enquiry
    """
    formatted_url = common.format_url(self.SvDAPI, self.SvDAPI_FLAGS, "&%d" % random.randint(1, 9999999));
    self.raw_results = requests.get(formatted_url)
    return

  def format_results(self):
    """Extract the results from a wiki XML content
    """  
    results = self.raw_results.json()["SvDSearch"]["results"]["articles"][0:20]
    output = "\n" 
    if self.interested == -1:
      i = 0
      for article in results:
        output = output + "%-4d" %i + '%-13s' % article["friendlyDateShort"] + article["title"] + "\n"
        i = i + 1
    else:
      output = output + '<b>%-15s' % results[self.interested]["friendlyDateShort"] + results[self.interested]["title"] + "</b>\n"
      output = output + '<code>' + results[self.interested]["description"] + "</code>\n"
      fulltext = requests.get(results[self.interested]["url"])
      soup = BeautifulSoup(fulltext.text)
      [s.extract() for s in soup('script')]
      all_div = soup.findAll("div","articletext")
      if len(all_div) > 0:
        output = output + all_div[0].get_text().replace("\n\n", "\n")
        
      output = output + "<tt>Source: " + results[self.interested]["url"]  + "</tt>\n"
    self.results = common.format_color(output)
    return

def main():
  if len(sys.argv) < 2:
    svd = SvD(-1)
  else:
    svd = SvD(int(sys.argv[1]))
  print svd.get_results()

if __name__ == "__main__":
  main()
