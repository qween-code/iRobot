# Last War: Survival Game Bot - Detaylı Ürün Gereksinimleri Belgesi (PRD)

**Versiyon:** 4.0 (Güncellenmiş - 2025)
**Son Güncelleme:** 23 Kasım 2025
**Proje Kodu:** LastWarAutoBot Pro

---

## 📋 Yönetici Özeti

### Ürün Vizyonu
LastWarAutoBot Pro, Last War: Survival Game için yapay zeka destekli, açık kaynaklı bir otomasyon platformudur. YOLOv8 tabanlı görüntü tanıma, Docker konteynerizasyonu ve gelişmiş anti-ban algoritmaları ile oyun içi tekrarlayan görevleri otomatikleştirir.

### İş Değeri
- **Zaman Tasarrufu:** Manuel oynama süresini %85-95 azaltır
- **Kaynak Optimizasyonu:** 24/7 farming ile kaynak toplama %1000+ artış
- **Ölçeklenebilirlik:** Multi-account desteği (1-50+ hesap)
- **Topluluk Değeri:** Açık kaynak, özelleştirilebilir modüler yapı

### Hedef Pazar
- **Birincil:** İleri seviye oyuncular, alliance liderleri
- **İkincil:** Bot geliştiricileri, otomasyon meraklıları
- **Üçüncül:** Araştırmacılar, eğitim amaçlı kullanıcılar

### Kritik Riskler
⚠️ **UYARI:** Bu bot eğitim amaçlıdır. Last War'ın Terms of Service'ini ihlal eder ve kalıcı ban ile sonuçlanabilir.

---

## 🎮 Oyun Analizi

### Oyun Profili
- **Geliştirici:** FUNFLY PTE. LTD. (First Fun)
- **Tür:** Zombie Survival Strategy
- **Platform:** iOS, Android
- **Piyasa:** Global (özellikle Çin, ABD, Türkiye)
- **MAU (2025):** ~12M+
- **Yıllık Gelir:** $900M+

### Temel Oyun Döngüleri

#### 1. Kaynak Yönetimi (Zaman Dağılımı: %60)
**Kaynak Türleri:**
- **Temel:** Gold, Iron, Food
- **Gelişmiş:** Meteorite Iron, Spice, Quartz
- **Premium:** VIP Points, Speedups, Gems

**Toplama Yöntemleri:**
| Yöntem | Verim | Sıklık | Otomasyon Zorluğu |
|--------|-------|--------|-------------------|
| City Resource Production | Orta | 4-8 saat | Kolay |
| Mine Raiding | Yüksek | 6 atak/gün | Orta |
| Zombie Hunting | Çok Yüksek | Sınırsız (stamina) | Kolay |
| Events (Golden Zombies) | Ekstra Yüksek | Event süresi | Zor |

**2025 Güncellemeleri:**
- Meteorite Iron farming artık VIP 8+ gerektiriyor
- Resource overflow detection (anti-bot) eklendi
- Tile respawn timers randomize edildi

#### 2. Zombie Hunting (Zaman Dağılımı: %25)

**Zombie Türleri:**
```
Ironhead (Level 1-30)    → Iron + Courage Medals
Glutton (Level 1-30)     → Food + Hero EXP
Miser (Level 1-30)       → Gold + Alliance Points
Golden Zombies (Events)  → Massive rewards + Boss summons
```

**Hunting Döngüsü:**
1. Stamina check → 2. Deploy troops → 3. Battle → 4. Collect rewards → 5. Heal troops → 6. Repeat

**Bot İçin Kritik:**
- Monica herosu %39 bonus sağlar (her zaman deploy edilmeli)
- Optimal level selection (player level + 2-3)
- Stamina management (regenerasyon vs speedup kullanımı)

#### 3. Troop & Hero Sistemi (Zaman Dağılımı: %10)

**Troop Tipleri:**
- Infantry (Tank, yüksek HP)
- Rider (Hızlı, yüksek attack)
- Shooter (Range, AOE damage)

**Hero Sistemi:**
- **Rarities:** R < SR < SSR < UR
- **Kritik Herolar:** Monica (farming), Emma (PvE), Max (combat)
- **Gear Fusion:** 2025'te eklenen karmaşık UI (bot için challenge)

**Otomasyon Hedefleri:**
- Auto-train idle troops
- Auto-promote (resource threshold check)
- Auto-heal post-battle
- Hero EXP farming (campaign auto-replay)

#### 4. Base Building (Zaman Dağılımı: %5)

**Öncelik Sırası:**
1. HQ (max: Level 35, 2025)
2. Barracks, Hospital, Drill Ground
3. Walls (defense)
4. Academy (tech research)

