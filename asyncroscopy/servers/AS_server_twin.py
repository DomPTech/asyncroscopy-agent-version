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
        """Return current stage position (placeholder)"""
        positions = [np.random.uniform(-10, 10) for _ in range(5)]
        positions = np.array(positions, dtype=np.float32)
        self.sendString(package_message(positions))

    def set_magnification(self, args: dict):
        """Set magnification (placeholder for twin)"""
        value = args.get('value', 1000.0)
        msg = f"Magnification set to {value}x (simulated)"
        self.sendString(package_message(msg))

    def get_status(self, args=None):
        """Return the server status"""
        msg = f"Microscope is {self.factory.status}"
        self.sendString(package_message(msg))

    def calibrate_screen_current(self, args=None):
        """Mock calibration"""
        msg = "Screen current calibrated (simulated)"
        self.sendString(package_message(msg))

    def set_current(self, args: dict):
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
        msg = "Beam blanked (simulated)"
        self.sendString(package_message(msg))

    def unblank_beam(self, args: dict):
        """Mock unblank beam"""
        duration = args.get("duration")
        if duration:
            msg = f"Beam unblanked for {duration}s (simulated)"
        else:
            msg = "Beam unblanked (simulated)"
        self.sendString(package_message(msg))


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9001
    print(f"[AS] Server running on port {port}...")
    reactor.listenTCP(port, ASFactory())
    reactor.run()