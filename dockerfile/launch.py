import os
import re
import shutil
import subprocess
from string import Template
import time
import local
import workshop


def mod_param(name, mods):
    return ' -{}="{}" '.format(name, ";".join(mods))


def env_defined(key):
    return key in os.environ and len(os.environ[key]) > 0


CONFIG_FILE = os.environ["ARMA_CONFIG"]
KEYS = "/arma3/keys"

if not os.path.isdir(KEYS):
    if os.path.exists(KEYS):
        os.remove(KEYS)
    os.makedirs(KEYS)

if os.environ["SKIP_INSTALL"] in ["", "false"]:
    # Install Arma

    steamcmd = ["/steamcmd/steamcmd.sh"]
    # не забудем про винду
    steamcmd.extend(["+@sSteamCmdForcePlatformType", "windows"])
    steamcmd.extend(["+force_install_dir", "/arma3"])
    steamcmd.extend(["+login", os.environ["STEAM_USER"], os.environ["STEAM_PASSWORD"]])
    steamcmd.extend(["+app_update", "233780"])
    steamcmd.extend(["-language", "Russian"])
    if env_defined("STEAM_BRANCH"):
        steamcmd.extend(["-beta", os.environ["STEAM_BRANCH"]])
    if env_defined("STEAM_BRANCH_PASSWORD"):
        steamcmd.extend(["-betapassword", os.environ["STEAM_BRANCH_PASSWORD"]])
    steamcmd.extend(["validate"])
    if env_defined("STEAM_ADDITIONAL_DEPOT"):
        for depot in os.environ["STEAM_ADDITIONAL_DEPOT"].split("|"):
            depot_parts = depot.split(",")
            steamcmd.extend(
                ["+login", os.environ["STEAM_USER"], os.environ["STEAM_PASSWORD"]]
            )
            steamcmd.extend(
                ["+download_depot", "233780", depot_parts[0], depot_parts[1]]
            )
    steamcmd.extend(["+quit"])
    subprocess.call(steamcmd)

if env_defined("STEAM_ADDITIONAL_DEPOT"):
    for depot in os.environ["STEAM_ADDITIONAL_DEPOT"].split("|"):
        depot_parts = depot.split(",")
        depot_dir = (
            f"/steamcmd/linux32/steamapps/content/app_233780/depot_{depot_parts[0]}/"
        )
        for file in os.listdir(depot_dir):
            shutil.copytree(depot_dir + file, "/arma3/", dirs_exist_ok=True)
            print(f"Moved {file} to /arma3")

# pause 
if os.environ["PAUSE_START"] in ["1", "true"]:
    i = 1
    while i <= 10:
        print("sleep to install wine setup")
        time.sleep(19)
# Mods

mods = []

if os.environ["MODS_PRESET"] != "":
    mods.extend(workshop.preset(os.environ["MODS_PRESET"]))

if os.environ["MODS_LOCAL"] == "true" and os.path.exists("mods"):
    mods.extend(local.mods("mods"))

launch_0 = "{}".format(
    os.environ["ARMA_BINARY"],
)
#!!!тут указан полный путь к профилю и если папку поменять работать не будет!!!
launch_1 = "Z:\\arma3\\arma3server.exe -limitFPS={} -world={} {} {}".format(
    os.environ["ARMA_LIMITFPS"],
    os.environ["ARMA_WORLD"],
    os.environ["ARMA_PARAMS"],
    mod_param("mod", mods),
)

if os.environ["ARMA_CDLC"] != "":
    for cdlc in os.environ["ARMA_CDLC"].split(";"):
        launch_1 += " -mod={}".format(cdlc)

clients = int(os.environ["HEADLESS_CLIENTS"])
print("Headless Clients:", clients)

if clients != 0:
    launch_1_hc=launch_1
    with open("/arma3/configs/{}".format(CONFIG_FILE)) as config:
        data = config.read()
        regex = r"(.+?)(?:\s+)?=(?:\s+)?(.+?)(?:$|\/|;)"

        config_values = {}

        matches = re.finditer(regex, data, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            config_values[match.group(1).lower()] = match.group(2)

        if "headlessclients[]" not in config_values:
            data += '\nheadlessclients[] = {"127.0.0.1"};\n'
        if "localclient[]" not in config_values:
            data += '\nlocalclient[] = {"127.0.0.1"};\n'

        with open("/arma3/tmp/arma3.cfg", "w") as tmp_config:
            tmp_config.write(data)
        #launch_1_hc += ' -config=arma3\\tmp\\arma3.cfg'
        launch_1_hc += ' -config=tmp\\arma3.cfg'

    client_launch = launch_1_hc
    client_launch += " -client -connect=127.0.0.1 -port={}".format(os.environ["PORT"])
    if "password" in config_values:
        client_launch += " -password={}".format(config_values["password"])

    for i in range(0, clients):
        hc_template = Template(
            os.environ["HEADLESS_CLIENTS_PROFILE"]
        )  # eg. '$profile-hc-$i'
        hc_name = hc_template.substitute(
            profile=os.environ["ARMA_PROFILE"], i=i, ii=i + 1
        )

        hc_launch = client_launch + ' -name="{}"'.format(hc_name)
        print("LAUNCHING ARMA CLIENT {} WITH".format(i), hc_launch)
        file = open("/arma3/start_h_client.bat", "w")
        file.write(hc_launch)
        file.close()
        #subprocess.Popen(hc_launch, shell=True)
        launch_hc_bat=launch_0
        launch_hc_bat+="start_h_client.bat"
        subprocess.Popen(launch_hc_bat, shell=True)
        #subprocess.Popen(launch_hc_bat,)
        #os.system(launch_hc_bat) #работает но не идет дальше!
        time.sleep(15)

else:
    launch_1_serv=launch_1
    #launch_1 += ' -config=arma3\\configs\\{}'.format(CONFIG_FILE)
#launch_1 += ' -config=arma3\\configs\\{}'.format(CONFIG_FILE)
launch_1 += ' -config=configs\\{}'.format(CONFIG_FILE)
#launch += ' -port={} -name="{}" -profiles="arma3/configs/profiles"'.format(
#пробуем указать путь до профиля

#!!!тут указан полный путь к профилю и если папку поменять работать не будет!!!

launch_1 += ' -port={} -name={} -profiles=Z:\\arma3\\configs\\profiles'.format(
    os.environ["PORT"], os.environ["ARMA_PROFILE"]
)

if os.path.exists("servermods"):
    launch_1 += mod_param("serverMod", local.mods("servermods"))

print("LAUNCHING ARMA SERVER WITH", launch_0, launch_1, flush=True)
file = open("/arma3/start_server.bat", "w")
file.write(launch_1)
file.close()
launch_server_bat=launch_0
launch_server_bat+="start_server.bat"
os.system(launch_server_bat)
#subprocess.Popen(launch_server_bat)