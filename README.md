0. build container using files from `dockerfile` directory. i.e.: 
```docker build -t steam-wine dockerfile/```
1. put mods in directories mentioned in `docker-compose.yml`. They are bind-mounted, so you can use single mod installation for multiple arma instances, i.e. dev and prod.
2. put mod's keys in `./keys`
3. create `./arma/donotrun` file so arma will not run first time you run container.
4. start novnc container
4. start arma container to install game from steam 
(if your steam need 2factor auth -- you need to set up coorrect key in ~/.steam and map it into container) 
5. open vnc session (http://localhost:6901 from the server by default)
6. install wine environment using wintricks
i.e:
```
docker-compose exec arma3w winetricks vcrun2013
docker-compose exec arma3w winetricks vcrun2015
docker-compose exec arma3w winetricks d3dx11_43
docker-compose exec arma3w winetricks mdac28
```
That will run installers with gui, so you click "next-next-next" in vnc session.

7. stop arma container
8. remove `./arma/donotrun`
9. start container again. observe logs. have fun.

