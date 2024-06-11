from django import forms
from .models import Reservation, SeatingPlan

class AssignReservationForm(forms.ModelForm):
    class Meta:
        model = SeatingPlan
        fields = ['reservation']
    
    reservation = forms.ModelChoiceField(
        queryset=Reservation.objects.filter(seatingplan__isnull=True),  # Nur Reservierungen ohne Sitzplan
        label="Unassigned Reservations"
    )
