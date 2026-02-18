from ..scenario_features.scpi_transmission_feature import ScpiTransmissionFeature
from ..utils.base_socket_connector import BaseSocketConnector


class SocketScpiFeature(ScpiTransmissionFeature):
    """transmission feature that uses a native socket for sending SCPI commands"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._socket_connector = None
        self._receive_buffer_size = 4096

    @property
    def ip_address(self) -> str:
        """
        :return: returns the IP address of the device to connect to
        """
        raise NotImplementedError

    @property
    def port_number(self) -> int:
        """
        :return: returns the port number of the device to connect to
        """
        return 5025

    @property
    def receive_buffer_size(self) -> int:
        """
        :return: specifies the receive buffer the socket should use
        """
        return 4096

    @property
    def receive_timeout(self) -> float:
        """
        :return: specifies the receive-timeout the socket should use
        """
        return 30

    def connect(self, *args, **kwargs):
        if self._socket_connector is not None:
            raise ValueError('already connected')
        self._socket_connector = BaseSocketConnector(
            ip_address=self.ip_address,
            port=self.port_number,
            receive_buffer_size=self.receive_buffer_size,
            timeout=self.receive_timeout,
        )
        self._socket_connector.connect()

    def disconnect(self, *args, **kwargs):
        self._socket_connector.disconnect()
        self._socket_connector = None

    def query_values(self, command: bytes, *args, **kwargs) -> bytes:
        response = self._socket_connector.send_query(command + b'\n', no_response=False)
        if response is None:
            raise self.NoResponseError(f'does not receive any response for command `{command}`')
        return response

    def write_values(self, command: bytes, *args, **kwargs) -> bytes:
        return self._socket_connector.send_query(command + b'\n', no_response=True)
