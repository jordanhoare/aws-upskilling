from aws_cdk import Stack
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_lambda as _lambda
from constructs import Construct

from .hitcounter import HitCounter


class HitCounterStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Defines an AWS Lambda resource
        my_lambda = _lambda.Function(
            self,
            "HelloHandler",
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset("lambda"),
            handler="hello.handler",
        )

        hello_with_counter = HitCounter(
            self,
            "HelloHitCounter",
            downstream=my_lambda,
        )

        apigw.LambdaRestApi(
            self,
            "Endpoint",
            handler=hello_with_counter._handler,
        )
