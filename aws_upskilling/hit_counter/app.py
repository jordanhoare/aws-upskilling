#!/usr/bin/env python3

import aws_cdk as cdk

from hit_counter.hit_counter_stack import HitCounterStack


app = cdk.App()
HitCounterStack(app, "hit-counter")

app.synth()
