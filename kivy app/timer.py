import time

"""Use timer in main.py add time bonus to score"""
class TimerApp:
    def __init__(self, runtime):
        """ This functions runs a countdown for a given time
        :param runtime:
        :return:
        """
        while runtime > 0:
            time.sleep(1)
            #print runtime
            runtime -= 1


if __name__ == '__main__':
    timerApp(10)
