from oauth2_provider.contrib.rest_framework import TokenHasScope


class ProductListPermission(TokenHasScope):
    """
    : 首页汉典产品列表均可查看
    """

    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        else:
            return super().has_permission(request, view)
