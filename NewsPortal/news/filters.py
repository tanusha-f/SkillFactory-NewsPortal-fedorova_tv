from django_filters import FilterSet, CharFilter, DateFilter, ChoiceFilter
from .models import Post, Author, Category
from django.forms.widgets import DateInput


class PostFilter(FilterSet):
    def __init__(self, *args, **kwargs):
        super(PostFilter, self).__init__(*args, **kwargs)
        auth = []
        for names in Author.objects.all().order_by('user__username').values('id', 'user__username'):
            auth.append((names.get('id'), names.get('user__username')))
        self.filters['author'].extra.update(
            {
                'choices': auth
            }
        )
        cat = []
        for names in Category.objects.all().values('id', 'name'):
            cat.append((names.get('id'), names.get('name')))
        self.filters['category'].extra.update(
            {
                'choices': cat
            }
        )

    type = ChoiceFilter(field_name='type', label='Тип публикации', choices=Post.TYPE)
    author = ChoiceFilter(field_name='author', label='Имя автора')
    title = CharFilter(field_name='head', lookup_expr='icontains',
                       label='Заголовок')
    data = DateFilter(field_name='time_in', lookup_expr='gt',
                      label='Опубликовано не ранее', widget=DateInput(format='%d.%m.%Y', attrs={'type': 'date'}))
    category = ChoiceFilter(field_name='category', label='Категория', )

    class Meta:
        model = Post
        fields = ('type', 'author', 'title', 'data', 'category',)
