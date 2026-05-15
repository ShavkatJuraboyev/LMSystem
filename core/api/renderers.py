from django.utils.translation import gettext_lazy as _
from rest_framework.renderers import JSONRenderer


class StandardJSONRenderer(JSONRenderer):
    """
    API javoblarini yagona formatda qaytaradi.

    Success:
    {
        "success": true,
        "message": "Muvaffaqiyatli bajarildi.",
        "data": ...,
        "errors": null
    }

    Error:
    {
        "success": false,
        "message": "Xatolik yuz berdi.",
        "data": null,
        "errors": ...
    }
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get("response") if renderer_context else None

        # drf-spectacular schema endpointlarini o'rab yubormaslik kerak
        request = renderer_context.get("request") if renderer_context else None
        path = getattr(request, "path", "") or ""
        if path.startswith("/api/schema") or path.startswith("/api/swagger") or path.startswith("/api/redoc"):
            return super().render(data, accepted_media_type, renderer_context)

        if isinstance(data, dict) and {"success", "data", "errors"}.issubset(data.keys()):
            return super().render(data, accepted_media_type, renderer_context)

        is_error = bool(response is not None and response.exception)

        payload = {
            "success": not is_error,
            "message": str(_("Xatolik yuz berdi." if is_error else "Muvaffaqiyatli bajarildi.")),
            "data": None if is_error else data,
            "errors": data if is_error else None,
        }

        return super().render(payload, accepted_media_type, renderer_context)
