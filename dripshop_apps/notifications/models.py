from django.db import models
from django.conf import settings
from dripshop_apps.core.abstract_models import AbstractTimeStampModel

class Notification(AbstractTimeStampModel):
    """
    notification model
    """
    NOTIFICATION_TYPES = (
        ("random", "random"),
        ("order_placed", "order Placed"),
        ("order_updated", "Order Updated"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=555)
    notification_type = models.CharField(max_length=55, choices=NOTIFICATION_TYPES, default='random')
    link = models.URLField(max_length=555, blank=True, null=True )
    viewed = models.BooleanField(default=False)


    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ('-created_date',)

    @property
    def is_viewed(self):
        if viewed:
            return True
        

    
