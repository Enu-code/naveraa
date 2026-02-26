from django.shortcuts import render, get_object_or_404
from masters.models import Location
from .forms import QRComplaintForm

def qr_complaint_view(request, token=None):
    location_obj = None
    is_qr = False
    initial_data = {}

    # If they scanned a QR code, grab the token!
    if token:
        location_obj = get_object_or_404(Location, qr_token=token, qr_enabled=True)
        initial_data = {'site': location_obj.site, 'location': location_obj}
        is_qr = True

    if request.method == 'POST':
        form = QRComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            
            # If from QR, we force the location so users can't tamper with the dropdowns
            if is_qr:
                ticket.site = location_obj.site
                ticket.location = location_obj
                ticket.source = 'QR'
            else:
                ticket.source = 'Manual'
                
            ticket.save()
            return render(request, 'tickets/success.html', {'location': ticket.location})
    else:
        form = QRComplaintForm(initial=initial_data)

    # We send all locations to the HTML so the dropdowns can update dynamically
    all_locations = Location.objects.filter(qr_enabled=True)

    return render(request, 'tickets/complaint_form.html', {
        'form': form,
        'is_qr': is_qr,
        'location_obj': location_obj,
        'all_locations': all_locations
    })