import django_filters
from .models import Product, Size


class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    sizes = django_filters.ModelMultipleChoiceFilter(
        queryset=Size.objects.all(),
        field_name="sizes",
        to_field_name="slug"
    )

    class Meta:
        model = Product
        fields = ['category', 'available', 'color', 'sizes', 'price_min', 'price_max']
