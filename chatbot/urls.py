from ninja import NinjaAPI
from .views import router


api = NinjaAPI()
api.add_router("", router)
