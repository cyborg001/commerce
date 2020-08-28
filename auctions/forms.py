from django import forms

class BidForm(forms.Form):
    new_price    = forms.IntegerField(label='New Bid',min_value=0)

class AuctionForm(forms.Form):
    title = forms.CharField(max_length=64)
    description = forms.CharField(widget=forms.Textarea)
    url_image = forms.CharField(max_length=100,required=False)
    category = forms.CharField(max_length=100,required=False)
    starting_bid = forms.IntegerField(min_value=0)

class CommentForm(forms.Form):
    comentario = forms.CharField(widget=forms.Textarea)
