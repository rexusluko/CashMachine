import hashlib
from django.template.loader import render_to_string
import pdfkit
import os
import qrcode
from django.urls import reverse
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseNotFound, FileResponse
from rest_framework import viewsets, status
from rest_framework.views import APIView

from cash_machine.models import Item
from cash_machine.sirealizers import ItemSerializer, CashMachineSerializer
from myshop.settings import WKHTMLTOPDF_CMD, MEDIA_DIR

config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class CashMachineAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CashMachineSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        item_ids = serializer.validated_data['items']
        unique_items = {}
        bad_ids = set()
        total_amount = 0

        for item_id in item_ids:
            if item_id in unique_items:
                unique_items[item_id][1] += unique_items[item_id][0].price
                unique_items[item_id][2] += 1
                total_amount += unique_items[item_id][0].price
            elif item_id not in bad_ids:
                item = Item.objects.filter(id=item_id).first()
                if item:
                    unique_items[item_id] = [item, item.price, 1]
                    total_amount += item.price
                else:
                    bad_ids.add(item_id)

        if bad_ids:
            return Response({"error": f"Items with the following IDs do not exist: {', '.join(map(str, bad_ids))}"},
                            status=status.HTTP_400_BAD_REQUEST)

        timestamp = timezone.now().strftime("%d.%m.%Y %H:%M")
        html_content = render_to_string('pdf_template.html', {
            'items': unique_items.values(),
            'total_amount': total_amount,
            'creation_time': timestamp
        })
        hash_code = hashlib.sha256(timestamp.encode('utf-8')).hexdigest()

        pdf_file_path = f'{MEDIA_DIR}/{hash_code}.pdf'
        pdfkit.from_string(html_content, output_path=pdf_file_path, configuration=config)

        media_url = reverse('media', kwargs={'filename': f'{hash_code}.pdf'})

        qr_code_image_path = f'{MEDIA_DIR}/{hash_code}.png'
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(request.build_absolute_uri(media_url))
        qr.make(fit=True)

        qr_code_image = qr.make_image(fill_color="black", back_color="white")
        qr_code_image.save(qr_code_image_path)

        with open(qr_code_image_path, 'rb') as f:
            qr_code_image_data = f.read()

        os.remove(qr_code_image_path)

        return HttpResponse(qr_code_image_data, content_type='image/png')


class MediaAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, filename):
        file_path = os.path.join(MEDIA_DIR, filename)

        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'))
        else:
            return Response({'error': 'File not found'}, status=404)
