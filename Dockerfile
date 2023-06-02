FROM python:3.10.11

# 

RUN mkdir /code

WORKDIR /code

# 


COPY requirements.txt /code

# 


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 


COPY app-agua /code

# 

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


