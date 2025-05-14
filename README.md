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
│   ├── ocr_engine/  
│   ├── db_manager/  
│   ├── access_control/  
│   └── reporting/  
└── scripts/  
    └── init_db.sql  

## Описание модулей
- video_capture: захват и предобработка кадра, вычисление метрик качества
- ocr_engine: детекция знака (YOLOv8), распознавание (Tesseract), постобработка
- db_manager: модели SQLAlchemy, CRUD-операции, верификация по blacklist и access_rules
- access_control: управление GPIO-шлагбаумом, аудиоподсказки
- reporting: генерация PDF/XLSX-отчетов, веб-дашборд на FastAPI + Plotly
