import common
import util
import sys
import os

class Wiki(object):
  """A class of Wiki enquiry
  """
  WIKIAPI       = "http://en.wikipedia.org/w/api.php"
  WIKIAPI_FLAGS = {
    "action"          : "query",
    "redirects"       : "true",
    "prop"            : "extracts",
    "exintro"         : "true",
    "exsectionformat" : "plain",
    "format"          : "xml"
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
    @cond
    >>> wiki = Wiki("HelloWorld")
    >>> wiki.format_keywords
    >>> wiki.keywords
    titles=HelloWorld
    @endcond
    """
    formatted_titles = common.format_texts(self.titles);
    self.keywords = "titles=" + formatted_titles
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
    results = util.get_contents_text(self.raw_results, 'extract')
    self.results = common.format_color(results);
    return

def main():
    sys.argv.pop(0)
    wiki = Wiki(sys.argv)
    print wiki.get_results()

if __name__ == "__main__":
    main()
