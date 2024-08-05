import requests, json, jsondata, subprocess, re
from pathlib import Path
from datatypes import htmlelement, htmldoc, headers, httpReturn
from urllib.parse import unquote

def search(handler):
  response = htmldoc(Path("/home/songmanager/assets/template.html").read_text())
  searchbar = htmlelement("div", c="searchbar").contain(htmlelement("input", id="query", type="text")).contain(htmlelement("button", onclick="validate(13)").contain("search"))
  try:
    data = requests.get(f'https://youtube.googleapis.com/youtube/v3/search?part=snippet&q={handler.query_data["search"]}&type=video&maxResults=10&key=(google api key)', headers=headers([("Accept", "application/json")])).text
    try:
      if handler.query_data["raw"] == "true":
        return httpReturn(data, [("Content-Type", "application/json")], 200)
    except:
      pass
    data = json.loads(data)
    for video in data["items"]:
      try:
        response += htmlelement("iframe", width="560", height="315", src=f"https://www.youtube.com/embed/{video["id"]["videoId"]}", title="YouTube video player", frameborder="0", allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share", referrerpolicy="strict-origin-when-cross-origin", allowfullscreen=None)
      except:
        response += htmlelement("b").contain("unable to load video")
    response.elements.insert(1, searchbar)
  except:
    response += htmlelement("div", style="text-align: center; width: 100%; margin: 0; position: absolute; top: 50%; -ms-transform: translateY(-50%); transform: translateY(-50%);").contain(searchbar).contain(htmlelement("b").contain("Please submit a search"))
  response += htmlelement("script", src="/assets/search.js")
  return httpReturn(response, [("Content-Type", "text/html")], 200) 

def getsongid(file: str):
  id = None
  for idcandidate in re.findall("([A-Za-z0-9-_]{11})", file):
    if f"(youtube, {idcandidate}).mp3" in file:
      id = idcandidate
  return id

libraries = {
  "music": "/jellyfin/music/",
  "31": "/jellyfin/31/",
  "extra music": "/jellyfin/extra music/"
}

def libs(handler):
  response = htmldoc()
  for library in libraries:
    response += htmlelement("a", href=f"/view?library={library}").contain(library).inside(htmlelement("div"))
  return httpReturn(response, [("Content-type", "text/html")], 200)
    

def data(handler, edit=False):
  try:
    if handler.query_data['library'] in libraries:
      library = libraries[handler.query_data["library"]]
    else:
      library = "/jellyfin/music/"
  except:
    library = "/jellyfin/music/"
  file_contents = jsondata.list_recursive(library)
  if handler.url.query == "raw":
    file_contents = json.dumps(file_contents)
    return httpReturn(file_contents, [("Content-Type", "application/json")], 200)
  response = htmldoc(Path("/home/songmanager/assets/jsontemplate.html").read_text())
  response += htmlelement("button", c="editbutton").contain("Edit").link("/edit" if library == "/jellyfin/music/" else f"/edit?library={handler.query_data["library"]}").inside(htmlelement("div", c="titlebar").contain(htmlelement("div", c="titlebartext", id="library").contain(library.split("/")[2])), not edit)
  for folder in sorted(file_contents.keys()):
    button = htmlelement("button", c="collapsible").contain(folder)
    buttoncount = 0
    content = htmlelement("div", c="content")
    for file in sorted(file_contents[folder].keys()):
      if file_contents[folder][file] == "audio":
        id = getsongid(file)
        content = content.contain(htmlelement("div", c="song", id=file.replace("'", "")).contain(htmlelement("image", src=f"https://i.ytimg.com/vi/{id}/hqdefault.jpg", height=160), id is not None).contain(htmlelement("image", src=f"https://i.ytimg.com/vi/Izj49FLY4JQ/hqdefault.jpg", height=160), id is None).contain(htmlelement("div", c="file").contain(file.replace(f" (youtube, {id}).mp3", "").split(" (soundcloud, ")[0])).contain("<br>"))
        buttoncount += 1
    response += button.contain(htmlelement("div", style="float: right;").contain(f" {buttoncount}"))
    response += content
  response += htmlelement("script", src="/assets/collapsible.js")
  response += htmlelement("script", src="/assets/contextmenu.js")
  return httpReturn(response, [("Content-Type", "text/html")], 200)

def error(handler, code: int):
  match code:
    case 403:
      return httpReturn(f"you are not authorized to access the file at /{handler.url.path.removesuffix("/").removeprefix("/")}", [("Content-Type", "text/html")], 403)
    case 404:
      return httpReturn("404 not found", [("Content-Type", "text/html")], 404)
    case _:
      return httpReturn(f"error {code}", [("Content-Type", "text/html")], code)
      
def giveheadersback(handler):
  response = ""
  for header in handler.headers.items():
    response += header[0]+", "+header[1]+"<br>"
  return httpReturn(response, [("Content-Type", "text/html")], 200)

def get_file(handler):
  file_mime = subprocess.getoutput('file -bi "/home/songmanager/'+(file := handler.url.path.removesuffix("/").removeprefix("/"))+'"').split(";")[0]  
  file_contents = Path("/home/songmanager/"+file).read_bytes()
  return httpReturn(file_contents, [("Content-Type", file_mime)], 200)

def get_file_direct(file):
  file_mime = subprocess.getoutput(f'file -bi {file}').split(";")[0]  
  file_contents = Path(file).read_bytes()
  return httpReturn(file_contents, [("Content-Type", file_mime)], 200)

def retrievesong(handler):
  try:
    if handler.query_data['library'] in libraries:
      library = libraries[handler.query_data["library"]]
    else:
      library = "/jellyfin/music/"
  except:
    library = "/jellyfin/music/"
  try:
    song = handler.query_data["song"]
  except:
    return httpReturn("please provide an album and a song", [("Content-Type", "text/html")], 400)
  for folder in (file_contents := jsondata.list_recursive(library)):
    for file in file_contents[folder]:
      if file.replace("'", "").encode("utf-8", "replace").decode() == (test := unquote(song)):
        print(f"we got here at {folder}/{file}")
        return httpReturn(Path(f"{library}{folder}/{file}").read_bytes(), [("Content-Type", "audio/mpeg")], 200)
  print(test)
  return get_file_direct("/home/songmanager/assets/sadtrombone.mp3")

paths = {
  "search": search,
  "view": data,
  "": libs,
  "headers": giveheadersback,
  "songs": {
    "get": retrievesong,
    "root": lambda handler : httpReturn(handler.url.query, [("content-type", "text/html")], 200),
  },
  "edit": lambda handler : data(handler, True)
}

