from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm


class PostListView(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = ['-time_in']
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['all'] = len(self.get_queryset())
        return context


class PostsSearchView(ListView):
    model = Post
    template_name = 'posts_search.html'
    context_object_name = 'postss'
    ordering = ['-time_in']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['time_now'] = datetime.utcnow()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'


class PostAddView(CreateView):
    model = Post
    template_name = 'post_add.html'
    context_object_name = 'add'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_add.html'
    context_object_name = 'update'
    form_class = PostForm

    def get_object(self, **kwargs):
        pk_id = self.kwargs.get('pk')
        return Post.objects.get(pk=pk_id)


class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
