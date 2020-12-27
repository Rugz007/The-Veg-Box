from django.http import HttpResponse
from django.views.generic import View

from django.template.loader import get_template
from sales.models import Order, OrderItem
from sales.utils import render_to_pdf
from num2words import num2words

from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView

from rest_framework import permissions, status
from sales.serializers import AddOrderSerializer, AddOrderItemSerializer
from rest_framework.response import Response

class GenerateReceipt(View):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, id):
        order = Order.objects.get(id=id)
        items = OrderItem.objects.filter(order=order.id)
        if order.customer_name is None:
            order.customer_name = ''
        if order.customer_phone is None:
            order.customer_phone = ''
        context = {
            "receipt_id": order.id,
            "biller_name": order.biller.name,
            "customer_name": order.customer_name,
            "customer_phone": order.customer_phone,
            "mode_of_payment": order.mode_of_payment,
            "order_items": items,
            "total": str(order.total),
            "total_in_words": num2words(order.total, lang='en_IN').title() + ' Rupees Only',
            "date_time": order.created_at
        }
        pdf = render_to_pdf('pdf/receipt.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Receipt_%s.pdf" % (str(order.id))
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

class AddOrderView(APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_classes = (AddOrderSerializer)

    def post(self, request, format='json'):
        serializer = self.serializer_classes(data=self.request.data)
        if serializer.is_valid():
            order = serializer.save()
            if order:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddOrderItemsView(APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_classes = (AddOrderItemSerializer)

    def post(self, request, format='json'):
        serializer = self.serializer_classes(data=self.request.data, many=True)
        if serializer.is_valid():
            print(serializer.data)
            orderitems = serializer.save()
            if orderitems:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteOrderItemsView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, id):
        orderItemCount = OrderItem.objects.filter(order=id).count()
        if orderItemCount > 0:
            orderitems = OrderItem.objects.filter(order=id)
            if orderitems:
                orderitems.delete()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

class UpdateOrderView(RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = AddOrderSerializer
    permission_classes = (permissions.AllowAny,)