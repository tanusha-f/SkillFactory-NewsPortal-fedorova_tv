from django.urls import path
from .views import PostListView, PostDetailView, PostsSearchView, PostAddView, PostUpdateView, PostDeleteView


urlpatterns = [
    path('', PostListView.as_view()),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('search/', PostsSearchView.as_view()),
    path('add/', PostAddView.as_view()),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]
