from django.core.validators import MinValueValidator
from django.db import models


class Customer(models.Model):
    customer_id = models.BigAutoField(primary_key=True)

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=30)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class TableCategory(models.Model):
    table_category_id = models.BigAutoField(primary_key=True)

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    capacity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Table(models.Model):
    table_id = models.BigAutoField(primary_key=True)

    table_number = models.CharField(
        max_length=20,
        unique=True
    )

    table_category = models.ForeignKey(
        TableCategory,
        on_delete=models.PROTECT,
        related_name="tables"
    )

    capacity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["table_number"]

    def __str__(self):
        return f"Table {self.table_number}"


class ReservationStatus(models.Model):
    reservation_status_id = models.BigAutoField(
        primary_key=True
    )

    name = models.CharField(
        max_length=50,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Reservation(models.Model):
    reservation_id = models.BigAutoField(
        primary_key=True
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="reservations"
    )

    table = models.ForeignKey(
        Table,
        on_delete=models.PROTECT,
        related_name="reservations"
    )

    status = models.ForeignKey(
        ReservationStatus,
        on_delete=models.PROTECT,
        related_name="reservations"
    )

    reservation_date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    number_of_guests = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "reservation_date",
            "start_time"
        ]

        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    number_of_guests__gte=1
                ),
                name="reservation_guests_positive"
            )
        ]

    def __str__(self):
        return (
            f"Reservation #{self.reservation_id} - "
            f"{self.customer} - "
            f"{self.reservation_date}"
        )


class Payment(models.Model):
    payment_id = models.BigAutoField(
        primary_key=True
    )

    reservation = models.OneToOneField(
        Reservation,
        on_delete=models.CASCADE,
        related_name="payment"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_status = models.CharField(
        max_length=50
    )

    payment_method = models.CharField(
        max_length=50,
        blank=True
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"Payment #{self.payment_id} "
            f"for Reservation #{self.reservation_id}"
        )


class AuditLog(models.Model):
    audit_log_id = models.BigAutoField(
        primary_key=True
    )

    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name="audit_logs"
    )

    action = models.CharField(
        max_length=100
    )

    details = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.action} - "
            f"Reservation #{self.reservation_id}"
        )
