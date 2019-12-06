from handian_tcm import neo_graph
from .permissions import ProductListPermission

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from oauth2_provider.contrib.rest_framework import TokenHasScope

from tcm import models
from tcm.serializers import (
    TcmSerializer, LiteratureSerializer, HandianProductSerializer,
    LiteratureByProductSerializer,
)

# from tcm.filters import LiteratureIDFilterBackend

# neo4j 导入mysql数据库
# from tcm.utils import sys_tcm, sys_literatures


class TcmView(viewsets.ModelViewSet):
    permission_classes = [TokenHasScope, ]
    required_scopes = ['basic:read']
    serializer_class = TcmSerializer
    queryset = models.TCM.objects.all()
    lookup_field = 'neo_id'


class LiteratureView(viewsets.ModelViewSet):
    permission_classes = [TokenHasScope, ]
    required_scopes = ['basic:read']
    serializer_class = LiteratureSerializer
    queryset = models.Literature.objects.all()
    lookup_field = 'neo_id'


class HandianProductView(viewsets.ModelViewSet):
    permission_classes = [ProductListPermission]
    required_scopes = ['basic:read']
    queryset = models.HandianProduct.objects.all()
    lookup_field = 'neo_id'

    def get_serializer_class(self):
        if self.action == 'literatures':
            return LiteratureByProductSerializer

        return HandianProductSerializer

    @action(detail=False)
    def retrieve_relationship(self, request, neo_id=None, relationship=None):
        # 节点关系(始--关系--末)
        response_links = list()
        # 节点信息
        response_node = list()

        relationship_upper = relationship.upper()

        instance = self.get_object()

        center_node = neo_graph.nodes.match('HandianProduct', name=instance.name).first()

        if not center_node:
            return Response({
                'links': None,
                'data': None,
            })

        START_ID = center_node.identity

        response_node.append({
            'name': center_node['name'],
            'id': START_ID,
        })

        demo = neo_graph.match((center_node,), r_type=relationship_upper)

        for d in demo:
            e_node = d.end_node
            END_ID = e_node.identity
            response_links.append({
                'start': START_ID,
                'end': END_ID,
                'rel': relationship_upper
            })
            response_node.append({
                'name': e_node['name'],
                'id': END_ID
            })

        return Response({
            'links': response_links,
            'data': response_node,
        })

    @action(detail=False)
    def relationships(self, request, neo_id=None):
        product = self.get_object()

        response_rels = list()

        all_rels = neo_graph.run('match (p:HandianProduct)-[r]-(n) where p.name="{}" return distinct type(r) as tp'.format(product.name))

        for rel in all_rels:
            response_rels.append(rel.get('tp'))

        return Response(response_rels)

    @action(detail=False)
    def literatures(self, request, neo_id=None):
        response_literatures_id = list()
        response_queryset = list()
        product = self.get_object()

        # neo4j
        neo_product = neo_graph.nodes.match('HandianProduct', name=product.name).first()
        rel_literatures = neo_graph.match((neo_product,), r_type='REFERENCE')
        for rel_node in rel_literatures:
            response_literatures_id.append(rel_node.end_node.identity)

        # mysql
        for l_id in response_literatures_id:
            try:
                literature_instance = models.Literature.objects.get(neo_id=l_id)
            except models.Literature.DoesNotExist:
                raise ValueError('数据不存在')
            else:
                response_queryset.append(literature_instance)
        # 未分页
        serializer = LiteratureByProductSerializer(response_queryset, many=True, context={'request': request})
        return Response(serializer.data)

    # override retrieve to response relationship
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        relationships = neo_graph.run('match (p:HandianProduct)-[r]->(n) where p.name="{}" return distinct type(r) as tp'.format(instance.name)).data()

        # 节点关系(始--关系--末)
        response_links = list()
        # 节点信息
        response_node = list()

        a = neo_graph.nodes.match('HandianProduct', name=instance.name).first()

        if not a:
            return Response({
                'links': None,
                'data': None,
            })

        START_ID = a.identity

        response_node.append({
            'name': a['name'],
            'id': START_ID,
        })

        # all relationships => all first nodes => all second nodes
        for tp in relationships:
            rel_name = tp.get('tp')
            demo = neo_graph.match((a,), r_type=rel_name)

            for d in demo:
                e_node = d.end_node
                END_ID = e_node.identity

                # 第二级节点
                second_nodes = neo_graph.match((e_node, ))

                for s_d in second_nodes:
                    second_name = s_d.end_node['name']
                    SECOND_NODE_ID = s_d.identity
                    second_rel_name = type(s_d).__name__
                    response_node.append({
                        'name': second_name,
                        'id': SECOND_NODE_ID
                    })
                    response_links.append({
                        'start': END_ID,
                        'end': SECOND_NODE_ID,
                        'rel': second_rel_name
                    })

                response_links.append({
                    'start': START_ID,
                    'end': END_ID,
                    'rel': rel_name
                })
                response_node.append({
                    'name': e_node['name'],
                    'id': END_ID
                })

        return Response({
            'links': response_links,
            'data': response_node,
        })
