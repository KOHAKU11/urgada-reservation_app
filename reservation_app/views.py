import json

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.db.models import Q

from .models import (
    Customer,
    TableCategory,
    Table,
    ReservationStatus,
    Reservation,
    Payment,
    AuditLog,
)

from .forms import (
    CustomerForm,
    TableCategoryForm,
    TableForm,
    ReservationStatusForm,
    ReservationForm,
    PaymentForm,
)


def get_data(request):

    if request.content_type == "application/json":

        try:
            return json.loads(
                request.body.decode("utf-8")
                or "{}"
            )

        except json.JSONDecodeError:

            return {}

    return request.POST


def form_error(form, message):

    return JsonResponse(
        {
            "success": False,
            "message": message,
            "errors": form.errors.get_json_data(),
        },
        status=400,
    )


# ==========================================================
# CUSTOMER
# ==========================================================

@require_http_methods(["GET", "POST"])
def customer_list(request):

    if request.method == "GET":

        customers = Customer.objects.all()

        data = list(
            customers.values(
                "customer_id",
                "first_name",
                "last_name",
                "email",
                "phone",
                "created_at",
                "updated_at",
            )
        )

        return JsonResponse(
            {
                "customers": data
            }
        )

    form = CustomerForm(
        get_data(request)
    )

    if form.is_valid():

        customer = form.save()

        return JsonResponse(
            {
                "success": True,
                "message": "Customer created.",
                "customer_id": customer.pk,
            },
            status=201,
        )

    return form_error(
        form,
        "Invalid customer data."
    )


@require_http_methods(
    ["GET", "PUT", "PATCH", "POST", "DELETE"]
)
def customer_detail(request, pk):

    customer = get_object_or_404(
        Customer,
        pk=pk
    )

    if request.method == "GET":

        return JsonResponse(
            {
                "customer_id": customer.pk,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "email": customer.email,
                "phone": customer.phone,
            }
        )

    if request.method == "DELETE":

        customer.delete()

        return JsonResponse(
            {
                "success": True,
                "message": "Customer deleted."
            }
        )

    form = CustomerForm(
        get_data(request),
        instance=customer
    )

    if form.is_valid():

        form.save()

        return JsonResponse(
            {
                "success": True,
                "message": "Customer updated."
            }
        )

    return form_error(
        form,
        "Invalid customer data."
    )


# ==========================================================
# TABLE CATEGORY
# ==========================================================

@require_http_methods(["GET", "POST"])
def table_category_list(request):

    if request.method == "GET":

        categories = TableCategory.objects.all()

        data = list(
            categories.values(
                "table_category_id",
                "name",
                "description",
                "capacity",
            )
        )

        return JsonResponse(
            {
                "table_categories": data
            }
        )

    form = TableCategoryForm(
        get_data(request)
    )

    if form.is_valid():

        category = form.save()

        return JsonResponse(
            {
                "success": True,
                "message": "Table category created.",
                "table_category_id": category.pk,
            },
            status=201,
        )

    return form_error(
        form,
        "Invalid table category data."
    )


@require_http_methods(
    ["GET", "PUT", "PATCH", "POST", "DELETE"]
)
def table_category_detail(request, pk):

    category = get_object_or_404(
        TableCategory,
        pk=pk
    )

    if request.method == "GET":

        return JsonResponse(
            {
                "table_category_id": category.pk,
                "name": category.name,
                "description": category.description,
                "capacity": category.capacity,
            }
        )

    if request.method == "DELETE":

        category.delete()

        return JsonResponse(
            {
                "success": True,
                "message": "Table category deleted."
            }
        )

    form = TableCategoryForm(
        get_data(request),
        instance=category
    )

    if form.is_valid():

        form.save()

        return JsonResponse(
            {
                "success": True,
                "message": "Table category updated."
            }
        )

    return form_error(
        form,
        "Invalid table category data."
    )


# ==========================================================
# TABLE
# ==========================================================

@require_http_methods(["GET", "POST"])
def table_list(request):

    if request.method == "GET":

        tables = Table.objects.select_related(
            "table_category"
        )

        data = list(
            tables.values(
                "table_id",
                "table_number",
                "table_category_id",
                "table_category__name",
                "capacity",
                "is_active",
            )
        )

        return JsonResponse(
            {
                "tables": data
            }
        )

    form = TableForm(
        get_data(request)
    )

    if form.is_valid():

        table = form.save()

        return JsonResponse(
            {
                "success": True,
                "message": "Table created.",
                "table_id": table.pk,
            },
            status=201,
        )

    return form_error(
        form,
        "Invalid table data."
    )


