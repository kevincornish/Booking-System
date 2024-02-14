from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import *
from .utils import *


def index(request):
    return render(request, "index.html", {})


def logout_view(request):
    logout(request)
    return redirect("home")


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


@login_required
def booking(request):
    weekdays = validWeekday(22)

    validateWeekdays = isWeekdayValid(weekdays)

    if request.method == "POST":
        day = request.POST.get("day")
        request.session["day"] = day

        return redirect("bookingSubmit")

    return render(
        request,
        "booking/booking.html",
        {
            "weekdays": weekdays,
            "validateWeekdays": validateWeekdays,
        },
    )


@login_required
def bookingSubmit(request):
    user = request.user
    times = [
        "3 PM",
        "3:30 PM",
        "4 PM",
        "4:30 PM",
        "5 PM",
        "5:30 PM",
        "6 PM",
        "6:30 PM",
        "7 PM",
        "7:30 PM",
    ]
    today = datetime.now()
    minDate = today.strftime("%Y-%m-%d")
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime("%Y-%m-%d")
    maxDate = strdeltatime

    day = request.session.get("day")

    hour = checkTime(times, day)
    if request.method == "POST":
        time = request.POST.get("time")
        date = dayToWeekday(day)

        if day <= maxDate and day >= minDate:
            if date == "Monday" or date == "Saturday" or date == "Wednesday":
                if Appointment.objects.filter(day=day).count() < 11:
                    if Appointment.objects.filter(day=day, time=time).count() < 1:
                        AppointmentForm = Appointment.objects.get_or_create(
                            user=user,
                            day=day,
                            time=time,
                        )
                        messages.success(request, "Appointment Saved!")
                        return redirect("home")
                    else:
                        messages.success(
                            request, "The Selected Time Has Been Reserved Before!"
                        )
                else:
                    messages.success(request, "The Selected Day Is Full!")
            else:
                messages.success(request, "The Selected Date Is Incorrect")
        else:
            messages.success(
                request, "The Selected Date Isn't In The Correct Time Period!"
            )

    return render(
        request,
        "booking/bookingSubmit.html",
        {
            "times": hour,
        },
    )


@login_required
def userPanel(request):
    user = request.user
    appointments = Appointment.objects.filter(user=user).order_by("day", "time")
    return render(
        request,
        "booking/userPanel.html",
        {
            "user": user,
            "appointments": appointments,
        },
    )


@login_required
def editAppointment(request, id):
    appointment = Appointment.objects.get(pk=id)
    userdatepicked = appointment.day
    today = datetime.today()
    minDate = today.strftime("%Y-%m-%d")

    delta24 = (userdatepicked).strftime("%Y-%m-%d") >= (
        today + timedelta(days=1)
    ).strftime("%Y-%m-%d")
    weekdays = validWeekday(22)

    validateWeekdays = isWeekdayValid(weekdays)

    if request.method == "POST":
        day = request.POST.get("day")

        request.session["day"] = day

        return redirect("editAppointmentTime", id=id)

    return render(
        request,
        "booking/editAppointment.html",
        {
            "weekdays": weekdays,
            "validateWeekdays": validateWeekdays,
            "delta24": delta24,
            "id": id,
        },
    )


@login_required
def editAppointmentTime(request, id):
    user = request.user
    times = [
        "3 PM",
        "3:30 PM",
        "4 PM",
        "4:30 PM",
        "5 PM",
        "5:30 PM",
        "6 PM",
        "6:30 PM",
        "7 PM",
        "7:30 PM",
    ]
    today = datetime.now()
    minDate = today.strftime("%Y-%m-%d")
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime("%Y-%m-%d")
    maxDate = strdeltatime

    day = request.session.get("day")

    hour = checkEditTime(times, day, id)
    appointment = Appointment.objects.get(pk=id)
    userSelectedTime = appointment.time
    if request.method == "POST":
        time = request.POST.get("time")
        date = dayToWeekday(day)

        if day <= maxDate and day >= minDate:
            if date == "Monday" or date == "Saturday" or date == "Wednesday":
                if Appointment.objects.filter(day=day).count() < 11:
                    if (
                        Appointment.objects.filter(day=day, time=time).count() < 1
                        or userSelectedTime == time
                    ):
                        AppointmentForm = Appointment.objects.filter(pk=id).update(
                            user=user,
                            day=day,
                            time=time,
                        )
                        messages.success(request, "Appointment Edited!")
                        return redirect("home")
                    else:
                        messages.success(
                            request, "The Selected Time Has Been Reserved Before!"
                        )
                else:
                    messages.success(request, "The Selected Day Is Full!")
            else:
                messages.success(request, "The Selected Date Is Incorrect")
        else:
            messages.success(
                request, "The Selected Date Isn't In The Correct Time Period!"
            )
        return redirect("userPanel")

    return render(
        request,
        "booking/editAppointmentTime.html",
        {
            "times": hour,
            "id": id,
        },
    )


@login_required
def staffAppointments(request):
    today = datetime.today()
    minDate = today.strftime("%Y-%m-%d")
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime("%Y-%m-%d")
    maxDate = strdeltatime
    items = Appointment.objects.filter(day__range=[minDate, maxDate]).order_by(
        "day", "time"
    )

    return render(
        request,
        "accounts/Appointments.html",
        {
            "items": items,
        },
    )
