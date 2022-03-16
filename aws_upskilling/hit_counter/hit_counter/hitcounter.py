from aws_cdk import aws_dynamodb as ddb
from aws_cdk import aws_lambda as _lambda
from constructs import Construct


class HitCounter(Construct):
    @property
    def handler(self):
        return self._handler

    def __init__(
        self, scope: Construct, id: str, downstream: _lambda.IFunction, **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        # We defined a DynamoDB table with path as the partition key (every DynamoDB table must have a single partition key).
        table = ddb.Table(
            self,
            "Hits",
            partition_key={"name": "path", "type": ddb.AttributeType.STRING},
        )

        # We defined a Lambda function which is bound to the lambda/hitcount.handler code.
        # We wired the Lambda’s environment variables to the function_name and table_name of our resources.
        self._handler = _lambda.Function(
            self,
            "HitCountHandler",
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler="hitcount.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "DOWNSTREAM_FUNCTION_NAME": downstream.function_name,
                "HITS_TABLE_NAME": table.table_name,
            },
        )

        table.grant_read_write_data(self.handler)
        downstream.grant_invoke(self.handler)