@require_http_methods(
    ["GET", "PUT", "PATCH", "POST", "DELETE"]
)
def table_detail(request, pk):

    table = get_object_or_404(
        Table,
        pk=pk
    )

    if request.method == "GET":

        return JsonResponse(
            {
                "table_id": table.pk,
                "table_number": table.table_number,
                "table_category_id": table.table_category_id,
                "capacity": table.capacity,
                "is_active": table.is_active,
            }
        )

    if request.method == "DELETE":

        table.delete()

        return JsonResponse(
            {
                "success": True,
                "message": "Table deleted."
            }
        )

    form = TableForm(
        get_data(request),
        instance=table
    )

    if form.is_valid():

        form.save()

        return JsonResponse(
            {
                "success": True,
                "message": "Table updated."
            }
        )

    return form_error(
        form,
        "Invalid table data."
    )


# ==========================================================
# RESERVATION STATUS
# ==========================================================

@require_http_methods(["GET", "POST"])
def reservation_status_list(request):

    if request.method == "GET":

        statuses = ReservationStatus.objects.all()

        data = list(
            statuses.values(
                "reservation_status_id",
                "name",
                "description",
            )
        )

        return JsonResponse(
            {
                "reservation_statuses": data
            }
        )

    form = ReservationStatusForm(
        get_data(request)
    )

    if form.is_valid():

        status = form.save()

        return JsonResponse(
            {
                "success": True,
                "message": "Reservation status created.",
                "reservation_status_id": status.pk,
            },
            status=201,
        )

    return form_error(
        form,
        "Invalid reservation status."
    )


@require_http_methods(
    ["GET", "PUT", "PATCH", "POST", "DELETE"]
)
def reservation_status_detail(
    request,
    pk
):

    status = get_object_or_404(
        ReservationStatus,
        pk=pk
    )

    if request.method == "GET":

        return JsonResponse(
            {
                "reservation_status_id": status.pk,
                "name": status.name,
                "description": status.description,
            }
        )

    if request.method == "DELETE":

        status.delete()

        return JsonResponse(
            {
                "success": True,
                "message": "Reservation status deleted."
            }
        )

    form = ReservationStatusForm(
        get_data(request),
        instance=status
    )

    if form.is_valid():

        form.save()

        return JsonResponse(
            {
                "success": True,
                "message": "Reservation status updated."
            }
        )

    return form_error(
        form,
        "Invalid reservation status."
    )


# ==========================================================
# RESERVATION
# ==========================================================

@require_http_methods(["GET", "POST"])
def reservation_list(request):

    if request.method == "GET":

        reservations = Reservation.objects.select_related(
            "customer",
            "table",
            "status"
        )

        # Filter by customer
        customer_id = request.GET.get(
            "customer"
        )

        if customer_id:

            reservations = reservations.filter(
                customer_id=customer_id
            )

        # Filter by reservation date
        reservation_date = request.GET.get(
            "reservation_date"
        )

        if reservation_date:

            reservations = reservations.filter(
                reservation_date=reservation_date
            )

        data = list(
            reservations.values(
                "reservation_id",

                "customer_id",
                "customer__first_name",
                "customer__last_name",

                "table_id",
                "table__table_number",

                "status_id",
                "status__name",

                "reservation_date",
                "start_time",
                "end_time",

                "number_of_guests",
                "notes",
            )
        )

        return JsonResponse(
            {
                "reservations": data
            }
        )

    form = ReservationForm(
        get_data(request)
    )

    if form.is_valid():

        with transaction.atomic():

            reservation = form.save()

            AuditLog.objects.create(
                reservation=reservation,
                action="CREATED",
                details="Reservation created."
            )

        return JsonResponse(
            {
                "success": True,
                "message": "Reservation created.",
                "reservation_id": reservation.pk,
            },
            status=201,
        )

    return form_error(
        form,
        "Invalid reservation data."
    )


