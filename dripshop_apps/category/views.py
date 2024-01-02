from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from .models import Category
from dripshop_apps.product.models import Product

class PublishedCategoryListView(ListView):
    model = Category
    template_name = 'category/category_list.html'
    context_object_name = 'categories'
    paginate_by = 2  # Adjust the number of items per page as needed

    def get_queryset(self):
        return Category.objects.get_published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Paginate published categories
        published_categories = Category.objects.get_published()
        paginator = Paginator(published_categories, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            published_categories = paginator.page(page)
        except PageNotAnInteger:
            published_categories = paginator.page(1)
        except EmptyPage:
            published_categories = paginator.page(paginator.num_pages)

        context['categories'] = published_categories

        # Paginate featured categories
        featured_categories = Category.objects.get_featured()
        paginator_featured = Paginator(featured_categories, self.paginate_by)
        page_featured = self.request.GET.get('page_featured')

        try:
            featured_categories = paginator_featured.page(page_featured)
        except PageNotAnInteger:
            featured_categories = paginator_featured.page(1)
        except EmptyPage:
            featured_categories = paginator_featured.page(paginator_featured.num_pages)

        context['featured_categories'] = featured_categories

        return context

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category/category_detail.html'
    context_object_name = 'category'
    paginate_by = 10  # Adjust the number of items per page as needed

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Featured products for the category
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

        # Published products for the category
        published_products = Product.objects.published().filter(category=self.object)
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