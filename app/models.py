import os
import uuid
from django.db import models
from django.forms import ValidationError
# from django.core.exceptions import ValidationError
# from django.utils.translation import gettext_lazy as _

def validate_file_extension(value):

    allowed_extensions = ['.ipa', '.apk', '.app']

    ext = os.path.splitext(value.name)[1]

    if ext not in allowed_extensions:
        raise ValidationError("Only {} files are allowed.".format(", ".join(allowed_extensions)))




class File(models.Model):
    name = models.CharField(max_length=225)
    unique_name = models.CharField(max_length=225, unique=True)
    id = models.UUIDField( primary_key = True,default = uuid.uuid4,editable = False)

    class Meta:
        db_table = 'files'
    
    def __str__(self):
        return  self.name
    
    # def clean(self):
    #     pattern = re.compile('.*\.ipa$','.*\.apk$')
        
    #     if not pattern.search(self.pdf):
    #         raise ValidationError(_('Only .ipa and apk files are accepted'))000
    0



