from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]
SIZE_CHOICES = [(j, str(j)) for j in ['XS','S','M','L','XL','XXL']]
COLOR_CHOICES = [(k, str(k)) for k in ['Green','Blue','Red','Orange','Yellow','Black','White']]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
                                choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int)
    size = forms.TypedChoiceField(
                                choices=SIZE_CHOICES,
                                coerce=str)
    color = forms.TypedChoiceField(
                                choices=COLOR_CHOICES,
                                coerce=str)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
