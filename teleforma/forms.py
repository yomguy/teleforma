from teleforma.models import *
from django.forms import ModelForm, ModelChoiceField, BooleanField
from postman.forms import WriteForm as PostmanWriteForm
from postman.fields import BasicCommaSeparatedUserField

from registration.forms import RegistrationForm
from django.utils.translation import ugettext_lazy as _
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSet
from captcha.fields import CaptchaField

from teleforma.models.core import Course, Professor
from tinymce.widgets import TinyMCE
from itertools import cycle


class ConferenceForm(ModelForm):

    class Meta:
        model = Conference


class UserForm(ModelForm):

    captcha = CaptchaField()
    accept = BooleanField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'accept']


RegistrationForm.base_fields.update(UserForm.base_fields)


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'wifi_login', 'wifi_pass', 'language', 'expiration_date',
                    'init_password', ]

RegistrationForm.base_fields.update(ProfileForm.base_fields)


class StudentForm(ModelForm):

    class Meta:
        model = Student
        exclude = ['user', 'trainings', 'options']


RegistrationForm.base_fields.update(StudentForm.base_fields)


class CustomRegistrationForm(RegistrationForm):

    def save(self, profile_callback=None):
        user = super(CustomRegistrationForm, self).save(profile_callback=None)
        profile, c = Profile.objects.get_or_create(user=user, \
            address=self.cleaned_data['address'], \
            telephone=self.cleaned_data['telephone'])


class ProfileInline(InlineFormSet):

    model = Profile
    can_delete = False
    exclude = ['wifi_login', 'wifi_pass', 'language', 'expiration_date',
                    'init_password']


class StudentInline(InlineFormSet):

    model = Student
    can_delete = False
    fields = ['portrait', 'level', 'iej', 'period', 'training', 'platform_only', 'procedure',
                'written_speciality', 'oral_1', 'promo_code']


    def get_factory_kwargs(self):
        kwargs = super(StudentInline, self).get_factory_kwargs()

        def get_field_qs(field, **kwargs):
            formfield = field.formfield(**kwargs)
            if field.name == 'period':
                formfield.queryset = Period.objects.filter(is_open=True)
            elif field.name == 'portrait':
                formfield.widget.attrs.update(accept="image/*;capture=camera")
            return formfield

        kwargs.update({
            'formfield_callback': get_field_qs
        })
        return kwargs


class NewsItemForm(ModelForm):
    class Meta:
        model = NewsItem
        exclude = ['created', 'creator', 'deleted']
        widgets = {
            'description': TinyMCE({'cols':80, 'rows':30}),
        }



class WriteForm(PostmanWriteForm):
    recipients = BasicCommaSeparatedUserField(label=(_("Recipients"), _("Recipient")), help_text='')
    course = ModelChoiceField(queryset=Course.objects.all(), required=False)

    class Meta(PostmanWriteForm.Meta):
        fields = ('course', 'recipients', 'subject', 'body')

    def clean_recipients(self):
        """compute recipient if 'auto' is set"""
        recipients = self.cleaned_data['recipients']
        course = self.cleaned_data.get('course')
        return recipients