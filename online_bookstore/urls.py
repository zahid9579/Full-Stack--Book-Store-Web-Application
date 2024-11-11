
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Login view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('testapp.urls')), 
    path('', RedirectView.as_view(url='/book/', permanent=False)),
 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
