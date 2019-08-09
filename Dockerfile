FROM centos/python-36-centos7

WORKDIR /opt/app-root/src 

COPY requirements.txt ./  

RUN pip install --no-cache-dir -r requirements.txt

COPY aws-secret-retriever.py ./  

USER 1001

ENTRYPOINT [ "python", "./aws-secret-retriever.py" ]
