FROM public.ecr.aws/lambda/python:3.11

COPY requirements.txt app.py notion_connector.py openai_processor.py ${LAMBDA_TASK_ROOT}/

RUN pip3 install -r requirements.txt

CMD [ "app.lambda_handler" ]
