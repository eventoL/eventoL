from reduces import basic_reduce
from rest_framework.response import Response
from django.contrib.gis.admin import ModelAdmin
from rest_framework import serializers, viewsets, filters


class ViewSetBuilder(object):

    def __init__(self, cls, cls_form=None, cls_serializer=None, reduce_func=None, cls_admin=None):
        self.cls = cls
        self.cls_admin = cls_admin or ModelAdmin
        self.cls_form = cls_form
        self.cls_serializer = cls_serializer
        self.reduce_func = reduce_func or basic_reduce
        self.fields = cls.for_filter() if "for_filter" in dir(cls) else cls._meta.get_all_field_names()

    def set_fields(self, fields):
        self.fields = fields

    def build(self):
        if not self.cls_serializer:
            class Serializer(serializers.HyperlinkedModelSerializer):
                if self.cls_form:
                    class Meta(self.cls_form.Meta):
                        pass
                else:
                    class Meta(object):
                        model = self.cls
            self.cls_serializer = Serializer

        class ViewSet(viewsets.mixins.ListModelMixin, viewsets.mixins.RetrieveModelMixin, viewsets.GenericViewSet):
            queryset = self.cls.objects.all()
            serializer_class = self.cls_serializer
            filter_backends = (filters.DjangoFilterBackend,)
            filter_fields = self.fields
            ordering_fields = '__all__'
            cls_admin = self.cls_admin
            cls = self.cls

            def retrieve(this, request, *args, **kwargs):
                return_value = super(ViewSet, this).retrieve(request, *args, **kwargs)
                model_list = this.list(request, *args, **kwargs).data
                instance = [inst for inst in model_list if inst['url'].split('/')[-2] == kwargs.get('pk')]
                return_value.data = instance[0] if len(instance) > 0 else {}
                return return_value

            def list(this, request, *args, **kwargs):
                if not request.GET.get('reduce', None):
                    this.queryset = this.cls_admin(this.cls, this.ordering_fields).get_queryset(request)
                if 'filter_by' in dir(self.cls):
                    for filter_key, filter_value in request.GET.items():
                        this.queryset = self.cls.filter_by(this.queryset, filter_key, filter_value)
                return_value = super(ViewSet, this).list(request, *args, **kwargs)
                if request.GET.get('reduce', None):
                    return_value.data = self.reduce_func(this.filter_queryset(this.get_queryset()))
                return return_value

        return ViewSet
