
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls), # Ši viena eilutė „įtraukia“ visų modelių admin puslapius
    path ('accounts/', include('django.contrib.auth.urls')),
    path('', include('okr.urls')), # Čia sakome: "Viską, kas ne admin, siųsk į okr programėlę"
]




