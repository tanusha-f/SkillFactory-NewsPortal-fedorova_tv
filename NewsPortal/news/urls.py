from django.urls import path
from .views import PostsView, PostDetailView, PostsSearchView, PostAddView, PostUpdateView, PostDeleteView, subs_add


urlpatterns = [
    path('', PostsView.as_view()),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('search/', PostsSearchView.as_view()),
    path('add/', PostAddView.as_view()),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('subsadd/<int:pk>', subs_add, name='subsadd'),
]
