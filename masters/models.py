import secrets
import qrcode
from io import BytesIO
from django.core.files import File
from django.db import models

def generate_qr_token():
    return secrets.token_urlsafe(8)

# ----------------------
# SITE MODEL
# ----------------------
class Site(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# ----------------------
# AREA MODEL
# ----------------------
class Area(models.Model):
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name='areas'
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.site.name}"

# ----------------------
# LOCATION MODEL
# ----------------------
class Location(models.Model):
    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        related_name='locations'
    )

    name = models.CharField(max_length=100)
    floor = models.CharField(max_length=50, blank=True, null=True)

    qr_token = models.CharField(
        max_length=50,
        unique=True,
        default=generate_qr_token
    )

    qr_enabled = models.BooleanField(default=True)

    qr_image = models.ImageField(
        upload_to='qr_codes/',
        blank=True,
        null=True
    )

    def __str__(self):
        # 🌟 MAGIC: This links all three together so the dropdown looks perfect!
        return f"{self.name} - {self.area.name} ({self.area.site.name})"

    # ----------------------
    # AUTO QR GENERATION
    # ----------------------
    def save(self, *args, **kwargs):
        if not self.qr_image:
            qr_url = f"http://127.0.0.1:8000/q/{self.qr_token}/"

            qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=4
            )
            qr.add_data(qr_url)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            buffer = BytesIO()
            img.save(buffer, format="PNG")

            file_name = f"qr_{self.name.replace(' ', '_')}_{self.qr_token}.png"
            self.qr_image.save(file_name, File(buffer), save=False)

        super().save(*args, **kwargs)