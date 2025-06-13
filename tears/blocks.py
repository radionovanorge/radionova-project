from django.db import models
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from django.utils.translation import gettext_lazy as _

class Weekday(models.TextChoices):
    MONDAY = "1", _("Mandag")
    TUESDAY = "2", _("Tirsdag")
    WEDNESDAY = "3", _("Onsdag")
    THURSDAY = "4", _("Torsdag")
    FRIDAY = "5", _("Fredag")
    SATURDAY = "6", _("Lørdag")
    SUNDAY = "7", _("Søndag")

class TimeChoices(models.TextChoices):
    T0000 = "00:00", "00:00"
    T0030 = "00:30", "00:30"
    T0100 = "01:00", "01:00"
    T0130 = "01:30", "01:30"
    T0200 = "02:00", "02:00"
    T0230 = "02:30", "02:30"
    T0300 = "03:00", "03:00"
    T0330 = "03:30", "03:30"
    T0400 = "04:00", "04:00"
    T0430 = "04:30", "04:30"
    T0500 = "05:00", "05:00"
    T0530 = "05:30", "05:30"
    T0600 = "06:00", "06:00"
    T0630 = "06:30", "06:30"
    T0700 = "07:00", "07:00"
    T0730 = "07:30", "07:30"
    T0800 = "08:00", "08:00"
    T0830 = "08:30", "08:30"
    T0900 = "09:00", "09:00"
    T0930 = "09:30", "09:30"
    T1000 = "10:00", "10:00"
    T1030 = "10:30", "10:30"
    T1100 = "11:00", "11:00"
    T1130 = "11:30", "11:30"
    T1200 = "12:00", "12:00"
    T1230 = "12:30", "12:30"
    T1300 = "13:00", "13:00"
    T1330 = "13:30", "13:30"
    T1400 = "14:00", "14:00"
    T1430 = "14:30", "14:30"
    T1500 = "15:00", "15:00"
    T1530 = "15:30", "15:30"
    T1600 = "16:00", "16:00"
    T1630 = "16:30", "16:30"
    T1700 = "17:00", "17:00"
    T1730 = "17:30", "17:30"
    T1800 = "18:00", "18:00"
    T1830 = "18:30", "18:30"
    T1900 = "19:00", "19:00"
    T1930 = "19:30", "19:30"
    T2000 = "20:00", "20:00"
    T2030 = "20:30", "20:30"
    T2100 = "21:00", "21:00"
    T2130 = "21:30", "21:30"
    T2200 = "22:00", "22:00"
    T2230 = "22:30", "22:30"
    T2300 = "23:00", "23:00"
    T2330 = "23:30", "23:30"


class ImageWithDescriptionBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True)
    description = blocks.TextBlock(required=False, help_text="Beskrivelse under bildet")

    class Meta:
        label = "Bilde med beskrivelse"
        icon = "image"