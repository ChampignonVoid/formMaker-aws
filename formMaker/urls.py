from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView


# Test for sentry
def trigger_error(request):
    1 / 0


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', RedirectView.as_view(url=reverse_lazy('index'), permanent=True)),
    path('register/', include('register.urls')),
    path('', include('main.urls')),
    path('sentry-debug/', trigger_error),  # debug url
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
