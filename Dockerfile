FROM dockhardman/ac-clip:0.2.x-BASE

LABEL maintainer="AllenChou <f1470891079@gmail.com>"


# Application
WORKDIR /app

COPY .  /app/

EXPOSE 51000 51001

CMD ["make", "serv_clip_transformers"]
