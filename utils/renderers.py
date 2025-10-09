from rest_framework.renderers import JSONRenderer

class StandardJSONRenderer(JSONRenderer):
    """
    Renderer global para unificar la estructura de las respuestas DRF.
    """
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get('response', None) # type: ignore
        status_code = getattr(response, 'status_code', 200)

        # Si viene de un error (por ejemplo 400, 404, 500)
        success = 200 <= status_code < 300

        # Estructura estándar
        formatted = {
            'success': success,
            'message': '',
            'data': None,
            'errors': None,
        }

        # Si DRF mandó data normal
        if isinstance(data, dict):
            # Si DRF ya contiene claves conocidas, respetarlas
            if 'results' in data or 'count' in data:
                formatted['data'] = data  # para respuestas paginadas
            elif 'detail' in data and not success:
                formatted['message'] = data.get('detail')
            else:
                formatted['data'] = data
        else:
            formatted['data'] = data

        # Si hay errores
        if not success:
            formatted['errors'] = data

        return super().render(formatted, accepted_media_type, renderer_context)
