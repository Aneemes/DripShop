from django.views.generic import ListView, DetailView
from .models import Category

class PublishedCategoryListView(ListView):
    model = Category
    template_name = 'category/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.get_published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_categories'] = Category.objects.get_featured()
        return context

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category/category_detail.html'
    context_object_name = 'category'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add featured products for the category to the context
        context['featured_products'] = self.object.featured_products.all()
        return context
