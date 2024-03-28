# 
FROM python:3.9

#
COPY ./requirements.txt /code/requirements.txt

#
COPY ./ /code/streamlit

#
WORKDIR /code/streamlit

# 
RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8501

# 
ENTRYPOINT ["streamlit", "run", "streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]