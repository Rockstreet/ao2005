from django.db import models
from embed_video.fields import EmbedVideoField
from django.utils.translation import ugettext_lazy as _, ugettext

class Video(models.Model):
    title = models.CharField(_("Название"), max_length=1000, default='')
    # file = ImageSpecField(_("Изображение"), upload_to='gallery', blank=True, sizes=((250,250),))
    youtube_url = EmbedVideoField(_("Youtube адрес видео"), blank=True)
    num = models.IntegerField(_("Порядковый номер"), default=0, blank=True, db_index=True)


    class Meta:
        verbose_name = _("Видеоролик")
        verbose_name_plural = _("Видеоролики")
        ordering = ['num', 'title', ]


    def __str__(self):
        return self.title