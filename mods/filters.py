import django_filters
from .models import Post


class PostFilter(django_filters.FilterSet):

    CHOICES = (
        ('ascending', 'Ascending'),
        ('descending', 'Descending'),
    )

    CATEGORIES = (
        ('1', 'Combat'),
        ('2', 'Food'),
        ('3', 'Storage'),
        ('4', 'Magic'),
        ('5', 'World Gen'),
        ('6', 'API and Library'),
        ('7', 'Mobs and Creatures'),
        ('8', 'Armor, Tools and Weapons'),
        ('9', 'Cosmetic'),
        ('10', 'Technology'),
        ('11', 'Miscellaneous'),
        ('12', 'Other'),
    )

    category = django_filters.ChoiceFilter(choices=Post.CATEGORY_CHOICES)
    version = django_filters.ChoiceFilter(label='Version', choices=Post.MOD_VERSION)
    ordering = django_filters.ChoiceFilter(label='Ordering', choices=CHOICES, method='filter_by_order')

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'content': ['icontains'],
            'tags': ['icontains'],
        }

    def filter_by_order(self, queryset, name, value):
        expression = 'date_posted' if value == 'ascending' else '-date_posted'
        return queryset.order_by(expression)
