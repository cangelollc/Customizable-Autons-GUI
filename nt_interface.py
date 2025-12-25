import time
from ntcore import NetworkTableInstance
import json


class NTInterface:
    def __init__(self):
        # Get default NT instance
        self.inst = NetworkTableInstance.getDefault()

        self.inst.setServer("127.0.0.1")
        self.inst.startClient4("DynamicAutoGuiClient")

        # Wait a moment to connect
        time.sleep(0.5)

        self.table = self.inst.getTable("SmartDashboard/DynamicAutos")

        self.routine_json_pub = self.table.getStringTopic(
            "routineJson").publish()

        time.sleep(0.1)

    def publish_routine_json(self, routine_dict: dict):
        """Publish an autonomous routine as JSON to NetworkTables"""
        json_str = json.dumps(routine_dict)
        self.routine_json_pub.set(json_str)
        self.inst.flush()
        print()
        print("Published routine JSON to NT:", json_str)
        print()

    def get_block_types_json(self) -> str:
        entry = self.table.getStringTopic("BlockTypes").getEntry("")
        while entry.get("") == "":
            self.inst.flush()
            time.sleep(0.1)

        return entry.get("")


if __name__ == "__main__":
    nt = NTInterface()

    print("Block Types JSON from NT:", nt.get_block_types_json())
