При составлениия использовались два проекта:
https://github.com/BrettMayson/Arma3Server
https://github.com/aaaler/arma3-wine

0. Build container using files from `dockerfile` directory. i.e.: 
```docker build -t steam-wine dockerfile/```
1. Check settings mentioned in `docker-compose.yml`. At least you need to:
 - Populate mods, fix path to them. Client mods listed in ARMA3MODS variable. 
 They are bind-mounted, so you can use single mod installation for multiple arma instances, i.e. dev and prod.
 - Server mods should be located in project dir and listed in ARMA3SERVERMODS variable.
 - Set steam credentials
 - Replace EXTERNAL_IP_HERE with your external ip.
2. Put mod's keys in `./keys`
3. Create `./arma/donotrun` file so arma will not run first time you run container.
4. Start novnc container. You need something to act like windows desktop.
5. Start arma container. That will begin installation of arma 3 windows server from steam.
(if your steam need 2factor auth -- you need to set up coorrect key in ~/.steam and map it into container) 
6/.Open vnc session (http://localhost:6901 from the server by default)
7. install wine environment using wintricks
i.e:
```
docker-compose exec arma3w winetricks vcrun2013
docker-compose exec arma3w winetricks vcrun2015
docker-compose exec arma3w winetricks d3dx11_43
docker-compose exec arma3w winetricks mdac28
```
That will run installers with gui, so you click "next-next-next" in vnc session.

8. stop arma container
9. remove `./arma/donotrun`
10. start container again. observe logs. have fun.

