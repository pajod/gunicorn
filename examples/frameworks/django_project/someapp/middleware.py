import os
import time
from multiprocessing import Process, Queue


def child_process(queue):
    # import requests
    while True:
        print(*queue.get())
        # requests.get('https://requestb.invalid/15s95oz1')


class GunicornSubProcessTestMiddleware:
    def __init__(self, get_response):
        super().__init__()
        self.get_response = get_response
        self.queue = Queue()
        self.process = Process(target=child_process, args=(self.queue,))
        self.process.start()

    def __call__(self, request):
        self.queue.put(("REQUEST",))
        response = self.get_response(request)
        self.queue.put(("RESPONSE", response.status_code))
        return response
