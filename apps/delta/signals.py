from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone


@receiver(pre_save)
def add_timestamps(sender, instance, *args, **kwargs):
    now = timezone.now()
    if instance._state.adding:
        instance.criado_em = now
    instance.modificado_em = now
