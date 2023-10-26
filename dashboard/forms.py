from django import forms
from django.forms import ModelForm

from shop.models import Product, Category, Subcategory
from orders.models import OrderItem, Order


class AddProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'image', 'code', 'title', 'number', 'price', 'description']

    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class AddCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class AddSubcategoryForm(ModelForm):
    class Meta:
        model = Subcategory
        fields = ['name', 'category']
    
    # def __init__(self, *args, **kwargs):
    #     super(AddSubcategoryForm, self).__init__(*args, **kwargs)
    #     self.fields['name'].widget.attrs['class'] = 'form-control'
    #     self.fields['category'].widget.attrs['class'] = 'form-control'


class EditProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'image', 'code', 'title', 'number', 'price', 'description']

    def __init__(self, *args, **kwargs):
        super(EditProductForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ApproveForm(ModelForm):
    class Meta:
        model = Order
        fields = ('status', 'refuse', 'date_receive')
        exclude = ('user', 'created')