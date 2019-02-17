from django import forms
from django.contrib.auth.models import User, Group


class UserForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User

        fields = ['first_name', 'last_name',
                  'email', 'username', 'password', 'role']

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            # we get the 'initial keyword argument or initialize it
            # as a dict if it didn't exists
            initial = kwargs.setdefault('initial', {})
            # The widget for a MultipleChoiceFields expects
            # A list of primary key for the selected data.
            if kwargs['instance'].groups.all():
                initial['role'] = kwargs['instance'].groups.all()[0]
            else:
                initial['role'] = None

        forms.ModelForm.__init__(self, *args, **kwargs)

    def save(self):
        password = self.cleaned_data.pop('password')
        role = self.cleaned_data.pop('role')
        u = super().save()
        u.groups.set([role])
        u.set_password(password)
        u.save()
        return u
