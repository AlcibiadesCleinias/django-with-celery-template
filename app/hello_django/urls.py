from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from upload.views import image_upload, example_log_counter_view

urlpatterns = [
    path("", image_upload, name="upload"),
    path("foo-counter", example_log_counter_view, name="example_log_counter_view"),
    path("admin/", admin.site.urls),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
