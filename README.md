# Drone Security Simulation

## Overview

The **Drone Security Simulation** project aims to simulate various cybersecurity threats to drone systems, particularly focusing on **GPS spoofing** and **jamming attacks**. This project models the effects of different types of jamming attacks, including **Continuous Wave (CW) Jamming**, **Sweeping Jamming**, **Pulsed Jamming**, and **Directional Jamming**. It also incorporates a **Gradual GPS Spoofing Attack** to simulate gradual interference in drone positioning. The purpose of this project is to analyze how these attacks affect drone navigation and communication systems.

## Project Objectives

- Simulate the impact of different jamming methods on drone communication.
- Implement a gradual GPS spoofing attack to manipulate drone positioning over time.
- Visualize the drone's movement, the path it takes, and the interference caused by attacks.
- Compare the effects of different jamming methods and GPS spoofing in a controlled environment.

## What We Intended to Do

We set out to model the following aspects:
1. **Drone Positioning:** Simulate the movement of a drone in a 3D environment.
2. **Jamming Attacks:** Implement and visualize multiple jamming techniques affecting drone communication.
3. **GPS Spoofing Attack:** Gradually alter the drone’s GPS position to simulate a spoofing attack.
4. **Visualization:** Display the drone’s trajectory and its path on a 3D plot, including jamming effects.

## What We Received

The final outcome of the project was a simulation environment where:
- The drone moves smoothly in 3D space.
- Different types of jamming attacks (CW, Sweeping, Pulsed, and Directional) are applied to simulate their effects on the drone’s communication system.
- A gradual GPS spoofing attack shifts the drone’s position in a smooth manner.
- All these factors are visualized on a 3D plot, with the drone's position shown as a blue dot and its path traced in real-time.

## Results

The simulation demonstrated the following:
- **Impact of Jamming Attacks:** Each type of jamming attack showed varying degrees of interference, with the Directional Jamming being the most focused and causing targeted interference.
- **GPS Spoofing:** The gradual GPS spoofing attack smoothly manipulated the drone’s position, mimicking a real-world GPS spoofing scenario.
- **Visualization:** The 3D plot effectively visualized the drone's trajectory, allowing us to see the path taken as well as the interference caused by the attacks.

## Key Features

- **Gradual GPS Spoofing Attack:** Alters the drone’s position over time in a controlled and smooth manner.
- **Multiple Jamming Techniques:**
  - **Continuous Wave Jamming (CW):** Constant interference at a specific frequency.
  - **Sweeping Jamming:** Sweeping frequency jamming over time.
  - **Pulsed Jamming:** Intermittent pulses of interference.
  - **Directional Jamming:** Directional interference based on the relative positions of the drone and jammer.
- **3D Visualization:** The drone’s position is plotted in real-time with a 3D trajectory, and jamming effects are visualized on the same plot.

## Technologies and Libraries Used

The following packages were used in the development of the project:

- **contourpy**: 1.3.1
- **cycler**: 0.12.1
- **fonttools**: 4.56.0
- **kiwisolver**: 1.4.8
- **matplotlib**: 3.10.1
- **numpy**: 2.2.4
- **packaging**: 24.2
- **pandas**: 2.2.3
- **pillow**: 11.1.0
- **pyparsing**: 3.2.3
- **python-dateutil**: 2.9.0.post0
- **pytz**: 2025.2
- **seaborn**: 0.13.2
- **six**: 1.17.0
- **tzdata**: 2025.2

## How to Run the Project

### Prerequisites
Ensure you have Python 3.x installed. You will also need the following libraries:

```
pip install contourpy cycler fonttools kiwisolver matplotlib numpy packaging pandas pillow pyparsing python-dateutil pytz seaborn six tzdata
```

### Run the Stats File
Now run the n_scen_stat.py file to get the results of running all the attak simulations

```
python n_scen_stat.py
```

### Opening Results Directory
Now you can see a new directory with the name "results" appear in the path. Open the directory to view the graph results

### Expected Output
The simulation will generate a 3D plot with the drone’s position shown as a blue dot. The plot will also display the path the drone takes, and the effects of the different jamming attacks will be visible as interference patterns.

#### Contributors

- Andy Li
- Kumara Venkata Rohit Varma
- Derrick Buabeng 
- Raghavi Allamreddy Gari
- Dacena Martin
- Abhinav Sai Mahendra