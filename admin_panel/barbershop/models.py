from django.db import models


class Barber(models.Model):
    name = models.CharField("Имя", max_length=100)
    specialty = models.CharField("Специализация", max_length=200, default="Стрижки")
    photo = models.ImageField("Фото", upload_to="barbers/", blank=True, null=True)
    telegram_id = models.BigIntegerField("Telegram ID", blank=True, null=True)
    is_active = models.BooleanField("Активен", default=True)
    rating = models.DecimalField("Рейтинг", max_digits=3, decimal_places=1, default=5.0)

    class Meta:
        verbose_name = "Барбер"
        verbose_name_plural = "Барберы"

    def __str__(self):
        return self.name


class WorkSchedule(models.Model):
    DAYS = [
        (0, "Понедельник"), (1, "Вторник"), (2, "Среда"),
        (3, "Четверг"), (4, "Пятница"), (5, "Суббота"), (6, "Воскресенье"),
    ]
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name="schedules", verbose_name="Барбер")
    day_of_week = models.IntegerField("День недели", choices=DAYS)
    start_time = models.TimeField("Начало работы", default="10:00")
    end_time = models.TimeField("Конец работы", default="20:00")
    slot_duration = models.IntegerField("Длит. слота (мин)", default=30)
    is_working = models.BooleanField("Рабочий день", default=True)

    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписание"
        unique_together = ("barber", "day_of_week")

    def __str__(self):
        return f"{self.barber} — {self.get_day_of_week_display()}"


class Service(models.Model):
    name = models.CharField("Название", max_length=200)
    price = models.IntegerField("Цена (сом)")
    duration_minutes = models.IntegerField("Длительность (мин)", default=30)
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги (Прайс)"

    def __str__(self):
        return f"{self.name} — {self.price} сом"


class Client(models.Model):
    telegram_id = models.BigIntegerField("Telegram ID", unique=True)
    name = models.CharField("Имя", max_length=200)
    phone = models.CharField("Телефон", max_length=30, blank=True)
    language = models.CharField("Язык", max_length=5, default="ru")
    loyalty_points = models.IntegerField("Баллы лояльности", default=0)
    referral_code = models.CharField("Реф. код", max_length=20, blank=True)
    is_blocked = models.BooleanField("Заблокирован", default=False)
    created_at = models.DateTimeField("Дата регистрации", auto_now_add=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return f"{self.name} ({self.telegram_id})"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("pending",   "⏳ Ожидает"),
        ("confirmed", "✅ Подтверждено"),
        ("completed", "💈 Завершено"),
        ("cancelled", "❌ Отменено"),
    ]
    PAYMENT_CHOICES = [
        ("unpaid",    "💵 Не оплачено"),
        ("prepaid",   "💳 Предоплата"),
        ("paid",      "✅ Оплачено"),
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Клиент")
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, verbose_name="Барбер")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Услуга")
    date = models.DateField("Дата")
    time = models.TimeField("Время")
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default="pending")
    payment_status = models.CharField("Оплата", max_length=20, choices=PAYMENT_CHOICES, default="unpaid")
    promo_code = models.CharField("Промокод", max_length=20, blank=True)
    notes = models.TextField("Заметки", blank=True)
    created_at = models.DateTimeField("Создана", auto_now_add=True)

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        ordering = ["-date", "-time"]

    def __str__(self):
        return f"{self.client} → {self.barber} | {self.date} {self.time}"


# ★ УНИКАЛЬНЫЕ МОДЕЛИ ДЛЯ КР ★

class Promotion(models.Model):
    title = models.CharField("Название акции", max_length=200)
    description = models.TextField("Описание")
    discount_percent = models.IntegerField("Скидка (%)", default=10)
    promo_code = models.CharField("Промокод", max_length=20, unique=True)
    start_date = models.DateField("Начало")
    end_date = models.DateField("Конец")
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции 🎁"

    def __str__(self):
        return f"{self.title} ({self.discount_percent}%)"


class Review(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, verbose_name="Запись")
    rating = models.IntegerField("Оценка (1-5)", default=5)
    text = models.TextField("Комментарий", blank=True)
    created_at = models.DateTimeField("Дата отзыва", auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы ⭐"

    def __str__(self):
        return f"{'⭐' * self.rating} — {self.appointment.client}"
