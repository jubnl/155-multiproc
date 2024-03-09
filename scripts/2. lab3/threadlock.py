import threading
import time


# classe compteur de thread
class CompteurThread:
    def __init__(self):
        self.i = 0
        self.lock = threading.Lock()

    # boucle infine qui augmente la valeure de i
    def compter(self, numT):
        while True:
            with self.lock:
                self.i += 1
                print(f"Le thread numéro {numT} a incrémenté le compteur i à {self.i}")
                time.sleep(1)
                print(f"Le thread numéro {numT} a attendu et le compteur i est à {self.i}")


# objet compteur de thread
ct = CompteurThread()

for _ in range(5):
    t = threading.Thread(target=ct.compter, args=[_])
    t.start()
