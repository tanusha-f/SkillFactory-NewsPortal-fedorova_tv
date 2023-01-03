from django.urls import path
from news.views import PostAddView, PostUpdateView, PostDeleteView, PostDetailView


urlpatterns = [
    path('<int:pk>/', PostDetailView.as_view(), name='art_detail'),
    path('add/', PostAddView.as_view()),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='art_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='art_delete'),
]
