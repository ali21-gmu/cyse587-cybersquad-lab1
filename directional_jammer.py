import random
import time
import numpy as np

class DirJammer:
    def __init__(self, jamming_probability, noise_intensity, jamming_center=(38.8977, -77.0365), jamming_radius=0.0, jamming_power_dbm=-70):
        self.jamming_probability = jamming_probability
        self.noise_intensity = noise_intensity  # Higher value increases interference
        self.jamming_power_dbm = jamming_power_dbm  # Default jamming signal power in dBm
        self.jamming_center = jamming_center   # Default location: White House
        self.jamming_radius = jamming_radius

    def jam_signal(self, message):
        # Check if the drone is within the jamming area
        distance = np.sqrt((message['latitude'] - self.jamming_center[0])**2 + (message['longitude'] - self.jamming_center[1])**2)
        if distance <= self.jamming_radius:
            print("[Jammer] Jamming message:", message)
            if random.random() < self.noise_intensity:
                print("[Jammer] Message completely lost!")
                return None, True  # Message is lost
            else:
                message['latitude'] += random.uniform(-0.1, 0.1)
                message['longitude'] += random.uniform(-0.1, 0.1)
                message['altitude'] += random.uniform(-100, 100)
                return message, True
        return message, False

    def jamming_signal_power(self):
        """Returns the power of the jamming signal in dBm."""
        return self.jamming_power_dbm

    def jamming_update(self, counter):
        pass