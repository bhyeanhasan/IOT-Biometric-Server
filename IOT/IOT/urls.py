from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('customers.urls')),
    path('admin/', admin.site.urls),
]


# from django.urls import include, path
# from rest_framework import routers
# from rest_framework.authtoken.views import obtain_auth_token
# from api import views
#
# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)
#
# # Wire up our API using automatic URL routing.
# # Additionally, we include login URLs for the browsable API.
# urlpatterns = [
#     # path('', include(router.urls)),
#     path('api/', include('api.urls')),
#     path('api/login-token', obtain_auth_token),
#     path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
#     path('admin/', admin.site.urls),
# ]
