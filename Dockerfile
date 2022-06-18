FROM dockhardman/ac-clip:0.1.0

LABEL maintainer="AllenChou <f1470891079@gmail.com>"


# Application
WORKDIR /app

COPY .  /app/

EXPOSE 51000

CMD ["make", "serv_clip_transformers"]
