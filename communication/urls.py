from django.urls import path

from communication.apps import CommunicationConfig
from communication.views import (CommunicationCreateView,
                                 CommunicationDeleteView,
                                 CommunicationDetailView,
                                 CommunicationListView,
                                 CommunicationUpdateView)

app_name = CommunicationConfig.name

urlpatterns = [
    path("communication", CommunicationListView.as_view(), name="communication_list"),
    path(
        "communication/create/",
        CommunicationCreateView.as_view(),
        name="communication_create",
    ),
    path(
        "communication/<int:pk>/",
        CommunicationDetailView.as_view(),
        name="communication_detail",
    ),
    path(
        "communication/<int:pk>/update/",
        CommunicationUpdateView.as_view(),
        name="communication_update",
    ),
    path(
        "communication/<int:pk>/delete/",
        CommunicationDeleteView.as_view(),
        name="communication_delete",
    ),
]
