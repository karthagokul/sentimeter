
from multiprocessing import Process, BoundedSemaphore
from time import sleep

def do_work(A, B):
    sleep(.4)
    print(A, B)

def worker(sema, *args):
    try:
        do_work(*args)
    finally:
        sema.release() #allow a new process to be started now that this one is exiting

def main():
    tasks = zip(range(65,91), bytes(range(65,91)).decode())
    sema = BoundedSemaphore(4) #only every 4 workers at a time
    procs = []
    for arglist in tasks:
        sema.acquire() #wait to start until another process is finished
        procs.append(Process(target=worker, args=(sema, *arglist)))
        procs[-1].start()

        #cleanup completed processes
        while not procs[0].is_alive():
            procs.pop(0)
    for p in procs:
        p.join() #wait for any remaining tasks
    print("done")

if __name__ == "__main__":
    main()