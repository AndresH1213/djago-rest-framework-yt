from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from django.http import http_404
from django.shortcuts import get_object_or_404

from api.mixin import StaffEditorPermissionMixin, UserQuerySetMixin

from .models import Product
from .serializers import ProductSerializer


class ProductListCreateAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.ListCreateAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # we don't need declare this because in settings we've declared DEFAULT_AUTHENTICATION_CLASSES
    # authentication_classes = [
    #   authentication.SessionAuthentication,
    #   TokenAuthentication
    # ]
    # we don't need this because we've define our mixin
    # permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]

    def perform_create(self, serializer):
        # print(serializer.validated_data)
        # its better to remove it in the serializer model
        # email = serializer.validated_data.pop("email")
        # print(email)
        serializer.save(user=self.request.user)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(content=content)
        # send a Django signal

    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset(*args, **kwargs)
    #     request = self.request
    #     user = request.user
    #     if not user.is_authenticated:
    #         return Product.objects.none()
    #     return qs.filter(user=request.user)


product_list_create_view = ProductListCreateAPIView.as_view()


class ProductDetailAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.RetrieveAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'pk'


product_detail_view = ProductDetailAPIView.as_view()


class ProductUpdateAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.UpdateAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [permissions.DjangoModelPermissions]
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title


product_update_view = ProductUpdateAPIView.as_view()


class ProductDestroyAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.DestroyAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        # isntance
        super().perform_destroy(instance)


product_delete_view = ProductDestroyAPIView.as_view()

# class ProductListAPIView(generics.RetrieveAPIView):
#   """
#     Not gonna use this method, because we can user ListCreate
#   """

#   queryset = Product.objects.all()
#   serializer_class = ProductSerializer
#   # lookup_field = 'pk'

# product_list_view = ProductListAPIView.as_view()


class ProductMixinView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        print(args, kwargs)
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, args, kwargs)

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = "this is a single view doing cool stuff"
        serializer.save(content=content)


product_mixin_view = ProductMixinView.as_view()

# def post(self, request, *args, **kwargs):
#   return

# @api_view(['GET', 'POST'])
# def product_alt_view(request, pk=None, *args, **kwargs):
#   method = request.method

#   if method == "GET":
#     if pk is not None:
#       #detail view
#       # queryset = Product.objects.filter(pk=pk)
#       obj = get_object_or_404(Product, pk=pk)
#       data = ProductSerializer(obj, many=False).data

#       return Response(data)

#     queryset = Product.objects.all()
#     data = ProductSerializer(queryset, many=True).data
#     return Response(data)
#     # url args??
#     # get request => dtail view
#     # list view
#   if method == "POST":
#     # create an item
#     serializer = ProductSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True): # to let the client know the error
#       title = serializer.validated_data.get('title')
#       content = serializer.validated_data.get('content') or None
#       if content is None:
#         content = title
#       serializer.save(content=content)
#       print(serializer.data)
#       return Response(serializer.data)
#     return Response({"invalid": "not good data"}, status=400)
