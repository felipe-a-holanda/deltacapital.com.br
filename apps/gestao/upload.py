import datetime
import os
import unicodedata
from os.path import join, normpath,splitext
from django.core.files.storage import default_storage
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_text, force_str


@deconstructible
class UploadToPath(object):
    def __init__(self, upload_to):
        self.document_type = upload_to

    def __call__(self, instance, filename):
        if not instance.pk:
            from .models import Proposta
            i = Proposta.objects.create()
            instance.pk = i.pk
            instance.criada_em = i.criada_em
        return self.generate_filename(instance, filename)

    def get_directory_name(self, instance):
        date = str(instance.criada_em.date())
        pk = str(instance.pk)
        return normpath(join(date, pk))

    def get_filename(self, filename):
        filename = default_storage.get_valid_name(os.path.basename(filename))
        filename = force_text(filename)
        filename = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('ascii')
        name, ext = splitext(filename)
        print(f"name=[{name}] and ext=[{ext}]")
        return normpath(f"{self.document_type}{ext}")

    def generate_filename(self, instance, filename):
        return join(self.get_directory_name(instance), self.get_filename(filename))




@deconstructible
class UploadToPath2(object):
    def __init__(self, upload_to):
        self.upload_to = upload_to

    def __call__(self, instance, filename):
        return self.generate_filename(filename)

    def get_directory_name(self):
        return os.path.normpath(force_text(datetime.datetime.now().strftime(force_str(self.upload_to))))

    def get_filename(self, filename):
        filename = default_storage.get_valid_name(os.path.basename(filename))
        filename = force_text(filename)
        filename = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('ascii')
        return os.path.normpath(filename)

    def generate_filename(self, filename):
        return os.path.join(self.get_directory_name(), self.get_filename(filename))