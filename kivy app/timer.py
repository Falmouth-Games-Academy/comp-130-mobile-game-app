import time

"""Use timer in main.py add time bonus to score"""
class timerApp:
    def __init__(self, runtime):
        while runtime > 0:
            time.sleep(1)
            #print runtime
            runtime -= 1


if __name__ == '__main__':
    timerApp(10)
