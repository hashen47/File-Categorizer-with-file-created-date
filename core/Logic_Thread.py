from threading import Thread
from .Logic import Categorizer



class Logic_Thread(Thread):
    def __init__(self, src, dst, update_func):
        super().__init__()
        self.src = src
        self.dst = dst
        self.update_func = update_func
        self.daemon = True


    def run(self):
        self.categorizer = Categorizer(self.src, self.dst, self.update_func)