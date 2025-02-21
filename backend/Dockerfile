FROM continuumio/miniconda3

WORKDIR /app
COPY environment.yml .

RUN conda env create -f environment.yml
# Activate conda environment in shell
SHELL ["conda", "run", "-n", "captions-app", "/bin/bash", "-c"]

COPY . .

CMD ["conda", "run", "-n", "captions-app", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 