from aws_cdk import core
from test_dep.test_dep_stack import LambdaPhotoCheck



app = core.App()
LambdaPhotoCheck(app, "Photo-Check-Lmd")
app.synth()