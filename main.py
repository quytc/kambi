import os
import time
import Queue
import signal
import logging
import threading
from flask import Flask, jsonify
from threading import Thread
from tasks import threaded_task, blocker
from signal import signal, SIGINT
from sys import exit

app = Flask(__name__)

class ServiceExit(Exception): pass

def shutdown(signal_received, frame):
  print(' CTRL-C detected')
  raise ServiceExit

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def error_handler(msg, code):
  logging.error(msg)
  return jsonify(msg), code

@app.errorhandler(404)
def resource_not_found(e):
  return error_handler('error: page not found', 404)


@app.route("/", defaults={'request_type': "list_file", 'dir_name': '', 'file_type': 'ls'})
@app.route("/<string:request_type>/", defaults={'dir_name': '','file_type': 'ls'})
@app.route("/<string:request_type>/<string:dir_name>/", defaults={'file_type': 'ls'})
@app.route("/<string:request_type>/<string:dir_name>/<string:file_type>")



def main(request_type, dir_name, file_type):
  # the queue que is to store return value of threads
  que = Queue.Queue()
  if request_type == 'list_files':

    dir_path = os.path.join(os.getcwd(), dir_name)

    # if the directory does not exist
    if not os.path.exists(dir_path):
      return error_handler('error: Folder does not exits', 400)

    # if the directory is not readable
    if not os.access(dir_path, os.R_OK):
      return error_handler('error: Folder can not be read', 401)

    # declare filter including path to directory and file type to pass to thread method
    filter = (dir_path,file_type)
    thread = Thread(target=lambda q, arg: q.put(threaded_task(arg,lock)), args=(que, filter))

  else:

    if request_type == 'blocking':
      thread = Thread(target=lambda q, arg: q.put(blocker(arg)), args=(que,lock))
    else:
      return error_handler('error: Request is not implemented', 500)

  # start the thread and add it the the list of thread
  thread.start()
  threads.append(thread)

  return jsonify(que.get())

if __name__ == "__main__":
  # declare a list of thread
  threads = []

  # Define a global lock
  lock = threading.Lock()

  # Declare a exit signal
  signal(SIGINT, shutdown)

  try:
    app.run(debug = True)
  except ServiceExit:
    # wait for outstanding threads to finish
    for t in threads:
      t.join()
    # exit the program
    exit(0)

  print("Program Exit")



