from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator


class SuperUserPermission:
    @method_decorator(
        user_passes_test(lambda u: u.is_staff and u.is_superuser)
    )
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class UserAuthPermission:
    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
