from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.views.static import serve
from pets.views import pet_list


urlpatterns = [
    # Custom Admin Panel at /admin-panel/
    path('admin-panel/', include('custom_admin.urls')),
    # Redirect default /admin/ to /admin-panel/ as requested by user
    path('admin/', RedirectView.as_view(url='/admin-panel/', permanent=False)),
    path('django-admin/', admin.site.urls),

    path('', pet_list, name='home'),
    path('pets/', include('pets.urls')),
    path('adoptions/', include('adoptions.urls')),
    path('accounts/', include('accounts.urls')),
    path('api/', include('pets.api_urls')),
    path('api/', include('adoptions.api_urls')),
    path('community/', include('community.urls')),
    path('store/', include('store.urls')),
    path('vets/', include('vets.urls')),

    # Backwards compatibility redirect for password-reset
    path('accounts/password-reset/', RedirectView.as_view(pattern_name='forgot_password', permanent=False), name='password_reset'),

    # Explicit media serving fallback (ensures uploaded media works even if DEBUG=False or in /tmp)
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
