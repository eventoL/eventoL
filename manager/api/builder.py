from rest_framework import serializers, viewsets
from rest_framework.filters import DjangoFilterBackend


def basic_reduce(queryset):
    return {'total': queryset.count()}


def count_if(list, conditions):
    count = 0
    for element in list:
        try:
            if all(element[key] == value for key, value in conditions.items()):
                count += 1
        except Exception:
            pass
    return count


def count_by(list, getter, increment=None):
    return_dict = {}
    for element in list:
        try:
            field = getter(element)
            if field in return_dict:
                return_dict[field] += increment(element) if increment else 1
            else:
                return_dict[field] = increment(element) if increment else 1
        except Exception:
            pass
    return return_dict


class ViewSetBuilder():

    def __init__(self, cls, cls_form=None, reduce_func=None):
        self.cls = cls
        self.cls_form = cls_form
        self.reduce_func = reduce_func or basic_reduce

    def build(self):
        class Serializer(serializers.HyperlinkedModelSerializer):
            if self.cls_form:
                class Meta(self.cls_form.Meta):
                    pass
            else:
                class Meta(object):
                    model = self.cls

        class ViewSet(viewsets.ModelViewSet):
            queryset = self.cls.objects.all()
            serializer_class = Serializer
            filter_backends = (DjangoFilterBackend,)
            filter_fields = self.cls._meta.get_all_field_names()
            ordering_fields = '__all__'

            def list(this, request, *args, **kwargs):
                for filter_key, filter_value in request.GET.items():
                    this.queryset = self.cls.filter_by(this.queryset, filter_key, filter_value)
                return_value = super(ViewSet, this).list(request, *args, **kwargs)
                if request.GET.get('reduce', None):
                    return_value.data = self.reduce_func(this.filter_queryset(this.get_queryset()))
                return return_value

        return ViewSet
