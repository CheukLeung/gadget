import common
import util
import sys
import os

class Translate(object):
  """A class of Translate enquiry
  """
  TRANSLATEAPI        = "https://query.yahooapis.com/v1/public/yql"
  TRANSLATEAPI_FLAGS  = {
    "diagnostics"   : "true",
    "env"           : "store%3A%2F%2Fdatatables.org%2Falltableswithkeys",
  }

  def __init__(self, language, sentences):
    """Constructor of the Wiki enquiry
    @param sentences sentences to be searched
    """
    ## sentences to be searched
    self.sentences = sentences
    ## language to translate to
    self.language = language
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
    formatted_sentences = common.format_texts(self.sentences);
    self.keywords = "q=select%20*%20from%20google.translate%20where%20q%3D%22" 
    self.keywords = self.keywords + formatted_sentences 
    self.keywords = self.keywords + "%22%20and%20target%3D%22"
    self.keywords = self.keywords + self.language
    self.keywords = self.keywords + "%22%3B"
    return

  def get_content(self):
    """Get the content of the translate enquiry
    """
    formatted_url = common.format_url(self.TRANSLATEAPI, self.TRANSLATEAPI_FLAGS, self.keywords);
    self.raw_results = common.get_url_content(formatted_url)
    return
    
  def format_results(self):
    """Extract the results from a wiki XML content
    """  
    results = util.get_contents_text(self.raw_results, 'trans')
    self.results = common.format_color(results);
    return

def main():
    sys.argv.pop(0)
    lang = sys.argv.pop(0)
    translate = Translate(lang, sys.argv)
    print translate.get_results()

if __name__ == "__main__":
    main()
