#!/usr/bin/env python
import os, subprocess, time,json,sys
from threading import Thread
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

def port_forward():
  try:
    port = sys.argv[1]
    #default
    if port == "d":
      port = 5173

  except:
    return
  cmd = ["portward",f"{port}"]
  run(cmd, codespace=True)
    

def update_counter():
  global counter
  if counter >= 3:
    counter = 0
  else:
    counter += 1

def start_in_clipboard():
  cmd = ["termux-clipboard-get"]
  reset_cmd = ["termux-clipboard-set",""]
  result = run(cmd).get("output")
  if "start" and ":" in result:
    run(reset_cmd)
    return True
  else:
    return False

def toast(text: str):
  cmd = ["termux-toast","-g","top","-c","yellow","-b","#FF121214",text]
  run(cmd)
  wait()

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
  timer = 0
  while True:
    commit_msg = json.loads(run(["termux-dialog","-t","'COMMIT MESSAGE'", "-i","'TYPE 👉stop: TO PAUSE'"]).get("output")).get("text")
    if "stop" and ":" in commit_msg:
      toast("COPY 👉start: TO CLIPBOARD TO START RAPIDEV")
      while True:
        wait()
        start = start_in_clipboard()
        if start:
          #reset
          commit_msg = ""
          timer = timer - timer - 19
          break
      
    is_commit = commit_msg.split()
    if is_commit:
      cmd1 = ["git","add","."]
      cmd2 = ["git","commit","-m",commit_msg]
      cmd3 = ["git","push","-u","origin","main","-f"]
      reset_cmd = ["git", "reset", "--soft", "HEAD^"
]
      cmd_sequence = [cmd1,cmd2,cmd3]
      for cmd in cmd_sequence:
        result = run(cmd)
        status_code = result.get("code")
        if status_code != 0:
          toast("😟:PUSH FAILED! Check your Internet Connection and Try Again...")
          toast(result.get("output"))
          if cmd == cmd_sequence[2]:
            run(reset_cmd)
          return False
        else:
          toast(result.get("output"))
      return True
    timer += 20
    if timer > 300:
      timer = 300
    #checking for start while waiting
    for i in range(timer):
      is_start = start_in_clipboard()
      if is_start:
        break
      wait()

def keep_pulling():
  cmd = ["git","pull"]
  fix_cmds = [["git","restore","."],["git","clean","-fd"]]
  while True:
    pull = run(cmd,show=True, codespace=True)
    status_code = pull.get("code")
    if status_code != 0:
      print("[!]",RED("ERROR PULLING!"),"Code:",status_code)
      print("[?]",YELLOW("Caused by untracked or uncommited files in Working directory..."))
      print("[*]",GREEN("FIXING"))
      for fix_cmd in fix_cmds:
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
    server = Thread(target=port_forward)
    server.start()
    keep_pulling()
  else:
    animation("LOCAL")    
    while True:
      is_changed = scan_for_changes()
      if is_changed:
        while True:
          pushed = push()
          if pushed:
            break
      else:
        wait()

try:
  with style.hidden_cursor():
    main()

except KeyboardInterrupt:
  print("\r",CLEARLINE,BLUE("BYE! HAVE A GREAT DAY"))
  print("\033[?25h")
  sys.exit()