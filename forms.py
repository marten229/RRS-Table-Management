from django import forms
from .models import Reservation, SeatingPlan

class AssignReservationForm(forms.ModelForm):
    vorhandene_reservierung = forms.ModelChoiceField(
        queryset=Reservation.objects.filter(seatingplan__isnull=True),  # Nur Reservierungen ohne Sitzplan
        required=False,
        label="Nicht zugewiesene Reservierungen"
    )
    neue_reservierung_name = forms.CharField(required=False, label="Neuer Reservierungsname")
    neue_reservierung_email = forms.EmailField(required=False, label="Neue Reservierungs-E-Mail")
    neue_reservierung_telefon = forms.CharField(required=False, label="Neue Reservierungs-Telefonnummer")
    neue_reservierung_datum = forms.DateField(required=False, label="Neues Reservierungsdatum")
    neue_reservierung_uhrzeit = forms.TimeField(required=False, label="Neue Reservierungsuhrzeit")
    neue_reservierung_dauer = forms.IntegerField(required=False, label="Neue Reservierungsdauer")
    neue_reservierung_gaeste = forms.IntegerField(required=False, label="Anzahl der Gäste")

    class Meta:
        model = SeatingPlan
        fields = []

    def clean(self):
        cleaned_data = super().clean()
        vorhandene_reservierung = cleaned_data.get("vorhandene_reservierung")
        neue_reservierung_name = cleaned_data.get("neue_reservierung_name")

        if not vorhandene_reservierung and not neue_reservierung_name:
            raise forms.ValidationError("Sie müssen entweder eine vorhandene Reservierung auswählen oder Details für eine neue Reservierung eingeben.")

        return cleaned_data
