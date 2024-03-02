import json

from flask import Flask, Response

from .controllers.FlaskRestOrderController import FlaskRestOrderController
from .DiContainer import DiContainer
from .errors.OrderServiceError import OrderServiceError
from .utils import get_stack_trace

di_container = DiContainer()
app = Flask(__name__)


@app.errorhandler(OrderServiceError)
def handle_order_service_error(error: OrderServiceError):
    return Response(
        json.dumps(
            {
                'errorMessage': error.message,
                'stackTrace': get_stack_trace(error.cause),
            }
        ),
        status=error.status_code,
        mimetype='application/json',
    )


@app.errorhandler(Exception)
def handle_unspecified_error(error: Exception):
    return Response(
        json.dumps(
            {
                'errorMessage': str(error),
                'stackTrace': get_stack_trace(error),
            }
        ),
        status=500,
        mimetype='application/json',
    )


FlaskRestOrderController.register(app, route_base='/')

if __name__ == '__main__':
    app.run()
