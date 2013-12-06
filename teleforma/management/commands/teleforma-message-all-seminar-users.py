from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.core.mail import send_mail, mail_admins
from django.utils import translation
from telemeta.models import *
from telemeta.util.unaccent import unaccent
from teleforma.models import *
import logging
import datetime
from postman.models import *
from postman.utils import email_visitor, notify_user



class Command(BaseCommand):
    help = "Broadcast a message to all users thanks to their subscription"
    message_template = 'teleforma/messages/seminar_remind.txt'
    subject_template = 'teleforma/messages/seminar_remind_subject.txt'
    language_code = 'fr_FR'

    def handle(self, *args, **options):
        users = User.objects.all()
        translation.activate(self.language_code)
        sender_email = settings.DEFAULT_FROM_EMAIL
        sender = User.objects.get(email=sender_email)
        today = datetime.datetime.now()

        for user in users:
            auditor = user.auditor.all()
            professor = user.professor.all()

            if auditor and not professor and user.is_active and user.email:
                auditor = auditor[0]
                seminars = auditor.seminars.all()
                for seminar in seminars:
                    if seminar.expiry_date:
                        delta = seminar.expiry_date - today
                        if delta.days < 30:
                            context = {}
                            organization = seminar.course.department.name
                            site = Site.objects.get_current()
                            path = reverse('teleforma-seminar-detail', kwargs={'pk':seminar.id})
                            gender = auditor.get_gender_display()

                            if seminar.sub_title:
                                title = seminar.sub_title + ' : ' + seminar.title
                            else:
                                title = seminar.title

                            context['gender'] = gender
                            context['first_name'] = user.first_name
                            context['last_name'] = user.last_name
                            context['site'] = site
                            context['path'] = path
                            context['title'] = title
                            context['organization'] = organization
                            context['date'] = seminar.expiry_date
                            
                            text = render_to_string(self.message_template, context)
                            subject = render_to_string(self.subject_template, context)
                            subject = '%s : %s' % (seminar.title, subject)

                            mess = Message(sender=sender, recipient=user, subject=subject[:119], body=text)
                            mess.moderation_status = 'a'
                            mess.save()
                            #notify_user(mess, 'acceptance')
                            
                            print user.username, seminar.title
