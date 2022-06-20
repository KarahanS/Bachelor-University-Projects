
class InputLoader:
    """Used for loading an input file and
    creating an iterator for retriving the
    tokens in each line
    """
    def __init__(self, file_name):
        file = open(file_name, "r")
        self.lines = file.readlines()
        file.close()

    def line_iterator(self):
        """
        Creates an iterator for retrieving the
        tokens and the line for each line of the
        input file.

        Usage:
            for tokens, line in i.line_iterator():
                # do something with the list of tokens
                # and the line
                print(tokens, line)
        """
        for line in self.lines:
            tokens = list(filter(lambda s: len(s)>0, map(lambda s: s.strip(), line.split(" "))))
            if(tokens): yield tokens, line.replace("\n", "")
