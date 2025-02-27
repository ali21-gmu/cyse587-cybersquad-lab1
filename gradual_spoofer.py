import random
import numpy as np
import time

class GradSpoofer:
    """
    This class simulates ADS-B spoofing by modifying legitimate drone messages
    or injecting entirely fake drones into the system.
    """
    def __init__(self, spoof_probability=0.3, fake_drone_id="FAKE123"):
        self.spoof_probability = spoof_probability
        self.fake_drone_id = fake_drone_id

    def spoof_message(self, message):
        """Modify a real drone message or inject a fake drone."""
        if random.random() < self.spoof_probability:
            lat_lon_drift = random.uniform(-0.0005, 0.0005)
            alt_drift = random.uniform(-0.05, 0.05)
            print("[Spoofer] Spoofing message:", message)
            spoofed_message = message.copy()
            spoofed_message['latitude'] += lat_lon_drift
            spoofed_message['longitude'] += lat_lon_drift
            spoofed_message['altitude'] += alt_drift
            spoofed_message['drone_id'] = self.fake_drone_id if random.random() < 0.5 else message['drone_id']
            return spoofed_message, True
        return message, False