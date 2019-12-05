from rest_framework import filters

from tcm import models

from handian_tcm import neo_graph


class LiteratureIDFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        handian_product_id = request.GET.get('product_id')

        response_literatures = list()

        # 产品 => 相关文献
        if handian_product_id is not None:
            product = models.HandianProduct.objects.get(neo_id=handian_product_id)

            neo_product = neo_graph.nodes.match('HandianProduct', name=product.name).first()

            rel_literatures = neo_graph.match((neo_product,), r_type='REFERENCE')

            for rel in rel_literatures:
                response_literatures.append(rel.end_node)

        else:
            response_literatures = queryset

        return response_literatures
