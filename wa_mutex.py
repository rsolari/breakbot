import threading
import time
from wa_bot import WAInterface

class WAMutexInterface(threading.Thread):
    def __init__(self, users, master_msg_handler, master_stopped_handler, worker_msg_handler, worker_stopped_handler):
        self.users = users
        self.wa_workers = []
        self.wa_master = None
        for user in users:
            if self.wa_master == None:
                self.wa_master = WAInterface(user["phone"], user["password"], master_msg_handler, master_stopped_handler)
                self.wa_workers.append(self.wa_master)
            else:
                wa_worker = WAInterface(user["phone"], user["password"], worker_msg_handler, worker_stopped_handler)
                self.wa_workers.append(wa_worker)

    def start(self):
        for worker in self.wa_workers:
            worker.start()

    def stop(self):
        for worker in self.wa_workers:
            worker.stop()

    def wait_connected(self):
        for worker in self.wa_workers:
            worker.wait_connected()

    def send(self, target, message):
        self.wa_workers[self.get_index()].send(target,message)

    PERIOD = 300 

    def get_index(self):
        epoch_seconds = int(time.time())
        i = epoch_seconds / PERIOD % len(self.wa_workers)
