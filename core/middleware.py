from django.conf import settings
from django.utils import translation


class APILanguageMiddleware:
    """
    API tilini dinamik tanlash uchun middleware.

    Ustuvorlik tartibi:
    1) ?lang=uz / ?lang=ru / ?lang=en
    2) X-Language: uz / ru / en
    3) Accept-Language header
    4) settings.LANGUAGE_CODE
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_languages = {code for code, _name in getattr(settings, "LANGUAGES", [])}

    def __call__(self, request):
        lang = (
            request.GET.get("lang")
            or request.headers.get("X-Language")
            or translation.get_language_from_request(request, check_path=True)
            or settings.LANGUAGE_CODE
        )

        lang = str(lang).lower().split(",")[0].strip()
        if "-" in lang:
            # en-US -> en, ru-RU -> ru
            lang = lang.split("-")[0]

        if lang not in self.allowed_languages:
            lang = settings.LANGUAGE_CODE

        translation.activate(lang)
        request.LANGUAGE_CODE = lang

        response = self.get_response(request)
        response.setdefault("Content-Language", lang)
        translation.deactivate()
        return response
