LIST_IP = {}


def list_ip(request):
    client_ip = get_client_ip(request)
    if LIST_IP.get(client_ip):
        print("IP такой есть = ", client_ip)
    else:
        LIST_IP[client_ip] = client_ip
        print("IP новый = ", client_ip)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(',')[0]
    else:
        client_ip = request.META.get('REMOTE_ADDR')
    return client_ip