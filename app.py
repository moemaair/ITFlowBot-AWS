#!/usr/bin/env python3
import aws_cdk as cdk
from itflow_bot.itflow_bot_stack import ITFlowBotStack

app = cdk.App()
ITFlowBotStack(app, "ITFlowBotStack",
    description="AWS Lex IT Flow Bot Stack"
)

app.synth()