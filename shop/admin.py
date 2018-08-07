from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import Item, Item_image, Category, Order, Status, Brands, OrderItem
import nested_admin



from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)
class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline, ]
admin.site.register(User, UserProfileAdmin)


class Item_imageInline(nested_admin.NestedTabularInline):
    model = Item_image
    extra = 1
    ordering = ['num', ]





class ItemAdmin(nested_admin.NestedModelAdmin):
    inlines = [Item_imageInline,]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ('category',)
    # list_display = ('title', 'published_date', 'start_date', 'end_date', 'main_page')

    # list_filter = ['published_date', 'main_page']
    exclude=("file",)
    search_fields = ['title']

admin.site.register(Item, ItemAdmin)

class CategoryAdmin(DjangoMpttAdmin):
    exclude = ('num',)
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Category, CategoryAdmin)


class ItemInLineOrder(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('item','cols','price')
    exclude = ('title',)


    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False



class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id','created_date','total_price', 'type_diliver', )

    readonly_fields = ('total_price','type_diliver','email','address','phone_number','order_pay','name','customer')

    inlines = [
        ItemInLineOrder,
    ]



admin.site.register(Order, OrdersAdmin)






admin.site.register(Brands)


#class OrderAdmin(admin.ModelAdmin):
    #pass

    # readonly_fields=('customer', )


    # list_display = ('title', 'published_date', 'main_page')
    # list_editable = ['main_page', ]
    # list_filter = ['published_date', 'main_page']
    # search_fields = ['title', 'text']

#admin.site.register(Order, OrderAdmin)


#class StatusAdmin(admin.ModelAdmin):
    #list_display = ('title', 'num', 'default_status')
    #list_editable = ['default_status', ]

#admin.site.register(Status, StatusAdmin)
