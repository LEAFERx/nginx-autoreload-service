#!/usr/bin/python3

import os
import re
import pyinotify
import logging
from threading import Timer

# Param
LOG_PATH = "/path/to/service/log"
CONF_PATHS = [
  "/path/to/conf",
]
DELAY = 5
SUDO = False
RELOAD_COMMAND = "nginx -s reload"
if SUDO:
  RELOAD_COMMAND = "sudo " + RELOAD_COMMAND

# Log
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
log_handler = logging.FileHandler(LOG_PATH)
log_handler.setLevel(logging.INFO)
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)

# Reloader
def reload_nginx():
  os.system(RELOAD_COMMAND)
  logger.info("nginx is reloaded")

t = Timer(DELAY, reload_nginx)

def trigger_reload_nginx(pathname, action):
  logger.info("nginx monitor is triggered because %s is %s" % (pathname, action))
  global t
  if t.is_alive():
    t.cancel()
    t = Timer(DELAY, reload_nginx)
    t.start()
  else:
    t = Timer(DELAY, reload_nginx)
    t.start()

events = pyinotify.IN_MODIFY | pyinotify.IN_CREATE | pyinotify.IN_DELETE

watcher = pyinotify.WatchManager()
watcher.add_watch(CONF_PATHS, events, rec=True, auto_add=True)

class EventHandler(pyinotify.ProcessEvent):
  def process_default(self, event):
    if event.name.endswith(".conf"):
      if event.mask == pyinotify.IN_CREATE:
        action = "created"
      if event.mask == pyinotify.IN_MODIFY:
        action = "modified"
      if event.mask == pyinotify.IN_DELETE:
        action = "deleted"
      trigger_reload_nginx(event.pathname, action)
 
handler = EventHandler()
notifier = pyinotify.Notifier(watcher, handler)

# Start
logger.info("Start Monitoring")
notifier.loop()