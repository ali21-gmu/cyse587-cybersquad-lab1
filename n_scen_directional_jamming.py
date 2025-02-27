import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from drone import Drone
from route import RouteGenerator
from gcs import GCS
from adsbchannel import ADSBChannel
from jammer import Jammer

# Define central location
center_lat, center_lon = 38.8977, -77.0365  # White House location

# Initialize GCS
gcs = GCS(center_lat, center_lon)
gcs_pos = (center_lat, center_lon)

# Create RouteGenerator instance
route_gen = RouteGenerator(center_lat, center_lon, num_routes=1, waypoints_per_route=5, max_offset=0.02)
routes = route_gen.generate_routes()

# Initialize drones
drones = [
    Drone(
        id=f"{i+1}",
        drone_type=f"type{i+1}",
        acceleration_rate=2.0,
        climb_rate=3.0,
        speed=10.0 + i * 5,
        position_error=2.0,
        altitude_error=1.0,
        battery_consume_rate=0.05,
        battery_capacity=10.0 + i * 5,
        route=routes[i]
    )
    for i in range(len(routes))
]

# Initialize communication channel and Directional Jammer
channel = ADSBChannel()
jammer = Jammer(jamming_probability=0.0, noise_intensity=0.1, jamming_center=(38.8977, -77.0365), jamming_radius=0.01)  # Directional jamming effect

# Create 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']

# Plot waypoints
for i, route in enumerate(routes):
    latitudes = [p[0] for p in route]
    longitudes = [p[1] for p in route]
    altitudes = [p[2] for p in route]
    ax.scatter(latitudes, longitudes, altitudes, color="green", label=f"Route {i+1} Waypoints")

# Plot GCS position
gcs_marker, = ax.plot([gcs.position[0]], [gcs.position[1]], [gcs.position[2]], 'ks', markersize=8, label="GCS")

# Initialize drone markers
drone_markers = {}
for i, drone in enumerate(drones):
    marker, = ax.plot([], [], [], 'o', color=colors[i % len(colors)], markersize=6, label=f"Drone {drone.id}")
    drone_markers[drone.id] = marker

ax.set_xlabel("Latitude")
ax.set_ylabel("Longitude")
ax.set_zlabel("Altitude (m)")
ax.legend()

def update(frame):
    active_drones = False
    
    for drone in drones:
        status = drone.calculate_navigation(1)

        if status == -2:
            print(f"Drone {drone.id} battery depleted.")
        elif status == 0:
            print(f"Drone {drone.id} completed its route.")
        else:
            active_drones = True
            
            # Simulate original message
            original_message = {
                'drone_id': drone.id,
                'latitude': drone.current_position[0],
                'longitude': drone.current_position[1],
                'altitude': drone.current_position[2],
                'timestamp': time.time()
            }
            
            # Check if the drone is within the jamming area
            distance = np.sqrt((original_message['latitude'] - jammer.jamming_center[0])**2 + 
                               (original_message['longitude'] - jammer.jamming_center[1])**2)
            if distance <= jammer.jamming_radius:
                jammed_message, is_jammed = jammer.jam_signal(original_message)
                if is_jammed:
                    print(f"Drone {drone.id} communication jammed in directional area! Message lost.")
                    continue  # Skip updating this drone
            else:
                jammed_message = original_message  # No jamming effect
            
            # Update drone marker position
            marker = drone_markers[drone.id]
            marker.set_data([jammed_message['latitude']], [jammed_message['longitude']])
            marker.set_3d_properties([jammed_message['altitude']])
    
    if not active_drones:
        print("All drones have completed their routes or are inactive.")
        ani.event_source.stop()  # Stop animation properly
    
    return list(drone_markers.values())

# Run animation
ani = FuncAnimation(fig, update, frames=range(100), interval=100, blit=False)
plt.show()