import time
from typing import Union
import socket
import select


# TODO improve!!!
class BaseSocketConnector:
    """
    This class provides a manager class for connecting and interacting with a remove socket. It can be used for sync
    communication with the remote device.
    """

    def __init__(self, ip_address: str, port=5025, receive_buffer_size=4096, timeout: float = 30):
        """
        :param ip_address: the ip address of the remote device
        :param port: the port of the remote device
        :param receive_buffer_size: the receive-buffer-size to use as a receive-buffer
        :param timeout: the timeout to set for the global
        """
        self._ip = ip_address
        self._port = port
        self._socket: Union[socket.socket, None] = None
        self._receive_buffer_size = receive_buffer_size
        self._receive_timeout = timeout

    @property
    def termination_char(self) -> bytes:
        """
        :return: specifies the expected termination character
        """
        return b'\n'

    def connect(self):
        """
        Connects the socket to the remote device
        """
        if self._socket is not None:
            raise ValueError('socket was already created')
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._ip, self._port))
        self._socket.setblocking(False)

    def send_query(self, cmd: bytes, no_response=False) -> Union[bytes, None]:
        """
        Sends a command to the remote device. If ``no_response`` is True, the method will not wait for a response,
        otherwise the method will wait up to the global defined timeout for a response.

        The method raises an TimeoutError if it does not receive a response within the global defined timeout.

        :param cmd: the command to sent
        :param no_response: True, if the caller expects a response for the command, False otherwise
        :return: the response or None
        """
        self._socket.sendall(cmd)
        if no_response:
            return None

        response = self.read_all_from_socket(timeout=self._receive_timeout)
        if response is None:
            raise TimeoutError(f'did not receive a response for sending command `{cmd}` within {self._receive_timeout} '
                               f'seconds')
        return response

    def read_all_from_socket(self, timeout: float, max_wait_for_followup_msg_time: float=0.5) -> Union[bytes, None]:
        """
        Receives data from a socket until no further data is available for more than ``max_wait_for_followup_msg_time``
        seconds and the termination char is received.

        This implementation is used, because most of the devices terminate their response with ``\\n``, but they
        can also send ``\\n`` characters within their data. When waiting for up to ``max_wait_for_followup_msg_time``
        seconds, this will increase the certainty that the received char is really the response termination char.

        :param timeout: timeout in seconds
        :param max_wait_for_followup_msg_time: max wait time for follow-up messages
        :return: The received message as bytes (including the termination character) or None on timeout
        """
        # TODO improve
        buffer = b''
        start_time = time.perf_counter()
        while (time.perf_counter() - start_time) < timeout:
            # Wait for readable data using select
            readable, _, _ = select.select([self._socket], [], [], max_wait_for_followup_msg_time)

            if not readable:
                if buffer != b'' and buffer[-1] == self.termination_char:
                    return buffer
                continue

            data = self._socket.recv(self._receive_buffer_size)
            if not data:
                raise ConnectionError('connection was closed by remote')

            buffer += data

        return None

    def disconnect(self):
        """
        :return: disconnects the socket connection
        """
        self._socket.close()
        self._socket = None
