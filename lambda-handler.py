from io import BytesIO
from PIL import Image
import torch
import json
import base64


model = torch.hub.load('yolov5', 'custom', "best300.pt", source="local")
model.conf = 0.443


def lambda_handler(event, context):

    body = json.loads(event['body'])
    
    image_bytes = body['image'].encode('utf-8')
    try:
        img = Image.open(BytesIO(base64.b64decode(image_bytes))).convert(mode='L')
    except:
        return {'statusCode': 400,
                'body': json.dumps(
                    {"answer": "File is no image or corrupt."}
                )}

    result = model(img).pandas().xyxy[0]

    if result.empty:
        return {'statusCode': 200,
                'body': json.dumps(
                    {"answer": "No meter found."}
                )}

    # look into shortest img dimension
    # complain if meter takes up more then
    # reasonable % in that dimesnion
    img_width, img_height = img.size

    if img_width < img_height:
        meter_size_frac = (result["xmax"] - result["xmin"]) / img_width
    else:
        meter_size_frac = (result["ymax"] - result["ymin"]) / img_height
    if any(meter_size_frac.values > 0.10):
        return {'statusCode': 200,
                'body': json.dumps(
                    {"answer": "Image to close."}
                )}

    return {'statusCode': 200,
                'body': json.dumps(
                    {"answer": "Okay"}
                )}