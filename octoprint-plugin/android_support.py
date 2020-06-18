# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import octoprint.util
import octoprint.logging

__plugin_pythoncompat__ = ">3,<4"
__plugin_name__ = "Octo4a Android support"
__plugin_version__ = "1.0.0"
__plugin_description__ = "Android support for OctoPrint"
from serial import SerialTimeoutException

class Octo4aSerial(octoprint.util.comm.MachineCom):
    def __init__(self, logger, baud):
        self.logger = logger
        self.timeout = 5
        self.logger.info(baud)
        self.logger.info("INIT")
        self.lastBaud = baud
        self.closed = False
        self.input = open('/data/data/io.feelfreelinux.octo4a/files/home/input', 'rb')
        self.output = open('/data/data/io.feelfreelinux.octo4a/files/home/output', 'wb')
        self.output.write(("!octo4a: BAUDRATE" + str(baud) + '\n').encode("utf-8"))

    def readline(self, size=None, eol='n'):
        if (hasattr(self, 'baudrate') and self.baudrate != self.lastBaud):
            self.lastBaud = self.baudrate
            self.output.write(("!octo4a: BAUDRATE" + str(self.lastBaud ) + '\n').encode("utf-8"))

        return self.input.readline(size)

    def write(self, data):
        self.output.write(data)
        self.output.flush()
        self.logger.info("WRITE")
    def close(self):
        self.output.write(("!octo4a: CLOSE\n").encode("utf-8"))
        self.closed = True
        self.logger.info("CLOSING")


class Octo4aSerialHandlerPlugin(octoprint.plugin.StartupPlugin):
    def serial_callback(self, comm_instance, port, baudrate, read_timeout, *args, **kwargs):
        return Octo4aSerial(self._logger, baudrate)

def __plugin_load__():
    plugin = Octo4aSerialHandlerPlugin()

    global __plugin_implementation__
    __plugin_implementation__ = plugin

    global __plugin_hooks__
    __plugin_hooks__ = {"octoprint.comm.transport.serial.factory": plugin.serial_callback}
