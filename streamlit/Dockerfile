FROM python:3.8

# create destination directory
RUN mkdir -p /home/work
WORKDIR /home/work

# copy files
COPY ../streamlit/requirements.txt ./

# Installation
RUN pip3 install -r requirements.txt
RUN pip install spacy
RUN python -m spacy download en_core_web_sm
RUN pip install transformers
RUN pip install nltk
RUN pip install matplotlib
RUN pip install numpy
RUN pip install pyspark
RUN pip install pymongo
RUN pip install sklearn
RUN pip install imblearn
RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113

# Run command
CMD ["streamlit","run", "streamlit_app.py"]