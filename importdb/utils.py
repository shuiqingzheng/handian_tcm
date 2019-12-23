from django.db import connection
from handian_tcm import neo_graph
from py2neo import NodeMatcher
from tcm import models
import math
import gevent


READ_LIMIT = 300
matcher = NodeMatcher(neo_graph)


def same_code_literature(literature, i):
    literature.name = i['name']
    literature.summary = i['summary']
    literature.image = i['image']
    literature.download_name = i['download_name']
    literature.issue = i['issue']
    literature.author = i['author']
    literature.title = i['title']
    literature.name = i['name']
    literature.manager_id = i['manager_id']
    literature.publish_time = i['publish_time']
    literature.product_id = i['product_id']
    literature.download_url = i['download_url']
    literature.state = i['state']
    literature.read_count = i['read_count']
    literature.operate_time = i['operate_time']


def inner_sys(nodes):
    model_list = []
    for i in set(nodes):
        literature = models.Literature()
        literature.neo_id = i.identity
        same_code_literature(literature, i)
        model_list.append(literature)
    models.Literature.objects.bulk_create(model_list)


def sys_literatures():
    with connection.cursor() as cursor:
        a = cursor.execute('delete from tcm_literature;')
        print('删除的条数:{}'.format(a))

    all_jobs = []

    len_nodes = matcher.match('Literature').__len__()
    for page in range(math.ceil(len_nodes / READ_LIMIT)):
        nodes = matcher.match('Literature').skip(READ_LIMIT * page).limit(READ_LIMIT)
        all_jobs.append(gevent.spawn(inner_sys, nodes))

    gevent.joinall(all_jobs)


def same_code_tcm(tcm, i):
    tcm.bei = i['bei']
    tcm.bie = i['bie']
    tcm.cang = i['cang']
    tcm.chu = i['chu']
    tcm.du = i['du']
    tcm.name = i['name']
    tcm.fu = i['fu']
    tcm.ge = i['ge']
    tcm.gong = i['gong']
    tcm.gui = i['gui']
    tcm.han = i['han']
    tcm.hua = i['hua']
    tcm.jian = i['jian']
    tcm.jing = i['jing']
    tcm.lai = i['lai']
    tcm.lin = i['lin']
    tcm.pao = i['pao']
    tcm.pic = i['pic']
    tcm.pin = i['pin']
    tcm.sheng = i['sheng']
    tcm.wen = i['wen']
    tcm.xing = i['xing']
    tcm.yao = i['yao']
    tcm.yong = i['yong']
    tcm.yuan = i['yuan']
    tcm.zai = i['zai']
    tcm.zf = i['zf']
    tcm.zhai = i['zhai']
    tcm.zhuang = i['zhaung']
    tcm.zhi = i['zhi']
    tcm.zhu = i['zhu']


def inner_sys_tcm(nodes):
    model_list = []
    for i in nodes:
        tcm = models.TCM()
        tcm.neo_id = i.identity
        same_code_tcm(tcm, i)
        model_list.append(tcm)

    models.TCM.objects.bulk_create(model_list)


def sys_tcm():
    with connection.cursor() as cursor:
        a = cursor.execute('delete from tcm_tcm;')
        print('删除的TCM条数:{}'.format(a))

    len_nodes = matcher.match('TCM').__len__()
    all_jobs = []
    for page in range(math.ceil(len_nodes / READ_LIMIT)):
        nodes = matcher.match('TCM').skip(READ_LIMIT * page).limit(READ_LIMIT)
        all_jobs.append(gevent.spawn(inner_sys_tcm, nodes))

    gevent.joinall(all_jobs)


def same_code_product(instance, i):
    instance.name = i['name']


def same_code_term(instance, i):
    instance.name = i['name']
    instance.english = i['english']
    instance.content = i['content']


def inner_sys_term(nodes):
    model_list = []
    for i in nodes:
        term = models.Term()
        term.neo_id = i.identity
        same_code_term(term, i)
        model_list.append(term)

    models.Term.objects.bulk_create(model_list)


def sys_term():
    with connection.cursor() as cursor:
        a = cursor.execute('delete from tcm_term;')
        print('删除的Term条数:{}'.format(a))

    len_nodes = matcher.match('Term').__len__()
    all_jobs = []
    for page in range(math.ceil(len_nodes / READ_LIMIT)):
        nodes = matcher.match('Term').skip(READ_LIMIT * page).limit(READ_LIMIT)
        all_jobs.append(gevent.spawn(inner_sys_term, nodes))

    gevent.joinall(all_jobs)


def inner_sys_product(nodes):
    model_list = []
    for i in nodes:
        product = models.HandianProduct()
        product.neo_id = i.identity
        same_code_product(product, i)
        model_list.append(product)

    models.HandianProduct.objects.bulk_create(model_list)


def sys_product():
    with connection.cursor() as cursor:
        a = cursor.execute('delete from tcm_handianproduct;')
        print('删除的HandianProduct条数:{}'.format(a))

    len_nodes = matcher.match('HandianProduct').__len__()

    all_jobs = []
    for page in range(math.ceil(len_nodes / READ_LIMIT)):
        nodes = matcher.match('HandianProduct').skip(READ_LIMIT * page).limit(READ_LIMIT)

        all_jobs.append(gevent.spawn(inner_sys_product, nodes))

    gevent.joinall(all_jobs)


same_code_prescription = same_code_product


def inner_sys_prescription(nodes):
    model_list = []
    for i in nodes:
        prescription = models.Prescription()
        prescription.neo_id = i.identity
        same_code_prescription(prescription, i)
        model_list.append(prescription)

    models.Prescription.objects.bulk_create(model_list)


def sys_prescription():
    with connection.cursor() as cursor:
        a = cursor.execute('delete from tcm_prescription;')
        print('删除的Prescription条数:{}'.format(a))

    len_nodes = matcher.match('Prescription').__len__()
    all_jobs = []

    for page in range(math.ceil(len_nodes / READ_LIMIT)):
        nodes = matcher.match('Prescription').skip(READ_LIMIT * page).limit(READ_LIMIT)
        all_jobs.append(gevent.spawn(inner_sys_prescription, nodes))

    gevent.joinall(all_jobs)


same_code_xingwei = same_code_product


def inner_sys_xingwei(nodes):
    model_list = []
    for i in nodes:
        xing = models.XingWei()
        xing.neo_id = i.identity
        same_code_xingwei(xing, i)
        model_list.append(xing)

    models.XingWei.objects.bulk_create(model_list)


def sys_xingwei():
    with connection.cursor() as cursor:
        a = cursor.execute('delete from tcm_xingwei;')
        print('删除的Xingwei条数:{}'.format(a))

    len_nodes = matcher.match('Xingwei').__len__()
    all_jobs = []

    for page in range(math.ceil(len_nodes / READ_LIMIT)):
        nodes = matcher.match('Xingwei').skip(READ_LIMIT * page).limit(READ_LIMIT)
        all_jobs.append(gevent.spawn(inner_sys_xingwei, nodes))

    gevent.joinall(all_jobs)


MODEL_FUNC_NAME = {
    'HandianProduct': sys_product,
    'Literature': sys_literatures,
    'TCM': sys_tcm,
    'Prescription': sys_prescription,
    'XingWei': sys_xingwei,
    'Term': sys_term,
}
