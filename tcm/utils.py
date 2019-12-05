from handian_tcm import neo_graph

from py2neo import NodeMatcher

from tcm import models

matcher = NodeMatcher(neo_graph)


def same_code(literature, i):
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


def sys_literatures():
    nodes = matcher.match('Literature')

    for i in list(nodes):
        # 判断是否已经存在
        try:
            obj_literature = models.Literature.objects.get(neo_id=i.identity)
        except models.Literature.DoesNotExist:
            literature = models.Literature()
            literature.neo_id = i.identity
            same_code(literature, i)
            literature.save()
        else:
            same_code(obj_literature, i)
            obj_literature.save()


def same_code_tcm(tcm, i):
    tcm.bei = i['bei']
    tcm.bie = i['bie']
    tcm.cang = i['cang']
    tcm.chu = i['chu']
    tcm.du = i['du']
    tcm.fieldname = i['fieldname']
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


def sys_tcm():
    nodes = matcher.match('TCM')

    for i in nodes:
        # 判断是否已经存在
        try:
            obj_tcm = models.TCM.objects.get(neo_id=i.identity)
        except models.TCM.DoesNotExist:
            tcm = models.TCM()
            tcm.neo_id = i.identity
            same_code_tcm(tcm, i)
            tcm.save()
        else:
            same_code_tcm(obj_tcm, i)
            obj_tcm.save()