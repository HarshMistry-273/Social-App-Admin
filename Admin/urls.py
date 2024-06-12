from django.urls import path, include
from rest_framework import routers
from .Views import user_view, comment_view, like_view, post_view, follow_view
from .views import *

router = routers.DefaultRouter()
router.register(r'users', user_view.Users)
router.register(r'posts', post_view.Posts)
router.register(r'comments', comment_view.Comments)
router.register(r'likes', like_view.Likes)
router.register(r'follows', follow_view.Follows)

urlpatterns = [
    path('stats/', Analytics.as_view(), name='root'),
    path('', include(router.urls)),
    path('login/', Login.as_view()),
    path('export/users/', ExportUsers.as_view(), name='user_export'),

    # path('login-token/', login)
]

