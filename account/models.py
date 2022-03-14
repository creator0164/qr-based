from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractUser
import qrcode
from PIL import Image, ImageDraw
from io import BytesIO
from django.core.files import File


def get_profile_image_filepath(self, filename):
    return 'qr_code/' + str(self.pk) + '/qr_code.png'


class User(AbstractUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    course = models.CharField(max_length=50, null=True, blank=True)
    year_and_section = models.CharField(max_length=50, null=True, blank=True)
    student_no = models.IntegerField(default=100000)
    qr_code = models.ImageField(max_length=255, upload_to=get_profile_image_filepath,
                                null=True, blank=True)
    is_active = models.BooleanField(default=False)

    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        qr_image = qrcode.make(self.username)
        qr_offset = Image.new('RGB', (310, 310), 'white')
        qr_offset.paste(qr_image)
        file_name = f'{self.username}-{self.id}qr.png'
        stream = BytesIO()
        qr_offset.save(stream, 'PNG')
        self.qr_code.save(file_name, File(stream), save=False)
        qr_offset.close()
        super().save(*args, **kwargs)
