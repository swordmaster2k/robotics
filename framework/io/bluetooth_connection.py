import socket

from .connection import Connection


class BluetoothConnection(Connection):
    """
    Wrapper class for the Python3.3 bluetooth socket implementation, it
    communicates with the bluetooth device using input and output files.
    """

    def __init__(self, addr, port):
        """
        Creates a new BluetoothConnection to the bluetooth address on the
        specified port.

        :param addr:
        :param port:
        :return:
        """
        self.addr = addr
        self.port = port

        self.sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.sock.connect((self.addr, self.port))

        Connection.__init__(self, self.sock.makefile('r'), self.sock.makefile('w'), self.sock)

    def close(self):
        """
        Closes the socket connection and any open files.
        :return:
        """
        self.infile.close()
        self.outfile.close()
        self.sock.close()
        self.closed = True