**Speedup Stratejisi:**
- <5 dakika: Instant speedup
- 5-60 dakika: Alliance help bekleme
- >60 dakika: Speedup items (threshold-based)

---

## 🤖 Rakip Bot Analizi (2025 Güncellenmiş)

### Piyasa Durumu
- **Toplam Bot Sağlayıcı:** 12+ aktif
- **Fiyat Aralığı:** $0 (basic) - $79/ay (cloud premium)
- **Toplam Kullanıcı Tahmini:** 100K+
- **Ban Şikayet Oranı:** %15-30 (forumlara göre)

### Ana Rakipler

#### 1. GnBots
**Özellikler:**
- 30+ oyun desteği (multi-game platform)
- Auto gather, zombie hunt, troop management
- Rotation mode (multi-account switch)
- PC/Mobile/Cloud versiyonları

**Fiyatlandırma:**
- PC Basic: Free (limited features)
- Mobile: Abonelik ($15-25/ay, tahmin)

**Güçlü Yönler:**
- Geniş oyun desteği
- Büyük kullanıcı tabanı (1M+ iddia)
- Aktif support

**Zayıf Yönler:**
- Kapalı kaynak (no customization)
- Update gecikmeleri (oyun patch'lerinden 2-5 gün sonra)
- Ban reports var (TrustPilot'ta %5-10)

#### 2. BoostBot
**Özellikler:**
- Unlimited accounts (30+ PC'de test edilmiş)
- Advanced event sync (rallies, gold zombies)
- VIP auto-collect
- Setup service (müşteri desteği ile kurulum)

**Fiyatlandırma:**
- PC Pro: $15/ay
- Cloud: $79/ay
- Farm-for-Me Service: $8/ay

**Güçlü Yönler:**
- Professional topluluk (top players kullanıyor)
- 24/7 cloud infrastructure
- Money-back guarantee (24 saat)

**Zayıf Yönler:**
- Pahalı (özellikle cloud)
- Manuel setup hala gerekli
- Forum'da ban reports (nadir ama var)

#### 3. GodLikeBots
**Özellikler:**
- Human-like schedules (realistic intervals)
- "0 ban record" iddiası
- Zombie hunt + gather + gifts
- Cheat-free approach (sadece bot, mod yok)

**Fiyatlandırma:**
- Abonelik modeli
- 14 gün refund garantisi

**Güçlü Yönler:**
- Güvenlik odaklı marketing
- Etik positioning
- Realistic behavior patterns

**Zayıf Yönler:**
- Sınırlı feature set (events zayıf)
- Multi-game desteği yok
- Küçük topluluk

#### 4. LastWar Bot
**Özellikler:**
- Daily tasks, rallies, digs/eggs
- Gold zombie auto-join
- Stability focus (crash recovery)
- Auto-reopen (phone login after restart)

**Fiyatlandırma:**
- Belirsiz (muhtemelen $10-20/ay)

**Güçlü Yönler:**
- Oyuna özel optimizasyon
- Stability vurgusu

**Zayıf Yönler:**
- Limited reviews (küçük oyuncu)
- Feature set basic
- Advanced automation yok

### Piyasa Fırsatları

**Bizim Botun Avantajları:**
1. **Açık Kaynak:** Community customization, transparency
2. **AI-First:** YOLOv8 detection (rakipler basic template matching)
3. **Docker Native:** True multi-instance, resource efficiency
4. **Advanced Anti-Ban:** ML-based behavior learning
5. **Free/Self-Hosted:** No subscription lock-in

**Rekabet Stratejisi:**
- Open-source olarak trust kazanma
- Technical community'ye hitap etme
- Premium features için optional paid support
- Faster updates (community-driven)

---

## 🛠️ Teknik Mimari

### Sistem Bileşenleri

```
┌─────────────────────────────────────────────────────────────┐
│                     LastWarAutoBot Pro                       │
├─────────────────────────────────────────────────────────────┤
│  [Web Dashboard] ←→ [API Gateway] ←→ [Bot Orchestrator]    │
│                                              ↓               │
│                                    [Task Scheduler]          │
│                                         ↓   ↓   ↓            │
│                              [Bot Instance 1..N]             │
│                                         ↓                    │
│                            [Computer Vision Module]          │
│                              - YOLOv8 Detector               │
│                              - OpenCV Processor              │
│                              - Template Matcher              │
│                                         ↓                    │
│                            [Action Executor]                 │
│                              - ADB Controller                │
│                              - Input Randomizer              │
│                              - Anti-Ban Layer                │
│                                         ↓                    │
│                            [Emulator / Device]               │
│                              - LDPlayer                      │
│                              - NoxPlayer                     │
│                              - Real Device (ADB)             │
└─────────────────────────────────────────────────────────────┘
```

### Tech Stack

#### Core Technologies
| Katman | Teknoloji | Versiyon | Kullanım Nedeni |
|--------|-----------|----------|-----------------|
| Language | Python | 3.12+ | Ecosystem, ML kütüphaneleri |
| Containerization | Docker | 24.0+ | Isolation, scaling |
| Orchestration | Docker Compose / K8s | Latest | Multi-instance |
| CV Framework | OpenCV | 4.8+ | Image processing |
| AI/ML | PyTorch + YOLOv8 | 2.0+ / v8 | Object detection |
| Device Control | ADB / scrcpy | Latest | Android interaction |
| Web Framework | Flask + React | 3.0+ / 18+ | Dashboard |
| Database | PostgreSQL + Redis | 15+ / 7+ | State, caching |
| Monitoring | Prometheus + Grafana | Latest | Metrics, alerts |

#### Kütüphane Bağımlılıkları
```
# Core
opencv-python==4.8.1.78
numpy==1.24.3
pillow==10.0.0

# AI/ML
torch==2.1.0
torchvision==0.16.0
ultralytics==8.0.200  # YOLOv8

# Device Control
pure-python-adb==0.3.0.dev0
scrcpy-client==0.1.0

# Automation
pyautogui==0.9.54
pydirectinput==1.0.4

# Anti-Ban
scipy==1.11.3  # Gaussian distributions
faker==19.12.0  # Fake data generation

# Web & API
flask==3.0.0
flask-cors==4.0.0
flask-socketio==5.3.5
pydantic==2.5.0

# Database
psycopg2-binary==2.9.9
redis==5.0.1

# Utilities
pyyaml==6.0.1
python-dotenv==1.0.0
loguru==0.7.2
schedule==1.2.0
```

### Modüler Yapı

```
src/
├── core/
│   ├── bot_controller.py      # Ana bot orchestrator
│   ├── state_machine.py       # Karar motoru
│   └── task_scheduler.py      # Görev zamanlayıcı
├── vision/
│   ├── yolo_detector.py       # YOLOv8 entegrasyonu
│   ├── template_matcher.py    # OpenCV template matching
│   ├── ocr_reader.py          # Text detection (Tesseract)
│   └── ui_navigator.py        # UI element locator
├── actions/
│   ├── farming.py             # Resource gathering logic
│   ├── zombie_hunting.py      # Zombie hunt automation
│   ├── troop_management.py    # Train/heal/promote
│   ├── building.py            # Construct/upgrade
│   └── events.py              # Alliance/special events
├── device/
│   ├── adb_controller.py      # ADB command wrapper
│   ├── emulator_manager.py    # Emulator lifecycle
│   └── input_simulator.py     # Touch/swipe randomization
├── anti_ban/
│   ├── behavior_randomizer.py # Human-like patterns
│   ├── timing_variance.py     # Delay randomization
│   └── detection_avoider.py   # Anti-cheat countermeasures
├── models/
│   ├── game_state.py          # State models
│   ├── config.py              # Configuration schemas
│   └── analytics.py           # Metrics models
├── api/
│   ├── rest_api.py            # REST endpoints
│   └── websocket.py           # Real-time updates
└── utils/
    ├── logger.py              # Structured logging
    ├── metrics.py             # Performance tracking
    └── helpers.py             # Utility functions
```

---

## 🎯 Özellik Detayları

### 1. Core Otomasyon Özellikleri

#### A. Kaynak Farming
**Kullanıcı Hikayesi:**
> "Bir oyuncu olarak, botun otomatik olarak en verimli kaynak tile'larını bulup saldırmasını istiyorum, böylece manuel farming yapmak zorunda kalmam."

**Kabul Kriterleri:**
- [ ] Bot, haritada resource tiles'ı tespit edebilmeli (OpenCV + YOLO)
- [ ] Tile level'ı oyuncu gücüne göre seçmeli (düşük risk)
- [ ] Attack öncesi scout yapabilmeli (opsiyonel)
- [ ] Rally vs solo attack kararı verebilmeli
- [ ] 6 atak/gün limitini takip etmeli
- [ ] Troops full heal durumunda farming yapmamalı

**Teknik Uygulama:**
```python
class ResourceFarming:
    def __init__(self, vision_module, adb_controller):
        self.vision = vision_module
        self.adb = adb_controller
        self.attack_count = 0
        self.daily_limit = 6

    async def farm_resources(self, resource_type='iron', target_level=None):
        """
        Main farming loop
        """
        if self.attack_count >= self.daily_limit:
            logger.info("Daily attack limit reached")
            return

        # 1. Navigate to world map
        await self.navigate_to_map()

        # 2. Find optimal tile
        tile = await self.find_best_tile(resource_type, target_level)

        # 3. Attack
        if tile:
            await self.execute_attack(tile)
            self.attack_count += 1

        # 4. Return to city
        await self.return_to_city()

    async def find_best_tile(self, resource_type, target_level):
        """
        YOLO-based tile detection
        """
        # Screenshot
        screenshot = await self.adb.screenshot()

        # YOLO detection
        detections = self.vision.detect_tiles(screenshot, resource_type)

        # Filter by level and occupancy
        valid_tiles = [t for t in detections
                       if t.level <= target_level and not t.occupied]

        # Select closest or highest level
        return self.select_optimal_tile(valid_tiles)
```

**Anti-Ban Özellikleri:**
- Tile selection randomization (%20 variance)
- Attack timing variance (5-60 saniye random delay)
- Path randomization (farklı tile route'ları)

#### B. Zombie Hunting

**Kullanıcı Hikayesi:**
> "Bot, stamina'ya göre en uygun zombie type/level'ı otomatik seçip, troops deploy edip heal etsin."

**Kabul Kriterleri:**
- [ ] Zombie type selection (Ironhead/Glutton/Miser based on need)
- [ ] Level optimization (player level + 2-3 için max verim)
- [ ] Monica hero otomatik deploy
- [ ] Stamina threshold check (minimum %20 reserve)
- [ ] Post-battle auto-heal
- [ ] Courage Medal tracking

**Hunting Stratejisi:**
```python
class ZombieHunting:
    ZOMBIE_TYPES = {
        'ironhead': {'reward': 'iron', 'priority': 1},
        'glutton': {'reward': 'food', 'priority': 2},
        'miser': {'reward': 'gold', 'priority': 3}
    }

    async def hunt_loop(self, resource_priority=['iron', 'food', 'gold']):
        """
        Continuous hunting with stamina management
        """
        while True:
            # Check stamina
            stamina = await self.get_stamina()
            if stamina < self.config.min_stamina_threshold:
                logger.info("Low stamina, waiting...")
                await asyncio.sleep(300)  # 5 min
                continue

            # Select target
            zombie_type = self.select_zombie_by_priority(resource_priority)
            optimal_level = await self.calculate_optimal_level()

            # Execute hunt
            await self.deploy_troops(zombie_type, optimal_level, hero='Monica')
            await self.wait_for_battle_completion()
            await self.collect_rewards()
            await self.heal_troops()

            # Random delay (anti-ban)
            await self.random_delay(10, 60)

    def calculate_optimal_level(self):
        """
        Player level + 2-3 için en iyi verim/risk dengesi
        """
        player_level = self.get_player_level()
        return min(player_level + random.randint(2, 3), 30)
```

**Golden Zombie Event Automation:**
```python
async def golden_zombie_event(self):
    """
    Phase 1: Discovery (small zombies)
    Phase 2: Boss killing (coordinated rallies)
    """
    event_active = await self.check_event_status()

    if event_active:
        # Phase 1: Hunt small golden zombies
        for _ in range(20):  # Discovery phase
            await self.hunt_golden_zombie(boss=False)

        # Phase 2: Join rallies for bosses
        await self.auto_join_rallies(target='golden_boss', max_joins=10)
```

#### C. Troop Management

**Özellikler:**
1. **Auto-Train:**
   - Idle barracks detection
   - Resource threshold check (don't drain below 20%)
   - Balanced training (Infantry:Rider:Shooter = 1:1:1 veya custom ratio)

2. **Auto-Promote:**
   - Tier upgrade when resources available
   - Priority: Highest tier first

3. **Auto-Heal:**
   - Post-battle immediate heal
   - Speedup kullanımı (<5 min instant, >5 min wait)

```python
class TroopManager:
    async def manage_troops(self):
        """
        Comprehensive troop management
        """
        # 1. Heal wounded
        wounded = await self.get_wounded_count()
        if wounded > 0:
            await self.heal_all(use_speedup=wounded < 1000)

        # 2. Train idle barracks
        idle_barracks = await self.check_idle_barracks()
        if idle_barracks and self.has_sufficient_resources():
            await self.train_troops(ratio=self.config.troop_ratio)

        # 3. Promote if possible
        if await self.can_promote():
            await self.promote_troops()
```

### 2. Gelişmiş AI Özellikleri

#### A. YOLOv8 Nesne Tespiti

**Kullanım Alanları:**
1. **UI Element Detection:** Buttons, menus, pop-ups
2. **Game Object Detection:** Zombies, tiles, troops
3. **Dynamic UI Adaptation:** Oyun güncellemeleri sonrası otomatik adapte

**Model Eğitimi:**
```python
# Dataset hazırlama
# 1. Oyun screenshot'ları (1000+ çeşitli durumlar)
# 2. Roboflow ile annotation (buttons, tiles, zombies, vb.)
# 3. YOLOv8 fine-tuning

from ultralytics import YOLO

class GameVision:
    def __init__(self):
        # Pre-trained model yükle
        self.model = YOLO('models/lastwar_yolov8n.pt')

    def detect_elements(self, screenshot):
        """
        Detect all game UI elements
        """
        results = self.model(screenshot, conf=0.6)

        detections = []
        for r in results:
            boxes = r.boxes
            for box in boxes:
                detections.append({
                    'class': r.names[int(box.cls)],
                    'confidence': float(box.conf),
                    'bbox': box.xyxy[0].tolist()
                })

        return detections

    def find_button(self, screenshot, button_name):
        """
        Find specific button by name
        """
        detections = self.detect_elements(screenshot)
        buttons = [d for d in detections if d['class'] == button_name]

        if buttons:
            return buttons[0]['bbox']  # Return first match
        return None
```

**Avantajlar:**
- Template matching'e göre %40 daha hızlı
- UI değişikliklerine adaptif
- Partial occlusion'da bile çalışır

#### B. Karar Ağacı (State Machine)

```python
class BotStateMachine:
    """
    AI-driven decision making
    """
    def __init__(self):
        self.state = 'idle'
        self.priority_queue = PriorityQueue()

    async def decide_next_action(self):
        """
        Decision tree based on game state
        """
        game_state = await self.analyze_game_state()

        # Priority logic
        if game_state['resources_full']:
            return 'upgrade_buildings'
        elif game_state['troops_wounded'] > 1000:
            return 'heal_troops'
        elif game_state['stamina'] > 80:
            return 'hunt_zombies'
        elif game_state['daily_attacks'] < 6:
            return 'farm_resources'
        elif game_state['alliance_helps_available']:
            return 'collect_helps'
        else:
            return 'idle_tasks'  # VIP collect, quests, etc.

    async def analyze_game_state(self):
        """
        OCR + YOLO ile oyun durumunu analiz et
        """
        screenshot = await self.adb.screenshot()

        return {
            'resources_full': await self.check_resource_cap(screenshot),
            'troops_wounded': await self.ocr_wounded_count(screenshot),
            'stamina': await self.ocr_stamina(screenshot),
            'daily_attacks': self.get_attack_count_from_db(),
            'alliance_helps_available': await self.detect_notification_badge(screenshot)
        }
```

### 3. Anti-Ban Sistemi

#### A. Human Behavior Simulation

**Prensipler:**
1. **Timing Variance:** Gaussian distribution ile action delays
2. **Mouse Movement:** Bezier curves ile natural mouse paths
3. **Action Randomization:** %10-20 sapma ile action sequences
4. **Session Patterns:** Realistic play sessions (2-4 saat play, 1-2 saat break)

```python
class HumanBehavior:
    def __init__(self):
        self.session_start = time.time()
        self.actions_per_session = []

    def random_delay(self, min_sec=5, max_sec=60, distribution='gaussian'):
        """
        Human-like delays
        """
        if distribution == 'gaussian':
            mean = (min_sec + max_sec) / 2
            std = (max_sec - min_sec) / 6  # 99.7% within range
            delay = np.random.normal(mean, std)
            delay = np.clip(delay, min_sec, max_sec)
        else:
            delay = random.uniform(min_sec, max_sec)

        time.sleep(delay)

    def bezier_swipe(self, start, end, duration=0.5):
        """
        Natural swipe with Bezier curve
        """
        # Generate control points
        control1 = (
            start[0] + random.randint(-50, 50),
            start[1] + random.randint(-50, 50)
        )
        control2 = (
            end[0] + random.randint(-50, 50),
            end[1] + random.randint(-50, 50)
        )

        # Generate curve points
        points = self.calculate_bezier_curve(start, control1, control2, end, steps=20)

        # Execute swipe
        self.adb.swipe_along_path(points, duration)

    def should_take_break(self):
        """
        Decide if bot should pause (human-like session)
        """
        session_duration = time.time() - self.session_start

        # After 2-4 hours, take 30-120 min break
        if session_duration > random.uniform(7200, 14400):  # 2-4 hours
            break_duration = random.uniform(1800, 7200)  # 30-120 min
            logger.info(f"Taking human-like break for {break_duration/60:.1f} minutes")
            time.sleep(break_duration)
            self.session_start = time.time()
            return True

        return False
```

#### B. Detection Avoidance

**Tespit Edilen Anti-Cheat Mekanizmaları (2025):**
1. **Behavior Analytics:** Sabit interval detection
2. **RPC Monitoring:** Memory reading attempts
3. **Click Pattern Analysis:** Perfect pixel clicks
4. **Resource Overflow Detection:** Kaynak caps aşımı
5. **Captcha-like Events:** Random verification tasks

**Countermeasures:**
```python
class AntiCheatAvoider:
    def __init__(self):
        self.anomaly_score = 0
        self.max_anomaly_threshold = 100

    async def check_detection_risk(self):
        """
        Self-assessment of ban risk
        """
        risk_factors = {
            'constant_intervals': self.check_timing_variance(),
            'perfect_clicks': self.check_click_randomness(),
            '24_7_activity': self.check_session_breaks(),
            'resource_overflow': self.check_resource_caps()
        }

        self.anomaly_score = sum(risk_factors.values())

        if self.anomaly_score > self.max_anomaly_threshold:
            logger.warning("High detection risk! Pausing bot...")
            await self.emergency_pause()

    def check_resource_caps(self):
        """
        Ensure resources never overflow (anti-detection)
        """
        current_resources = self.get_current_resources()
        resource_caps = self.get_resource_caps()

        for resource, amount in current_resources.items():
            if amount > resource_caps[resource] * 0.8:  # 80% threshold
                logger.warning(f"{resource} near cap, prioritizing spending")
                return 50  # High risk score

        return 0
```

#### C. Network Masking

**Multi-Account Opsiyonları:**
- **Proxy Rotation:** Her hesap farklı IP
- **Device Fingerprinting:** Emulator device IDs randomize
- **Timing Stagger:** Hesaplar arası 5-30 dakika offset

```python
class MultiAccountManager:
    def __init__(self, accounts):
        self.accounts = accounts
        self.proxy_pool = self.load_proxies()

    async def run_accounts_staggered(self):
        """
        Run multiple accounts with staggered timing
        """
        for idx, account in enumerate(self.accounts):
            # Assign unique proxy
            proxy = self.proxy_pool[idx % len(self.proxy_pool)]

            # Stagger start time (0-30 min offset)
            delay = random.uniform(0, 1800)
            await asyncio.sleep(delay)

            # Launch bot instance
            await self.launch_bot_instance(account, proxy)

    async def launch_bot_instance(self, account, proxy):
        """
        Docker instance with unique network config
        """
        docker_config = {
            'image': 'lastwarautobot:latest',
            'environment': {
                'ACCOUNT_ID': account.id,
                'PROXY': proxy,
                'DEVICE_ID': self.generate_device_id()
            },
            'network_mode': 'bridge'
        }

        # Launch container
        container = await self.docker_client.containers.run(**docker_config)
        logger.info(f"Launched bot for account {account.username}")
```

---

## 📊 Non-Fonksiyonel Gereksinimler

### Performans
| Metrik | Hedef | Ölçüm Yöntemi |
|--------|-------|---------------|
| CPU Kullanımı | <20% per instance | `psutil` monitoring |
| RAM Kullanımı | <512MB per instance | Container stats |
| Response Time | <500ms (action decision) | Prometheus metrics |
| Uptime | 99%+ (24/7 operation) | Uptime monitoring |
| Concurrent Instances | 50+ (single server) | Load testing |

### Güvenlik
- **Encryption:** AES-256 for credentials
- **Secrets Management:** `.env` + Docker secrets
- **API Authentication:** JWT tokens
- **Rate Limiting:** 100 req/min per user
- **Audit Logging:** All actions logged

### Uyumluluk
**Desteklenen Platformlar:**
- Windows 10/11 (x64)
- macOS 12+ (Intel & Apple Silicon)
- Linux (Ubuntu 20.04+, Debian 11+)

**Emulator Uyumluluğu:**
- LDPlayer 4.0+
- NoxPlayer 7.0+
- BlueStacks 5.0+ (experimental)
- Headless Android (via Anbox)

---

## 🗺️ Yol Haritası (6 Aylık)

### Faz 1: Araştırma & Prototip (Hafta 1-3)
**Hedefler:**
- Oyun UI mapping (1000+ screenshot dataset)
- Rakip bot reverse engineering
- Anti-cheat mekanizma analizi
- Proof-of-concept (basic gather + hunt)

**Deliverables:**
- Technical design document
- YOLOv8 initial model (50%+ accuracy)
- Docker dev environment

### Faz 2: Core Development (Hafta 4-10)
**Sprint 1 (Hafta 4-5):** Device control layer
- ADB wrapper
- Emulator lifecycle management
- Screenshot pipeline

**Sprint 2 (Hafta 6-7):** Vision module
- OpenCV template matching
- YOLOv8 integration
- OCR for text reading

**Sprint 3 (Hafta 8-10):** Core automation
- Resource farming
- Zombie hunting
- Troop management

**Milestones:**
- [ ] Bot can auto-farm resources (6 attacks/day)
- [ ] Bot can hunt zombies (stamina-based loop)
- [ ] Bot can heal/train troops

### Faz 3: Advanced Features (Hafta 11-16)
**Sprint 4 (Hafta 11-12):** AI decision engine
- State machine implementation
- Priority queue system
- ML-based hero selection

**Sprint 5 (Hafta 13-14):** Multi-account scaling
- Docker Compose orchestration
- Account rotation
- Proxy integration

**Sprint 6 (Hafta 15-16):** Anti-ban enhancements
- Behavior randomization
- Session patterns
- Detection risk monitoring

**Milestones:**
- [ ] Bot can run 10+ accounts simultaneously
- [ ] Anti-ban score <30% detection risk
- [ ] 24/7 operation without crashes

### Faz 4: Web Dashboard (Hafta 17-20)
**Features:**
- Real-time account monitoring
- Resource gain charts
- Bot control (start/stop/config)
- Alert notifications (Telegram/Discord)

**Tech Stack:**
- Backend: Flask + Flask-SocketIO
- Frontend: React + TailwindCSS
- Database: PostgreSQL + Redis

### Faz 5: Testing & Hardening (Hafta 21-23)
**Testing Types:**
- Unit tests (80%+ coverage)
- Integration tests (emulator environments)
- Stress tests (50 concurrent instances)
- Security audit (penetration testing)

**Ban Simulation:**
- Intentional risky behavior to trigger anti-cheat
- Analyze detection patterns
- Refine anti-ban algorithms

### Faz 6: Deployment & Maintenance (Hafta 24+)
**Launch Checklist:**
- [ ] GitHub release (v1.0.0)
- [ ] Documentation (setup guides, API docs)
- [ ] Docker Hub images
- [ ] Community setup (Discord, forum)

**Ongoing:**
- Monthly game update adaptations
- Community feature requests
- Bug fixes
- Model retraining (quarterly)

---

## 💰 Maliyet & Kaynak Tahmini

### Geliştirme Maliyetleri
| Kalem | Miktar | Birim Fiyat | Toplam |
|-------|--------|-------------|--------|
| Senior Dev (6 ay) | 1 FTE | $8K/ay | $48K |
| ML Engineer (3 ay) | 0.5 FTE | $10K/ay | $15K |
| QA Tester (2 ay) | 0.5 FTE | $5K/ay | $5K |
| Cloud Infrastructure | 6 ay | $200/ay | $1.2K |
| Emulator Licenses | - | - | $0 (free) |
| **TOPLAM** | | | **$69.2K** |

### İşletme Maliyetleri (Aylık, 1000 kullanıcı)
- Server Costs: $500/ay (AWS EC2 + RDS)
- Bandwidth: $100/ay
- Monitoring/Logging: $50/ay
- **TOPLAM:** $650/ay

### Revenue Potansiyeli (Opsiyonel)
**Model 1: Freemium**
- Basic: Free (self-hosted, limited features)
- Pro: $15/ay (cloud-hosted, unlimited accounts)
- Enterprise: $50/ay (priority support, custom features)

**Tahmini Revenue (1000 kullanıcı, %10 conversion):**
- 900 Free: $0
- 80 Pro: $1,200/ay
- 20 Enterprise: $1,000/ay
- **TOPLAM:** $2,200/ay

**Alternatif: Tamamen Açık Kaynak + Sponsorship**
- GitHub Sponsors: $500-2000/ay (community bağlı)
- Consulting/Support: $1000+/ay

---

## ⚖️ Yasal & Etik Considerations

### Terms of Service İhlali
**Last War ToS (Özetle):**
> "Third-party software, bots, or any automated tools are strictly prohibited and may result in permanent account bans and legal action."

**Sonuçlar:**
- **Kullanıcı Hesap Ban:** %70+ tespit riski (24/7 kullanımda)
- **IP/Device Ban:** Muhtemel (multi-account durumunda)
- **Yasal Risk:** Düşük (genelde civil, ban ile sınırlı)

### Etik Kullanım Kılavuzu
**Bu botu kullanmadan önce:**
1. **Eğitim Amaçlı:** Sadece öğrenme için kullanın
2. **Kendi Hesap:** Başkalarının hesaplarını botlamayın
3. **Finansal Risk Kabul:** Para harcadıysanız, ban riski bilinci
4. **Topluluk:** Oyun dengesini bozmayın (fair play)

**Önerilen Kullanım:**
- Offline test environments
- Private servers (mümkünse)
- Minimal usage (test accounts only)

### Open Source Disclaimer
```
MIT License

Copyright (c) 2025 LastWarAutoBot Contributors

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
USE AT YOUR OWN RISK. AUTHORS ARE NOT RESPONSIBLE FOR BANS,
ACCOUNT LOSS, OR ANY DAMAGES ARISING FROM USE OF THIS SOFTWARE.

THIS SOFTWARE IS FOR EDUCATIONAL PURPOSES ONLY.
USING BOTS IN LAST WAR: SURVIVAL VIOLATES THE GAME'S TERMS OF SERVICE.
```

---

## 📚 Ek Kaynaklar

### Araştırma Kaynakları
1. **Bot Providers:**
   - [BoostBot Last War Bot](https://boostbot.org/last-war-survival-bot/)
   - [GnBots Last War Bot](https://www.gnbots.com/shop/last-war-survival-bot/)
   - [GodLikeBots Last War Bot](https://godlikebots.com/last-war-survival-bot/)
   - [LastWar Bot Official](https://lastwarbot.com/)

2. **Oyun Stratejileri:**
   - [Last War Handbook - Golden Zombies Guide](https://lastwarhandbook.com/guides/golden-zombies-event-guide)
   - [Last War Resource Raiding Guide 2025](https://lootbar.gg/blog/en/last-war-resource-raiding-guide-how-to-farm-smarter-in-2025.html)
   - [BlueStacks Tips & Tricks](https://www.bluestacks.com/blog/game-guides/last-warsurvival-game/lws-tips-tricks-en.html)

3. **Teknik Referanslar:**
   - [Master Mobile Game Automation with Python](https://www.toolify.ai/ai-news/master-mobile-game-automation-with-python-and-opencv-2852)
   - [OpenCV Game Bot (GitHub)](https://github.com/mibho/autoclient)
   - [YOLOv8 Android Integration](https://github.com/ultralytics/ultralytics/pull/5251/files)

4. **Anti-Cheat Analizi:**
   - [Last War Cheats Analysis](https://godlikebots.com/last-war-survival-cheats-hacks/)
   - [FearLess Cheat Engine Forum](https://fearlessrevolution.com/viewtopic.php?t=28717)

### Topluluk Kaynakları
- **Discord:** (TBD - proje launch sonrası)
- **GitHub Discussions:** Issue tracking, feature requests
- **Reddit:** r/lastwarsurvival (unofficial, risk reports)

---

## 📝 Değişiklik Geçmişi

### v4.0 (23 Kasım 2025)
- ✅ 2025 piyasa araştırması eklendi
- ✅ Güncel rakip bot analizi (GnBots, BoostBot, vb.)
- ✅ YOLOv8 entegrasyonu detaylandırıldı
- ✅ Anti-ban stratejileri güncellendi
- ✅ Yol haritası 6 aya yayıldı
- ✅ Maliyet analizi eklendi

### v3.0 (Önceki Versiyon)
- Temel PRD yapısı
- Oyun mekaniklerinin dökümantasyonu
- İlk teknik spesifikasyonlar

---

## 🎯 Sonuç

LastWarAutoBot Pro, açık kaynak felsefesi ile gelişmiş AI teknolojilerini birleştiren, piyasadaki en kapsamlı Last War otomasyon çözümü olmayı hedefliyor.

**Başarı Kriterleri:**
1. ✅ %95+ otomasyon (manuel müdahale minimal)
2. ✅ <30% ban riski (advanced anti-ban ile)
3. ✅ 50+ concurrent instances (tek server'da)
4. ✅ 1000+ GitHub stars (ilk 6 ayda)
5. ✅ Active community (100+ contributors)

**Gelecek Vizyonu:**
- Multi-game support (State of Survival, Last Shelter, vb.)
- AI-as-a-Service (cloud-based bot hosting)
- Academic partnerships (game automation research)

---

**⚠️ SON UYARI:** Bu belge, teknik bir referans ve eğitim materyalidir. Gerçek uygulamada ban riskinizi bilmeli ve sorumluluğu kabul etmelisiniz. Etik ve yasal sınırlar içinde hareket edin.

**Hazırlayan:** LastWarAutoBot Contributors
**İletişim:** GitHub Issues
**Lisans:** MIT (Educational Use Only)
