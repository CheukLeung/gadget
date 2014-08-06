import xml.etree.ElementTree as ET

def get_contents(xml, element):
  """Extract all matching element from a wiki XML content
  @param xml text in XML format to get content from
  @param element element to be searched
  """  
  contents = []
  root = ET.fromstring(xml.encode('utf-8'))
  for item in root.iter(element):
    contents.append(item.text)
  return contents
  
def get_contents_text(xml, element):

  """Extract the results in text from a XML content
  @param xml text in XML format to get content from
  @param element element to be searched
  """  
  result = ""
  contents = get_contents(xml, element)
  for content in contents:
    result = result + "\n" + content
  return result
