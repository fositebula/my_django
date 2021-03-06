#coding=utf-8
data_str = u"""
device_type: sp9850ka
job_name: lava_test_job_from_ci
timeouts:
  job:
    minutes: 120
  action:
    minutes: 65
priority: medium
visibility: public
protocols:
  lava-lxc:
    name: lxc-test
    template: debian
    distribution: debian
    release: sid
actions:
- deploy:
    namespace: tlxc
    timeout:
      minutes: 60
    to: lxc
    packages:
    - android-tools-adb
    - android-tools-fastboot
    - systemd
    - systemd-sysv
    os: debian
- boot:
    namespace: tlxc
    prompts:
    - 'root@(.*):/#'
    timeout:
      minutes: 5
    method: lxc
- deploy:
    timeout:
      minutes: 65
    to: fastboot
    namespace: droid
    images:
    -
    os: debian
- boot:
    namespace: droid
    prompts:
    - 'shell@sp9850ka_1h10:/ $'
    - 'root@(.*):/#'
    timeout:
      minutes: 5
    method: fastboot
    failure_retry: 2
- test:
    namespace: tlxc
    timeout:
      minutes: 5
    definitions:
    - repository:
        metadata:
          name: get-adb-serial-number
          format: "Lava-Test-Shell Test Definition 1.0"
          description: "Gets the adb serial number"
          maintainer:
            - erin.liu@spreadtrum.com
          os:
            - debian
          devices:
            - lxc
          scope:
            - functional
        run:
          steps:
            - lava-lxc-device-add
            - adb start-server
            - adb devices
      from: inline
      path: inline/get-adb-serial.yaml
      name: get-adb-serial
"""
import yaml

class AndroidData(object):
    job_data = yaml.load(data_str)
    def __init__(self, data, device_type, jobname = None):
        self.data = data
        self.device_type = device_type

    def _set_job_data(self):
        imgs = {}
        self.job_data['device_type'] = self.device_type
        if 'boot' in self.data:
            imgs["boot"] = {"url": self.data['boot']}
        if 'system' in self.data:
            imgs["system"] = {"url": self.data['system']}
        if 'userdata' in self.data:
            imgs["userdata"] = {"url": self.data['userdata']}
        if 'uboot' in self.data:
            imgs["uboot"] = {"url": self.data['uboot']}
        if 'tos' in self.data:
            imgs["tos"] = {"url": self.data['tos']}
        self.job_data["actions"][2]['deploy']['images'] = imgs

    def get_data_str(self):
        self._set_job_data()
        return yaml.dump(self.job_data)

if __name__ == '__main__':
    data = yaml.load(data_str)
    print(data)
    print(yaml.dump(data))

