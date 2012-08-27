# -*- coding: utf-8 -*- 

from django.forms import ModelForm
from django import forms
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _
from dwitter.main.models import Member

class MemberForm(ModelForm):
    image = forms.ImageField(label=u'Εικόνα', required=False)
    class Meta:
        model = Member
        exclude = ('user','following')
        widgets = {'descr':widgets.Textarea(attrs={'rows':'3','class':'input-xlarge'})}

class SearchForm(forms.Form):
    member = forms.CharField(label=_(u'Users'), required=False, help_text=_(u'Words seperated with spaces.'),
            widget = widgets.TextInput(attrs={'placeholder':_(u'Users'),'class':'input-xlarge'}))
    hash = forms.CharField(label=_(u'Hash tags'), required=False, help_text=_(u'Tags without # seperated with spaces.'),
            widget = widgets.TextInput(attrs={'placeholder':_(u'Hash tags'),'class':'input-xlarge'}))

