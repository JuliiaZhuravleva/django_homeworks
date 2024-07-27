FROM python:3.9

WORKDIR /app

COPY stocks_products/requirements.txt /stocks_products/
RUN pip install -r /stocks_products/requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["gunicorn", "--chdir", "stocks_products", "--bind", "0.0.0.0:8000", "stocks_products.wsgi:application"]