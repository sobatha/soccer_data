FROM continuumio/anaconda3

RUN pip install --upgrade pip

# RUN conda install -c conda-forge streamlit
RUN pip install streamlit

WORKDIR /app

COPY . /app