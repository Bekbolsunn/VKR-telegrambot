# BarberBoss Bishkek — Telegram Bot + Django Admin

ВКР: «Разработка Telegram-бота для автоматизации онлайн-записи клиентов в барбершоп»
Автор: Каратай уулу Бекболсун

---

## Быстрый старт

### 1. Установка зависимостей

```bash
pip3 install -r requirements.txt
```

### 2. Запуск Telegram бота

```bash
# Скопируй .env файл
cp .env.example .env

# Вставь токен бота (получить у @BotFather)
# Открой .env и заполни BOT_TOKEN=...

# Запуск
cd bot
python3 main.py
```

### 3. Запуск Django Admin панели

```bash
cd admin_panel

# Создать таблицы БД
python3 manage.py migrate

# Загрузить тестовые данные
python3 manage.py loaddata barbershop/fixtures/sample_data.json

# Создать администратора
python3 manage.py createsuperuser

# Запустить сервер
python3 manage.py runserver
```

Открыть: http://127.0.0.1:8000/admin/

---

## Структура проекта

```
barber-telegram/
├── bot/
│   ├── main.py              # Точка входа бота
│   ├── config.py            # Настройки и моковые данные
│   ├── handlers/
│   │   ├── start.py         # Модуль 1: Запуск и регистрация
│   │   ├── price.py         # Модуль 2: Прайс
│   │   ├── booking.py       # Модуль 3: Запись к барберу
│   │   ├── my_bookings.py   # Модуль 5: Управление записями
│   │   ├── promotions.py    # ★ КР: Акции и скидки
│   │   ├── loyalty.py       # ★ КР: Система лояльности + реферал
│   │   ├── gallery.py       # ★ КР: Галерея стрижек
│   │   ├── location.py      # ★ КР: Геолокация
│   │   └── reviews.py       # ★ КР: Отзывы после визита
│   └── keyboards/
│       └── inline.py        # Все inline-клавиатуры
│
└── admin_panel/
    ├── manage.py
    ├── core/
    │   ├── settings.py      # Django + Unfold тема
    │   └── urls.py
    └── barbershop/
        ├── models.py        # Все модели БД
        ├── admin.py         # Настройка Django Admin
        └── fixtures/
            └── sample_data.json  # Тестовые данные
```

---

## Уникальные функции для рынка КР 🇰🇬

| Функция | Описание |
|---|---|
| 🎁 Система лояльности | Баллы за каждый визит (1 сом = 1 балл) |
| 👥 Реферальная программа | Приведи друга — получи 150 баллов |
| 📅 Праздничные акции | Нооруз (-21%), 8 марта, День независимости (-31%) |
| 💳 Мобильные платежи | Mbank / O!Pay / Elsom предоплата |
| ⭐ Отзывы | Авто-запрос через 1 час после визита |
| 📸 Галерея стрижек | Референсы: Классика, Фейд, Борода, Дизайн |
| 📍 Геолокация | Адрес + навигатор (2GIS, Google Maps) |
