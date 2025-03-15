from django.shortcuts import render
from django.http import JsonResponse

def scan_qr(request):
    return render(request, 'gym/scan_qr.html')

def process_qr(request):
    if request.method == "POST":
        qr_data = request.POST.get("qr_data", "")
        # Process the QR data (save to DB, authenticate, etc.)
        return JsonResponse({"message": "QR scanned successfully!", "data": qr_data})
    return JsonResponse({"error": "Invalid request"}, status=400)


__all__ = ['scan_qr', 'process_qr']
