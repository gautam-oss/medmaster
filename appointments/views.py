from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Appointment
from .forms import AppointmentForm


def check_appointment_conflict(doctor, appointment_date, appointment_time, exclude_id=None):
    conflicts = Appointment.objects.filter(
        doctor=doctor,
        appointment_date=appointment_date,
        appointment_time=appointment_time,
        status__in=['pending', 'confirmed']
    )
    if exclude_id:
        conflicts = conflicts.exclude(id=exclude_id)
    return conflicts.exists()


@login_required
def book_appointment(request):
    if not hasattr(request.user, 'patient'):
        messages.error(request, 'Only patients can book appointments.')
        return redirect('users:dashboard')

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient

            if appointment.appointment_date < timezone.now().date():
                messages.error(request, 'Cannot book appointments in the past.')
                return render(request, 'appointments/book.html', {'form': form})

            if appointment.appointment_date == timezone.now().date():
                if appointment.appointment_time < timezone.now().time():
                    messages.error(request, 'Cannot book appointments in the past.')
                    return render(request, 'appointments/book.html', {'form': form})

            if check_appointment_conflict(appointment.doctor, appointment.appointment_date, appointment.appointment_time):
                messages.error(request, 'This time slot is already booked. Please choose another time or doctor.')
                return render(request, 'appointments/book.html', {'form': form})

            appointment.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('appointments:success', appointment_id=appointment.id)
    else:
        form = AppointmentForm()

    return render(request, 'appointments/book.html', {'form': form})


@login_required
def my_appointments(request):
    if hasattr(request.user, 'patient'):
        appointments = Appointment.objects.filter(patient=request.user.patient).select_related('doctor__user')
    elif hasattr(request.user, 'doctor'):
        appointments = Appointment.objects.filter(doctor=request.user.doctor).select_related('patient__user')
    else:
        appointments = []
    return render(request, 'appointments/list.html', {'appointments': appointments})


@login_required
def appointment_success(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if hasattr(request.user, 'patient') and appointment.patient != request.user.patient:
        messages.error(request, 'You can only view your own appointments.')
        return redirect('appointments:my_appointments')
    return render(request, 'appointments/success.html', {'appointment': appointment})


@login_required
def update_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if not hasattr(request.user, 'doctor'):
        messages.error(request, 'Only doctors can update appointments.')
        return redirect('appointments:my_appointments')

    if appointment.doctor != request.user.doctor:
        messages.error(request, 'You can only update your own appointments.')
        return redirect('appointments:my_appointments')

    if request.method == 'POST':
        new_status = request.POST.get('status')
        notes = request.POST.get('notes', '')
        valid_statuses = ['pending', 'confirmed', 'completed', 'cancelled']

        if new_status not in valid_statuses:
            messages.error(request, 'Invalid status selected.')
            return render(request, 'appointments/update.html', {'appointment': appointment})

        if appointment.status == 'cancelled' and new_status == 'confirmed':
            messages.error(request, 'Cannot confirm a cancelled appointment.')
            return render(request, 'appointments/update.html', {'appointment': appointment})

        if appointment.status == 'completed' and new_status == 'cancelled':
            messages.error(request, 'Cannot cancel a completed appointment.')
            return render(request, 'appointments/update.html', {'appointment': appointment})

        appointment.status = new_status
        appointment.notes = notes
        appointment.save()
        messages.success(request, f'Appointment status updated to {appointment.get_status_display()}!')
        return redirect('appointments:my_appointments')

    return render(request, 'appointments/update.html', {'appointment': appointment})
