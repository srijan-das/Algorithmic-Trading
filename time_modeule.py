import numpy as np
import time

def fibonacci(n) :
    if n<=1 :
        return n
    else :
        return (fibonacci(n-1) + fibonacci(n-2))

def main() :
    num = np.random.randint(1, 25)
    print("{}th fibonacci number is {}".format(num, fibonacci(num)))

starttime = time.time()
timeout = time.time() + 60*0.1

while time.time() <= timeout :
    try:
        main()
        time.sleep(1 - ((time.time() - starttime) % 1.0 ))
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received. Exiting..")
        exit()
