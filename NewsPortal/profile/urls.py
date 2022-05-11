from django.urls import path
from .views import IndexView, SubsUpdateView, PostsAuthorView

urlpatterns = [
    path('', IndexView.as_view()),
    path('subs', SubsUpdateView.as_view()),
    path('posts', PostsAuthorView.as_view()),
]
