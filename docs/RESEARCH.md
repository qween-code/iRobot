# Research Findings - Last War Bot Ecosystem (2025-2026)

## Open Source Last War Bots (GitHub)

### 1. NotEnoughTina/FirstLady (BEST REFERENCE)
- **URL:** https://github.com/NotEnoughTina/FirstLady
- **Language:** Python
- **Architecture:** Modular (core/game/automation/utils)
- **Key Features:**
  - Secretary management with OCR alliance tag filtering
  - Alliance donations (auto, 25000s interval)
  - Help detection (5s interval)
  - Map exchange, dig checking, cleanup
  - Discord webhook notifications
  - Config-driven design (JSON): game_config.json, positions.json
  - ADB-based communication
  - Template matching + Tesseract OCR
  - Auto-cleanup (24h file retention)
  - Log rotation (10MB max)
- **Lessons Learned:**
  - Config-driven > hardcoded positions
  - Interval-based scheduling is effective
  - OCR has limitations with similar characters (S/s, O/0)

### 2. davidbourrel/BOT-for-Last-War-vice-president
- **URL:** https://github.com/davidbourrel/BOT-for-Last-War-vice-president
- **Status:** DEPRECATED (game updated VP role)
- **Key Discovery: Anti-Bot System**
  - Last War has anti-bot modal dialogs
  - `CheckAndCloseAntiBotModal()` function needed
  - Tesseract OCR is unreliable for this game
  - Game updates can break bot completely
- **Tech:** PyAutoGUI, Pillow, OpenCV, Tesseract

### 3. bazmar59/lastWarAutoFL
- **URL:** https://github.com/bazmar59/lastWarAutoFL
- **Language:** Java (not Python)
- **Features:** Auto First Lady, crash recovery, stats tracking
- **Emulator:** BlueStacks

### 4. lastwarfirstladybot/lastwarfirstladybot
- **URL:** https://github.com/lastwarfirstladybot/lastwarfirstladybot
- **Tech:** PyAutoGUI + PIL + BlueStacks macros
- **Features:** First Lady role automation

### 5. rawrafied/LastWarBot
- **URL:** https://github.com/rawrafied/LastWarBot
- **Minimal info available**

## Roboflow Last War Dataset
- **URL:** https://universe.roboflow.com/last-war-survival-bot/last-war-survival-bot-2-vxotg
- **Images:** 522 open source gaming screenshots
- **Pre-trained model available**
- **Can be used to bootstrap YOLO training**

## Commercial Bots Analysis

### GnBots
- 30+ game support, 1M+ users claimed
- Free PC basic, paid mobile/cloud
- Image recognition based
- Update delays (2-5 days after patches)

### BoostBot
- $15/mo PC, $79/mo Cloud, $8/mo Farm-for-Me
- 30+ accounts supported
- 24h money-back guarantee
- Setup service included

### GodLikeBots
- Claims "0 bans" with human-like schedules
- 14-day refund policy
- Conservative approach (bot only, no mods)

### LastWar Bot (lastwarbot.com)
- Daily tasks, rallies, digs/eggs
- Stability-focused
- Auto-reopen after crash

### VOX Last War Bot (altcheats.com)
- Additional commercial option
- Limited public info

### FirstLadyBot (firstladybot.com)
- Specialized for First Lady/VP roles
- Separate commercial product

## Fast Screenshot Technologies

### adbblitz (FASTEST)
- **URL:** https://github.com/hansalemaos/adbblitz
- Raw scrcpy H264 stream → NumPy directly
- No scrcpy.exe needed, no root required
- ~5ms per frame
- USB and TCP support

### adbnativeblitz
- **URL:** https://github.com/hansalemaos/adbnativeblitz
- Native ADB screenshots at scrcpy speed
- ~10ms per frame
- Pure Python, NumPy arrays output

### py-scrcpy-client
- **URL:** https://leng-yue.github.io/py-scrcpy-client/
- Python wrapper for scrcpy protocol
- ~15ms per frame
- Event-based frame callbacks
- BGR NumPy ndarray output

### Standard ADB screencap
- ~200ms per frame (SLOW)
- Always available as fallback
- No additional dependencies

## YOLO Model Evolution

### YOLO26 (January 2026) - LATEST
- **Paper:** https://arxiv.org/abs/2509.25164
- NMS-free, DFL-free architecture
- 43% faster CPU inference than YOLO11
- Edge/mobile optimized
- Export: TFLite, CoreML, ONNX, TensorRT
- Nano variant: 38.9ms CPU, 1.7ms GPU, 40.9% mAP

