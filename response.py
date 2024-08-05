import responses, os, datatypes

def normalizePaths(path: str) -> str:
  return path.removesuffix("/").removeprefix("/")

unauthorized_files = ["jsondata.py", "responses.py", "response.py", "server.py", "assets/template.html"]
def respond(handler) -> datatypes.httpReturn:
  paths = responses.paths
  path: list = normalizePaths(handler.url.path).split("/")
  for segment in path: 
    if segment in paths:
      paths = paths[segment]
      if isinstance(paths, dict):
        if segment == path[len(path)-1] and "root" in paths:
          paths = paths["root"]
  if callable(paths):
    return paths(handler)
  path = normalizePaths(handler.url.path)
  if os.path.exists("/home/songmanager/"+path) and not (".." in path):
    if not path in unauthorized_files:
      return responses.get_file(handler)
    else:
      return responses.error(handler, 403)
  else:
    return responses.error(handler, 404)