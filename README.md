# Flappy Bird with Reinforcement Learning 🐦

A Flappy Bird game implementation using Q-Learning reinforcement learning algorithm to train an AI agent to play the game autonomously.

## 🎮 Overview

This project implements the classic Flappy Bird game with an AI agent that learns to play using Q-Learning. The agent observes the game state (bird position, pipe positions, velocity) and learns optimal actions (flap or no flap) through trial and error.

## ✨ Features

- **Multiple Game Modes**:
  - `normal`: Human player with UI
  - `train`: Train AI agent with UI visualization
  - `noui`: Train AI agent without UI (faster training)
  - `ai`: Watch trained AI play with UI

- **Q-Learning Implementation**:
  - State discretization for efficient learning
  - Configurable learning parameters (alpha, gamma, epsilon)
  - Persistent Q-value storage in JSON format

- **Flexible Training**:
  - Customizable number of training episodes
  - Adjustable FPS for training speed
  - Real-time learning progress tracking

## 🚀 Quick Start

### Prerequisites

- Python 3.x
- pygame

### Installation

1. Clone the repository:
```bash
git clone https://github.com/dinhxuanhuy/AutoFlapBird-with-ReinforcementLearning.git
cd AutoFlapBird-with-ReinforcementLearning
```

2. Install dependencies:
```bash
pip install pygame
```

### Usage

#### Train the AI (with UI):
```bash
python main.py --mode train --episodes 1000
```

#### Train the AI (without UI - faster):
```bash
python main.py --mode noui --episodes 10000
```

#### Watch trained AI play:
```bash
python main.py --mode ai
```

#### Play manually:
```bash
python main.py --mode normal
```

#### Command Line Arguments:
- `--mode`: Game mode (`normal`, `train`, `noui`, `ai`)
- `--episodes`: Number of training episodes (default: 10000)
- `--fps`: Frames per second (default: 60)
- `--max-score`: Maximum score per episode (default: 1000000)

## 🧠 Q-Learning Implementation

### State Representation
The agent perceives the game state as a string format: `"x_y_vel"` where:
- `x`: Horizontal distance from bird to next pipe (discretized)
- `y`: Vertical distance from bird to pipe gap center (discretized)
- `vel`: Current vertical velocity of the bird

### Action Space
- `0`: Do nothing (let gravity pull the bird down)
- `1`: Flap (give the bird an upward impulse)

### Reward System
- `+1`: For each frame the bird stays alive
- `-1000`: When the bird crashes (death penalty)

### Learning Parameters
- **Alpha (α)**: Learning rate (default: 0.7)
- **Gamma (γ)**: Discount factor (default: 1.0)
- **Epsilon (ε)**: Exploration rate (default: 0.0 for exploitation)

## 📁 Project Structure

```
FlappyBirdWithRL/
├── main.py              # Main game loop and entry point
├── config.py            # Configuration settings and argument parsing
├── agent.py             # Q-Learning agent implementation
├── player.py            # Bird physics and behavior
├── components.py        # Game components (pipes, ground, background)
├── qvalues.json         # Saved Q-values from training
├── data/
│   ├── flappy.ico      # Game icon
│   ├── hitmasks_data.pkl # Collision detection data
│   ├── qvalues.json    # Backup Q-values
│   └── assets/
│       ├── audio/      # Sound effects
│       └── sprites/    # Game sprites and images
└── __pycache__/        # Python cache files
```

## 🔧 Configuration

Key parameters can be modified in `config.py`:

- **Window dimensions**: 288x512 pixels
- **Pipe gap size**: 100 pixels
- **Physics constants**: Gravity, flap strength, terminal velocity
- **Training parameters**: Learning rate, discount factor, exploration

## 📊 Training Progress

During training, the agent:
1. Starts with random actions (exploration)
2. Gradually learns better strategies through Q-value updates
3. Saves learned Q-values to `qvalues.json` for persistence
4. Can resume training from previously saved knowledge

## 🎯 Performance

The trained agent can achieve:
- Consistent high scores after sufficient training
- Near-optimal pipe navigation
- Stable flight patterns
- Score improvements over multiple training sessions

## 🛠️ Customization

### Adjusting Learning Parameters
Modify the `Agent` class initialization in `config.py`:
```python
agent = Agent(
    path="data/qvalues.json",
    alpha=0.7,      # Learning rate
    gamma=1.0,      # Discount factor
    epsilon=0.1     # Exploration rate
)
```

### Changing Game Physics
Modify physics constants in `player.py`:
```python
self.playerAccY = 1      # Gravity
self.playerFlapAcc = -9  # Flap strength
self.playerMaxVelY = 10  # Terminal velocity
```

## 📈 Monitoring Training

The agent provides training feedback:
- Episode count and scores
- Q-value updates
- Learning progress indicators
- Crash/success statistics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Original Flappy Bird game concept by Dong Nguyen
- Q-Learning algorithm implementation inspired by reinforcement learning research
- Pygame community for the excellent game development framework

## 📞 Contact

- **Author**: Dinh Xuan Huy
- **Repository**: [AutoFlapBird-with-ReinforcementLearning](https://github.com/dinhxuanhuy/AutoFlapBird-with-ReinforcementLearning)

---

**Happy Learning!** 🎓✨

Watch your AI bird evolve from a clumsy beginner to a Flappy Bird master through the power of reinforcement learning!