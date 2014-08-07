import xml.etree.ElementTree as ET
  
def get_contents(xml, element):
  """Extract all matching element from a XML content
  @param xml text in XML format to get content from
  @param element element to be searched
  """  
  contents = []
  root = ET.fromstring(xml.encode('utf-8'))
  for item in root.iter(element):
    contents.append(item)
  return contents
  
def get_contents_text(xml, element, newline=True):

  """Extract the results in text from a XML content
  @param xml text in XML format to get content from
  @param element element to be searched
  """  
  result = ""
  contents = get_contents(xml, element)
  for content in contents:
    result = result + "\n" * newline + content.text + " "
  return result
