from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.company_list_and_creation, name='company_app-create'),
    url(r'^create/$', views.CreateCompanyViewSet.as_view, name='company_app-create'),
    url(r'^details/(?P<_id>[^/]{36})/$', views.retrieve_company_details),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
