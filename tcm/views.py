from handian_tcm import neo_graph
from .permissions import ProductListPermission
from .utils import get_info_from_node
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError, NotFound
from oauth2_provider.contrib.rest_framework import TokenHasScope

from tcm import models
from tcm.serializers import (
    TcmSerializer, LiteratureSerializer, HandianProductSerializer,
    LiteratureByProductSerializer, PrescriptionSerializer,
    XingWeiSerializer, PrescriptionUrlSerializer, TcmUrlSerializer,
    TermSerializer, TermUrlSerializer,
)


class TermView(viewsets.ModelViewSet):
    permission_classes = [TokenHasScope, ]
    required_scopes = ['basic:read']
    serializer_class = TermSerializer
    queryset = models.Term.objects.all()
    lookup_field = 'neo_id'


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

        center_node = neo_graph.nodes.match(
            'HandianProduct',
            name=instance.name
        ).first()

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
        response_result = get_info_from_node(instance, 'HandianProduct')
        if not response_result:
            raise NotFound

        return Response(response_result)


class PrescriptionView(viewsets.ModelViewSet):
    permission_classes = [TokenHasScope, ]
    required_scopes = ['basic:read']
    queryset = models.Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    lookup_field = 'neo_id'


class XingWeiView(viewsets.ModelViewSet):
    permission_classes = [TokenHasScope, ]
    required_scopes = ['basic:read']
    queryset = models.XingWei.objects.all()
    serializer_class = XingWeiSerializer
    lookup_field = 'neo_id'


class SearchView(viewsets.ViewSet):
    """
    : 搜索模块
    """
    permission_classes = [TokenHasScope, ]
    required_scopes = ['basic:read']

    def strip_str(self, s):
        _search = s.strip()
        if not _search:
            raise ParseError(detail='查询字段不可为空')

        return _search

    @action(detail=True)
    def get_literature(self, request, search, *args, **kwargs):
        """
        - 根据search关键字, 查询相关文献列表
        """
        _search = self.strip_str(search)

        search_params = _search.split(' ')
        # search_query = Q()
        # 查找文献相关的列表=>目前以title查询
        initial_query = 'n.title contains "%s"'
        cypher_where = list()

        if search_params:
            for p in search_params:
                # search_query |= Q(title__icontains=p)
                cypher_query = initial_query % p
                cypher_where.append(cypher_query)

        cypher = ' OR '.join(cypher_where)

        id_list = neo_graph.run('match (n:Literature) where {} return distinct ID(n) as id'.format(cypher)).data()

        _ids = [i.get('id') for i in id_list]
        result = models.Literature.objects.filter(neo_id__in=_ids).order_by('-neo_id')

        serializers = LiteratureByProductSerializer(result, many=True, context={'request': request})

        return Response(serializers.data)

    @action(detail=False)
    def get_about(self, request, info, search, *args, **kwargs):
        """
        - 根据关键字, 查询对应类型的列表
        - info: 查询数据的类型; eg. term
        - search: 查询关键字
        """
        _search = self.strip_str(search)
        model_type = str(info).upper()

        from .constants import STRING_TO_NEO_NAME
        neo_model_name = STRING_TO_NEO_NAME.get(model_type)

        if neo_model_name:
            node_list = neo_graph.run('match (n:{}) where n.name contains "{}" return distinct ID(n) as id, n.name as name'.format(neo_model_name, _search)).data()
        else:
            raise NotFound

        return Response(node_list)

    def same_part(self, search, model, model_type):
        _search = self.strip_str(search)

        try:
            node = neo_graph.run('match (n:{}) where n.name="{}" return ID(n) as id'.format(model_type, _search)).data()
            if len(node) == 1:
                result = model.objects.get(neo_id__in=[i.get('id') for i in node])
            else:
                raise NotFound

        except model.DoesNotExist:
            raise NotFound

        return result

    @action(detail=False)
    def get_term(self, request, search, *args, **kwargs):
        """
        - 根据search关键字, 查询医学名词二级图谱
        """
        result = self.same_part(search, models.Term, 'Term')
        response_json = get_info_from_node(result, 'Term')
        return Response(response_json)

    @action(detail=False)
    def get_prescription(self, request, search, *args, **kwargs):
        """
        - 根据search关键字, 查询中医方剂二级图谱
        """
        result = self.same_part(search, models.Prescription, 'Prescription')
        response_json = get_info_from_node(result, 'Prescription')
        return Response(response_json)

    @action(detail=False)
    def get_tcm(self, request, search, *args, **kwargs):
        """
        - 根据search关键字, 查询中药材二级图谱
        """
        result = self.same_part(search, models.TCM, 'TCM')
        response_json = get_info_from_node(result, 'TCM')
        return Response(response_json)

    def about_same_part(self, search, model, model_type, rel_node_name):
        """
        : search=>搜索的字段内容
        : model=>数据表
        : model_type=>当前的Neo4j数据类型
        : rel_node_name=>中间关系模型,借助此模型进行查询相关节点
        """
        result = self.same_part(search, model, model_type)
        rel_nodes_id_list = neo_graph.run('match (n:{})-[r1]-(m:{})-[r2]-(n2:{}) where n.name="{}" return distinct ID(n2) as id'.format(model_type, rel_node_name, model_type, result.name)).data()
        _id_list = [info.get('id') for info in rel_nodes_id_list]
        result = model.objects.filter(neo_id__in=_id_list)
        return result

    @action(detail=False)
    def about_prescription(self, request, search, *args, **kwargs):
        """
        - 查询中医方剂相关列表
        """
        result = self.about_same_part(search, models.Prescription, 'Prescription', 'TCM')
        serializer = PrescriptionUrlSerializer(result, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False)
    def about_tcm(self, request, search, *args, **kwargs):
        """
        - 查询中药材相关列表
        """
        result = self.about_same_part(search, models.TCM, 'TCM', 'Prescription')
        serializer = TcmUrlSerializer(result, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False)
    def about_term(self, request, search, *args, **kwargs):
        """
        - 查询医学名词相关列表
        """
        # TODO: 无数据, API
        result = self.about_same_part(search, models.Term, 'Term', 'Term')

        serializer = TermUrlSerializer(result, many=True, context={'request': request})
        return Response(serializer.data)
