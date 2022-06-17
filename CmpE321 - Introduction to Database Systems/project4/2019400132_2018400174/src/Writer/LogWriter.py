import time

class LogWriter:

    def __init__(self, file_name):
        """Opens a log file in append mode.
        """
        self.file = open(file_name, "a")

    def write(self, command, success):
        """Saves the command to the log file.

        Args:
            - command (str): Command which was run
            - success (bool): Whether the operation was succesful
        """
        self.file.write("%d,%s,%s\n" % (int(time.time()), command, "success" if success else "failure"))

    def close(self):
        self.file.close()