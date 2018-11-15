FROM alpine:latest

RUN apk --update --upgrade add bash cairo pango gdk-pixbuf py3-cffi py3-pillow py-lxml
RUN pip3 install weasyprint gunicorn flask

RUN mkdir /myapp
WORKDIR /myapp
ADD ./wsgi.py /myapp
ADD ./templates /myapp/templates

RUN mkdir /root/.fonts
#ADD ./fonts/* /root/.fonts/
RUN apk --no-cache add msttcorefonts-installer fontconfig && \
    update-ms-fonts && \
    fc-cache -f

CMD gunicorn --bind 0.0.0.0:5001 wsgi:app
