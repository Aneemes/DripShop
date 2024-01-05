from dripshop_apps.wishlist.models import Wishlist

def user_wishlist(request):
    wishlist = None
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).first()
    return {'user_wishlist': wishlist}