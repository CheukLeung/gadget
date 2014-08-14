# -*- coding: utf-8 -*-
import common
import util
import sys
import os

class Wiki(object):
  """A class of Wiki enquiry
  """
  WIKIAPI_FLAGS = {
    "action"          : "query",
    "redirects"       : "true",
    "prop"            : "extracts",
    "exintro"         : "true",
    "exsectionformat" : "plain",
    "exvariant"       : "zh-hk",
    "format"          : "xml"
  }

  def __init__(self, lang, titles):
    """Constructor of the Wiki enquiry
    @param titles titles to be searched
    """
    self.WIKIURL = "http://%s.wikipedia.org/wiki/" % lang
    self.WIKIAPI = "http://%s.wikipedia.org/w/api.php" % lang
    self.lang = lang
    ## titles to be searched
    self.titles = titles
    ## keywords
    self.keywords = None
    ## URL visit
    self.url = None
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
    formatted_titles = common.format_texts(self.titles)
    self.url = self.WIKIURL + formatted_titles
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
    if self.lang != "zh":
      results = results + "\n<tt>Source: " + self.url + "</tt>\n"
    self.results = common.format_color(results).encode('utf-8')
    return
    
def main():
  sys.argv.pop(0)
  lang = sys.argv.pop(0)
  wiki = Wiki(lang, sys.argv)
  print wiki.get_results()

if __name__ == "__main__":
  main()
