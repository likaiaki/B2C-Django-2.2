def onemiddleware(get_response):
    print("init被调用")
    def middleware(request):
        print("bofore request")
        response = get_response(request)
        print("after request")
        return response
    return middleware