@require_http_methods(
    ["GET", "PUT", "PATCH", "POST"]
)
def reservation_detail(
    request,
    pk
):

    reservation = get_object_or_404(
        Reservation,
        pk=pk
    )

    if request.method == "GET":

        return JsonResponse(
            {
                "reservation_id": reservation.pk,

                "customer_id": reservation.customer_id,

                "table_id": reservation.table_id,

                "status_id": reservation.status_id,

                "reservation_date":
                    reservation.reservation_date,

                "start_time":
                    reservation.start_time,

                "end_time":
                    reservation.end_time,

                "number_of_guests":
                    reservation.number_of_guests,

                "notes":
                    reservation.notes,
            }
        )

    form = ReservationForm(
        get_data(request),
        instance=reservation
    )

    if form.is_valid():

        with transaction.atomic():

            form.save()

            AuditLog.objects.create(
                reservation=reservation,
                action="UPDATED",
                details="Reservation updated."
            )

        return JsonResponse(
            {
                "success": True,
                "message": "Reservation updated."
            }
        )

    return form_error(
        form,
        "Invalid reservation data."
    )


@require_http_methods(
    ["POST", "DELETE"]
)
def reservation_cancel(
    request,
    pk
):

    reservation = get_object_or_404(
        Reservation,
        pk=pk
    )

    cancelled_status = (
        ReservationStatus.objects
        .filter(name__iexact="Cancelled")
        .first()
    )

    if cancelled_status is None:

        cancelled_status = (
            ReservationStatus.objects.create(
                name="Cancelled",
                description="Reservation was cancelled."
            )
        )

    with transaction.atomic():

        reservation.status = cancelled_status

        reservation.save(
            update_fields=[
                "status",
                "updated_at"
            ]
        )

        AuditLog.objects.create(
            reservation=reservation,
            action="CANCELLED",
            details="Reservation cancelled."
        )

    return JsonResponse(
        {
            "success": True,
            "message": "Reservation cancelled."
        }
    )


# ==========================================================
# PAYMENT
# ==========================================================

@require_http_methods(["GET", "POST"])
def payment_list(request):

    if request.method == "GET":

        payments = Payment.objects.select_related(
            "reservation"
        )

        reservation_id = request.GET.get(
            "reservation"
        )

        if reservation_id:

            payments = payments.filter(
                reservation_id=reservation_id
            )

        data = list(
            payments.values(
                "payment_id",
                "reservation_id",
                "amount",
                "payment_status",
                "payment_method",
                "paid_at",
            )
        )

        return JsonResponse(
            {
                "payments": data
            }
        )

    form = PaymentForm(
        get_data(request)
    )

    if form.is_valid():

        payment = form.save()

        return JsonResponse(
            {
                "success": True,
                "message": "Payment created.",
                "payment_id": payment.pk,
            },
            status=201,
        )

    return form_error(
        form,
        "Invalid payment data."
    )


@require_http_methods(
    ["GET", "PUT", "PATCH", "POST"]
)
def payment_detail(
    request,
    pk
):

    payment = get_object_or_404(
        Payment,
        pk=pk
    )

    if request.method == "GET":

        return JsonResponse(
            {
                "payment_id": payment.pk,
                "reservation_id":
                    payment.reservation_id,
                "amount": payment.amount,
                "payment_status":
                    payment.payment_status,
                "payment_method":
                    payment.payment_method,
                "paid_at":
                    payment.paid_at,
            }
        )

    form = PaymentForm(
        get_data(request),
        instance=payment
    )

    if form.is_valid():

        form.save()

        return JsonResponse(
            {
                "success": True,
                "message": "Payment updated."
            }
        )

    return form_error(
        form,
        "Invalid payment data."
    )


# ==========================================================
# AUDIT LOG
# ==========================================================

@require_http_methods(["GET"])
def audit_log_list(request):

    audit_logs = AuditLog.objects.select_related(
        "reservation"
    )

    reservation_id = request.GET.get(
        "reservation"
    )

    if reservation_id:

        audit_logs = audit_logs.filter(
            reservation_id=reservation_id
        )

    data = list(
        audit_logs.values(
            "audit_log_id",
            "reservation_id",
            "action",
            "details",
            "created_at",
        )
    )

    return JsonResponse(
        {
            "audit_logs": data
        }
    )


@require_http_methods(["GET"])
def audit_log_detail(
    request,
    pk
):

    audit_log = get_object_or_404(
        AuditLog,
        pk=pk
    )

    return JsonResponse(
        {
            "audit_log_id":
                audit_log.pk,

            "reservation_id":
                audit_log.reservation_id,

            "action":
                audit_log.action,

            "details":
                audit_log.details,

            "created_at":
                audit_log.created_at,
        }
    )