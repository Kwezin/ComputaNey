import json
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.utilities.typing import LambdaContext
from routes.index import router
from aws_lambda_powertools.logging import Logger

logger = Logger()
app = APIGatewayHttpResolver()
app.include_router(router)

# novo terraform
def lambda_handler(event: dict, context: LambdaContext):
  logger.info(f'event: {event}')

  try:
    return app.resolve(event, context)

  except Exception as err:
    return {
      "statusCode": 500,
      "body": json.dumps({
          "error": True,
          "message": str(err)
      }),
      "headers": {
        "Content-Type": "application/json"
      }
    }