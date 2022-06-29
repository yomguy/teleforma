# -*- coding: utf-8 -*-

from optparse import make_option
import logging
import os
from copy import deepcopy

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse
from teleforma.models.core import Conference, Period
from teleforma.models.crfpa import Student
from teleforma.models.notification import notify
from teleforma.views.core import get_courses
import datetime


class Logger:
    """A logging object"""

    def __init__(self, file):
        self.logger = logging.getLogger('myapp')
        self.hdlr = logging.FileHandler(file)
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.hdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.hdlr)
        self.logger.setLevel(logging.INFO)


class Command(BaseCommand):
    help = """Publish conferences and notify users when \
            conference.date_publish is equal or greater \
            than current date """

    def add_arguments(self, parser):
        parser.add_argument('--logfile', type=str, required=True,
                            help='log file to use')

        parser.add_argument('--period', type=str, required=True,
                            help='period to process')

    def handle(self, *args, **options):
        logpath = options['logfile']
        logger = Logger(logpath)

        period_name = options['period']
        period = Period.objects.get(name=period_name)

        conferences = Conference.objects.filter(
                        period=period,
                        status=2,
                        notified=False,
                        date_publish__lte=datetime.datetime.now()
                        )

        for conference in conferences:
            conference.status = 3
            conference.save()
            logger.logger.info("Conference published: " + conference.public_id)
         
            media = conference.media.filter(mime_type='video/mp4')[0]
            url = reverse('teleforma-media-detail', args=[conference.period.id, media.id])
            message = "Nouvelle conférence publiée : " + str(conference)

            students = Student.objects.filter(period=conference.period)
            for student in students:
                if student.user:
                    courses = get_courses(student.user, period=conference.period)
                    for course in courses:
                        if conference.course == course['course'] and \
                                conference.course_type in course['types']:
                            notify(student.user, message, url)
                            logger.logger.info("Student notified: " + student.user.username)

            conference.notified = True
            conference.save()
