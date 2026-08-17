from django.urls import path

from . import views


app_name = "reservation_app"


urlpatterns = [

    # ======================================================
    # CUSTOMERS
    # ======================================================

    path(
        "customers/",
        views.customer_list,
        name="customer-list"
    ),

    path(
        "customers/add/",
        views.customer_list,
        name="customer-add"
    ),

    path(
        "customers/<int:pk>/",
        views.customer_detail,
        name="customer-detail"
    ),

    path(
        "customers/<int:pk>/edit/",
        views.customer_detail,
        name="customer-edit"
    ),

    path(
        "customers/<int:pk>/delete/",
        views.customer_detail,
        name="customer-delete"
    ),


    # ======================================================
    # TABLE CATEGORIES
    # ======================================================

    path(
        "table-categories/",
        views.table_category_list,
        name="table-category-list"
    ),

    path(
        "table-categories/add/",
        views.table_category_list,
        name="table-category-add"
    ),

    path(
        "table-categories/<int:pk>/",
        views.table_category_detail,
        name="table-category-detail"
    ),

    path(
        "table-categories/<int:pk>/edit/",
        views.table_category_detail,
        name="table-category-edit"
    ),

    path(
        "table-categories/<int:pk>/delete/",
        views.table_category_detail,
        name="table-category-delete"
    ),


    # ======================================================
    # TABLES
    # ======================================================

    path(
        "tables/",
        views.table_list,
        name="table-list"
    ),

    path(
        "tables/add/",
        views.table_list,
        name="table-add"
    ),

    path(
        "tables/<int:pk>/",
        views.table_detail,
        name="table-detail"
    ),

    path(
        "tables/<int:pk>/edit/",
        views.table_detail,
        name="table-edit"
    ),

    path(
        "tables/<int:pk>/delete/",
        views.table_detail,
        name="table-delete"
    ),


    # ======================================================
    # RESERVATION STATUSES
    # ======================================================

    path(
        "reservation-statuses/",
        views.reservation_status_list,
        name="reservation-status-list"
    ),

    path(
        "reservation-statuses/add/",
        views.reservation_status_list,
        name="reservation-status-add"
    ),

    path(
        "reservation-statuses/<int:pk>/",
        views.reservation_status_detail,
        name="reservation-status-detail"
    ),

    path(
        "reservation-statuses/<int:pk>/edit/",
        views.reservation_status_detail,
        name="reservation-status-edit"
    ),

    path(
        "reservation-statuses/<int:pk>/delete/",
        views.reservation_status_detail,
        name="reservation-status-delete"
    ),


    # ======================================================
    # RESERVATIONS
    # ======================================================

    path(
        "reservations/",
        views.reservation_list,
        name="reservation-list"
    ),

    path(
        "reservations/add/",
        views.reservation_list,
        name="reservation-add"
    ),

    path(
        "reservations/<int:pk>/",
        views.reservation_detail,
        name="reservation-detail"
    ),

    path(
        "reservations/<int:pk>/edit/",
        views.reservation_detail,
        name="reservation-edit"
    ),

    path(
        "reservations/<int:pk>/cancel/",
        views.reservation_cancel,
        name="reservation-cancel"
    ),


    # ======================================================
    # PAYMENTS
    # ======================================================

    path(
        "payments/",
        views.payment_list,
        name="payment-list"
    ),

    path(
        "payments/add/",
        views.payment_list,
        name="payment-add"
    ),

    path(
        "payments/<int:pk>/",
        views.payment_detail,
        name="payment-detail"
    ),

    path(
        "payments/<int:pk>/edit/",
        views.payment_detail,
        name="payment-edit"
    ),


    # ======================================================
    # AUDIT LOGS
    # ======================================================

    path(
        "audit-logs/",
        views.audit_log_list,
        name="audit-log-list"
    ),

    path(
        "audit-logs/<int:pk>/",
        views.audit_log_detail,
        name="audit-log-detail"
    ),

]