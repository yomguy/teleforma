# -*- coding: utf-8 -*-
# Copyright (c) 2007-2012 Parisson SARL

# This software is a computer program whose purpose is to backup, analyse,
# transcode and stream any audio content with its metadata over a web frontend.

# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".

# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.

# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.

# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
#
# Authors: Guillaume Pellerin <yomguy@parisson.com>

import os.path
from django.conf.urls import patterns, url, include
from django.conf import settings
from django.views.generic.base import RedirectView
from django.views.generic.list import ListView
from teleforma.models import *
from teleforma.views import *
from telemeta.views import *
from teleforma.forms import *
from registration.views import *
from jsonrpc import jsonrpc_site

htdocs_forma = os.path.dirname(__file__) + '/static/teleforma/'
profile_view = CRFPAProfileView()
document = DocumentView()
media = MediaView()

urlpatterns = patterns('',

    # login
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'telemeta/login.html'},
        name="teleforma-login"),
    # (r'^accounts/register0/$', RegistrationView.as_view(), {'form_class':CustomRegistrationForm}),
    url(r'^accounts/register/$', UserAddView.as_view(), name="teleforma-register"),
    url(r'^accounts/register/(?P<username>.*)/complete/$', UserCompleteView.as_view(), name="teleforma-register-complete"),
    url(r'^accounts/register/(?P<username>.*)/download/$', RegistrationPDFViewDownload.as_view(), name="teleforma-registration-download"),
    url(r'^accounts/register/(?P<username>.*)/view/$', RegistrationPDFView.as_view(), name="teleforma-registration-view"),
        
    url(r'^correctors/register/$', CorrectorAddView.as_view(), name="teleforma-corrector-register"),
    url(r'^correctors/register/(?P<username>.*)/complete/$', CorrectorCompleteView.as_view(), name="teleforma-corrector-register-complete"),
    url(r'^correctors/register/(?P<username>.*)/download/$', CorrectorRegistrationPDFViewDownload.as_view(), name="teleforma-corrector-registration-download"),
    url(r'^correctors/register/(?P<username>.*)/view/$', CorrectorRegistrationPDFView.as_view(), name="teleforma-corrector-registration-view"),

    url(r'^users/(?P<username>[A-Za-z0-9+@._-]+)/profile/$', profile_view.profile_detail,
                               name="teleforma-profile-detail"),
    url(r'^accounts/(?P<username>[A-Za-z0-9._-]+)/profile/$', profile_view.profile_detail, name="telemeta-profile-detail"),
    url(r'^accounts/(?P<username>[A-Za-z0-9._-]+)/profile/edit/$', profile_view.profile_edit, name="telemeta-profile-edit"),
    
    url(r'^captcha/', include('captcha.urls')),

    # Help
    url(r'^help/$', HelpView.as_view(), name="teleforma-help"),

    # Home
    url(r'^$', HomeRedirectView.as_view(), name="teleforma-home"),

    # Telemeta
    url(r'^', include('telemeta.urls')),

    # Desk
    url(r'^desk/$', HomeRedirectView.as_view(), name="teleforma-desk"),
    url(r'^desk/periods/(?P<period_id>.*)/courses/$', CourseListView.as_view(), name="teleforma-desk-period-list"),
    url(r'^desk/periods/(?P<period_id>.*)/courses_pending/$', CoursePendingListView.as_view(), name="teleforma-desk-period-pending"),
    url(r'^desk/periods/(?P<period_id>.*)/courses/(?P<pk>.*)/detail/$', CourseView.as_view(),
        name="teleforma-desk-period-course"),

    url(r'^desk/periods/(?P<period_id>.*)/medias/(?P<pk>.*)/detail/$', MediaView.as_view(), name="teleforma-media-detail"),
    url(r'^desk/periods/(?P<period_id>.*)/medias/(?P<pk>.*)/embed/$', MediaViewEmbed.as_view(), name="teleforma-media-embed"),
    url(r'^desk/periods/(?P<period_id>.*)/medias/(?P<pk>.*)/download/$', media.download, name="teleforma-media-download"),
    url(r'^desk/periods/(?P<period_id>.*)/medias/(?P<pk>.*)/stream/$', media.stream, name="teleforma-media-stream"),

    url(r'^desk/documents/(?P<pk>.*)/detail/$', DocumentView.as_view(),
        name="teleforma-document-detail"),
    url(r'^desk/documents/(?P<pk>.*)/download/$', document.download,
        name="teleforma-document-download"),
    url(r'^desk/documents/(?P<pk>.*)/view/$', document.view,
        name="teleforma-document-view"),

    url(r'^archives/annals/$', AnnalsView.as_view(), name="teleforma-annals"),
    url(r'^archives/annals/by-iej/(\w+)/$', AnnalsIEJView.as_view(), name="teleforma-annals-iej"),
    url(r'^archives/annals/by-course/(\w+)/$', AnnalsCourseView.as_view(), name="teleforma-annals-course"),

    url(r'^desk/periods/(?P<period_id>.*)/conferences/(?P<pk>.*)/video/$',
        ConferenceView.as_view(), name="teleforma-conference-detail"),
    url(r'^desk/periods/(?P<period_id>.*)/conferences/(?P<pk>.*)/audio/$',
        ConferenceView.as_view(template_name="teleforma/course_conference_audio.html"),
        name="teleforma-conference-audio"),
    url(r'^desk/conference_record/$', ConferenceRecordView.as_view(),
        name="teleforma-conference-record"),
    url(r'^desk/periods/(?P<period_id>.*)/conferences/list/$', ConferenceListView.as_view(),
        name="teleforma-conferences"),

    # APPOINTMENTS
    url(r'^desk/periods/(?P<period_id>.*)/appointments/$', Appointments.as_view(),
       name="teleforma-appointments"),
    url(r'^desk/periods/appointments/cancel$', cancel_appointment,
       name="teleforma-appointment-cancel"),

    # Postman
    url(r'^messages/write/(?:(?P<recipients>[^/#]+)/)?$', WriteView.as_view(), name='postman_write'),
    url(r'^messages/', include('postman.urls')),


    # Users
    url(r'^users/training/(?P<training_id>.*)/iej/(?P<iej_id>.*)/course/(?P<course_id>.*)/list/$',
        UsersView.as_view(), name="teleforma-users"),

    url(r'^users/training/(?P<training_id>.*)/iej/(?P<iej_id>.*)/course/(?P<course_id>.*)/export/$',
        UsersExportView.as_view(), name="teleforma-users-export"),

    url(r'^users/(?P<id>.*)/login/$', UserLoginView.as_view(), name="teleforma-user-login"),

    # Ajax update training
    url(r'^update-training/(?P<id>.*)/$', update_training, name="update-training"),

    # News Item
    url(r'^desk/periods/(?P<period_id>.*)/medias/(?P<pk>.*)/detail/$', MediaView.as_view(), name="teleforma-media-detail"),
    url(r'^newsitems/create', NewsItemCreate.as_view(), name='newsitem-create'),
    url(r'^newsitems/update/(?P<pk>.*)', NewsItemUpdate.as_view(), name='newsitem-update'),
    url(r'^newsitems/delete/(?P<pk>.*)', NewsItemDelete.as_view(), name='newsitem-delete'),
    url(r'^newsitems/(?P<period_id>.*)/list', NewsItemList.as_view(), name='newsitem-list'),

    # JSON RPC
    url(r'json/$', jsonrpc_site.dispatch, name='jsonrpc_mountpoint'),
    url(r'jsonrpc/$', jsonrpc_site.dispatch, name='jsonrpc_mountpoint'),

#    url(r'^private_files/', include('private_files.urls')),

    # JQCHAT
    url(r'^', include('jqchat.urls')),

    # EXAM
    url(r'^', include('teleforma.exam.urls')),
                       

    # Payment
    url(r'^payment/(?P<pk>.*)/start/$', PaymentStartView.as_view(),
        name="teleforma-payment-start"),

    url(r'^payment/bank_auto/(?P<merchant_id>.*)',
        bank_auto, name='teleforma-bank-auto'),
    url(r'^payment/bank_success/(?P<merchant_id>.*)',
        bank_success, name='teleforma-bank-success'),
    url(r'^payment/bank_cancel/(?P<merchant_id>.*)',
        bank_cancel, name='teleforma-bank-cancel'),

    url(r'^echec-de-paiement',
        bank_fail, name='teleforma-bank-fail'),

)
