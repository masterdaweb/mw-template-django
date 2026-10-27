from django.db import models


class Upload(models.Model):
    """A file sent from the home page: in the bucket, described here."""

    file = models.FileField(upload_to='uploads/%Y/%m/')
    name = models.CharField(max_length=255)
    size = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def is_image(self):
        return self.name.lower().rsplit('.', 1)[-1] in {'png', 'jpg', 'jpeg', 'gif', 'webp', 'avif', 'svg'}
