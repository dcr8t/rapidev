import os, subprocess, time,json,sys
from datetime import datetime
from blessed import Terminal
style = Terminal()
os.system("clear")
RED = style.bold_red
GREEN = style.bold_green
BLUE = style.bold_blue
YELLOW = style.bold_yellow
CLEARLINE = style.clear_eol
counter = 0
spin = ["|","/","-","\\"]

def update_counter():
  global counter
  if counter >= 3:
    counter = 0
  else:
    counter += 1

def run(command,show=False,codespace=False):
  now = datetime.now().strftime("___%H:%M:%S   %d/%m/%Y")
  try:
    process = subprocess.run(command,capture_output=True, text=True)
    result = process.stdout
    error = process.stderr
    run_status = {"code": process.returncode, "output": result}
    if show:
      if codespace:
        print(result,now,end="\r",sep="",flush=True)
        
        print(style.move_up + CLEARLINE,end="")
      else:
        print(result)
    return run_status
  except Exception as e:
    print(RED("FAILED EXECUTION"))
    print(str(e))
    if command[0].split():
      print(YELLOW("...have you installed"),GREEN(command[0]),"??")
    sys.exit()

def wait(n=2):
  time.sleep(n)

def scan_for_changes():
  print(CLEARLINE,GREEN(f"{spin[counter]} SCANNING FOR CHANGES {spin[counter]}"),end="\r")
  update_counter()
  command = ["git","status","--porcelain"]
  scan_result = run(command).get("output").split()
  return scan_result

def push():
  print(CLEARLINE,GREEN(f"{spin[counter]} PUSHING TO GITHUB {spin[counter]}"), end="\r")
  update_counter()
  tries = 0
  while True:
    commit_msg = json.loads(run(["termux-dialog","-t","'COMMIT MESSAGE'"])).get("text")
    is_commit = commit_msg.split()
    if is_commit:
      cmd1 = ["git","add","."]
      cmd2 = ["git","commit","-m",commit_msg]
      cmd3 = ["git","push","-u","origin","main"]
      cmd_sequence = [cmd1,cmd2,cmd3]
      for cmd in cmd_sequence:
        run(cmd)
      return True
    tries += 20
    wait(tries)

def keep_pulling():
  cmd = ["git","pull"]
  fix_cmd = ["git","restore",".","&&","git","clean","-fd"]
  while True:
    pull = run(cmd,show=True,codespace=True)
    if pull.get("code") != 0:
      print("[!]",RED("ERROR PULLING!"))
      print("[?]",YELLOW("Caused by untracked or uncommited files in Working directory..."))
      print("[*]",GREEN("FIXING"))
      run(fix_cmd)
      print("[✔]",GREEN("FIXED!"))
      
    
    wait()
    
def check_environment():
  environment = os.path.abspath(os.getcwd())
  if "workspace" in environment:
    return True
  else:
    return False

def animation(status):
  print(style.center(BLUE("RAPi") + YELLOW("DEV")))
  print(style.center(GREEN(status)))
  print(style.center("=" * style.width))
  print()
  
  

def main():
  is_codespace = check_environment()
  if is_codespace:
    animation("CODESPACE")
    keep_pulling()
  else:
    animation("LOCAL")    
    while True:
      is_changed = scan_for_changes()
      if is_changed:
        push()
      else:
        wait()

try:
  with style.hidden_cursor():
    main()

except:
  print("\r",CLEARLINE,BLUE("BYE! HAVE A GREAT DAY"))
  print("\033[?25h")