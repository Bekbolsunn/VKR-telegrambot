from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline

from .models import Barber, WorkSchedule, Service, Client, Appointment, Promotion, Review


# ── Расписание (вложенная таблица внутри Барбера) ─────────────────────────
class WorkScheduleInline(TabularInline):
    model = WorkSchedule
    extra = 0
    fields = ("day_of_week", "is_working", "start_time", "end_time", "slot_duration")


# ── Барберы ───────────────────────────────────────────────────────────────
@admin.register(Barber)
class BarberAdmin(ModelAdmin):
    list_display = ("photo_preview", "name", "specialty", "rating_stars", "is_active", "total_appointments")
    list_filter = ("is_active",)
    search_fields = ("name", "specialty")
    inlines = [WorkScheduleInline]
    list_editable = ("is_active",)

    @admin.display(description="Фото")
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width:40px;height:40px;border-radius:50%;object-fit:cover">', obj.photo.url)
        return format_html('<div style="width:40px;height:40px;border-radius:50%;background:#6366f1;display:flex;align-items:center;justify-content:center;color:white;font-size:18px">✂</div>')

    @admin.display(description="Рейтинг")
    def rating_stars(self, obj):
        stars = "⭐" * round(float(obj.rating))
        return format_html('<span title="{}">{}</span>', obj.rating, stars)

    @admin.display(description="Записей")
    def total_appointments(self, obj):
        count = obj.appointment_set.count()
        return format_html('<b style="color:#a855f7">{}</b>', count)


# ── Расписание ────────────────────────────────────────────────────────────
@admin.register(WorkSchedule)
class WorkScheduleAdmin(ModelAdmin):
    list_display = ("barber", "get_day", "is_working", "start_time", "end_time", "slot_duration")
    list_filter = ("barber", "is_working")
    list_editable = ("is_working", "start_time", "end_time")

    @admin.display(description="День")
    def get_day(self, obj):
        return obj.get_day_of_week_display()


# ── Услуги ────────────────────────────────────────────────────────────────
@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ("name", "price_display", "duration_minutes", "is_active")
    list_filter = ("is_active",)
    list_editable = ("is_active",)
    search_fields = ("name",)

    @admin.display(description="Цена")
    def price_display(self, obj):
        return format_html('<b>{} сом</b>', obj.price)


# ── Клиенты ───────────────────────────────────────────────────────────────
@admin.register(Client)
class ClientAdmin(ModelAdmin):
    list_display = ("name", "phone", "loyalty_badge", "referral_code", "is_blocked", "created_at")
    list_filter = ("is_blocked", "language")
    list_editable = ("is_blocked",)
    search_fields = ("name", "phone", "telegram_id")
    readonly_fields = ("telegram_id", "created_at", "referral_code")

    @admin.display(description="Баллы")
    def loyalty_badge(self, obj):
        color = "#a855f7" if obj.loyalty_points >= 300 else "#6366f1"
        return format_html('<span style="background:{};color:white;padding:2px 8px;border-radius:12px">🏆 {}</span>', color, obj.loyalty_points)


# ── Записи ────────────────────────────────────────────────────────────────
@admin.register(Appointment)
class AppointmentAdmin(ModelAdmin):
    list_display = ("client", "barber", "service", "date", "time", "status", "payment_status", "status_badge", "payment_badge", "promo_code")
    list_filter = ("status", "payment_status", "barber", "date")
    list_editable = ("status", "payment_status")
    search_fields = ("client__name", "barber__name", "promo_code")
    date_hierarchy = "date"
    ordering = ("-date", "-time")

    @admin.display(description="Статус")
    def status_badge(self, obj):
        colors = {
            "pending":   "#f59e0b",
            "confirmed": "#10b981",
            "completed": "#6366f1",
            "cancelled": "#ef4444",
        }
        color = colors.get(obj.status, "#6b7280")
        return format_html(
            '<span style="background:{};color:white;padding:2px 10px;border-radius:12px;font-size:12px">{}</span>',
            color, obj.get_status_display()
        )

    @admin.display(description="Оплата")
    def payment_badge(self, obj):
        colors = {"unpaid": "#ef4444", "prepaid": "#f59e0b", "paid": "#10b981"}
        color = colors.get(obj.payment_status, "#6b7280")
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:12px;font-size:12px">{}</span>',
            color, obj.get_payment_status_display()
        )


# ── Акции 🇰🇬 ─────────────────────────────────────────────────────────────
@admin.register(Promotion)
class PromotionAdmin(ModelAdmin):
    list_display = ("title", "discount_badge", "promo_code", "start_date", "end_date", "is_active")
    list_filter = ("is_active",)
    list_editable = ("is_active",)
    search_fields = ("title", "promo_code")

    @admin.display(description="Скидка")
    def discount_badge(self, obj):
        return format_html(
            '<span style="background:#a855f7;color:white;padding:2px 10px;border-radius:12px;font-weight:bold">-{}%</span>',
            obj.discount_percent
        )


# ── Отзывы ────────────────────────────────────────────────────────────────
@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ("get_client", "rating_display", "get_barber", "text_preview", "created_at")
    list_filter = ("rating",)
    readonly_fields = ("appointment", "rating", "text", "created_at")

    @admin.display(description="Клиент")
    def get_client(self, obj):
        return obj.appointment.client

    @admin.display(description="Барбер")
    def get_barber(self, obj):
        return obj.appointment.barber

    @admin.display(description="Оценка")
    def rating_display(self, obj):
        return "⭐" * obj.rating

    @admin.display(description="Комментарий")
    def text_preview(self, obj):
        return (obj.text[:60] + "...") if len(obj.text) > 60 else obj.text or "—"
