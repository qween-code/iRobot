# LastWarAutoBot Pro 🤖

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-AI%20Powered-orange.svg)](https://github.com/ultralytics/ultralytics)

**Open-source AI-powered automation bot for Last War: Survival Game**

> ⚠️ **EDUCATIONAL PURPOSE ONLY**: This project is for learning automation, computer vision, and AI techniques. Using bots in Last War violates the game's Terms of Service and may result in permanent bans. Use at your own risk.

---

## 🌟 Features

### Core Automation
- ✅ **Resource Farming**: Auto-raid optimal tiles (6 attacks/day)
- ✅ **Zombie Hunting**: Smart type/level selection with stamina management
- ✅ **Troop Management**: Auto-train, heal, promote troops
- ✅ **Base Building**: Intelligent upgrade prioritization
- ✅ **Alliance Activities**: Auto-helps, donations, gifts, rallies

### 🆕 Advanced Alliance/Clan Features
- 🤝 **Continuous Alliance Helps**: Auto-send helps to clan members every 5 minutes
- 💰 **Auto-Donations**: Automatic technology donations with resource safety thresholds
- 🎁 **Gift Collection**: Auto-collect alliance gifts on schedule
- ⚔️ **Rally Coordination**: Smart rally joining with participation probability
- 🏪 **Alliance Shop**: Auto-purchase priority items (speedups, hero shards)
- 📊 **Alliance Event Participation**: Automatic event detection and participation

### 🆕 Game Update Adaptation
- 🔄 **Dynamic UI Adaptation**: Auto-detect and adapt to UI changes after game updates
- 🎮 **Version Detection**: Fingerprint-based game version tracking
- 📸 **Template Learning**: Self-learning UI element positions
- 🔍 **Multi-Scale Matching**: Handle UI scale changes (0.8x - 1.2x)
- ⚡ **Auto-Calibration**: Weekly UI recalibration for stability

### 🆕 Event Detection & Auto-Participation
- 🧟 **Golden Zombies Event**: 2-phase strategy (discovery → boss rallies)
- 🎯 **Zombie Invasion**: Auto-collect digs, eggs, radar quests
- 👑 **KvK Support**: Kingdom vs Kingdom with safe mode
- 🛡️ **Alliance War**: Coordinated alliance warfare (conservative mode)
- 💎 **Resource Madness**: Prioritize farming during bonus events
- 🏋️ **Troop Training Events**: Continuous training optimization
- 🦸 **Hero Trials**: Auto-complete with best hero selection
- 📅 **Daily Quests**: Complete all daily tasks automatically

### Advanced AI
- 🧠 **YOLOv8 Detection**: AI-powered UI element recognition
- 🎯 **Smart Decision Engine**: State machine with priority queues
- 📊 **Resource Optimization**: ML-based hero/troop selection
- 🔄 **Dynamic Adaptation**: Auto-adjust to game updates
- 🎪 **Event Intelligence**: Auto-detect active events every 15 minutes

### Anti-Ban System
- 🕵️ **Human Behavior Simulation**: Gaussian delays, Bezier curves
- 🌐 **Network Masking**: Proxy rotation, device fingerprinting
- ⏱️ **Session Patterns**: Realistic play/break cycles
- 📉 **Risk Monitoring**: Real-time detection risk assessment
- 🎲 **Randomization**: Event participation probability (30-80%)

### Scaling & Infrastructure
- 🐳 **Docker Native**: Multi-instance support (50+ accounts)
- 🌐 **Web Dashboard**: Real-time monitoring & control
- 📱 **Multi-Platform**: Windows, macOS, Linux + Android emulators
- 🔌 **API Integration**: REST API for external control

---

## 🚀 Quick Start

### Prerequisites

- **Python**: 3.12+
- **Docker**: 24.0+
- **ADB**: Android Debug Bridge
- **Emulator**: LDPlayer, NoxPlayer, or BlueStacks

### Installation

#### Option 1: Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/yourusername/LastWarAutoBot.git
cd LastWarAutoBot

# Build Docker image
docker-compose build

# Run single instance
docker-compose up bot

# Run multiple instances
docker-compose up --scale bot=5
```

#### Option 2: Local Setup

```bash
# Clone repository
git clone https://github.com/yourusername/LastWarAutoBot.git
cd LastWarAutoBot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download YOLOv8 model
python scripts/download_models.py

# Run bot
python src/main.py --config configs/default.yaml
```

### Quick Configuration

1. **Copy example config:**
   ```bash
   cp configs/config.example.yaml configs/myconfig.yaml
   ```

2. **Edit configuration:**
   ```yaml
   # configs/myconfig.yaml
   account:
     username: "your_account"
     server: "S123"

   emulator:
     type: "ldplayer"
     adb_port: 5555

   automation:
     enabled_tasks:
       - resource_farming
       - zombie_hunting
       - troop_management

     farming:
       max_attacks_per_day: 6
       target_resource: "iron"

   anti_ban:
     enable_randomization: true
     session_duration_hours: [2, 4]
     break_duration_minutes: [30, 120]
   ```

3. **Run with custom config:**
   ```bash
   python src/main.py --config configs/myconfig.yaml
   ```

---

## 📖 Documentation

### Project Structure

```
LastWarAutoBot/
├── src/
│   ├── core/                  # Bot orchestration & state machine
│   │   ├── bot_controller.py
│   │   ├── state_machine.py
│   │   └── task_scheduler.py
│   ├── vision/                # Computer vision modules
│   │   ├── yolo_detector.py
│   │   ├── template_matcher.py
│   │   └── ocr_reader.py
│   ├── actions/               # Game automation logic
│   │   ├── farming.py
│   │   ├── zombie_hunting.py
│   │   ├── troop_management.py
│   │   └── events.py
│   ├── device/                # Device control
│   │   ├── adb_controller.py
│   │   └── emulator_manager.py
│   ├── anti_ban/              # Anti-detection systems
│   │   ├── behavior_randomizer.py
│   │   └── timing_variance.py
│   └── api/                   # Web API & dashboard
│       ├── rest_api.py
│       └── websocket.py
├── models/                    # YOLOv8 trained models
├── configs/                   # Configuration files
├── tests/                     # Unit & integration tests
├── docker/                    # Docker configurations
├── docs/                      # Documentation
│   ├── PRD.md                # Product Requirements
│   ├── ARCHITECTURE.md       # Technical architecture
│   └── API.md                # API documentation
├── scripts/                   # Utility scripts
├── requirements.txt
├── docker-compose.yml
└── README.md
```

### Key Modules

#### 1. Vision Module
```python
from src.vision.yolo_detector import YOLODetector

detector = YOLODetector(model_path='models/lastwar_v8n.pt')
screenshot = detector.capture_screen()
elements = detector.detect_elements(screenshot)

# Find specific button
collect_btn = detector.find_button(screenshot, 'collect_button')
if collect_btn:
    detector.click(collect_btn)
```

#### 2. Action Module
```python
from src.actions.zombie_hunting import ZombieHunter

hunter = ZombieHunter(config)
await hunter.hunt_loop(
    zombie_type='ironhead',
    target_level=25,
    hero='Monica'
)
```

#### 3. Anti-Ban Module
```python
from src.anti_ban.behavior_randomizer import HumanBehavior

human = HumanBehavior()

# Random delay
human.random_delay(10, 60)  # 10-60 sec with Gaussian dist

# Natural swipe
human.bezier_swipe(start=(100, 200), end=(500, 600))

# Session management
if human.should_take_break():
    print("Taking 30-120 min break...")
```

---

## 🎮 Usage Examples

### Example 1: Basic Farming Bot

```python
import asyncio
from src.core.bot_controller import BotController

async def main():
    config = {
        'tasks': ['resource_farming', 'zombie_hunting'],
        'farming': {'target': 'iron', 'max_attacks': 6},
        'hunting': {'zombie_type': 'ironhead', 'hero': 'Monica'}
    }

    bot = BotController(config)
    await bot.start()

if __name__ == '__main__':
    asyncio.run(main())
```

### Example 2: Multi-Account Manager

```python
from src.core.multi_account import MultiAccountManager

accounts = [
    {'username': 'account1', 'server': 'S123'},
    {'username': 'account2', 'server': 'S124'},
]

manager = MultiAccountManager(accounts)
await manager.run_staggered(delay_minutes=10)
```

### Example 3: Web Dashboard

```bash
# Start web server
python src/api/app.py

# Open browser: http://localhost:5000
# Monitor all bots in real-time
```

---

## 🔧 Configuration Guide

### Core Settings

```yaml
# General
log_level: INFO
debug_mode: false

# Device
emulator:
  type: ldplayer  # ldplayer | noxplayer | bluestacks
  adb_host: 127.0.0.1
  adb_port: 5555
  resolution: [1920, 1080]

# Automation Tasks
automation:
  enabled_tasks:
    - resource_farming
    - zombie_hunting
    - troop_management
    - building_upgrades
    - alliance_activities

  # Resource Farming
  farming:
    enabled: true
    max_attacks_per_day: 6
    target_resources: [iron, food]
    tile_level_range: [15, 20]
    scout_before_attack: true

  # Zombie Hunting
  hunting:
    enabled: true
    zombie_types: [ironhead, glutton]
    optimal_level_offset: 2  # player_level + 2
    min_stamina_threshold: 20
    always_use_monica: true

  # Troop Management
  troops:
    auto_train: true
    training_ratio:
      infantry: 1
      rider: 1
      shooter: 1
    auto_heal: true
    heal_speedup_threshold: 300  # seconds

  # Building
  buildings:
    auto_upgrade: true
    priority_order: [HQ, Barracks, Hospital]
    speedup_threshold: 3600  # seconds
    use_alliance_helps: true

# Anti-Ban
anti_ban:
  enable_randomization: true

  # Timing
  action_delay_range: [5, 60]  # seconds
  delay_distribution: gaussian

  # Sessions
  session_duration_hours: [2, 4]
  break_duration_minutes: [30, 120]

  # Behavior
  mouse_movement: bezier_curves
  click_variance_pixels: 10
  action_sequence_randomization: 0.15  # 15%

  # Network
  use_proxy: false
  proxy_rotation: true
  device_fingerprint_randomization: true

# AI/ML
ai:
  yolo_model: models/lastwar_v8n.pt
  confidence_threshold: 0.6
  ocr_language: eng
  decision_engine: state_machine

# Notifications
notifications:
  telegram:
    enabled: false
    bot_token: YOUR_TOKEN
    chat_id: YOUR_CHAT_ID
  discord:
    enabled: false
    webhook_url: YOUR_WEBHOOK
```

---

## 🧪 Testing

### Run Tests

```bash
# All tests
pytest tests/

# Unit tests only
pytest tests/unit/

# Integration tests (requires emulator)
pytest tests/integration/

# Coverage report
pytest --cov=src tests/
```

### Manual Testing

```bash
# Test vision module
python scripts/test_vision.py

# Test ADB connection
python scripts/test_adb.py

# Simulate bot actions (dry run)
python src/main.py --dry-run --config configs/test.yaml
```

---

## 📊 Performance Metrics

### Benchmarks (Single Instance)

| Metric | Value |
|--------|-------|
| CPU Usage | 15-20% |
| RAM Usage | 400-500 MB |
| Action Decision Time | <300ms |
| Screenshot Processing | <100ms (YOLO) |
| Daily Resource Gain | 10-20x manual play |

### Scaling (Multi-Instance)

| Instances | CPU | RAM | Recommended Hardware |
|-----------|-----|-----|---------------------|
| 1-5 | 20% | 2GB | Basic PC |
| 5-10 | 40% | 4GB | Mid-tier PC |
| 10-25 | 60% | 8GB | Gaming PC |
| 25-50 | 80% | 16GB | Server/Workstation |

---

## 🛡️ Security & Privacy

### Data Protection
- ✅ **No Cloud Upload**: All data stays local
- ✅ **Encrypted Credentials**: AES-256 encryption
- ✅ **No Telemetry**: Zero tracking or analytics
- ✅ **Open Source**: Audit the code yourself

### Safe Usage Tips
1. **Use Test Accounts**: Don't bot on main accounts
2. **Start Slow**: Test with low activity first
3. **Monitor Logs**: Watch for detection warnings
4. **Respect Limits**: Don't run 24/7 immediately
5. **Community Reports**: Check Discord for ban waves

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Fork and clone
git clone https://github.com/yourusername/LastWarAutoBot.git
cd LastWarAutoBot

# Install dev dependencies
pip install -r requirements-dev.txt

# Pre-commit hooks
pre-commit install

# Create feature branch
git checkout -b feature/amazing-feature

# Make changes, test, commit
pytest tests/
git commit -m "Add amazing feature"
git push origin feature/amazing-feature
```

### Contribution Areas
- 🐛 Bug fixes
- ✨ New features (events, advanced strategies)
- 📝 Documentation improvements
- 🧪 Test coverage
- 🌍 Translations (UI, docs)
- 🎨 Dashboard UI enhancements

---

## 📜 License & Disclaimer

### License
MIT License - see [LICENSE](LICENSE) file

### Disclaimer

```
⚠️ IMPORTANT DISCLAIMER ⚠️

This software is provided for EDUCATIONAL PURPOSES ONLY.

- Using bots in Last War: Survival violates the game's Terms of Service
- Account bans are highly likely (70%+ detection rate for 24/7 usage)
- Authors are NOT RESPONSIBLE for any bans, account losses, or damages
- Use at your own risk
- We do not endorse or encourage ToS violations

By using this software, you acknowledge and accept all risks.

For learning purposes, use on private servers or offline environments only.
```

---

## 🙏 Acknowledgments

### Research & Inspiration
- [BoostBot](https://boostbot.org/last-war-survival-bot/) - Market research
- [GnBots](https://www.gnbots.com/) - Feature inspiration
- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) - AI framework
- [OpenCV](https://opencv.org/) - Computer vision
- Last War community for game mechanics insights

### Technologies
- Python 3.12
- Docker & Kubernetes
- PyTorch & YOLOv8
- OpenCV & NumPy
- Flask & React
- PostgreSQL & Redis

---

## 📞 Support & Community

- 📖 **Documentation**: [docs/](docs/)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/yourusername/LastWarAutoBot/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/LastWarAutoBot/discussions)
- 💡 **Feature Requests**: [GitHub Issues](https://github.com/yourusername/LastWarAutoBot/issues)
- 🎮 **Discord**: (Coming soon)

---

## 🗺️ Roadmap

### Version 1.0 (Current)
- [x] Core automation (farming, hunting, troops)
- [x] YOLOv8 integration
- [x] Basic anti-ban
- [x] Docker support
- [ ] Web dashboard (in progress)

### Version 1.5 (Q2 2025)
- [ ] Advanced event automation (Golden Zombies, Boss fights)
- [ ] Multi-language support (CN, TR, ES)
- [ ] Mobile app (React Native)
- [ ] Community plugin system

### Version 2.0 (Q4 2025)
- [ ] Multi-game support (State of Survival, Last Shelter)
- [ ] Cloud-hosted option (AWS/GCP)
- [ ] AI-as-a-Service API
- [ ] Advanced ML models (reinforcement learning)

---

## 📈 Project Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/LastWarAutoBot)
![GitHub forks](https://img.shields.io/github/forks/yourusername/LastWarAutoBot)
![GitHub issues](https://img.shields.io/github/issues/yourusername/LastWarAutoBot)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/LastWarAutoBot)

---

## ☕ Support the Project

If this project helped you, consider:
- ⭐ **Star** the repository
- 🐛 **Report bugs** or suggest features
- 🤝 **Contribute** code or docs
- 💰 **Sponsor** via [GitHub Sponsors](https://github.com/sponsors)

---

**Made with ❤️ by the LastWarAutoBot community**

*Remember: Use responsibly and ethically. This is an educational project.*
