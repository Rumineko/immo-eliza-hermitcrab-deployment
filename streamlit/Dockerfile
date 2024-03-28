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

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# 
ENTRYPOINT ["streamlit", "run", "streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]