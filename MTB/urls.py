from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lend_money.urls')),  # Include the lend_money app URLs
    # Include other app URLs here
]