import time
import threading
import random

class Philosophe(threading.Thread):
    def __init__(self, num, left_fork, right_fork):
        threading.Thread.__init__(self)
        self.num = num
        self.left_fork = left_fork
        self.right_fork = right_fork

    def run(self):
        for _ in range(3):
            self.think()
            self.starve()
            self.eat()

    def think(self):
        print(f"Le philosophe {self.num} pense.")
        time.sleep(random.randint(1, 5))

    def starve(self):
        print(f"Le philosophe {self.num} a faim.")
        self.left_fork.acquire()
        print(f"Le philosophe {self.num} a pris la fourchette gauche.")
        self.right_fork.acquire()
        print(f"Le philosophe {self.num} a pris la fourchette droite.")

    def eat(self):
        print(f"Le philosophe {self.num} commence à manger.")
        time.sleep(random.randint(1, 5))
        print(f"Le philosophe {self.num} a fini de manger.")
        self.left_fork.release()
        print(f"Le philosophe {self.num} a posé la fourchette gauche.")
        self.right_fork.release()
        print(f"Le philosophe {self.num} a posé la fourchette droite.")


if __name__ == "__main__":
    forks = [threading.Semaphore(1) for _ in range(3)]
    philosophes = [Philosophe(i + 1, forks[i], forks[(i + 1) % 3]) for i in range(3)]

    for philosophe in philosophes:
        philosophe.start()
