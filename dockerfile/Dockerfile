FROM debian:bullseye

RUN apt-get update \
    && \
    apt-get install -y --no-install-recommends --no-install-suggests \
        python3 \
        lib32stdc++6 \
        lib32gcc-s1 \
        libcurl4 \
        wget \
        mc \
        locales\
        ca-certificates \
    && \
    apt-get remove --purge -y \
    && \
    apt-get clean autoclean \
    && \
    apt-get autoremove -y \
    && \
    rm -rf /var/lib/apt/lists/*\
    && \
    mkdir -p /steamcmd \
    && \
    wget -qO- 'https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz' | tar zxf - -C /steamcmd

# Locale
RUN sed -i -e \
  's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen \
   && locale-gen

ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU:ru
ENV LC_LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8

# +Timezone (если надо на этапе сборки)
ENV TZ Asia/Barnaul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update \
    #&& apt-get install -y software-properties-common python-software-properties wget apt-transport-https\
    && apt-get install -y software-properties-common git-core wget apt-transport-https
    #&&  mkdir -pm755 /etc/apt/keyrings \
    #&& wget -O /etc/apt/keyrings/winehq-archive.key https://dl.winehq.org/wine-builds/winehq.key \
    #&& wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/ubuntu/dists/noble/winehq-noble.sources
    #&& wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/ubuntu/dists/jammy/winehq-jammy.sources
    #&& wget -nc https://dl.winehq.org/wine-builds/Release.key \
    #&& apt-key add Release.key \
    #&& apt-add-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ xenial main'
    #&& apt-add-repository 'https://dl.winehq.org/wine-builds/ubuntu/'
    #&& add-apt-repository ppa:wine/wine-builds

RUN dpkg --add-architecture i386 
RUN mkdir -pm755 /etc/apt/keyrings 
RUN wget -O /etc/apt/keyrings/winehq-archive.key https://dl.winehq.org/wine-builds/winehq.key
RUN wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/debian/dists/bullseye/winehq-bullseye.sources
#RUN wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/ubuntu/dists/jammy/winehq-jammy.sources

    #&& add-apt-repository ppa:wine/wine-builds \
RUN apt-get update 
    #&& apt-get install -y winehq-staging  winbind cabextract

#RUN apt-get install -y winehq-stable=8.0.1~bullseye-1 wine-stable=8.0.1~bullseye-1 wine-stable-i386=8.0.1~bullseye-1 wine-stable-amd64=8.0.1~bullseye-1

RUN apt-get install --install-recommends -y wine

RUN apt-get install --install-recommends -y winbind cabextract
#RUN cd /root \
#	&& wget http://media.steampowered.com/installer/steamcmd_linux.tar.gz \
#	&& tar -zxvf steamcmd_linux.tar.gz \
#	&& rm -f steamcmd_linux.tar.gz
RUN wget  https://raw.githubusercontent.com/Winetricks/winetricks/master/src/winetricks \
  && chmod +x winetricks \ 
  && mv -v winetricks /usr/bin


RUN echo 233780 > steam_appid.txt

EXPOSE 2302/udp
EXPOSE 2303/udp
EXPOSE 2304/udp
EXPOSE 2305/udp
EXPOSE 2306/udp

VOLUME /arma3
#VOLUME /profiles
#VOLUME /server

ENV STEAM_USERNAME=username
ENV STEAM_PASSWORD=password
ENV VALIDATE=1
ENV DISPLAY=novnc:0

ENV ARMA_BINARY=./arma3server
ENV ARMA_CONFIG=main.cfg
ENV ARMA_PARAMS=
ENV ARMA_PROFILE=main
ENV ARMA_WORLD=empty
ENV ARMA_LIMITFPS=100
ENV ARMA_CDLC=
ENV HEADLESS_CLIENTS=0
ENV HEADLESS_CLIENTS_PROFILE="\$profile-hc-\$i"
ENV PORT=2302
ENV STEAM_BRANCH=public
ENV STEAM_BRANCH_PASSWORD=
ENV STEAM_ADDITIONAL_DEPOT=
ENV MODS_LOCAL=true
ENV MODS_PRESET=
ENV SKIP_INSTALL=false
#остановка при первом запуске!
ENV PAUSE_START=true
#чтобы выполнить эти команды:
#docker-compose exec arma3w winetricks vcrun2013
#docker-compose exec arma3w winetricks vcrun2015
#docker-compose exec arma3w winetricks d3dx11_43
#docker-compose exec arma3w winetricks mdac28

WORKDIR /arma3

STOPSIGNAL SIGINT

#COPY *.sh /
COPY *.py /
COPY launch.py /script/launch.py
COPY workshop.py /script/workshop.py
COPY local.py /script/local.py
COPY keys.py /script/keys.py

CMD ["python3","/script/launch.py"]

#HEALTHCHECK --interval=30s --timeout=10s --retries=5 \
#  CMD /health.sh || exit 1
#ENTRYPOINT ["/docker-entry.sh"]

