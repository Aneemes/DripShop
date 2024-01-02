from django.views.generic import ListView, DetailView
from .models import Brand

class PublishedBrandListView(ListView):
    model = Brand
    template_name = 'brand/brand_list.html'
    context_object_name = 'brands'

    def get_queryset(self):
        return Brand.objects.get_published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_brands'] = Brand.objects.get_featured()
        return context

class BrandDetailView(DetailView):
    model = Brand
    template_name = 'brand/brand_detail.html'
    context_object_name = 'brand'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add featured products for the category to the context
        context['featured_products'] = self.object.featured_products.all()
        return context
