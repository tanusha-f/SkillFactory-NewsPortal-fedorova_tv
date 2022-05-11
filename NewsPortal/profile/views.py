from django.views.generic import TemplateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect

from news.models import Category, Post
from .forms import SubsForm


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class SubsUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'profile/subs.html'
    model = User
    form_class = SubsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context

    def get_object(self, **kwargs):
        return User.objects.get(username=self.request.user.username)

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        user.category_set.clear()
        for sub in request.POST.getlist('category_set'):
            user.category_set.add(Category.objects.get(pk=sub))
        return redirect(request.META['HTTP_REFERER'])


class PostsAuthorView(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(author__user=self.request.user).order_by('-time_in')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all'] = len(self.get_queryset())
        context['author'] = True

        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context
