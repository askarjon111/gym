from django.contrib.auth.decorators import user_passes_test


def is_gym_manager(user):
    return user.is_authenticated and user.roles.filter(title='manager').exists()


def gym_manager_required(view_func=None, login_url=None):
    actual_decorator = user_passes_test(
        lambda u: is_gym_manager(u),
        login_url=login_url,
    )

    if view_func:
        return actual_decorator(view_func)
    return actual_decorator
