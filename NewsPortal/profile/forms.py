from django.forms import ModelForm, MultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple
from django.contrib.auth.models import User
from news.models import Category


class SubsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SubsForm, self).__init__(*args, **kwargs)
        self.initial.update({'category_set': [cat for cat in kwargs['instance'].category_set.all().values_list('id', flat=True)]})
        choice = []
        for names in Category.objects.all().values('id', 'name'):
            choice.append((names.get('id'), names.get('name')))
        self.fields['category_set'].choices = choice

    category_set = MultipleChoiceField(label='Категории', widget=CheckboxSelectMultiple)

    class Meta:
        model = User
        fields = ('category_set',)
