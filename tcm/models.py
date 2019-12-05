from django.db import models


class TCM(models.Model):
    neo_id = models.IntegerField(verbose_name='TCM_ID', help_text='TCM_ID', blank=True, null=True, unique=True)

    bei = models.TextField(help_text='备注', verbose_name='备注', blank=True, null=True)
    bie = models.TextField(help_text='别名', verbose_name='别名', blank=True, null=True)
    cang = models.TextField(help_text='贮藏', verbose_name='贮藏', blank=True, null=True)
    chu = models.TextField(help_text='出处', verbose_name='出处', blank=True, null=True)
    du = models.TextField(help_text='毒性', verbose_name='毒性', blank=True, null=True)
    fieldname = models.TextField(help_text='中药名', verbose_name='中药名', blank=True, null=True)
    fu = models.TextField(help_text='复方', verbose_name='复方', blank=True, null=True)
    ge = models.TextField(help_text='各家论述', verbose_name='各家论述', blank=True, null=True)
    gong = models.TextField(help_text='功能主治', verbose_name='功能主治', blank=True, null=True)
    gui = models.TextField(help_text='规格', verbose_name='规格', blank=True, null=True)
    han = models.TextField(help_text='含量测定', verbose_name='含量测定', blank=True, null=True)
    hua = models.TextField(help_text='化学成分', verbose_name='化学成分', blank=True, null=True)
    jian = models.TextField(help_text='鉴别', verbose_name='鉴别', blank=True, null=True)
    jing = models.TextField(help_text='归经', verbose_name='归经', blank=True, null=True)
    lai = models.TextField(help_text='来源', verbose_name='来源', blank=True, null=True)
    lin = models.TextField(help_text='临床鉴定', verbose_name='临床鉴定', blank=True, null=True)
    pao = models.TextField(help_text='炮制', verbose_name='炮制', blank=True, null=True)
    pic = models.TextField(help_text='图片', verbose_name='图片', blank=True, null=True)
    pin = models.TextField(help_text='拼音', verbose_name='拼音', blank=True, null=True)
    sheng = models.TextField(help_text='生境分部', verbose_name='生境分部', blank=True, null=True)
    wen = models.TextField(help_text='英文名', verbose_name='英文名', blank=True, null=True)
    xing = models.TextField(help_text='性味', verbose_name='性味', blank=True, null=True)
    yao = models.TextField(help_text='药理作用', verbose_name='药理作用', blank=True, null=True)
    yong = models.TextField(help_text='用法用量', verbose_name='用法用量', blank=True, null=True)
    yuan = models.TextField(help_text='原形态', verbose_name='原形态', blank=True, null=True)
    zai = models.TextField(help_text='栽培', verbose_name='栽培', blank=True, null=True)
    zf = models.TextField(help_text='制法', verbose_name='制法', blank=True, null=True)
    zhai = models.TextField(help_text='摘录', verbose_name='摘录', blank=True, null=True)
    zhuang = models.TextField(help_text='性状', verbose_name='性状', blank=True, null=True)
    zhi = models.TextField(help_text='制剂', verbose_name='制剂', blank=True, null=True)
    zhu = models.TextField(help_text='注意', verbose_name='注意', blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.pk)

    class Meta:
        verbose_name = '中药名称'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class Literature(models.Model):
    neo_id = models.IntegerField(verbose_name='TCM_ID', help_text='TCM_ID', blank=True, null=True, unique=True)

    literature_id = models.IntegerField(help_text='ID', verbose_name='ID', blank=True, null=True)

    summary = models.TextField(help_text='摘要', verbose_name='摘要', blank=True, null=True)

    image = models.CharField(help_text='图片', verbose_name='图片', blank=True, null=True, max_length=255)

    download_name = models.TextField(help_text='下载标题', verbose_name='下载标题', blank=True, null=True)

    issue = models.TextField(help_text='主题', verbose_name='主题', blank=True, null=True)

    author = models.CharField(help_text='作者', verbose_name='作者', blank=True, null=True, max_length=50)

    title = models.CharField(help_text='文献题目', verbose_name='文献题目', blank=True, null=True, max_length=200)

    name = models.CharField(help_text='文献题目', verbose_name='文献题目', blank=True, null=True, max_length=200)

    manager_id = models.IntegerField(help_text='管理员ID', verbose_name='管理员ID', blank=True, null=True)

    publish_time = models.CharField(help_text='出版时间', verbose_name='出版时间', blank=True, null=True, max_length=100)

    product_id = models.IntegerField(help_text='产品序列号', verbose_name='产品序列号', blank=True, null=True)

    download_url = models.CharField(help_text='下载链接', verbose_name='下载链接', blank=True, null=True, max_length=255)

    state = models.CharField(help_text='状态', verbose_name='状态', blank=True, null=True, max_length=2)

    operate_time = models.CharField(help_text='操作时间', verbose_name='操作时间', blank=True, null=True, max_length=100)

    read_count = models.IntegerField(help_text='查阅此书', verbose_name='查阅此书', blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.pk)

    class Meta:
        verbose_name = '文献'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class HandianProduct(models.Model):
    neo_id = models.IntegerField(verbose_name='TCM_ID', help_text='TCM_ID', blank=True, null=True, unique=True)

    name = models.CharField(help_text='名称', verbose_name='名称', blank=True, null=True, max_length=50)

    def __str__(self):
        return '{}'.format(self.pk)

    class Meta:
        verbose_name = '汉典产品'
        verbose_name_plural = verbose_name
        ordering = ['-id']
