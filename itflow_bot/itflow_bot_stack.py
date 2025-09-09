from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_iam as iam,
    aws_logs as logs,
    Duration,
    CfnOutput
)
from constructs import Construct

class ITFlowBotStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create IAM role for Lex bot
        lex_role = iam.Role(
            self, "LexServiceRole",
            assumed_by=iam.ServicePrincipal("lexv2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonLexRunBotsOnly")
            ],
            description="IAM role for IT Flow Bot Lex service"
        )

        # Create Lambda execution role
        lambda_role = iam.Role(
            self, "LambdaExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
            ],
            description="IAM role for IT Flow Bot Lambda function"
        )

        # Create Lambda function for fulfillment
        fulfillment_lambda = lambda_.Function(
            self, "ITFlowBotFulfillment",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="lambda_function.lambda_handler",
            code=lambda_.Code.from_asset("lambda_functions"),
            timeout=Duration.seconds(30),
            role=lambda_role,
            environment={
                "LOG_LEVEL": "INFO"
            },
            description="Fulfillment function for IT Flow Bot"
        )

        # Grant Lex permission to invoke Lambda
        fulfillment_lambda.add_permission(
            "AllowLexInvoke",
            principal=iam.ServicePrincipal("lexv2.amazonaws.com"),
            action="lambda:InvokeFunction"
        )

        # Create CloudWatch Log Group for Lambda
        log_group = logs.LogGroup(
            self, "LambdaLogGroup",
            log_group_name=f"/aws/lambda/{fulfillment_lambda.function_name}",
            retention=logs.RetentionDays.ONE_WEEK
        )

        # Outputs
        CfnOutput(
            self, "LambdaFunctionArn",
            value=fulfillment_lambda.function_arn,
            description="The ARN of the Lambda fulfillment function - use this when configuring your Lex bot",
            export_name="ITFlowBot-LambdaArn"
        )

        CfnOutput(
            self, "LambdaFunctionName",
            value=fulfillment_lambda.function_name,
            description="The name of the Lambda fulfillment function",
            export_name="ITFlowBot-LambdaName"
        )

        CfnOutput(
            self, "LexServiceRoleArn",
            value=lex_role.role_arn,
            description="The ARN of the Lex service role - use this when creating your Lex bot",
            export_name="ITFlowBot-LexRoleArn"
        )