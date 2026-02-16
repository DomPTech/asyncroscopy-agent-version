# AS_server_twin.py

"""
mirrors the real thing.
"""

from twisted.internet import reactor, protocol
import numpy as np
import time
import sys

from asyncroscopy.servers.protocols.execution_protocol import ExecutionProtocol
from asyncroscopy.servers.protocols.utils import package_message, unpackage_message
# sys.path.insert(0, "C:\\AE_future\\autoscript_1_14\\")
#sys.path.insert(0, "/Users/austin/Desktop/Projects/autoscript_tem_microscope_client")
#import autoscript_tem_microscope_client as auto_script


# FACTORY — holds shared state (persistent across all connections)
class ASFactory(protocol.Factory):
    def __init__(self):
        # persistent states for all protocol instances
        self.microscope = None
        self.detectors = {}
        self.status = "Offline"
        self.stage_position = np.array([0, 0, 0, 0, 0], dtype=np.float32)
        self.magnification = 1000.0
        self.beam_blanked = True
        self.column_valve_open = False
        self.optics_mode = "TEM"

    def buildProtocol(self, addr):
        """Create a new protocol instance and attach the factory (shared state)."""
        proto = ASProtocol()
        proto.factory = self
        return proto


# PROTOCOL — handles per-connection command execution
class ASProtocol(ExecutionProtocol):
    def __init__(self):
        super().__init__()
        allowed = []
        for name, value in ExecutionProtocol.__dict__.items():
            if callable(value) and not name.startswith("_"):
                allowed.append(name)
        self.allowed_commands = set(allowed)

    def connect_AS(self, args: dict):
        """Connect to the microscope via AutoScript"""
        host = args.get('host')
        port = args.get('port')
        
        print(f"[AS] Connecting to microscope at {host}:{port}...")
        self.factory.microscope = 'Debugging'
        self.factory.status = "Ready"
        msg = "Connected to Digital Twin microscope."
        self.sendString(package_message(msg))

    def get_scanned_image(self, args: dict):
        """Return a scanned image using the indicated detector"""
        scanning_detector = args.get('scanning_detector')
        size = args.get('size')
        dwell_time = args.get('dwell_time')

        size = int(size)
        dwell_time = float(dwell_time)
        if dwell_time * size * size > 600:
            print(f"[AS] Error: Acquisition too long: {dwell_time*size*size} seconds")
            return None
        else:
            self.factory.status = "Busy"
            time.sleep(5)
            image = (np.random.rand(size, size) * 255).astype(np.uint8)
            self.factory.status = "Ready"
            self.sendString(package_message(image))

    def get_stage(self, args=None):
        """Return current stage position"""
        self.sendString(package_message(self.factory.stage_position))

    def set_magnification(self, args: dict):
        """Set magnification (placeholder for twin)"""
        value = args.get('value', 1000.0)
        self.factory.magnification = float(value)
        msg = f"Magnification set to {value}x (simulated)"
        self.sendString(package_message(msg))

    def get_status(self, args=None):
        """Return the server status"""
        msg = f"Microscope is {self.factory.status}"
        self.sendString(package_message(msg))

    def get_state(self, args=None):
        """Return the full microscope state as a dictionary"""
        state = {
            "status": self.factory.status,
            "stage_x": float(self.factory.stage_position[0]),
            "stage_y": float(self.factory.stage_position[1]),
            "stage_z": float(self.factory.stage_position[2]),
            "magnification": self.factory.magnification,
            "beam_blanked": self.factory.beam_blanked,
            "column_valve_open": self.factory.column_valve_open,
            "optics_mode": self.factory.optics_mode
        }
        self.sendString(package_message(state))

    def calibrate_screen_current(self, args=None):
        """Mock calibration"""
        msg = "Screen current calibrated (simulated)"
        self.sendString(package_message(msg))

    def set_beam_current(self, args: dict):
        """Mock set current"""
        current = args.get("current", 0)
        msg = f"Current set to {current} pA (simulated)"
        self.sendString(package_message(msg))

    def place_beam(self, args: dict):
        """Mock place beam"""
        x = args.get("x", 0.5)
        y = args.get("y", 0.5)
        msg = f"Beam moved to {x}, {y} (simulated)"
        self.sendString(package_message(msg))

    def blank_beam(self, args=None):
        """Mock blank beam"""
        self.factory.beam_blanked = True
        msg = "Beam blanked (simulated)"
        self.sendString(package_message(msg))

    def tune_C1A1(self, args=None):
        """Mock tune_C1A1"""
        msg = "C1A1 tuned (simulated)"
        self.sendString(package_message(msg))

    def unblank_beam(self, args: dict):
        """Mock unblank beam"""
        duration = args.get("duration")
        self.factory.beam_blanked = False
        if duration:
            msg = f"Beam unblanked for {duration}s (simulated)"
            # Note: In a real twisted server we'd use reactor.callLater to re-blank
        else:
            msg = "Beam unblanked (simulated)"
        self.sendString(package_message(msg))

    def set_microscope_status(self, args: dict):
        """Set microscope status (valves, optics mode)"""
        parameter = args.get("parameter")
        value = args.get("value")
        
        if parameter == 'column_valve':
            self.factory.column_valve_open = (value == 'open')
            msg = f"Column valve {value} (simulated)"
        elif parameter == 'optics_mode':
            self.factory.optics_mode = value
            msg = f"Optics mode set to {value} (simulated)"
        else:
            msg = f"Parameter {parameter} not recognized (simulated)"
            
        self.sendString(package_message(msg))

    def get_atom_count(self, args=None):
        """Mock get_atom_count"""
        count = 3600 # Matching user's notebook example
        msg = f"Current atom count: {count}"
        self.sendString(package_message(msg))

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9001
    print(f"[AS] Server running on port {port}...")
    reactor.listenTCP(port, ASFactory())
    reactor.run()