class SubdomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        parts = host.split('.')
        if len(parts) >= 2:
            request.subdomain = parts[0]
        else:
            request.subdomain = None
        return self.get_response(request)
