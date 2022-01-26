from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category, Review
from .forms import ProductForm, ReviewForm
from profiles.models import UserProfile

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)
    
    # reviews for the product
    product_review = product.review.all()

    if product_review.exists():
        any_reviews = True
    else:
        any_reviews = False

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        user_reviewed = product_review.filter(user_profile=profile).exists()
    else:
        user_reviewed = False


    context = {
        'product': product,
        'product_review': product_review,
        'any_reviews': any_reviews,
        'user_reviewed': user_reviewed,
    }

    return render(request, 'products/product_detail.html', context)

@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)

@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)

@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
        
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))

        

def reviews(request):
    """ A view that renders the views contents page """

    reviews = Review.objects.all()

    context = {
        'reviews': reviews,
    }

    return render(request, 'products/reviews.html', context)



def review_detail(request, review_id):
    """ A view that shows individual reviews  """

    Review = get_object_or_404(Review, pk=review_id)

    if request.method == 'GET':
        profile = UserProfile.objects.get(user=request.user)
        form = ReviewForm(request.GET)
        form_data = {
            'review': request.GET['review'],
        }
        productreview_form = ReviewForm(form_data)
        # check if form is valid
        if productreview_form.is_valid():
            context = {
                'reviews': reviews,
                    }
    return render(request, 'review_detail.html', context)
    
      
def add_review(request, product_id):
    """ Add a review to the product """

    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        profile = UserProfile.objects.get(user=request.user)
        form = ReviewForm(request.POST, request)

        form_data = {
            'review': request.POST['review'],
        }

        form = ReviewForm(form_data)
        # check if form is valid
        if  form.is_valid():
            productreview = form.save(commit=False)
            productreview.product = product
            productreview.user_profile = profile
            productreview.save()
            messages.success(request, 'Successfully added product review!')
            return redirect(reverse('product_detail', args=[product.id]))
        # form is not valid
        else:
            messages.error(request, 'Failed to add product review. ' +
                           'Please ensure the form is valid.')
    else:
        # check if the user has already made a review
        # for this product previously
        # if so redirect back to product page with an error message
        profile = UserProfile.objects.get(user=request.user)
        product_reviews = product.reviews.all()
        if product_reviews.filter(user_profile=profile).exists():
            messages.error(request, "You have already reviewed " +
                           "this product. You can update your " +
                           "review from below or your profile!")
            return redirect(reverse('review_detail', args=[product.id]))
        else:
            form = ReviewForm()

    template = 'products/add_review.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)




