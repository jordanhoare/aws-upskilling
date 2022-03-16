#!/usr/bin/env python3

import aws_cdk as cdk
from hit_counter.pipeline_stack import PipelineStack

app = cdk.App()
PipelineStack(app, "PipelineStack")

app.synth()
