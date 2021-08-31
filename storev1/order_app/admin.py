from django.contrib import admin
from .models import Order, orderItem

# Register your models here.

class OrderItemAdmin(admin.TabularInline):
	model = orderItem
	fieldsets = [
	('Product',{'fields':['product'],}),
	('Quantity',{'fields':['quantity'],}),
	('Price',{'fields':['price'],}),
	]
	readonly_fields = ['product','quantity','price']
	can_delete= False
	max_num = 0
	#template = 'admin/order/tabular.html'




@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ['id','billingName','email_address','created']
	list_display_links = ('id','billingName')
	search_fields = ['id','billingName','email_address']
	readonly_fields = ['id','token','total','email_address','created','billingName','billingAddress1','billingCity','billingPostCode','billingCountry','ShippingName','ShippingAddress1','ShippingCity','ShippingPostCode','ShippingCountry']
	fieldsets = [
	('ORDER INFORMATION',{'fields': ['id','token','total','created']}),
	('BILLING INFORMATION', {'fields': ['billingName','billingAddress1','billingCity','billingPostCode','billingCountry','email_address']}),
	('SHIPPING INFORMATION', {'fields': ['ShippingName','ShippingAddress1','ShippingCity','ShippingPostCode','ShippingCountry']}),
	]

	inlines = [
		OrderItemAdmin,
	]

	def has_delete_permission(self, request, obj=None):
		return False

	def has_add_permission(self, request):
		return False

