from PySide6.QtCore import QObject

from ok import Logger

logger = Logger.get_logger(__name__)


class Globals(QObject):
    __telemetry = False

    def __init__(self, exit_event):
        super().__init__()

    def get_telemetry(self) -> bool:
        return self.__telemetry

    def set_telemetry(self, telemetry: bool):
        self.__telemetry = telemetry



if __name__ == "__main__":
    glbs = Globals(exit_event=None)
