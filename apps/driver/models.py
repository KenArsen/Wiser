import os

from django.db import models
from django.utils.translation import gettext_lazy as _

from api.utils.image import ImageService


class Driver(models.Model, ImageService):
    CARGO_VAN = "CARGO VAN"
    SPRINTER_VAN = "SPRINTER VAN"
    VAN = "VAN"
    SPRINTER = "SPRINTER"
    BOX_TRUCK = "BOX TRUCK"
    SMALL_STRAIGHT = "SMALL STRAIGHT"
    LARGE_STRAIGHT = "LARGE STRAIGHT"
    LIFTGATE = "LIFTGATE"
    FLATBED = "FLATBED"
    TRACTOR = "TRACTOR"
    REEFER = "REEFER"
    TYPE_OF_ADS = (
        (CARGO_VAN, "CARGO VAN"),
        (SPRINTER_VAN, "SPRINTER VAN"),
        (VAN, "VAN"),
        (SPRINTER, "SPRINTER"),
        (BOX_TRUCK, "BOX TRUCK"),
        (SMALL_STRAIGHT, "SMALL STRAIGHT"),
        (LARGE_STRAIGHT, "LARGE STRAIGHT"),
        (LIFTGATE, "LIFTGATE"),
        (FLATBED, "FLATBED"),
        (TRACTOR, "TRACTOR"),
        (REEFER, "REEFER"),
    )

    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="First Name")
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Last Name")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Date of Birth")
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    ssn = models.CharField(max_length=255, blank=True, null=True, verbose_name="SSN")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Address")
    city = models.CharField(max_length=255, blank=True, null=True, verbose_name="City")
    state = models.CharField(max_length=255, blank=True, null=True, verbose_name="State")
    zip_code = models.CharField(max_length=255, blank=True, null=True, verbose_name="Zip")
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    emergency_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Emergency Phone")
    second_driver = models.BooleanField(default=False, verbose_name="Second Driver (team)")

    lisense_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="Lisense Number")
    lisense_state = models.CharField(max_length=255, blank=True, null=True, verbose_name="Lisense State")
    type = models.CharField(max_length=255, blank=True, null=True, verbose_name="Type")
    expiration_date = models.DateField(blank=True, null=True, verbose_name="Expiration Date")

    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Avatar")
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    vehicle_type = models.CharField(max_length=100, null=True, choices=TYPE_OF_ADS, default=SPRINTER_VAN,
                                    verbose_name="vehicle")
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = _("Driver")
        verbose_name_plural = _("Drivers")

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        try:
            # if advertisement new added
            if not self.pk:
                if self.avatar:
                    # image compress
                    self.compress_image('avatar', delete_source=True, max_width=300, max_height=300)
            else:
                if self.avatar:
                    # image compress
                    self.compress_image('avatar', delete_source=True, max_width=300, max_height=300)

            this = Driver.objects.get(id=self.id)

            if not this.avatar == self.avatar:
                if os.path.isfile(this.avatar.path):
                    os.remove(this.avatar.path)

        except:
            pass

        super(Driver, self).save(*args, **kwargs)
