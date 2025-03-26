import time
import numpy as np
import matplotlib.pyplot as plt
import os
from drone import Drone
from route import RouteGenerator
from gcs import GCS
from adsbchannel import ADSBChannel
from jammer import Jammer
from sweeping_jammer import SweepingJammer
from pn_jammer import PNJammer
from directional_jammer import DirJammer
from cw_jammer import CWJammer
from spoofer import Spoofer
from gradual_spoofer import GradSpoofer
import seaborn as sns


# Define central location (e.g., Washington, D.C.)
center_lat, center_lon = 38.8977, -77.0365  # White House location

# Initialize GCS
gcs = GCS(center_lat, center_lon)
gcs_pos = (center_lat, center_lon)

# Create a RouteGenerator instancz
route_gen = RouteGenerator(center_lat, center_lon, num_routes=2, waypoints_per_route=5, max_offset=0.02)
routes = route_gen.generate_routes()

# Function to initialize drones
def initialize_drones():
    return [
        Drone(
            id=f"{i+1}",
            drone_type=f"type{i+1}",
            acceleration_rate=2.0,
            climb_rate=3.0,
            speed=10.0 + i*5,
            position_error=2.0,
            altitude_error=1.0,
            battery_consume_rate=0.05,
            battery_capacity=10.0 + i*5,
            route=routes[i]
        )
        for i in range(len(routes))
    ]

# Simulation scenarios (each attack type)
scenarios = {
    "No Attacks": {"jamming": False, "spoofing": False},
    "Continuous Wave Jamming": {"jamming": True, "spoofing": False, "jam_type": "cw"},
    "Sweeping Jamming": {"jamming": True, "spoofing": False, "jam_type": "sweep"},
    "Pulsed Noise Jamming": {"jamming": True, "spoofing": False, "jam_type": "pn"},
    "Directional Jamming": {"jamming": True, "spoofing": False, "jam_type": "dir"},
    "Gradual Spoofing": {"jamming": False, "spoofing": True, "spoof_type": "grad"}
}

def plot_snr_data(results):
    """
    Plots SNR data as both line plots and box plots for each scenario.

    Parameters:
        results (dict): Dictionary containing SNR data for each scenario.
    """
   

    # Box Plot
    plt.figure(figsize=(12, 8))
    snr_data = []
    scenarios = []
    for scenario, data in results.items():
        if 'snr' in data and data['snr']:
            _, snr_values = zip(*data['snr'])
            snr_data.extend(snr_values)
            scenarios.extend([scenario] * len(snr_values))
    sns.boxplot(x=scenarios, y=snr_data)
    plt.xlabel('Scenario')
    plt.ylabel('SNR (dB)')
    plt.title('SNR Distribution across Different Scenarios')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.savefig('results/snr_box_plot.png')
    #plt.show()

def plot_latency_data(results):
    plt.figure(figsize=(12, 8))
    for scenario, data in results.items():
        if 'latency' in data and data['latency']:
            messages, latencies = zip(*data['latency'])
            plt.plot(messages, latencies, label=scenario)
    plt.xlabel('Total Messages Sent')
    plt.ylabel('Latency (ms)')
    plt.title('Latency over Simulation Time for Different Scenarios')
    plt.legend()
    plt.grid(True)
    plt.savefig('results/latency_plot.png')
    #plt.show()

def plot_throughput_data(results):
    plt.figure(figsize=(12, 8))
    for scenario, data in results.items():
        if 'throughput' in data and data['throughput']:
            times, throughputs = zip(*data['throughput'])
            plt.plot(times, throughputs, label=scenario)
    plt.xlabel('Elapsed Time (s)')
    plt.ylabel('Throughput (messages/second)')
    plt.title('Throughput over Simulation Time for Different Scenarios')
    plt.legend()
    plt.grid(True)
    plt.savefig('results/throughput_plot.png')
    #plt.show()

def plot_packet_loss_data(results, colors=None):
    """
    Plots packet loss over time for each scenario.

    Parameters:
        results (dict): Dictionary containing packet loss data for each scenario.
        colors (list, optional): List of colors for each scenario plot. Defaults to None.
        output_path (str, optional): File path to save the plot image. Defaults to 'results/packet_loss.png'.
    """
    if colors is None:
        colors = ['blue', 'green', 'orange', 'red', 'purple']

    plt.figure(figsize=(12, 8))

    for (scenario, data), color in zip(results.items(), colors):
        if 'packet_loss' in data and data['packet_loss']:
            times, packet_loss = zip(*data['packet_loss'])
            plt.plot(times, packet_loss, label=scenario, color=color)

    plt.xlabel('Total Messages Sent')
    plt.ylabel('Packet Loss (%)')
    plt.title('Packet Loss over Simulation Time for Different Scenarios')
    plt.legend()
    plt.grid(True)
    plt.savefig('results/packet_loss.png')
    #plt.show()



