data_str = """
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
      boot:
        url: file:///home/apuser/lavatest/boot-sp9850ka.img
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
    def __init__(self, *args, **kwargs):
        self.boot = kwargs['boot']
        self.system = kwargs['system']
        self.userdata = kwargs['userdata']
        self.uboot = kwargs['u-boot']
        self.tos = kwargs['tos']
        self.device_type = kwargs['device_type']
        self.job_name = kwargs['job_name']

    def _set_job_data(self):
        if not self.device_type:
            return None
        self.job_data['device_type'] = self.device_type
        self.job_data['job_name'] = self.job_name
        if self.boot:
            self.job_data["actions"][2]['images'].append({"boot":{"url":self.boot}})
        if self.system:
            self.job_data["actions"][2]['images'].append({"system":{"url":self.system}})
        if self.userdata:
            self.job_data["actions"][2]['images'].append({"userdata":{"url":self.userdata}})
        if self.uboot:
            self.job_data["actions"][2]['images'].append({"uboot":{"url":self.uboot}})
        if self.tos:
            self.job_data["actions"][2]['images'].append({"tos":{"url":self.tos}})
    def get_data_str(self):
        self._set_job_data()
        return yaml.dump(self.job_data)

if __name__ == '__main__':
    data = yaml.load(data_str)
    print(data)

