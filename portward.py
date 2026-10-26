#!/usr/bin/env python
import os, sys
os.system("clear")
try:
  port = sys.argv[1]
except:
  port = 5173

start_cmd = f'gh cs ports forward {port}:{port} -c "$CODESPACE_NAME"&'

main_cmd = f'echo "[*]SETTING {port} VISIBILITY PUBLIC" && gh cs ports visibility {port}:public -c "$CODESPACE_NAME" && stty echo && echo "[:]RESTARTING TO HOST VITE" && npx kill-port {port} && npm run dev'
os.system(start_cmd)
os.system(main_cmd)