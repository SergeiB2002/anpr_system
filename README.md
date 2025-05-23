# ANPR System
Автоматизированная система распознавания автомобильных номеров (ANPR) на Python

## Описание
Проект предназначен для видеозахвата RTSP-потока с IP-камер, обнаружения автомобильных номеров, их распознавания и управления доступом (шлагбаум, аудиоподсказки). Также ведётся логирование, верификация по базе данных и ежедневная генерация отчётов.

**Ключевые возможности:**
- Захват и предварительная обработка видео (стабилизация, коррекция яркости, выделение номера)
- Детекция и OCR номерных знаков (YOLOv8 + Tesseract)
- Верификация по базе PostgreSQL (blacklist, access_rules)
- Управление шлагбаумом через GPIO и аудиоподсказки
- Генерация PDF/XLSX-отчетов и веб-дашборд
- Развёртывание в Docker

## Структура проекта
anpr_system/  
├── docker-compose.yml  
├── Dockerfile  
├── requirements.txt  
├── entrypoint.py  
├── config/  
│   ├── config.yaml  
│   └── camera_settings.yml  
├── modules/  
│   ├── video_capture/  
│   │   ├── capture.py  
│   │   ├── preprocessing.py  
│   │   └── metrics.py  
│   ├── ocr_engine/  
│   │   ├── detection.py  
│   │   ├── recognition.py  
│   │   └── postprocessing.py  
│   ├── db_manager/  
│   │   ├── models.py  
│   │   └── crud.py  
│   ├── access_control/  
│   │   ├── control.py  
│   │   └── notificator.py  
│   └── reporting/  
│       ├── report_generator.py  
│       └── dashboard.py  
└── scripts/  
    └── init_db.sql  

## Описание модулей
- video_capture: захват и предобработка кадра, вычисление метрик качества
- ocr_engine: детекция знака (YOLOv8), распознавание (Tesseract), постобработка
- db_manager: модели SQLAlchemy, CRUD-операции, верификация по blacklist и access_rules
- access_control: управление GPIO-шлагбаумом, аудиоподсказки
- reporting: генерация PDF/XLSX-отчетов, веб-дашборд на FastAPI + Plotly

## Установка
1. Клонировать репозиторий:
   ```git clone https://github.com/<ваш-пользователь>/anpr_system.git
      cd anpr_system```

2. Настроить переменные окружения в .env или через docker-compose.yml:
   ```DATABASE_URL=postgresql://user:pass@db:5432/anpr_db
   RTSP_URL=rtsp://camera/stream
   LIGHT_SENSOR_ENDPOINT=http://sensor.local```

3. Запустить в Docker:
   ```docker-compose up --build -d```

4. Перейти по адресу http://localhost:8000/health для проверки статуса API.



