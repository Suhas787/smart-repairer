from django.contrib import admin
from django.urls import path, include

# --- MEDIA IMPORTS ---
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('repair.urls')),
    
    # ❌ I DISABLED THIS LINE BECAUSE IT IS CAUSING THE ERROR
    # path('api/', include('api.urls')), 
]

# --- SERVE MEDIA FILES (IMAGES) ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)