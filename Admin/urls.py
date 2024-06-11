from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'users', Users)
router.register(r'posts', Posts)
router.register(r'comments', Comments)
router.register(r'likes', Likes)
router.register(r'follows', Follows)

urlpatterns = [
    path('stats/', Analytics.as_view(), name='root'),
    path('', include(router.urls)),
    path('login/', Login.as_view()),
    path('export/users/', ExportUsers.as_view(), name='user_export'),

    # path('login-token/', login)
]

