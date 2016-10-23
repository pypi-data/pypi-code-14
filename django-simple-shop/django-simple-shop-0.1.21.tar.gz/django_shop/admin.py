from django.contrib import admin
from django.db import transaction
from django.utils.safestring import mark_safe
from django_summernote.admin import SummernoteModelAdmin

from .models import ProductCategory, Product, ProductImage, ProductEntry, \
    DeliveryType, PaymentType, Order, ProductOrder, \
    ProductCategoryCustomField, ProductCustomFieldValue, PackagingBox
from .admin_forms import ProductImageAdminForm, DeliveryTypeAdminForm, \
    PaymentTypeAdminForm, ProductCategoryCustomFieldForm, \
    ProductCustomFieldValueForm
from .utils.payment import get_description
from .utils.delivery import get_description as get_delivery_description


class ProductCategoryCustomFieldInline(admin.StackedInline):
    form = ProductCategoryCustomFieldForm
    model = ProductCategoryCustomField
    extra = 0
    fields = (
        ('name', 'key'),
        ('type', 'choices'),
        ('is_filter', 'required', 'hidden'),
    )
    prepopulated_fields = {
        'key': ('name',),
    }


@admin.register(ProductCategory)
class ProductCategoryAdmin(SummernoteModelAdmin):
    form = ProductImageAdminForm
    list_display = ('name', 'priority')
    prepopulated_fields = {
        'slug': ('name',),
    }
    fields = (
        ('name', 'priority'),
        'slug',
        'description',
        'image'
    )

    inlines = [
        ProductCategoryCustomFieldInline
    ]

    def get_fields(self, request, obj=None):
        if not request.user.has_perm('django_shop.category_can_edit_important'):
            return ProductCategory.NON_IMPORTANT_FIELDS
        return super(ProductCategoryAdmin, self).get_fields(request, obj=obj)

    def get_prepopulated_fields(self, request, obj=None):
        if not request.user.has_perm('django_shop.category_can_edit_important'):
            return {}
        return super(ProductCategoryAdmin, self).get_prepopulated_fields(request, obj=obj)

    def save_related(self, request, form, formsets, change):
        super(ProductCategoryAdmin, self).save_related(request, form,
                                                       formsets, change)
        for p in form.instance.products.all():
            p.check_fields()


class ProductImageInline(admin.TabularInline):
    form = ProductImageAdminForm
    model = ProductImage
    extra = 1


class ProductEntryInline(admin.TabularInline):
    fields = ('quantity', 'price')
    model = ProductEntry
    extra = 1

    def get_queryset(self, request):
        qs = super(ProductEntryInline, self).get_queryset(request)
        return qs.filter(quantity__gt=0)


class ProductCustomValueInline(admin.TabularInline):
    model = ProductCustomFieldValue
    form = ProductCustomFieldValueForm
    fields = ('field', 'value')
    readonly_fields = ('field',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    list_display = ('name', 'price', 'in_stock', 'is_weight')
    prepopulated_fields = {
        'slug': ('name',),
    }
    inlines = [
        ProductImageInline,
        ProductEntryInline,
    ]
    filter_horizontal = ('categories',)
    list_filter = (
        ('categories', admin.RelatedOnlyFieldListFilter),
    )
    actions = ['copy_products']

    def get_fields(self, request, obj=None):
        if not request.user.has_perm('django_shop.category_can_edit_important'):
            return Product.NON_IMPORTANT_FIELDS
        return super(ProductAdmin, self).get_fields(request, obj=obj)

    def get_prepopulated_fields(self, request, obj=None):
        if not request.user.has_perm('django_shop.category_can_edit_important'):
            return {}
        return super(ProductAdmin, self).get_prepopulated_fields(request, obj=obj)

    def get_form(self, request, obj=None, **kwargs):
        if obj is not None and ProductCustomValueInline not in self.inlines:
            self.inlines = [ProductCustomValueInline] + self.inlines

        return super(ProductAdmin, self).get_form(request, obj=obj, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.save()
        obj.check_fields()

    def save_related(self, request, form, formsets, change):
        super(ProductAdmin, self).save_related(request, form, formsets, change)
        form.instance.check_fields()

    def copy_products(self, request, queryset):
        if not request.user.has_perm('django_shop.add_product'):
            return
        for product in queryset:
            product.create_copy()
    copy_products.short_description = "Создать копии выбранных продуктов"


@admin.register(PaymentType)
class PaymentTypeAdmin(SummernoteModelAdmin):
    list_display = ('name', 'payment_type', 'payment_hook_name', 'is_active')
    form = PaymentTypeAdminForm

    def payment_hook_name(self, obj):
        return get_description(obj.payment_hook)
    payment_hook_name.short_description = 'Конкретный тип онлайн оплаты'


@admin.register(DeliveryType)
class DeliveryTypeAdmin(SummernoteModelAdmin):
    list_display = ('name', 'pricing_method', 'delivery_hook',
                    'actual_pricing', 'is_active')
    form = DeliveryTypeAdminForm

    def delivery_hook_name(self, obj):
        return get_delivery_description(obj.delivery_hook)
    delivery_hook_name.short_description = 'Конкретный тип API доставки'


class ProductOrderInline(admin.TabularInline):
    fields = ('__str__', 'quantity', 'price')
    readonly_fields = ('__str__', 'quantity', 'price')
    model = ProductOrder
    extra = 0

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'products_string_html', 'state', 'created',
                    'changed', 'full_price')
    fields = ('state', 'created', 'changed', 'delivery_type', 'delivery_price',
              'receiver', 'full_price', 'payment_method')
    readonly_fields = ('created', 'changed', 'receiver', 'full_price',
                       'payment_method')
    inlines = [
        ProductOrderInline
    ]

    def get_actions(self, request):
        actions = super(OrderAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super(OrderAdmin, self).get_form(request, obj, **kwargs)
        if obj is not None:
            # Modify form.base_fields['state'].choices
            form.base_fields['state'].choices = obj.get_state_choices()
        return form

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        with transaction.atomic():
            if change:
                current_version = Order.objects.get(pk=obj.id)
                if current_version.state == Order.STATE_CREATED and \
                        obj.state == Order.STATE_CONFIRMED:
                    obj.reduce_stock_amount()

            obj.save()

    def products_string_html(self, obj):
        return mark_safe(obj.products_string.replace('\n', '<br>'))
    products_string_html.short_description = 'Заказ'


admin.site.register(PackagingBox)
