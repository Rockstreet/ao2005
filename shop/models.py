from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager
from urllib.parse import urljoin
from django.core.urlresolvers import resolve, reverse
from django.conf import settings
from django.core.cache import cache
from multiselectfield import MultiSelectField
from django.utils.functional import lazy
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User as auth_user
from sorl.thumbnail import ImageField
from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name='related_name_user')
    name = models.CharField(_("Контактное лицо"), max_length=1000, default='')
    phone = models.CharField(_("Телефон"), max_length=1000, default='')
    company_name = models.CharField(_("Название компании"), max_length=1000, default='')
    inn = models.CharField(_("ИНН"), max_length=1000, default='')
    kpp = models.CharField(_("КПП"), max_length=1000, default='')
    orgn = models.CharField(_("ОГРН"), max_length=1000, default='')
    bank = models.CharField(_("Наименование банка"), max_length=1000, default='')
    bik = models.CharField(_("БИК"), max_length=1000, default='')
    rs = models.CharField(_("Р/C"), max_length=1000, default='')
    ks = models.CharField(_("К/C"), max_length=1000, default='')
    city = models.CharField(_("Город"), max_length=1000, default='')
    adres = models.CharField(_("Адрес доставки"), max_length=1000, default='')

    class Meta:
        verbose_name = _("Профиль пользователя")
        verbose_name_plural = _("Профили пользователя")


class BaseShop(models.Model):
    created_date = models.DateTimeField(_("Дата создания"), auto_now_add=True, editable=False)
    edited_date = models.DateTimeField(_("Дата редактирования"), auto_now=True, editable=False, null=True)

    title = models.CharField(_("Название"), max_length=1000, default='')
    meta_description = models.CharField(_("Description"), max_length=1000, blank=True)
    meta_keywords = models.CharField(_("Keywords"), max_length=1000, blank=True)
    slug = models.SlugField(_("Имя для url"), unique=True, blank=True, help_text=_("Только английские буквы, цифры и знаки минус и подчеркивание."))
    tags = TaggableManager(_("Тэги"), blank=True),
    file = ImageField(_("Фото для категории 250X250"), upload_to='category', blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Category(MPTTModel, BaseShop):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, verbose_name=u"Родительский элемент")
    content = RichTextUploadingField("Описание", blank=True)
    num = models.IntegerField(default=0, verbose_name=u'Порядковый номер')
    new_flag = models.BooleanField("Показывать как новинку", default=False)


    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        ordering = ['num']


class Item(BaseShop):

    content_small = models.CharField(_("Краткое описание"), max_length=800, default='', blank=True)
    content = RichTextUploadingField("Описание", blank=True)
    category = models.ManyToManyField(Category, verbose_name=u'Категория')
    status = models.BooleanField("Опубликовано", default=True)
    offer = models.BooleanField("Показывать в спецпредложениях", default=False, blank=True)
    price_1 = models.DecimalField(_("Цена"), max_digits=10, decimal_places=2, blank=True, null=True)
    num = models.IntegerField(default=0, verbose_name=u'Порядковый номер')



    class Meta:
        verbose_name = _("Товар")
        verbose_name_plural = _("Товары")
        ordering = ['num']



class Item_image(models.Model):
    title = models.CharField(_("Название"), max_length=1000, default='', blank=True)
    file = models.ImageField(_("Изображение"), upload_to='shop')
    item_variation = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True,)
    num = models.IntegerField(_("Порядковый номер"), default=0, blank=True, db_index=True)

    class Meta:
        verbose_name = _("Изображение")
        verbose_name_plural = _("Изображения")
        ordering = ['num', ]

    def __str__(self):
        return self.file.url


# Заказы
class BaseOrder(models.Model):
    created_date = models.DateTimeField(_("Дата создания"), auto_now_add=True, editable=False)
    edited_date = models.DateTimeField(_("Дата редактирования"), auto_now=True, editable=False, null=True)

    class Meta:
        abstract = True


class Status(models.Model):
    title = models.CharField('Название', max_length=255)
    num = models.IntegerField('Порядковый номер', default=0)
    default_status = models.BooleanField("Статус заказа при создании", default=False)

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказов'
        ordering = ['num']

    def __str__(self):
        return self.title


class Order(BaseOrder):
    customer = models.ForeignKey(auth_user, verbose_name=u'Пользователь')
    total_price = models.DecimalField(_("Общая стоимость"), max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.ForeignKey(Status, verbose_name=u'Текущий статус', blank=True, null=True)
    email = models.EmailField(_("Email"),  default='')
    address = models.TextField(_("Адрес доставки"))
    phone_number = PhoneNumberField(_("Телефон"),default='')

    class Meta:
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")


class OrderItem(BaseOrder):
    order = models.ForeignKey(Order, verbose_name=u'Заказ', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    title = models.CharField(_("Название"), default='', max_length=255)
    cols = models.IntegerField(_("Количество"), blank=True, default=0)
    price = models.DecimalField(_("Стоимость"), max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = _("Товар заказа")
        verbose_name_plural = _("Товары заказа")

    def __str__(self):
        return self.title
