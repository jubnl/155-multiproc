from random import randint
from threading import Thread, Semaphore
from time import sleep
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


class Philosopher(Thread):
    def __init__(self, num: int, left_fork: Semaphore, right_fork: Semaphore, runs_amount: int = 3):
        # init Thread super class
        super().__init__()

        assert num > 0, "Philosopher number must be a positive integer"
        assert runs_amount >= 0, "Runs amount must be a non-negative integer"

        self.num = num
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.runs_amount = runs_amount

    # override run method in Thread class
    def run(self):
        if self.runs_amount > 0:
            for _ in range(self.runs_amount):
                self.think()
                self.starve()
                self.eat()
        else:
            while True:
                self.think()
                self.starve()
                self.eat()
            

    def think(self):
        logging.info(f"Le philosophe {self.num} pense.")
        sleep(randint(1, 5))

    def starve(self):
        logging.info(f"Le philosophe {self.num} a faim.")
        self.left_fork.acquire()
        logging.info(f"Le philosophe {self.num} a pris la fourchette gauche.")
        self.right_fork.acquire()
        logging.info(f"Le philosophe {self.num} a pris la fourchette droite.")

    def eat(self):
        logging.info(f"Le philosophe {self.num} commence à manger.")
        sleep(randint(1, 5))
        logging.info(f"Le philosophe {self.num} a fini de manger.")
        self.left_fork.release()
        logging.info(f"Le philosophe {self.num} a posé la fourchette gauche.")
        self.right_fork.release()
        logging.info(f"Le philosophe {self.num} a posé la fourchette droite.")


if __name__ == "__main__":
    philosopher_amount = 3
    range_x = range(philosopher_amount)

    forks = [Semaphore(1) for _ in range_x]

    # (i + 1) % x -> next available fork
    philosophers = [
        Philosopher(i + 1, forks[i], forks[(i + 1) % philosopher_amount])
        # Philosopher(i + 1, forks[i], forks[(i + 1) % philosopher_amount], runs_amount=0)
        for i in range_x
    ]

    # start threads
    for philosopher in philosophers:
        philosopher.start()

    # wait for all threads to finish
    for philosopher in philosophers:
        philosopher.join()
