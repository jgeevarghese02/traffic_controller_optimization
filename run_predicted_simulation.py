# run_predicted_simulation.py

from simulation import run_simulation_with_custom_timings

# Your predicted timing vector (example)
timing_vector = [
    0.82, 0.67, 0.81, 0.34, 0.29, 0.41, 0.91, 1.02,
    0.76, 1.25, 0.53, 0.37, 0.23, 1.06, 0.54, 0.93
]

# Run the simulation with your predicted vector
result = run_simulation_with_custom_timings(timing_vector)

# Output the result
print("\nSimulation Result:")
print(result)