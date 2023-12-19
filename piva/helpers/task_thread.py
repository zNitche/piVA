import threading


class TaskThread:
    def __init__(self):
        self.process = None
        self.is_running = False

    def main(self, task):
        try:
            task()
        except Exception as e:
            pass

        finally:
            self.is_running = False

    def run(self, task):
        self.process = threading.Thread(target=self.main, args=[task])

        self.is_running = True
        self.process.start()

    def stop(self):
        self.is_running = False
