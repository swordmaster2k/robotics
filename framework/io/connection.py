"""
Super class that all connection types should inherit from defines and implements some of the
methods that a connection contains.
"""


class Connection():
    def __init__(self, infile, outfile, connection):
        self.infile = infile  # File opened with 'r' option.
        self.outfile = outfile  # File opened with 'w' option.

        self.connection = connection

        self.closed = self.infile.closed and self.outfile.closed

    def write(self, data):
        """
        Write data to the connection, assumes that the stream can be wrote to.
        :param data:
        :return:
        """
        if not self.outfile.closed:
            self.outfile.write(data)
            self.outfile.flush()

    def readline(self):
        """
        Read a line from the connection, assumes that the stream can be read from.
        :return:
        """
        if not self.infile.closed:
            return self.infile.readline()

    def close(self):
        """
        Base class will handle close because closing physical connection types vary.
        :return:
        """
        raise NotImplementedError