class htmlelement:
  def __init__(self, tag, **attributes):
    self.containedelements = []
    self.attributes = attributes
    self.tag = tag
  def contain(self, item: 'htmlelement | str', condition: bool = True):
    if condition:
      self.containedelements.append(item)
    return self
  def link(self, src):
    linkedElement = htmlelement("a", href=src).contain(self)
    return linkedElement
  def inside(self, element: 'htmlelement', actually: bool = True):
    if actually:
      return element.contain(self)
    else:
      return element
  def render(self):
    attrs = ""
    for attribute, value in self.attributes.items():
      attrs += (f" {attribute}='{value}'" if attribute != "c" else f" class='{value}'")
    rendervar = f"<{self.tag}{attrs}>"
    for element in self.containedelements:
      if isinstance(element, htmlelement):
        rendervar += element.render()
      else:
        rendervar += element
    return f"{rendervar}</{self.tag}>"
    
class htmldoc:
  def __init__(self, *elements: htmlelement | str) -> None:
    self.elements = []
    for element in elements:
      self.elements.append(element)
  def __add__(self, htmlelement: htmlelement | str):
    self.elements.append(htmlelement)
    return self
  def render(self):
    render = ""
    for element in self.elements:
      if isinstance(element, htmlelement):
        render += element.render()
      else:
        render+= element
    return render
        
class headers:
  def __init__(self, headers):
    self.headers: list[tuple[str, str]] = headers
  def items(self):
    return self.headers
  def add_header(self, header: tuple[str, str]) -> None:
    self.headers.append(header)      

class httpReturn:
  def __init__(self, response: str, headers: list[tuple[str, str]], status: int) -> None:
    self.response = response
    self.headers = headers
    self.status = status