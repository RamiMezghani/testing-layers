#!/usr/bin/env python3

import aws_cdk as cdk

from test_dep.test_dep_stack import TestDepStack


app = cdk.App()
TestDepStack(app, "test-dep")

app.synth()
