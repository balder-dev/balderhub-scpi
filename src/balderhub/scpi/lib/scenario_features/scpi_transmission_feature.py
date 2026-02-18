import balder


class ScpiTransmissionFeature(balder.Feature):
    """
    Base feature that is used to transmit SCPI commands.
    """
    ENCODING = 'ascii'

    class NoResponseError(Exception):
        """exception when no response is sent, but a response was expected."""

    class ConnectionError(Exception):
        """exception for everything regarding the connection"""

    def connect(self, *args, **kwargs):
        """
        Connects a SCPI compatible device.

        The method raises an :class:`ScpiTransmissionFeature.ConnectionError` if the connection fails.
        """
        raise NotImplementedError

    def disconnect(self, *args, **kwargs):
        """
        Disconnects the previously connected SCPI device.
        """
        raise NotImplementedError

    def query_values(self, command: bytes, *args, **kwargs) -> bytes:
        """
        Queries the SCPI command and returns the results of the SCPI command.

        The method raises an :class:`ScpiTransmissionFeature.NoResponseError` when the device does not respond.

        :param command: the bytes that should be transmitted
        :return: the response of the SCPI command
        """
        raise NotImplementedError

    def write_values(self, command: bytes, *args, **kwargs) -> None:
        """
        Transmits a SCPI command.

        :param command: the command to transmit
        """
        raise NotImplementedError
