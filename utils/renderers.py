from rest_framework.renderers import JSONRenderer

class StandardJSONRenderer(JSONRenderer):
    """
    Renderer global para unificar la estructura de las respuestas DRF.
    """
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # If the view already structured the data, just return it.
        if isinstance(data, dict) and "success" in data and "message" in data:
            return super().render(data, accepted_media_type, renderer_context)

        response = getattr(renderer_context, "response", None)
        status_code = response.status_code if response else 200

        success = 200 <= status_code < 300
        formatted = {
            "success": success,
            "message": data.get("message", "Éxito") if isinstance(data, dict) else "Éxito",
            "data": data.get("data", data) if isinstance(data, dict) else data,
            "errors": data.get("errors", None) if isinstance(data, dict) else None,
        }
        return super().render(formatted, accepted_media_type, renderer_context)
