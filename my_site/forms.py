from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
	CHOICES = (
				('database1','database1'),
				('database2','database2'),
				('database3','database3'),
				('database4','database4'),
				('database5','database5'),
			)

	first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
	email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
	database_choices =  forms.MultipleChoiceField(choices=CHOICES,widget=forms.CheckboxSelectMultiple)

	
class ProductForm(forms.Form):
	product_name = forms.CharField(max_length=30)
	product_slug = forms.CharField(max_length=30,required=False, help_text='Optional.')
	product_description = forms.CharField(widget=forms.Textarea)
	product_price = forms.FloatField(required=False,widget=forms.NumberInput()) 
	
	def __init__(self, *args, **kwargs):		
		database_choices_list = []
		if 'database_list' in kwargs:
			database_choices_list = kwargs['database_list']
			queryset = kwargs.pop('database_list')
		super(ProductForm, self).__init__(*args, **kwargs)
		self.fields['database_choice'] = forms.ChoiceField(choices =[ (each_db,each_db)  for each_db in database_choices_list ])
		

		