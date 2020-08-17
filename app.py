#!/usr/bin/env python3

from aws_cdk import core
import os
from argo_services.argo_services_stack import ArgoServicesStack


app = core.App()
ArgoServicesStack(app, "argo-services", env=core.Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"],
    region=os.environ["CDK_DEFAULT_REGION"]))

app.synth()
