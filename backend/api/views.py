from django.forms.models import model_to_dict # this is a serializer basically
from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.models import Product
from products.serializers import ProductSerializer

@api_view(["POST"])
def api_home(request, *args, **kwargs):
    """
    DRF API View
    """
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True): # to let the client know the error
        # instance = serializer.save()
        # instance = form.save()
        print(serializer.data)
        return Response(serializer.data)
        #serializer data is not actually creating an instance, in other words nothing was ever save in the database
        # which means that we don't have a real way to access to get_discount instance method
        # so serializer.save() is the only way to create an instance from productSerializer
    return Response(serializer.data)
