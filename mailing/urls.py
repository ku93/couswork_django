from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import (HomeView, MailingCreateView, MailingDeleteView,
                           MailingDetailView, MailingListView,
                           MailingUpdateView, SendMailingView)

app_name = MailingConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("mailing/", MailingListView.as_view(), name="mailing_list"),
    path("mailing/create/", MailingCreateView.as_view(), name="mailing_create"),
    path("mailing/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"),
    path(
        "mailing/<int:pk>/update/", MailingUpdateView.as_view(), name="mailing_update"
    ),
    path(
        "mailing/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"
    ),
    path("mailing/send/<int:pk>/", SendMailingView.as_view(), name="send_mailing"),
]
