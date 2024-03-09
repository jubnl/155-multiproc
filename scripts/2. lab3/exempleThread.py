import time
from random import randint
from threading import Thread


def carre(n, a):
    x = randint(0, 4)
    time.sleep(x)
    print(f"{a} Le carré: {n * n} avec un temps de {x}")


# création de thread
t1 = Thread(target=carre, args=(1, "t1"))
t2 = Thread(target=carre, args=(2, "t2"))
# démarrer le thread t1
t1.start()
# démarrer le thread t2
t2.start()
# # attendre que t1 soit exécuté
t1.join()
# # attendre que t2 soit exécuté
t2.join()
