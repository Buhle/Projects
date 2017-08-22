from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^create/$', views.staff_list_and_creation, name='create-staff'),
    # url(r'^members/(?P<_id>[^/]{36}/$', views.RetrieveStaffMembersViewSet.retrieve),
    url(r'^details/(?P<_id>[^/]{36})/$', views.retrieve_staff_details),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
