# DRAM Simulation Project

This project provides a comprehensive simulation framework for analyzing DRAM memory systems using DRAMsim3. The focus is on evaluating performance characteristics of different memory architectures, particularly HBM (High Bandwidth Memory), DDR3, and DDR4.

Key features include:
- Detailed simulation of memory timing, power consumption, and thermal behavior
- Support for various DRAM standards (DDR3, DDR4, HBM, HMC, GDDR)
- Performance comparison across different workloads (random, stream, matrix operations, etc.)
- Automated benchmark generation and visualization tools
- Thermal modeling capabilities for analyzing heat distribution

The project includes pre-configured memory controller settings and provides tools for generating custom memory access patterns. It's particularly useful for:
- Computer architecture research
- Memory system design optimization
- Performance prediction of real-world applications
- Educational purposes in computer engineering

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

## Thanks

We extend our sincere gratitude to the **University of Maryland Memory Systems Research Group** for creating and maintaining DRAMsim3. This project builds upon their excellent simulator, which provides the foundation for our memory system analysis.

Special recognition to the core contributors:
- **Shang Li**, **Zhiyuan Yang**, **Dhriaj Reddy**, **Ankur Srivastava**, and **Bruce Jacob**
- For their paper:  
  S. Li et al., "DRAMsim3: a Cycle-accurate, Thermal-Capable DRAM Simulator," IEEE Computer Architecture Letters, 2020.  
  [DOI: 10.1109/LCA.2020.2973991](https://doi.org/10.1109/LCA.2020.2973991)

**Project Resources**:  
🔗 GitHub Repository: [https://github.com/umd-memsys/DRAMsim3](https://github.com/umd-memsys/DRAMsim3)  

This simulator represents significant contributions to computer architecture research through its:
- Cycle-accurate modeling of modern DRAM standards
- Integrated thermal/power analysis capabilities
- Modular design enabling controller customization
- Seamless integration with full-system simulators like Gem5

We acknowledge their pioneering work in advancing memory system simulation and are grateful for their commitment to open-source research tools.
