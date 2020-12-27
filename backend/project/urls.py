from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from sales.views import GenerateReceipt

# Admin Panel Header Name
admin.site.site_header = "The VegBox"
admin.site.site_title = "The VegBox Admin Portal"
admin.site.index_title = "Welcome to The VegBox Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chaining/', include('smart_selects.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('api/accounts/', include('accounts.urls')),
    path('api/items/', include('items.urls')),
    path('api/sales/', include('sales.urls')),
    path('receipt/<int:id>/', GenerateReceipt.as_view(), name='receipt'),
    re_path('^.*', TemplateView.as_view(template_name = 'index.html'))

] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += [re_path(r'^.*',
#                         TemplateView.as_view(template_name='index.html'))]