### YOLO11 (2024)
- Enhanced CSPNet backbones
- Anchor-free detection
- Better than YOLOv8 on most benchmarks

### YOLOv8 (2023)
- Anchor-free, C2f module, decoupled head
- Most widely adopted, huge ecosystem
- Good for fine-tuning on game datasets

### Competitors
- **RF-DETR:** Superior accuracy, transformer-based
- **RT-DETR:** 53.1% AP at 108 FPS
- **YOLOv12:** Slightly slower but more accurate

## UI Detection Research

### VNIS Dataset (Mobile UI)
- 21 annotated UI element classes
- TextButton, UpperTaskBar, icons, etc.
- Ideal for training game UI detectors

### YOLOv8 for Mobile UI (2025 Study)
- Transfer learning from COCO-pretrained weights
- Precision 0.368→0.454, Recall 0.296→0.425
- Best for buttons and input fields
- Weak for ambiguous elements (iframes, labels)

## Anti-Cheat Analysis

### Last War's Defenses
1. **Anti-bot modal dialogs** - popup verification during suspicious activity
2. **Behavioral monitoring** - detects unnatural click patterns
3. **OCR resistance** - makes text hard to read for bots
4. **Game updates** - frequently changes UI to break bots

### Ban Enforcement
- GodLikeBots claims "0 bans, developers don't care"
- Official ToS explicitly prohibits bots
- Code of Conduct forbids "automation software, bots, hacks"
- Mixed signals: low enforcement but rules exist
- Community consensus: low risk if conservative

### Mitigation Strategies
1. Config-driven positions (easy update)
2. Multi-model fallback (YOLO26 → YOLOv8 → Template)
3. Anti-bot modal detection and handling
4. Human-like timing (Gaussian distribution)
5. Session patterns (play/break cycles)
6. Resource overflow prevention

## Key Technologies for Our Bot

### Recommended Stack (Updated)
| Component | Technology | Reason |
|-----------|-----------|--------|
| Screenshot | adbblitz/adbnativeblitz | 5-10ms, NumPy native |
| Detection | YOLO26 Nano | Edge-optimized, NMS-free |
| Fallback | Template matching + OCR | Always works |
| OCR | EasyOCR > Tesseract | More reliable |
| Control | ADB shell | Universal, no root |
| Config | JSON positions | Easy to update |
| Anti-bot | Modal detection + dismiss | Required for stability |

### Architecture Lessons from Open Source
1. **Config-driven design** (NotEnoughTina/FirstLady)
2. **Anti-bot handling** (davidbourrel)
3. **Modular routines** (secretary, donation, help)
4. **Crash recovery** (bazmar59)
5. **Interval-based scheduling** (not cron)
6. **Screenshot-based** (not injection)

## Sources
- [NotEnoughTina/FirstLady](https://github.com/NotEnoughTina/FirstLady)
- [davidbourrel/BOT-for-Last-War-vice-president](https://github.com/davidbourrel/BOT-for-Last-War-vice-president)
- [bazmar59/lastWarAutoFL](https://github.com/bazmar59/lastWarAutoFL)
- [Roboflow Last War Dataset](https://universe.roboflow.com/last-war-survival-bot/last-war-survival-bot-2-vxotg)
- [adbblitz](https://github.com/hansalemaos/adbblitz)
- [adbnativeblitz](https://github.com/hansalemaos/adbnativeblitz)
- [py-scrcpy-client](https://leng-yue.github.io/py-scrcpy-client/)
- [YOLO26 Paper](https://arxiv.org/abs/2509.25164)
- [Roboflow YOLO26 Blog](https://blog.roboflow.com/yolo26/)
- [VNIS UI Dataset Study](https://medium.com/@eslamelmishtawy/how-i-trained-yolov8-to-detect-mobile-ui-elements-using-the-vnis-dataset-f7f4b582fc09)
- [steve1316/android-cv-bot-template](https://github.com/steve1316/android-cv-bot-template)
- [GodLikeBots](https://godlikebots.com/last-war-survival-bot/)
- [BoostBot](https://boostbot.org/last-war-survival-bot/)
- [Last War Code of Conduct](https://lastwar-h5.lastwargame.com/app/code_conduct.html)
