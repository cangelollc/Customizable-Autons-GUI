import time
from ntcore import NetworkTableInstance


class NTInterface:
    def __init__(self):
        self.inst = NetworkTableInstance.getDefault()
        self.inst.startClient4("DynamicAutoGuiClient")

        self.inst.startDSClient()

        self.table = self.inst.getTable("DynamicAutoConfigurations")
        self.routine_pub = self.table.getStringArrayTopic(
            "returnedRoutine").publish()
        time.sleep(0.1)

    def publish_routine(self, routine: list[str]):
        self.routine_pub.set(routine)
        self.inst.flush()
        print("Published routine:", routine)  # debugging


if __name__ == "__main__":
    nt_interface = NTInterface()
    # wait for networktables to connect, simulates startup time for the gui
    time.sleep(1)
    nt_interface.publish_routine(
        ["Test Block One", "Test Block Two", "Test Block Three"])
