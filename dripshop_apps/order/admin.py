from django.contrib import admin
from .models import Order, OrderItem
from django.contrib import messages

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('user', 'total_price', 'status')
    list_filter = ('status',)
    search_fields = ('user__username',)

    def save_model(self, request, obj, form, change):
        original_obj = self.model.objects.get(pk=obj.pk) if change else None

        if change and obj.status != 'cancelled' and original_obj.status == 'cancelled':
            if not self.check_product_stock(obj):
                messages.error(request, "One or more products in the order do not have sufficient stock.")
                return

        super().save_model(request, obj, form, change)

        if change and obj.status == 'cancelled' and original_obj.status != 'cancelled':
            self.update_product_stock(obj, increase=True)
        elif change and original_obj.status == 'cancelled' and obj.status != 'cancelled':
            self.update_product_stock(original_obj, increase=False)

    def check_product_stock(self, order):
        for order_item in order.orderitem_set.all():
            product = order_item.product
            quantity = order_item.quantity
            if product.stock < quantity:
                return False
        return True

    def update_product_stock(self, order, increase):
        for order_item in order.orderitem_set.all():
            product = order_item.product
            quantity = order_item.quantity
            if increase:
                product.stock += quantity
            else:
                product.stock -= quantity
            product.save()