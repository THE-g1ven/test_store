from django.db.models import Model
from django.db.models import CharField
from django.db.models import TextChoices
from django.db.models import ForeignKey
from django.db.models import CASCADE
from django.db.models import DateTimeField
from django.utils.translation import gettext_lazy as _
import binascii
import os


class DefaultModel(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class WarehouseAccount(DefaultModel):
    name = CharField(max_length=255)
    key = CharField(max_length=40)
    api_url = CharField(
        max_length=255,
        blank=True,
        help_text='ex: http://localhost:8000/api',
    )

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.name


class Order(DefaultModel):
    class StatusChoices(TextChoices):
        NEW = 'NEW', _('New')
        IN_PROCESS = 'IN_PROCESS', _('In Process')
        STORED = 'STORED', _('Stored')
        SEND = 'SEND', _('Send')

    order_number = CharField(max_length=255, unique=True)
    status = CharField(
        max_length=255,
        choices=StatusChoices.choices,
        default=StatusChoices.NEW,
    )
    warehouse_account = ForeignKey(
        WarehouseAccount,
        related_name='orders',
        on_delete=CASCADE,
    )

    def __str__(self):
        return f'Order: {self.order_number} - {self.warehouse_account.name} - {self.status}'
