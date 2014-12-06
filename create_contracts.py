#!/usr/bin/env python

import sys
from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.fv import Tenant
from cobra.model.vz import BrCP, Subj, RsSubjFiltAtt

from cobra.internal.codec.xmlcodec import toXMLStr

# setup the user properties
CONTRACT_WEB_CT = 'WebCt'
CONTRACT_APP_CT = 'AppCt'
CONTRACT_DB_CT = 'DbCt'

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

def create_contracts(modir, tenant_name):
    policy_universe = modir.lookupByDn('uni')
    fv_tenant = Tenant(policy_universe, tenant_name)

    # create Contract for web
    vz_ct_web = BrCP(fv_tenant, CONTRACT_WEB_CT)
    vz_subj_web = Subj(vz_ct_web, 'Web')
    vz_rs_subj_filt_att_web = RsSubjFiltAtt(vz_subj_web, 'http')

    #create contract for App
    vz_ct_app = BrCP(fv_tenant, CONTRACT_APP_CT)
    vz_subj_rmi = Subj(vz_ct_app, 'RMI')
    vz_rs_subj_filt_att_rmi = RsSubjFiltAtt(vz_subj_rmi, 'rmi')

    # create filter for sql
    vz_ct_db = BrCP(fv_tenant, CONTRACT_DB_CT)
    vz_subj_db = Subj(vz_ct_db, 'DbCt')
    vz_rs_subj_filt_att_db = RsSubjFiltAtt(vz_subj_db, 'sql')

    # print the query in XML format
    print toXMLStr(policy_universe, prettyPrint=True)

    # Commit the change using a ConfigRequest object
    configReq = ConfigRequest()
    configReq.addMo(policy_universe)
    modir.commit(configReq)
pass

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print 'Usage: create_contracts.py <hostname> <username> <password> <tenant_name>'
        sys.exit()
    else:
        hostname, username, password, tenant_name = sys.argv[1:]
        modir = apic_login(hostname, username, password)
        create_contracts(modir, tenant_name)
        modir.logout()
    pass
pass
