from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("accounts/logout/", views.logout_view),
    path("accounts/signup/", views.SignUp.as_view(), name="signup"),
    path("booking", views.booking, name="booking"),
    path("booking-submit", views.bookingSubmit, name="bookingSubmit"),
    path("user-panel", views.userPanel, name="userPanel"),
    path("editAppointment/<int:id>", views.editAppointment, name="editAppointment"),
    path(
        "editAppointmentTime/<int:id>",
        views.editAppointmentTime,
        name="editAppointmentTime",
    ),
    path("staffAppointments", views.staffAppointments, name="staffAppointments"),
]
