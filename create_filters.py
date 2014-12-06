#!/usr/bin/env python

import sys
from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.fv import Tenant
from cobra.model.vz import Filter, Entry

from cobra.internal.codec.xmlcodec import toXMLStr

FILTER_HTTP_NAME = 'http'
FILTER_RMI_NAME = 'rmi'
FILTER_SQL_NAME = 'sql'

def apic_login(hostname, username, password):
    url = "http://" + hostname
    sess = LoginSession(url, username, password)
    modir = MoDirectory(sess)
    try:
        modir.login()
    except:
        print 'Login error'
        exit(1)
    return modir
pass

def create_filters(modir, tenant_name):

    policy_universe = modir.lookupByDn('uni')
    fv_tenant = Tenant(policy_universe, tenant_name)

    # create filter for http
    vz_filter_http = Filter(fv_tenant, FILTER_HTTP_NAME)
    vz_entry_http = Entry(vz_filter_http, 'DPort-80', dFromPort='80', dToPort='80', etherT='ip', prot='tcp')

    #create filter for rmi
    vz_filter_rmi = Filter(fv_tenant, FILTER_RMI_NAME)
    vz_entry_rmi = Entry(vz_filter_http, 'DPort-1514', dFromPort='1514', dToPort='1514', etherT='ip', prot='tcp')

    # create filter for sql
    vz_filter_sql = Filter(fv_tenant, FILTER_RMI_NAME)
    vz_entry_sql = Entry(vz_filter_http, 'DPort-1433', dFromPort='1433', dToPort='1433', etherT='ip', prot='tcp')

    # print the query in XML format
    print toXMLStr(policy_universe, prettyPrint=True)

    # Commit the change using a ConfigRequest object
    configReq = ConfigRequest()
    configReq.addMo(policy_universe)
    modir.commit(configReq)
pass

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print 'Usage: create_filters.py <hostname> <username> <password> <tenant_name>'
        sys.exit()
    else:
        hostname, username, password, tenant_name = sys.argv[1:]
        modir = apic_login(hostname, username, password)
        create_filters(modir, tenant_name)
        modir.logout()
    pass
pass
