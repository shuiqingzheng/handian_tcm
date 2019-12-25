from handian_tcm import neo_graph

from django.conf import settings


def get_info_from_node(instance, model_type, page=None):
    """
    :Neo4j中获取两级节点信息
    :调用示例=> get_info_from_node(term_instance, 'Term', page=1)
    :return dict/None
    """
    a = neo_graph.nodes.match(model_type, name=instance.name).first()

    if not a:
        return None

    START_ID = a.identity

    return_json = {
        'data': [],
        'links': []
    }

    return_json['data'].append({
        'name': a['name'],
        'id': START_ID,
        'label': list(a.labels)[0]
    })

    if page:
        data = neo_graph.run('MATCH (n:{})-[r]-(m) where n.name="{}" '
                             'RETURN m.name as name, type(r) as tp, id(m) as id, labels(m) as labels '
                             'order by id skip {} limit {}'.format(
                                 model_type, instance.name,
                                 (page - 1) * settings.NEO_PAGE_SIZE, settings.NEO_PAGE_SIZE
                             )).data()
    else:
        data = neo_graph.run('MATCH (n:{})-[r]-(m) where n.name="{}" '
                             'RETURN m.name as name, type(r) as tp, id(m) as id, labels(m) as labels '
                             'order by id'.format(model_type, instance.name)).data()

    for val in data:
        return_json['data'].append({
            'name': val.get('name'),
            'id': val.get('id'),
            'label': list(val.get('labels'))[0]
        })
        return_json['links'].append({
            'start': START_ID,
            'end': val.get('id'),
            'rel': val.get('tp')
        })

    # all relationships => all first nodes => all second nodes
    # for tp in relationships:
    #     rel_name = tp.get('tp')
    #     demo = neo_graph.match((a,), r_type=rel_name)
    #     for d in demo:
    #         # print(type(d))
    #         e_node = d.end_node
    #         s_node = d.start_node
    #         # print(s_node)
    #         END_ID = e_node.identity

        # 第二级节点
        # second_nodes = neo_graph.match((e_node, ))

        # for s_d in second_nodes:
        #     second_name = s_d.end_node['name']
        #     SECOND_NODE_ID = s_d.identity
        #     second_rel_name = type(s_d).__name__
        #     return_json['data'].append({
        #         'name': second_name,
        #         'id': SECOND_NODE_ID
        #     })
        #     return_json['links'].append({
        #         'start': END_ID,
        #         'end': SECOND_NODE_ID,
        #         'rel': second_rel_name
        #     })

        # return_json['links'].append({
        #     'start': START_ID,
        #     'end': END_ID,
        #     'rel': rel_name
        # })
        # return_json['data'].append({
        #     'name': e_node['name'],
        #     'id': END_ID
        # })

    return return_json
