Introduction into SCPI Protocol
*******************************

The Standard Commands for Programmable Instruments (SCPI, pronounced “skippy”) is the de-facto standard language for
remotely controlling programmable test and measurement instruments such as oscilloscopes,
function generators, power supplies, digital multimeters, spectrum analyzers, and more.

This ``balderhub-scpi`` package is used for controlling these kind of devices:


+-----------------------+----------------------------------------------------------------------------------------------+
| Device Type           | BalderHub project                                                                            |
+=======================+==============================================================================================+
| Oscilloscopes         | `balderhub-waveformmonitor <https://hub.balder.dev/projects/waveformmonitor>`_               |
+-----------------------+----------------------------------------------------------------------------------------------+
| Function Generators   | `balderhub-waveformgenerator <https://hub.balder.dev/projects/waveformgenerator>`_           |
+-----------------------+----------------------------------------------------------------------------------------------+
| Power Supplies        | `balderhub-powersupply <https://hub.balder.dev/projects/powersupply>`_                       |
+-----------------------+----------------------------------------------------------------------------------------------+
| Digital Multimeters   | COMMING SOON                                                                                 |
+-----------------------+----------------------------------------------------------------------------------------------+


Defined in 1990 by the SCPI Consortium (now part of the IVI Foundation) as a consistent layer on top of IEEE 488.2,
SCPI solves the long-standing problem of vendor-specific command sets. Instead of learning a new command syntax for
every manufacturer, you can use the same commands for the same functionality across instruments from Keysight,
Rohde & Schwarz, Tektronix, Rigol, and others.

Core Functionality
==================

* **ASCII text-based**: Commands and responses are human-readable strings (e.g. ``*IDN?``, ``:MEASure:VOLTage:DC?``).
* **Hierarchical / tree structure**: Commands are organized into subsystems separated by colons (``:``). Example:
  ``:CONFigure:VOLTage:DC 10,0.001`` or ``:MEASure:VOLTage:DC?``
* **Set vs. Query**: The same base command can set a value or retrieve one by appending ``?``.
* **Short and long forms**: ``:MEAS:VOLT:DC?`` and ``:MEASURE:VOLTAGE:DC?`` are equivalent (case-insensitive).
* **Transport-independent**: Works over GPIB (IEEE 488.1), USB-TMC, Ethernet (VXI-11, HiSLIP, raw TCP), RS-232/422/485,
  etc.
* **IEEE 488.2 common commands**: Mandatory “star” commands such as ``*IDN?`` (identify), ``*RST`` (reset),
  ``*CLS`` (clear status), ``*OPC?`` (operation complete), etc.
* **Instrument classes**: Standardized command sets for device categories (e.g. all DC power supplies implement the
  same DCPSUPPLY base commands).

SCPI follows the principle of “forgiving listening, precise talking”: instruments accept flexible input formats but
always return data in a well-defined, consistent format. This makes it ideal for automated test equipment (ATE), lab
automation scripts, and any project that needs reliable, cross-vendor instrument control.
