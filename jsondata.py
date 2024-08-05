import os, sys, json
def debugcaller(function, input: any, debug: bool):
  if debug:
    function(input)

def list_recursive(folder: str, debug: bool = False) -> list[any]:
  dir = {}
  for element in range(len(list := os.listdir(folder))):
    try:
      debugcaller(print, "started element analyzation "+folder+list[element], debug)
    except:
      debugcaller(print, "started analyzing a non encodable element", debug)
    if os.path.isdir(folder+list[element]):
      dir[list[element]+"/"] = list_recursive(folder+list[element]+"/")
    else:
      dir[list[element]] = "audio" if os.path.splitext(list[element])[1] == ".mp3" else "who cares" #subprocess.getoutput('file -bi "'+folder+list[element]+'"')
  return dir

if __name__ == "__main__":
  try:
    debug = sys.argv[1] == "debug"
  except:
    debug = False
  dat = list_recursive("/jellyfin/music/", debug)
  print(json.dumps(dat))