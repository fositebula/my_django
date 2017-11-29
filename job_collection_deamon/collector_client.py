from twisted.internet.protocol import Protocol, ClientFactory
from string import Template


class CollectorProtocol(Protocol):
    def dataReceived(self, data):
        print(data)
        if data == "end":
            from twisted.internet import reactor
            reactor.stop()

        self.transport.write(self.factory.data)

    def connectionLost(self, reason):
        print("connect lost")

class CollcetorClientFactory(ClientFactory):
    protocol = CollectorProtocol
    def __init__(self, data):
        self.data = data
    def buildProtocol(self, addr):
        proto = ClientFactory.buildProtocol(self, addr=addr)
        return proto
    def clientConnectionFailed(self, connector, reason):
        print("connect failed reason: %s"%reason)
        from twisted.internet import reactor
        reactor.stop()

def stop(re):
    re.stop()

def main(data):
    factory = CollcetorClientFactory(data)
    from twisted.internet import reactor
    reactor.connectTCP("10.0.70.71", 5000, factory)
    reactor.callLater(5, stop, reactor)
    reactor.run()

JOB_INFO_JSON = """
{
    "branch":"${branch}",
    "project":"${project}",
    "buildid":"${buildid}",
    "submiter":"${submiter}",
    "verify_url":"${verify_url}",
    "gerrit_id":"${gerrit_id}",
    "port":"${port}",
    "compile_user":"${compile_user}",
    "module":"${module}",
    "testcase":"${testcase}",
    "manual_testcase":"${manual_testcase}",
    "phone_number":"${phone_number}",
    "test_description":"${test_description}",
    "project_num":"${project_num}",
    "test_task_type":"${test_task_type}",
    "buildid_from_where":0}
}
"""

if __name__ == '__main__':
#     branch_parm = sys.argv[1]
#     project_parm = sys.argv[2]
#     build_id_parm = sys.argv[3]
#     submit_user_parm = sys.argv[4]
#     verify_url_parm = sys.argv[5]
#     gerrit_id_parm = sys.argv[6]
#     port_parm = sys.argv[7]
#     compile_user_parm = sys.argv[8]
#     module_parm = sys.argv[9]
#     test_cases_parm = sys.argv[10]
#     manual_test_case_parm = sys.argv[11]
#     phone_number_parm = sys.argv[12]
#     test_description_parm = sys.argv[13]
#     project_num = sys.argv[14]
#     test_task_type_parm = sys.argv[15]

    branch_parm = 1
    project_parm = 2
    build_id_parm = 3
    submit_user_parm = 4
    verify_url_parm = 5
    gerrit_id_parm = 6
    port_parm = 7
    compile_user_parm = 8
    module_parm = 9
    test_cases_parm = 10
    manual_test_case_parm = 11
    phone_number_parm = 12
    test_description_parm = 13
    project_num = 14
    test_task_type_parm = 15
    template = Template(JOB_INFO_JSON)
    data = template.substitute(
        {"branch":branch_parm, "project":project_parm, "buildid":build_id_parm,
         "submiter":submit_user_parm, "verify_url": verify_url_parm, "gerrit_id":gerrit_id_parm,
         "port":port_parm, "compile_user":compile_user_parm, "module":module_parm,
         "testcase":test_cases_parm, "manual_testcase":manual_test_case_parm,
         "phone_number":phone_number_parm, "test_description":test_description_parm,
         "project_num":project_num, "test_task_type":test_task_type_parm},
         "buildid_from_where":0}
    )
    main(data)
    pass