# Function to run a simulation scenario
def run_simulation(jamming=False, spoofing=False, spoof_probability=0.3, jam_type=None, spoof_type=None):
    channel = ADSBChannel()
    # If there is a jammer, check which type to initialize
    if jamming:
        if jam_type == "sweep":
            jammer = SweepingJammer(jamming_probability=0.0, noise_intensity=0.1)  # Start with low jamming effect
        elif jam_type == "pn":
            jammer = PNJammer(jamming_probability=0.0, noise_intensity=0.1)
        elif jam_type == "dir":
            jammer = DirJammer(jamming_probability=0.3, noise_intensity=0.1, jamming_center=(38.8977, -77.0365), jamming_radius=0.015)
        elif jam_type == "cw":
            jammer = CWJammer(jamming_probability=0.0, noise_intensity=0.1)
    else:
        jammer = None
    
    # If there is a spoofer, check which type to initialize
    if spoofing and spoof_type == "grad":
        spoofer = GradSpoofer(spoof_probability=spoof_probability, fake_drone_id="FAKE-DRONE")
    else:
        spoofer = None

    drones = initialize_drones()

    total_messages = 0
    lost_messages = 0
    packet_loss_over_time = []
    snr_values = []
    latency_values = []
    throughput_values = []

    start_time = time.time()

    for drone in drones:
        counter = 1
        while True:
            status = drone.calculate_navigation(1)
            if status in [-1, -2, 0]:
                break

            send_time = time.time()
            original_message = {
                'drone_id': drone.id,
                'latitude': drone.current_position[0],
                'longitude': drone.current_position[1],
                'altitude': drone.current_position[2],
                'timestamp': send_time
            }

            received_message, delay_ns, corrupted, snr_db = channel.transmit(
                original_message, gcs_pos, jammer=jammer, spoofer=spoofer
            )
            receive_time = time.time()
            total_messages += 1

            if jamming and jammer:
                received_message, jammed = jammer.jam_signal(received_message)
                if jammed and received_message is None:
                    lost_messages += 1
                    packet_loss_over_time.append((total_messages, lost_messages / total_messages * 100))
                    continue
                if jam_type is not None:
                    jammer.jamming_update(counter) # Increases jamming probability and noise intensity over time for certain jammers

            if spoofing and spoofer:
                received_message, spoofed = spoofer.spoof_message(received_message)

            gcs.receive_update(
                received_message['drone_id'],
                (
                    received_message['latitude'],
                    received_message['longitude'],
                    received_message['altitude']
                )
            )

            if corrupted and not (jamming and jammed):
                lost_messages += 1

            packet_loss_over_time.append((total_messages, lost_messages / total_messages * 100))
            snr_values.append((total_messages, snr_db))

            # Calculate latency in milliseconds
            latency = (receive_time - send_time) * 1000
            latency_values.append((total_messages, latency))

            # Calculate throughput (messages per second)
            elapsed_time = receive_time - start_time
            throughput = total_messages / elapsed_time
            throughput_values.append((elapsed_time, throughput))

            # Keeps track of each iteration
            counter += 1

    return packet_loss_over_time, snr_values, latency_values, throughput_values



# Run simulations for each scenario and collect results  
results = {}
for scenario, params in scenarios.items():
    print(f"Running scenario: {scenario}")
    packet_loss_data, snr_data, latency_data, throughput_data = run_simulation(**params)
    results[scenario] = {
        'packet_loss': packet_loss_data,
        'snr': snr_data,
        'latency': latency_data,
        'throughput': throughput_data
    }

# Ensure the 'results' directory exists
if not os.path.exists('results'):
    os.makedirs('results')

# Plotting packet loss over time for each scenario
plot_packet_loss_data(results)

# Plotting SNR over time for each scenario
plot_snr_data(results)

# Plotting Latency over time for each scenario
plot_latency_data(results)

# Plotting Throughput over time for each scenario
plot_throughput_data(results)
