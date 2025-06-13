# DRAM Simulation Project

This project simulates DRAM memory systems using DRAMsim3, with a focus on HBM (High Bandwidth Memory) performance analysis.

## Project Structure

- `DRAMsim3-1.0.0/`: The main DRAMsim3 simulator source code
  - `configs/`: Configuration files for various DRAM types (DDR3, DDR4, HBM, etc.)
  - `src/`: Source code of the simulator
  - `scripts/`: Python scripts for analysis and visualization
- `build/`: Build directory for compiled binaries
- `*.png`: Performance comparison charts
- `*.csv`: Benchmark results

## Getting Started

1. Clone this repository
2. Build DRAMsim3:
   ```bash
   cd DRAMsim3-1.0.0
   make
   ```
3. Run simulations:
   ```bash
   ./dramsim3main configs/HBM_4Gb_x128.ini
   ```

## Features

- Supports various DRAM standards: DDR3, DDR4, HBM, HMC, GDDR
- Detailed performance statistics collection
- Thermal modeling capabilities
- Python scripts for data analysis and visualization

## Configuration

Edit `.ini` files in `configs/` directory to customize:
- Memory organization
- Timing parameters
- Power characteristics
- Thermal parameters

## Analysis Tools

- `run_memory_benchmarks.py`: Main performance evaluation script for comparing DDR3, DDR4 and HBM2 under different workloads
- `plot_stats.py`: Generate performance charts
- `heatmap.py`: Create thermal heatmaps
- `trace_gen.py`: Generate memory access traces

## License

This project uses the MIT License. See `DRAMsim3-1.0.0/LICENSE` for details.