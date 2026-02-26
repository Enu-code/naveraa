from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from tickets.models import Ticket

@login_required(login_url='login')
def dashboard(request):
    # Get all tickets, newest first
    tickets = Ticket.objects.all().order_by('-created_at')
    
    # Figure out who is logged in!
    if request.user.is_superuser:
        role = 'Admin'
    elif request.user.is_staff:
        role = 'Manager'
    else:
        role = 'Client'
        
    return render(request, 'accounts/dashboard.html', {'tickets': tickets, 'role': role})

@login_required(login_url='login')
def update_ticket_status(request, ticket_id):
    if request.method == 'POST':
        # Only Admins and Managers can do this
        if request.user.is_superuser or request.user.is_staff:
            ticket = get_object_or_404(Ticket, id=ticket_id)
            ticket.status = request.POST.get('status')
            ticket.save()
    return redirect('dashboard')

@login_required(login_url='login')
def delete_ticket(request, ticket_id):
    # ONLY Admins can delete
    if request.user.is_superuser:
        ticket = get_object_or_404(Ticket, id=ticket_id)
        ticket.delete()
    return redirect('dashboard')