from rest_framework import serializers, viewsets, filters


class ViewSetBuilder():

    def __init__(self, cls, cls_form=None, cls_serializer=None):
        self.cls = cls
        self.cls_form = cls_form
        self.cls_serializer = cls_serializer
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

        class ViewSet(viewsets.ModelViewSet):
            queryset = self.cls.objects.all()
            serializer_class = self.cls_serializer
            filter_backends = (filters.DjangoFilterBackend,)
            filter_fields = self.fields
            ordering_fields = '__all__'

        return ViewSet
