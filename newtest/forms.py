from django import forms

from .models import EmailTemplates

class EmailTemplatesForm(forms.ModelForm):
    class Meta:
        model = EmailTemplates
        fields = ('subject_template', 'body_template', 'send_messages')
