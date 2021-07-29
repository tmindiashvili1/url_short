from django import forms

class UrlShortForm(forms.Form):
    original_url = forms.CharField(required=True,label='Url',max_length=2083,error_messages={
        "required": "Your url must not be empty",
        "max_length": "Please enter a shorter url"
    })
    password = forms.CharField(required=False, label='Password',widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UrlShortForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'