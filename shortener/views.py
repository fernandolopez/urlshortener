from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.decorators import action
from django.http import Http404
from django.shortcuts import redirect
from .models import Url
from .services import create_url


class UrlSerializer(ModelSerializer):
    class Meta:
        model = Url
        fields = "__all__"

    shortened_url = SerializerMethodField()

    def get_shortened_url(self, obj):
        base_url = self.context["request"].build_absolute_uri("/")
        return f"{base_url}g/{obj.slug}"


class HandleUrls(ModelViewSet):
    queryset = Url.objects.all()
    serializer_class = UrlSerializer

    def create(self, request):
        url = request.data["url"]
        try:
            url_obj = create_url(url)
        except Exception as e:
            raise Response({"error": str(e)}, status=500)
        return Response(self.get_serializer(url_obj, many=False).data)

    @action(detail=False, methods=["GET"], url_path="top100")
    def top_100(self, request):
        top_100 = Url.objects.order_by("-visit_count")[:100]
        return Response(self.get_serializer(top_100, many=True).data)


def slug_redirect_handler(request, slug):
    try:
        url = Url.objects.filter(slug=slug).get()
    except Url.DoesNotExist:
        raise Http404()

    url.visit_count += 1
    url.save()

    return redirect(url.url)
