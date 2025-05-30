# Aether Circuit

Aether Circuit is a unique logic-based puzzle game where players connect energy nodes to a central core in a 2D grid, managing limited connections to avoid overloading the system. Each connection increases energy flow, and players must strategically link nodes to power the core while staying under the energy limit. This innovative puzzle experience combines circuit-building with risk management.

## Features
- **Dynamic Puzzles**: Connect nodes to a central core in a 6x6 grid, with procedurally generated node placements.
- **Energy Management**: Balance connections to avoid overloading the system’s energy capacity.
- **Minimalist Design**: Clean visuals optimized for browser-based play with Pygame.
- **Progressive Challenges**: Increasingly complex levels with more nodes as you advance.

## Installation
1. Ensure Python 3.8+ and Pygame are installed:
   ```bash
   pip install pygame
   ```
2. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/aether-circuit.git
   ```
3. Run the game:
   ```bash
   python aether_circuit.py
   ```

## How to Play
- **Objective**: Connect all nodes to the central core without exceeding the energy limit.
- **Controls**:
  - Click a node or core to select it, then click an adjacent node/core to connect them.
  - Connections can only be made between adjacent cells (up, down, left, right).
- **Mechanics**:
  - Each connection adds 20 energy units.
  - Exceeding the energy limit causes an overload, ending the game.
  - Connect all nodes to the core to advance to the next level.
- **Game Over**: Overloading the system ends the game. Press R to restart.

## Browser Compatibility
Aether Circuit is designed for Pyodide compatibility, ensuring seamless performance in browser environments without local file I/O or network dependencies.

## Contributing
Contributions are welcome! Please fork the repository and submit pull requests with your improvements. Adhere to PEP 8 standards and include relevant tests.

## Sponsor
Support the development of Aether Circuit by becoming a GitHub Sponsor! Your contributions help power this unique puzzle adventure.

[Become a Sponsor](https://github.com/sponsors/yourusername)

## License
MIT License. See [LICENSE](LICENSE) for details.