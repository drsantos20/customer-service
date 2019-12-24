

def update_address(message):
    from api.order.models import UserOrderAddress
    address = UserOrderAddress.objects.get(id=message.get('id'))
    address.latitude = message.get('lat')
    address.longitude = message.get('lng')
    address.save()
