import re
from django import forms
from .models import Ticket
from masters.models import Site, Location

class QRComplaintForm(forms.ModelForm):
    site = forms.ModelChoiceField(
        queryset=Site.objects.filter(active=True), 
        empty_label="Select the building...",
        widget=forms.Select(attrs={'class': 'form-select custom-input', 'id': 'id_site'})
    )
    location = forms.ModelChoiceField(
        queryset=Location.objects.filter(qr_enabled=True), 
        empty_label="Select the room...",
        widget=forms.Select(attrs={'class': 'form-select custom-input', 'id': 'id_location'})
    )

    class Meta:
        model = Ticket
        fields = ['site', 'location', 'category', 'description', 'reporter_phone', 'priority', 'photo']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select custom-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control custom-input', 'rows': 3, 'placeholder': 'Describe the problem...'}),
            'reporter_phone': forms.TextInput(attrs={
                'class': 'form-control custom-input', 
                'placeholder': 'Enter 10-digit number...', 
                'pattern': '\d{10}', 
                'maxlength': '10'
            }),
            'photo': forms.FileInput(attrs={'class': 'd-none', 'id': 'id_photo', 'accept': 'image/*'})
        }

    def clean_reporter_phone(self):
        phone = self.cleaned_data.get('reporter_phone')
        if phone and not re.match(r'^\d{10}$', phone):
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Magic loop to make every single field compulsory!
        for field_name, field in self.fields.items():
            field.required = True