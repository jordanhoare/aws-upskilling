#!/usr/bin/env python3

import aws_cdk as cdk

from hit_counter.hit_counter_stack import HitCounterStack

# from hit_counter.pipeline_stack import PipelineStack


app = cdk.App()
HitCounterStack(app, "hit-counter")

app.synth()
