FROM ubuntu:latest

RUN apt-get update \
    && apt-get install -y software-properties-common python-software-properties wget apt-transport-https\
    && wget -nc https://dl.winehq.org/wine-builds/Release.key \
    && apt-key add Release.key \
    && apt-add-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ xenial main'
    
RUN dpkg --add-architecture i386 \
    && apt-get update \
    && apt-get install -y winehq-staging  winbind cabextract
RUN cd /root \
	&& wget http://media.steampowered.com/installer/steamcmd_linux.tar.gz \
	&& tar -zxvf steamcmd_linux.tar.gz \
	&& rm -f steamcmd_linux.tar.gz
RUN wget  https://raw.githubusercontent.com/Winetricks/winetricks/master/src/winetricks \
  && chmod +x winetricks \ 
  && mv -v winetricks /usr/bin


RUN echo 233780 > steam_appid.txt

VOLUME /arma3
VOLUME /profiles
VOLUME /server

ENV STEAM_USERNAME=username
ENV STEAM_PASSWORD=password
ENV VALIDATE=1
ENV DISPLAY=novnc:0

#WORKDIR /arma3

COPY *.sh /

HEALTHCHECK --interval=30s --timeout=10s --retries=5 \
  CMD /health.sh || exit 1
ENTRYPOINT ["/docker-entry.sh"]

