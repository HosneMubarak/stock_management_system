from django import forms
from .models import Stock


class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity']

    # def clean_category(self):
    #     category = self.cleaned_data.get('category')
    #     if not category:
    #         raise forms.ValidationError("Category is required!")
    #     for instance in Stock.objects.all():
    #         if instance.category == category:
    #             raise forms.ValidationError(category + ' is already exist')
    #     return category

    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')
        if not item_name:
            raise forms.ValidationError("Item Name is required!")
        for instance in Stock.objects.all():
            if instance.category == item_name:
                raise forms.ValidationError(item_name + ' is already exist')
        return item_name


class StockSearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)

    class Meta:
        model = Stock
        fields = ['category', 'item_name']


class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity']


class IssueForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['issue_to', 'issue_quantity']


class ReceiveForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['receive_quantity']


class ReorderForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['reorder_level']


