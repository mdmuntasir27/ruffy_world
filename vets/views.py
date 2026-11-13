from django.shortcuts import render
from django.utils import timezone
from .models import Vet


def vet_list(request):
    # Access system clock time in the local timezone (Asia/Dhaka)
    now = timezone.localtime(timezone.now())
    current_hour = now.hour

    # Morning: 6AM to 2PM (06:00 to 13:59:59)
    # Mid: 2PM to 10PM (14:00 to 21:59:59)
    # Night: 10PM to 6AM (22:00 to 05:59:59)
    if 6 <= current_hour < 14:
        active_shift = 'morning'
        active_shift_title = 'Morning Shift (6:00 AM – 2:00 PM)'
    elif 14 <= current_hour < 22:
        active_shift = 'mid'
        active_shift_title = 'Mid Shift (2:00 PM – 10:00 PM)'
    else:
        active_shift = 'night'
        active_shift_title = 'Night Shift (10:00 PM – 6:00 AM)'

    # Filter option
    shift_filter = request.GET.get('shift', '')

    all_vets = Vet.objects.filter(is_available=True)
    if shift_filter in ['morning', 'mid', 'night']:
        vets = all_vets.filter(shift=shift_filter)
    elif shift_filter == 'active':
        vets = all_vets.filter(shift=active_shift)
    else:
        vets = all_vets

    # Group counts
    morning_vets = all_vets.filter(shift='morning')
    mid_vets = all_vets.filter(shift='mid')
    night_vets = all_vets.filter(shift='night')
    active_vets = all_vets.filter(shift=active_shift)

    context = {
        'vets': vets,
        'morning_vets': morning_vets,
        'mid_vets': mid_vets,
        'night_vets': night_vets,
        'active_vets': active_vets,
        'active_shift': active_shift,
        'active_shift_title': active_shift_title,
        'current_time_str': now.strftime('%I:%M %p'),
        'current_date_str': now.strftime('%A, %d %B %Y'),
        'shift_filter': shift_filter,
    }
    return render(request, 'vets/vet_list.html', context)

