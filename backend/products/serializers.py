from rest_framework import serializers
from rest_framework.reverse import reverse

from api.serializers import UserPublicSerializer
from .models import Product
from .validators import validate_title_no_hello, unique_product_title


class ProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail', lookup_field='pk', read_only=True)
    title = serializers.CharField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source="user", read_only=True)
    # related_products = ProductInlineSerializer(
    #     source='user.product_set.all', read_only=True, many=True)
    # user_data = serializers.SerializerMethodField(read_only=True)
    discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail', lookup_field='pk')
    # email = serializers.EmailField(write_only=True)
    title = serializers.CharField(
        validators=[unique_product_title, validate_title_no_hello])

    class Meta:
        model = Product
        fields = [
            'owner',  # user_id
            'url',
            'edit_url',
            # 'email',
            'pk',
            'title',
            'content',
            'price',
            'sale_price',
            # 'get_discount',
            'discount',
            # 'user_data',
            # 'related_products'
        ]

    # def get_user_data(self, obj):
    #     return {
    #         "username": obj.user.username
    #     }

    # def validate_title(self, value):
    #     qs = Product.objects.filter(title__iexact=value)
    #     if qs.exists():
    #         raise serializers.ValidationError(
    #             f"{value} is already a product name.")
    #     return value

    def create(self, validated_data):
        # email = validated_data.pop('email')
        obj = super().create(validated_data)
        # print(email, obj)
        return obj

    def update(self, instance, validated_data):
        # ensure that we are removing the email because it doesn't belongs to the model
        # email = validated_data.pop('email')
        return super().update(instance, validated_data)

    def get_edit_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("product-edit", kwargs={"pk": obj.pk}, request=request)

    def get_discount(self, obj):
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, Product):
            return None
        return obj.get_discount()


"""As we can actually modify the data that we are throwing back in the serializers
we can create more than one serializer per model and adjust each one to our needs"""
