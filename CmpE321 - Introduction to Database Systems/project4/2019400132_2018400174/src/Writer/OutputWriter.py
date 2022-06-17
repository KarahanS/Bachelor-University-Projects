
class OutputWriter:

    def __init__(self, file_name):
        self.file = open(file_name, "w")

    def __write(self, line):
        self.file.write(line + "\n")

    def close(self):
        self.file.close()

    """
    Helper methods
    """
    def __write_lines(self, lines):
        for line in lines:
            self.file.write(line + "\n")

    def write_types(self, types):
        self.__write_lines(types)

    def write_fields(self, fields):
        self.file.write(" ".join(str(f) for f in fields) + "\n")