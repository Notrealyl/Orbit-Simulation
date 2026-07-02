# Orbit Simulation
This was a 9th grade science project, the project stem from my liking of orbital mechanics (Astrophysics generally).

---

## The Features
* Using Runge-Kutta 4th Order Method
* N-Body Simulation
* Changeable Planet Value (Mass, Orbiting Velocity etc.)
* Collecting Data using Matplotlib

---

## Installation
1. Clone the repository
   ```bash
   git clone https://github.com/Notrealyl/Orbit-Simulation.git

2. Installed the required dependencies
   ```bash
   pip install -r requirements.txt

---

## Usage
* Changing Time Step
  ```python
  TIMESTEP = 3600 * N #N in seconds (Change N to a positive integers)

* Changing Planet Variable
  In def main() you can change the planet variable according to provided argument ex.
  ```python
  earth = Planet(Distance_X, Distance_Y, Radius, Color, Mass, "Name")
