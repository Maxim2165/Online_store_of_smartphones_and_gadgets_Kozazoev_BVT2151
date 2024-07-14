from .korzina import Korzina

def korzina(request):
    return {'korzina': Korzina(request)}