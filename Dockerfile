FROM public.ecr.aws/lambda/python:3.8

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}
COPY lambda-handler.py ${LAMBDA_TASK_ROOT}
COPY best300.pt ${LAMBDA_TASK_ROOT}
COPY mod_requirements.txt ${LAMBDA_TASK_ROOT}
COPY requirements.txt ${LAMBDA_TASK_ROOT}
COPY yolov5 ${LAMBDA_TASK_ROOT}/yolov5

# Install the function's dependencies
# opencv needs to be headless in this

#RUN apt-get update
RUN pip install -r mod_requirements.txt --target "${LAMBDA_TASK_ROOT}"
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD ["app.lambda_handler"] 