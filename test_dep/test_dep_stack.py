from aws_cdk import (
    aws_events as events,
    aws_lambda as lambda_,
    aws_events_targets as targets,
    aws_iam as _iam,
    core,
)


class LambdaPhotoCheck(core.Stack):
    def __init__(self, app: core.App, id: str) -> None:
        super().__init__(app, id)

        with open("lambda-handler.py", encoding="utf8") as fp:
            handler_code = fp.read()


        lambdaLayer = lambda_.LayerVersion(self, 'cdk-lambda-layer',
                  code = lambda_.AssetCode('layer/'),
                  compatible_runtimes = [lambda_.Runtime.PYTHON_3_8],
        )
        
        lambdaRole = _iam.Role(scope=self, id='cdk-lambda-role', assumed_by=_iam.ServicePrincipal('lambda.amazonaws.com'), role_name='cdk-lambda-role', managed_policies=[_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaVPCAccessExecutionRole'), _iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole')])

        lambdaFn = lambda_.Function(
            self, "photo-check-lmd",
            code=lambda_.InlineCode(handler_code),
            handler="index.handler",
            timeout=core.Duration.seconds(900),
            runtime=lambda_.Runtime.PYTHON_3_8,
            layers = [lambdaLayer],
            role = lambdaRole,
        )

        

        rule = events.Rule(
            self, "Rule",
            schedule=events.Schedule.rate(core.Duration.days(1)),
        )
        rule.add_target(targets.LambdaFunction(lambdaFn))


