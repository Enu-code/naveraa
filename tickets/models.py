from django.db import models
from masters.models import Site, Location, Area


class Ticket(models.Model):

    CATEGORY_CHOICES = [
    ('HVAC', 'HVAC'),
    ('Plumbing', 'Plumbing'),
    ('Electrical', 'Electrical'),
    ('Housekeeping', 'Housekeeping'),
    ('Carpentry', 'Carpentry'),
    ('STP/WTP', 'STP/WTP'),
    ('Safety', 'Safety'),
    ('Security', 'Security'),
    ('Parking', 'Parking'),
    ('other', 'other'),
]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Closed', 'Closed'),
    ]

    SOURCE_CHOICES = [
        ('QR', 'QR Code'),
        ('Manual', 'Manual Entry'),
    ]

    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='Medium')
    description = models.TextField()

    reporter_name = models.CharField(max_length=100, blank=True, null=True)
    reporter_phone = models.CharField(max_length=20, blank=True, null=True)
    photo = models.ImageField(upload_to='complaint_photos/', blank=True, null=True)

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Open')
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, default='QR')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket #{self.id} - {self.location.name} ({self.status})"