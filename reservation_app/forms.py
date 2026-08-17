from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from .models import (
    Customer,
    TableCategory,
    Table,
    ReservationStatus,
    Reservation,
    Payment,
)


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer

        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
        ]

        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email Address",
            "phone": "Phone Number",
        }


class TableCategoryForm(forms.ModelForm):

    class Meta:
        model = TableCategory

        fields = [
            "name",
            "description",
            "capacity",
        ]

        labels = {
            "name": "Category Name",
            "description": "Description",
            "capacity": "Table Capacity",
        }

        widgets = {
            "capacity": forms.NumberInput(
                attrs={
                    "min": 1
                }
            )
        }


class TableForm(forms.ModelForm):

    class Meta:
        model = Table

        fields = [
            "table_number",
            "table_category",
            "capacity",
            "is_active",
        ]

        labels = {
            "table_number": "Table Number",
            "table_category": "Table Category",
            "capacity": "Capacity",
            "is_active": "Active",
        }

        widgets = {
            "capacity": forms.NumberInput(
                attrs={
                    "min": 1
                }
            )
        }


class ReservationStatusForm(forms.ModelForm):

    class Meta:
        model = ReservationStatus

        fields = [
            "name",
            "description",
        ]

        labels = {
            "name": "Status Name",
            "description": "Description",
        }


class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation

        fields = [
            "customer",
            "table",
            "status",
            "reservation_date",
            "start_time",
            "end_time",
            "number_of_guests",
            "notes",
        ]

        labels = {
            "customer": "Customer",
            "table": "Table",
            "status": "Reservation Status",
            "reservation_date": "Reservation Date",
            "start_time": "Start Time",
            "end_time": "End Time",
            "number_of_guests": "Number of Guests",
            "notes": "Notes",
        }

        widgets = {
            "reservation_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "start_time": forms.TimeInput(
                attrs={
                    "type": "time"
                },
                format="%H:%M"
            ),

            "end_time": forms.TimeInput(
                attrs={
                    "type": "time"
                },
                format="%H:%M"
            ),

            "number_of_guests": forms.NumberInput(
                attrs={
                    "min": 1
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "rows": 3
                }
            ),
        }

    def clean_number_of_guests(self):

        guests = self.cleaned_data.get(
            "number_of_guests"
        )

        if guests is None or guests < 1:
            raise ValidationError(
                "Number of guests must be at least 1."
            )

        return guests

    def clean(self):

        cleaned_data = super().clean()

        reservation_date = cleaned_data.get(
            "reservation_date"
        )

        start_time = cleaned_data.get(
            "start_time"
        )

        end_time = cleaned_data.get(
            "end_time"
        )

        table = cleaned_data.get(
            "table"
        )

        guests = cleaned_data.get(
            "number_of_guests"
        )

        # Validate time
        if start_time and end_time:

            if end_time <= start_time:

                self.add_error(
                    "end_time",
                    "End time must be later than start time."
                )

        # Validate table capacity
        if table and guests:

            if guests > table.capacity:

                self.add_error(
                    "number_of_guests",
                    (
                        f"This table can only "
                        f"accommodate "
                        f"{table.capacity} guests."
                    )
                )

        # Prevent overlapping reservations
        if (
            reservation_date
            and start_time
            and end_time
            and table
        ):

            overlapping = Reservation.objects.filter(
                table=table,
                reservation_date=reservation_date
            ).filter(
                Q(start_time__lt=end_time)
                &
                Q(end_time__gt=start_time)
            )

            # Exclude current reservation when editing
            if self.instance.pk:

                overlapping = overlapping.exclude(
                    pk=self.instance.pk
                )

            if overlapping.exists():

                raise ValidationError(
                    "This table is already reserved "
                    "during the selected time."
                )

        return cleaned_data


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment

        fields = [
            "reservation",
            "amount",
            "payment_status",
            "payment_method",
            "paid_at",
        ]

        labels = {
            "reservation": "Reservation",
            "amount": "Amount",
            "payment_status": "Payment Status",
            "payment_method": "Payment Method",
            "paid_at": "Paid At",
        }

        widgets = {
            "amount": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0"
                }
            ),

            "paid_at": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local"
                }
            ),
        }