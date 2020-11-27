u"""
Конфиг URL для API.

Будет использоваться стандартный класс DRF BaseRouter.
"""

from rest_framework.routers import BaseRouter


router = BaseRouter

router.register()

urlpatterns = router.urls
