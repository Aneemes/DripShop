from django.contrib import admin
from django.db.models import Q
from .models import Product, ProductImage
from dripshop_apps.category.models import Category
from dripshop_apps.brand.models import Brand
from django.db.models import Q
import nested_admin

class ProductImageInline(nested_admin.NestedTabularInline):
    model = ProductImage
    extra = 1
    sortable_field_name = ''

class ProductAdmin(nested_admin.NestedModelAdmin):
    list_display = ['title', 'price', 'brand', 'category', 'stock']
    list_filter = ['brand', 'category']
    search_fields = ['title', 'price', 'brand__title', 'category__title']
    inlines = [ProductImageInline]

    fields = (
        'title',
        'description',
        'price',
        'stock',
        'category',
        'brand',
        'featured',
        'published',
        'thumbnail',
    )

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # Search for products based on ascendant category names recursively
        matching_categories = self.find_matching_categories(search_term)
        ascendant_categories = self.get_all_ascendant_categories(matching_categories)
        products_with_ascendant_categories = self.model.objects.filter(category__in=ascendant_categories)
        queryset |= products_with_ascendant_categories

        return queryset, use_distinct

    def find_matching_categories(self, search_term):
        # Find categories that match the search term
        return Category.objects.filter(title__icontains=search_term)

    def get_all_ascendant_categories(self, categories):
        # Recursively retrieve all ascendant categories
        ascendant_categories = list(categories)
        new_ascendants = Category.objects.filter(parent__in=categories)
        if new_ascendants:
            ascendant_categories.extend(self.get_all_ascendant_categories(new_ascendants))
        return ascendant_categories

    def get_brand_title(self, obj):
        return obj.brand.title if obj.brand else None
    
    def get_category_title(self, obj):
        return obj.category.title if obj.category else None

    get_brand_title.short_description = 'Brand'
    get_category_title.short_description = 'Category'

    # Define the labels for list filters
    list_filter = (
        ('brand', admin.RelatedOnlyFieldListFilter),
        ('category', admin.RelatedOnlyFieldListFilter),
    )

admin.site.register(Product, ProductAdmin)


