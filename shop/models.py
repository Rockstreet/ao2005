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

from decimal import *

from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name='related_name_user')
    name = models.CharField(_("ФИО"), max_length=1000, default='')
    phone = models.CharField(_("Телефон"), max_length=1000, default='')
    adres = models.CharField(_("Адрес доставки"), max_length=1000, default='')

    class Meta:
        verbose_name = _("Профиль пользователя")
        verbose_name_plural = _("Профили пользователя")


class BaseShop(models.Model):
    created_date = models.DateTimeField(_("Дата создания"), auto_now_add=True, editable=False)
    edited_date = models.DateTimeField(_("Дата редактирования"), auto_now=True, editable=False, null=True)

    title = models.TextField(_("Название"), default='')
    meta_description = models.TextField(_("Description"), blank=True)
    meta_keywords = models.TextField(_("Keywords"), blank=True)
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
    code1c = models.IntegerField(_("Код базы"),  default=0)


    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        ordering = ['num']

class Brands(models.Model):
    title = models.CharField(_("Название"), default='', max_length=255)
    file = ImageField(_("Логотип"), upload_to='category', blank=True)

    class Meta:
        verbose_name = _("Бренд")
        verbose_name_plural = _("Бренды")

    def __str__(self):
        return self.title


class Item(BaseShop):

    content_small = models.CharField(_("Краткое описание"), max_length=800, default='', blank=True)
    content = RichTextUploadingField("Описание", blank=True)
    category = models.ManyToManyField(Category, verbose_name=u'Категория')
    status = models.BooleanField("Опубликовано", default=True)
    offer = models.BooleanField("Показывать в спецпредложениях", default=False, blank=True)
    price_1 = models.DecimalField(_("Цена"), max_digits=10, decimal_places=2, blank=True, null=True)
    num = models.IntegerField(default=0, verbose_name=u'Порядковый номер')
    brand = models.ForeignKey(Brands, verbose_name=u'Бренд', null=True, blank=True, on_delete=models.CASCADE)
    in_stock = models.IntegerField(default=0, verbose_name=u'Количество на складе')
    id1c = models.IntegerField(default=0, verbose_name=u'1C - ID')


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

    OFFER = 1
    ONPAY = 2
    PAYED = 3
    SENDED = 4
    ENDED = 5


    Status = (
        (OFFER, 'Оформлен'),
        (ONPAY, 'Разрешена оплата'),
        (PAYED, 'Оплачен'),
        (SENDED, 'Отправлен'),
        (ENDED, 'Завершен'),
    )

    created_date = models.DateTimeField(_("Дата создания"), auto_now_add=True, editable=False)
    customer = models.ForeignKey(auth_user, verbose_name=u'Пользователь', blank=True, null=True)
    total_price = models.DecimalField(_("Общая стоимость"), max_digits=10, decimal_places=2, blank=True, null=True)
    email = models.EmailField(_("Email"),  default='')
    address = models.TextField(_("Адрес доставки"))
    name =  models.TextField(_("ФИО заказчика"),default='')
    phone_number = models.TextField(_("Телефон"),default='')
    type_diliver = models.TextField(_("Тип доставки"),default='')
    order_pay = models.TextField(_("Оплата"),default='')
    status = models.IntegerField(choices=Status, default=OFFER)



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



