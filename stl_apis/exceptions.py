from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        error_messages = []
        for field, errors in response.data.items():
            if isinstance(errors, list):
                for error in errors:
                    error_messages.append(str(error))
            else:
                error_messages.append(str(errors))
        
        response.data = {
            'success': False,
            'message': ', '.join(error_messages)
        }
    return response