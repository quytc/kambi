import time
import os

def list_files(filter):
    dir_path = filter[0]
    file_type = filter[1]
    print(dir_path)
    files = os.listdir(dir_path)
    result = []
    # Iterate over all the entries
    for entry in files:
        path = os.path.join(dir_path, entry)
        if os.path.isfile(path):
            if file_type == "ls":
                result.append(entry)
            else:
                if entry.endswith(str(file_type)):
                    result.append(entry)
    return result


def threaded_task(filter,lock):
    print("begin")
    while True:
      if not lock.locked():
        files = list_files(filter)
        break
    print("end")
    return files

def blocker(lock):
    while True:
      lock.acquire()
      print("lock acquired")
      time.sleep(5.0)
      print("lock released")
      lock.release()
      break
    return
