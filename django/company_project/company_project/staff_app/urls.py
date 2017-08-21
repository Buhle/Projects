from staff_app import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^create/$', views.CreateStaffViewSet.create, name='create-staff'),
    url(r'^members/(?P<id>[^/]+)/$', views.RetrieveStaffMembersViewSet.retrieve),
    url(r'^details/(?P<id>\d+)/$', views.retrieve_staff_details),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
