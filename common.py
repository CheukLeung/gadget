import requests

def format_texts(texts):
  """Format texts and remove not supported characters
  @param texts text array to be formatted
  """
  formatted_text = texts.pop(0)
  for text in texts:
    formatted_text = formatted_text + "%20" + text
  return formatted_text

def format_url(api, flags, keywords):
  """Form an URL with the input
  @param api API main address
  @param flags flags hashmap to be included
  @param keywords formatted keyword sting
  """
  url = api + '?' + keywords
  for key, item in flags.items():
    url = url + '&' + key + '=' + item
  return url
  
def get_url_content(url):
  """Get content from an URL
  @param url URL to get content
  """
  r = requests.get(url)
  return r.text

def format_color(text):
  """Format the text to output with colors
  @text text to be formatted
  """
  text = text.replace("<b>", color.BOLD)
  text = text.replace("<i>", color.ITALIC)
  text = text.replace("<li>", color.ITALIC)
  text = text.replace("<p>", "")
  text = text.replace("<ol>", color.ITALIC)
  text = text.replace("<ul>", "")
  text = text.replace("</b>", color.END)
  text = text.replace("</i>", color.END)
  text = text.replace("</li>", color.END)
  text = text.replace("</ol>", color.END)
  text = text.replace("</p>", "")
  text = text.replace("</ul>", "")  
  return text
  
class color:
  """Class for color key
  """
  PURPLE = '\033[95m'
  CYAN = '\033[96m'
  DARKCYAN = '\033[36m'
  BLUE = '\033[94m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  RED = '\033[91m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'
  ITALIC = '\033[3m'
  END = '\033[0m'
