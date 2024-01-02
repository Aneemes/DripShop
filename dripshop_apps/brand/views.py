from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from .models import Brand
from dripshop_apps.product.models import Product

class PublishedBrandListView(ListView):
    model = Brand
    template_name = 'brand/brand_list.html'
    context_object_name = 'brands'
    paginate_by = 12 

    def get_queryset(self):
        return Brand.objects.get_published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Paginate published brands
        published_brands = Brand.objects.get_published()
        paginator = Paginator(published_brands, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            published_brands = paginator.page(page)
        except PageNotAnInteger:
            published_brands = paginator.page(1)
        except EmptyPage:
            published_brands = paginator.page(paginator.num_pages)

        context['brands'] = published_brands

        # Paginate featured brands
        featured_brands = Brand.objects.get_featured()
        paginator_featured = Paginator(featured_brands, self.paginate_by)
        page_featured = self.request.GET.get('page_featured')

        try:
            featured_brands = paginator_featured.page(page_featured)
        except PageNotAnInteger:
            featured_brands = paginator_featured.page(1)
        except EmptyPage:
            featured_brands = paginator_featured.page(paginator_featured.num_pages)

        context['featured_brands'] = featured_brands

        return context


class BrandDetailView(DetailView):
    model = Brand
    template_name = 'brand/brand_detail.html'
    context_object_name = 'brand'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Featured products for the brand
        featured_products = self.object.featured_products.all()
        paginator_featured = Paginator(featured_products, self.paginate_by)
        page_featured = self.request.GET.get('page_featured')

        try:
            featured_products = paginator_featured.page(page_featured)
        except PageNotAnInteger:
            featured_products = paginator_featured.page(1)
        except EmptyPage:
            featured_products = paginator_featured.page(paginator_featured.num_pages)

        context['featured_products'] = featured_products

        # Published products for the brand
        published_products = Product.objects.published().filter(brand=self.object)
        paginator_published = Paginator(published_products, self.paginate_by)
        page_published = self.request.GET.get('page_published')

        try:
            published_products = paginator_published.page(page_published)
        except PageNotAnInteger:
            published_products = paginator_published.page(1)
        except EmptyPage:
            published_products = paginator_published.page(paginator_published.num_pages)

        context['published_products'] = published_products

        return context