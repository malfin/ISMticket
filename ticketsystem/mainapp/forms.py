from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User

from mainapp.models import Tickets, News, UserProfile


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = (
            'title',
            'text',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, item in self.fields.items():
            item.widget.attrs['class'] = 'form-control mt-2'
            item.widget.attrs['style'] = 'resize: none'
            item.help_text = ''


class SupportForm(forms.ModelForm):
    class Meta:
        model = Tickets
        fields = (
            'message',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, item in self.fields.items():
            item.widget.attrs['class'] = f'form-control {name} form-control'
            item.widget.attrs['style'] = f'resize: none'
            item.widget.attrs['placeholder'] = f'Опишите вашу проблему, как можно точнее.'


class CreateSupportForm(forms.ModelForm):
    class Meta:
        model = Tickets
        fields = (
            'category',
            'title',
            'message',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, item in self.fields.items():
            item.widget.attrs['class'] = f'form-control {name} form-control'
            item.widget.attrs['style'] = f'resize: none'


class SupportFormAdmin(forms.ModelForm):
    class Meta:
        model = Tickets
        fields = (
            'category',
            'title',
            'answer',
            'status',
            'desk',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, item in self.fields.items():
            item.widget.attrs['class'] = f'form-control {name} form-control'
            item.widget.attrs['style'] = f'resize: none'


class ChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, item in self.fields.items():
            item.widget.attrs['class'] = 'form-control'
            item.help_text = ''
            if name == 'password':
                item.widget = forms.HiddenInput()


class ChangeFormAdmin(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'is_superuser',
            'is_staff',
            'is_active',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, item in self.fields.items():
            item.widget.attrs['class'] = 'form-control'
            self.fields['is_superuser'].widget.attrs.update({'class': 'checkbox_animated'})
            self.fields['is_staff'].widget.attrs.update({'class': 'checkbox_animated'})
            self.fields['is_active'].widget.attrs.update({'class': 'checkbox_animated'})
            item.help_text = ''
            if name == 'password':
                item.widget = forms.HiddenInput()


class ChangePassword(PasswordChangeForm):
    class Meta:
        model = User
        fields = 'password'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, item in self.fields.items():
            item.widget.attrs['class'] = 'form-control'

    def get_form(self, form_class):
        return form_class(self.request.user, **self.get_form_kwargs())


class RegisterFormAdmin(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'email',
            'is_superuser',
            'is_staff',
            'is_active',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, item in self.fields.items():
            item.widget.attrs['class'] = f'form-control {name}'
            self.fields['is_superuser'].widget.attrs.update({'class': 'checkbox_animated'})
            self.fields['is_staff'].widget.attrs.update({'class': 'checkbox_animated'})
            self.fields['is_active'].widget.attrs.update({'class': 'checkbox_animated'})
            item.help_text = ''

    def save(self, commit=True):
        user = super().save(commit=commit)
        UserProfile.objects.create(user=user)
        return user
