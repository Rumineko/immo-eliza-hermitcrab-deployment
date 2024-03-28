# 
FROM python:3.9

#
COPY ./requirements.txt /code/requirements.txt

#
COPY ./ /code/api

#
WORKDIR /code

# 
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 
CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8000"]