Examples
********

Every SCPI compliant device, that should be controlled over SCPI needs to have a implementation of the
:class:`balderhub.scpi.lib.scenario_features.ScpiTransmissionFeature`.


For example, you can use the ready-to use setup implementation for raw socket communication with a compatible device.
For that, just overwrite the setup feature :class:`balderhub.scpi.lib.setup_features.SocketScpiFeature` and define your IP:

.. code-block:: python

    from balderhub.scpi.lib.setup_features import SocketScpiFeature


    class SiglentAwgSdg2042X(SocketScpiFeature):

        @property
        def ip_address(self) -> str:
            return '192.168.0.81'


.. note::
    Currently we do not have any ready to use features for NI-VISA or VISA. We always welcome contributions!
