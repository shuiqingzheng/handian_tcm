from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.apps import apps
from django.views import View

import tcm
from importdb.utils import MODEL_FUNC_NAME


class ImportDBView(View):

    def return_context(self):
        app_models = dict()
        for i, val in enumerate(apps.get_app_config('tcm').get_models()):
            app_models[i] = {
                'model_verbose_name': val._meta.verbose_name,
                'model_name': val.__name__,
            }

        context = {
            'site_header': '中医知识系统',
            'app_models': app_models
        }
        return context

    # 网页渲染=>选择同步的数据表
    def get(self, request, *args, **kwargs):
        context = self.return_context()
        return render(request, template_name='admin/importdb.html', context=context)

    # 数据同步=>同步已选数据表
    def post(self, request, *args, **kwargs):
        selected_models = request.POST.getlist('selected_model')
        context = self.return_context()

        if not selected_models:
            context.update({'no_msg': '未选择需同步数据表'})
            return render(request, template_name='admin/importdb.html', context=context)

        try:
            for model in selected_models:
                if model in MODEL_FUNC_NAME.keys():
                    MODEL_FUNC_NAME.get(model)()

        except Exception as e:
            context.update({'error_msg': '{}'.format(e)})
            return render(request, template_name='admin/importdb.html', context=context)

        context.update({'ok_msg': '完成同步'})
        return render(request, template_name='admin/importdb.html', context=context)
