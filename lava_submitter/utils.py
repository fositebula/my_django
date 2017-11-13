import requests
import os
import tarfile
import time
import random
from lava_submitter.JobData.android_data import AndroidData

def get_image_url(branch, project, url):
    image_url = url + "/artifact/sps.image/" + branch + "/" + project + ".tar.gz"
    return image_url

def time_stamp():
    ltime = time.localtime()
    time_str = time.strftime("%Y%m%d%H%M%S", ltime)
    return time_str

def make_local_path():
    ran_l = random.sample("abcdefjh", 4)
    ran_str = "".join(ran_l)

    return "/tmp/"+time_stamp()+"_"+ran_str+"/"

def download_image(url):
    local_path = make_local_path()
    print(local_path)
    file_name = url.split("/")[-1]
    if file_name.endswith("tar.gz"):
        os.mkdir(local_path)
        local_stor = local_path + file_name
        resp = requests.get(url)
        with open(local_stor, 'wb') as fd:
            fd.write(resp.content)
        return local_stor

def decompress(file_path):
    t = tarfile.open(file_path)
    local_path = "/".join(file_path.split("/")[:-1])
    print(local_path)
    t.extractall(local_path)
    t.close()
    return local_path

def get_image(image_type, local_path):
    if os.path.exists(local_path + "/" + image_type + "-sign.img"):
        return "http://"+local_path + "/" + image_type + "-sign.img"
    elif os.path.exists(local_path + "/" + image_type + ".img"):
        return "http://"+local_path + "/" + image_type + ".img"
    else:
        return None


if __name__ == '__main__':
    url = get_image_url("sprdroid7.0_trunk_k44", "sp9850kh_1h10_smtcmcc-userdebug-native",
                        "http://10.0.64.29:8080/jenkins/job/gerrit_do_verify_sprdroidn/76915/")
    f = download_image(url)
    path = decompress(f)
    print(get_image("boot", path))