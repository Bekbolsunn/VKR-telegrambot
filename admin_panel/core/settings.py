from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-barber-boss-bishkek-2026"
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    # Unfold ОБЯЗАТЕЛЬНО перед django.contrib.admin
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "barbershop",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Asia/Bishkek"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ══════════════════════════════════════════════════════════════
#  UNFOLD — настройка темы
# ══════════════════════════════════════════════════════════════
from django.urls import reverse_lazy

UNFOLD = {
    "SITE_TITLE": "BarberBoss Bishkek",
    "SITE_HEADER": "BarberBoss Admin",
    "SITE_SUBHEADER": "Панель управления барбершопом",
    "SITE_URL": "/",
    "SITE_ICON": None,
    "SITE_SYMBOL": "content_cut",          # Material icon
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": False,
    "THEME": "light",                        # dark / light
    "COLORS": {
        "primary": {
            "50":  "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7  100",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "Главная",
                "separator": False,
                "items": [
                    {
                        "title": "Дашборд",
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": "Записи",
                "separator": True,
                "items": [
                    {
                        "title": "Все записи",
                        "icon": "calendar_month",
                        "link": reverse_lazy("admin:barbershop_appointment_changelist"),
                    },
                    {
                        "title": "Клиенты",
                        "icon": "people",
                        "link": reverse_lazy("admin:barbershop_client_changelist"),
                    },
                ],
            },
            {
                "title": "Барберы",
                "separator": True,
                "items": [
                    {
                        "title": "Барберы",
                        "icon": "content_cut",
                        "link": reverse_lazy("admin:barbershop_barber_changelist"),
                    },
                    {
                        "title": "Расписание",
                        "icon": "schedule",
                        "link": reverse_lazy("admin:barbershop_workschedule_changelist"),
                    },
                ],
            },
            {
                "title": "Услуги и акции",
                "separator": True,
                "items": [
                    {
                        "title": "Услуги (Прайс)",
                        "icon": "payments",
                        "link": reverse_lazy("admin:barbershop_service_changelist"),
                    },
                    {
                        "title": "Акции",
                        "icon": "local_offer",
                        "link": reverse_lazy("admin:barbershop_promotion_changelist"),
                    },
                    {
                        "title": "Отзывы",
                        "icon": "star",
                        "link": reverse_lazy("admin:barbershop_review_changelist"),
                    },
                ],
            },
        ],
    },
}
