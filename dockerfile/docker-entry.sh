#!/bin/sh
/root/steamcmd.sh  +@sSteamCmdForcePlatformType windows +login $STEAM_USERNAME $STEAM_PASSWORD  +force_install_dir /arma3 +app_update 233780 +quit
[ -f /arma3/tbbmalloc.dll ] || ln -s  /arma3/\@ExileServer/tbbmalloc.dll /arma3/tbbmalloc.dll
[ -f /arma3/donotrun ] || wine /arma3/arma3server.exe -cfg=basic.cfg  -config=config.cfg -autoInit -profiles=profiles -mod=$ARMA3MODS -servermod=$ARMA3SERVERMODS &
sleep 15
tail -f `ls -ac /arma3/profiles/arma3server_* | cat | head -1` `ls -ac /arma3/profiles/server_* | cat | head -1`

