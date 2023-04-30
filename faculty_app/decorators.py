from django.contrib.auth.decorators import user_passes_test

def admin_required(view_func):
    decorated_view_func = user_passes_test(
        lambda user: user.is_authenticated and user.is_staff,
        login_url='admin:login',
        redirect_field_name=None
    )(view_func)
    return decorated_view_func

def user_required(view_func):
    decorated_view_func = user_passes_test(
        lambda user: user.is_authenticated and not user.is_staff,
        login_url='login',
        redirect_field_name=None
    )(view_func)
    return decorated_view_func
