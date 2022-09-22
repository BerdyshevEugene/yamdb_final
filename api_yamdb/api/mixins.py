from rest_framework import mixins, viewsets


class CDLMixinViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pass
