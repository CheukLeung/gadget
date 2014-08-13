import common
import util
import sys
import os
import re

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
    self.keywords = []
    ## XML raw results
    self.raw_results = None
    ## Printable results
    self.results = None

  def get_results(self):
    """Get a formatted results
    """
    self.format_keywords()
    for keyword in self.keywords:
      self.get_content(keyword)
      self.format_results()   
      print self.results
    return

  def format_keywords(self):
    """Format the keywords
    """
    
    formatted_sentences = common.format_texts(self.sentences);
    formatted_sentences = self.remove_color(formatted_sentences);
    while len(formatted_sentences) > 1002:
      index = formatted_sentences.rfind("%2E", 0, 999)
      first_part = formatted_sentences[:index+3]
      formatted_sentences = formatted_sentences[index+3:]
    
      current_key = "q=select%20*%20from%20google.translate%20where%20q%3D%22" 
      current_key = current_key + first_part
      current_key = current_key + "%22%20and%20target%3D%22"
      current_key = current_key + self.language
      current_key = current_key + "%22%3B"
    
      self.keywords.append(current_key)
    
    current_key = "q=select%20*%20from%20google.translate%20where%20q%3D%22" 
    current_key = current_key + formatted_sentences
    current_key = current_key + "%22%20and%20target%3D%22"
    current_key = current_key + self.language
    current_key = current_key + "%22%3B"
  
    self.keywords.append(current_key)

    return
  
  def remove_color(self, sentences):
    formatted_sentences = re.sub(r"\033\[\d*m", "", sentences)
    return formatted_sentences 
  
  def get_content(self, keyword):
    """Get the content of the translate enquiry
    """
    formatted_url = common.format_url(self.TRANSLATEAPI, self.TRANSLATEAPI_FLAGS, keyword);

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
  translate.get_results()

if __name__ == "__main__":
  main()
