from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import Post, Author, Category, UserCategory
from .filters import PostFilter
from .forms import PostForm


class PostsView(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = ['-time_in']
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all'] = len(self.get_queryset())
        context['author'] = False
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_object(self, **kwargs):
        pk_id = self.kwargs.get('pk')
        return Post.objects.get(pk=pk_id)

    def subs(self):
        subs_list = {}
        if self.request.user.pk:
            curr_post = self.get_object()
            for a in curr_post.category.values('id'):
                if not Category.objects.filter(pk=a.get('id'), subscribers=self.request.user).exists():
                    subs_list[a.get('id')] = Category.objects.get(pk=a.get('id')).name #.append(Category.objects.get(pk=a.get('id')).name)
        return subs_list

    def postcat(self):
        curr_post = self.get_object()
        post_cat = [cat for cat in curr_post.category.values_list('name', flat=True)]
        return post_cat

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subs'] = self.subs()
        context['post_cat'] = self.postcat()
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class PostsSearchView(ListView):
    model = Post
    template_name = 'posts_search.html'
    context_object_name = 'postss'
    ordering = ['-time_in']

    def get_queryset(self):
        queryset = super().get_queryset()
        return PostFilter(self.request.GET, queryset=queryset).qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['all'] = len(Post.objects.all())
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class PostAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    model = Post
    template_name = 'post_add.html'
    context_object_name = 'add'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context

    def get_initial(self):
        initial = super().get_initial()
        author = Author.objects.get(user=self.request.user)
        initial['author'] = author
        return initial

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return redirect("/profile/posts")


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    model = Post
    template_name = 'post_add.html'
    context_object_name = 'update'
    form_class = PostForm

    def get_form_kwargs(self):
        kwargs = super(PostUpdateView, self).get_form_kwargs()
        kwargs.update({'action': 'update'})
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        author = Author.objects.get(user=self.request.user)
        initial['author'] = author
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context

    def get_object(self, **kwargs):
        pk_id = self.kwargs.get('pk')
        return Post.objects.get(pk=pk_id)


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def subs_add(request, **kwargs):
    pk_id = kwargs.get('pk')

    UserCategory.objects.create(user=request.user, category=Category.objects.get(pk=pk_id))
    return redirect(request.META['HTTP_REFERER'])