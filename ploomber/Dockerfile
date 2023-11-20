FROM python:3.11

RUN pip install --no-cache-dir --upgrade pip
RUN mkdir wheels
COPY wheels/*.whl wheels
RUN pip install wheels/*.whl

ENTRYPOINT ["solara", "run", "solarathon.pages", "--host=0.0.0.0", "--port=80"]
