
from pathlib import Path
import os, tempfile
import numpy as np
import cv2
from django.core.files.storage import default_storage
from rest_framework import status


class PageApiView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = PageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        page = serializer.save()

        file_field = getattr(page, 'image', None)
        if file_field is None:
            return Response({'detail': 'image field not found on Page'}, status=500)

        abs_path = None
        tmp_to_cleanup = None   
        tmp_resized = None      
        try:
            abs_path = file_field.path  
        except Exception:
            suffix = Path(file_field.name).suffix or ''
            t = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            tmp_to_cleanup = t.name
            with file_field.open('rb') as src, open(t.name, 'wb') as dst:
                dst.write(src.read())
            abs_path = t.name

        ocr_path = abs_path
        try:
            data = np.fromfile(abs_path, np.uint8)
            img = cv2.imdecode(data, cv2.IMREAD_COLOR)
            if img is not None:
                TW, TH = 1920, 1080
                h, w = img.shape[:2]
                scale = min(TW / w, TH / h)
                nw, nh = int(round(w * scale)), int(round(h * scale))
                resized = cv2.resize(
                    img, (nw, nh),
                    interpolation=cv2.INTER_CUBIC if scale > 1 else cv2.INTER_AREA
                )
                canvas = np.full((TH, TW, 3), 255, np.uint8)  # 흰색 패딩
                x, y = (TW - nw) // 2, (TH - nh) // 2
                canvas[y:y+nh, x:x+nw] = resized

                ok, buf = cv2.imencode(".jpg", canvas, [int(cv2.IMWRITE_JPEG_QUALITY), 92])
                if ok:
                    t2 = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                    buf.tofile(t2.name)
                    t2.close()
                    tmp_resized = t2.name
                    ocr_path = tmp_resized
        except Exception:
           
            ocr_path = abs_path
        # --------------------------------------------------------

        text1 = text2 = ''
        try:
            
            text1, text2 = line(ocr_path)
        except Exception:
            text1 = text2 = ''

        
        for p in (tmp_resized, tmp_to_cleanup):
            if p:
                try:
                    os.remove(p)
                except Exception:
                    pass

        return Response({
            'id': page.id,
            'filename': file_field.name,
            'url': default_storage.url(file_field.name),
            'text1': text1,
            'text2': text2,
            'merged': f'{text1}{text2}',
        }, status=status.HTTP_201_CREATED)