import uuid
from django.db import models



# status can be used for all configration to save the history as archive, it can be use or unuse and it should be only one copy of the config in use,
# where the code name of the config should be the same in all copies


class Status(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)
    code_name = models.CharField(max_length=6)
    description = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    @property
    def get_name(self):
        return self.name





