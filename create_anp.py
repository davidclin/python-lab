#!/usr/bin/env python

import sys
from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.fv import Tenant, Ap, Ctx, BD, RsProv, RsCtx, Subnet, AEPg, RsBd, RsCons

from cobra.internal.codec.xmlcodec import toXMLStr


CTX_NAME = 'Apple-Router'

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

def create_3tier_application(modir, tenant_name):
    policy_universe = modir.lookupByDn('uni')
    fv_tenant = Tenant(policy_universe, tenant_name)

    # create context
    fv_ctx = Ctx(fv_tenant, CTX_NAME)

    #
    fv_bd = BD(fv_tenant, 'BD1')

    #
    fv_rs_ctx = RsCtx(fv_bd)
    fv_rs_ctx.__setattr__('tnFvCtxName', 'Apple-Router')
    fv_subnet_10 = Subnet(fv_bd,'10.0.0.1/24', scope='public')
    fv_subnet_20 = Subnet(fv_bd, '20.0.0.1/24', scope='public')
    fv_subnet_30 = Subnet(fv_bd, '30.0.0.1/24', scope='public')
    fv_subnet_40 = Subnet(fv_bd, '40.0.0.1/24', scope='public')

    #
    fv_ap = Ap(fv_tenant, '3-TierApp')

    fv_aepg_client = AEPg(fv_ap, 'Client')
    fv_rs_bd_client = RsBd(fv_aepg_client, tnFvBDName='BD1')
#    fv_rs_bd_client.__setattr__('tnFvBDName', 'BD1')
    fv_rs_cons_webct_client = RsCons(fv_aepg_client, 'WebCt')

    fv_aepg_web = AEPg(fv_ap, 'Web')
    fv_rs_bd_web = RsBd(fv_aepg_web, tnFvBDName='BD1')
    fv_rs_cons_webct_web = RsProv(fv_aepg_web, 'WebCt')
    fv_rs_cons_appct_web = RsCons(fv_aepg_web, 'AppCt')

    fv_aepg_app = AEPg(fv_ap, 'App')
    fv_rs_bd_app = RsBd(fv_aepg_app, tnFvBDName='DB1')
    fv_rs_cons_webct_app = RsProv(fv_aepg_app, 'WebCt')
    fv_rs_cons_appct_app = RsCons(fv_aepg_app, 'AppCt')

    fv_aepg_db = AEPg(fv_ap, 'DB')
    fv_rs_bd_db = RsBd(fv_aepg_db, tnFvBDName='BD1')
    fv_rs_prov_db = RsProv(fv_aepg_db, 'DbCt')

    print toXMLStr(policy_universe, prettyPrint=True)
    # Commit the change using a ConfigRequest object
    configReq = ConfigRequest()
    configReq.addMo(policy_universe)
    modir.commit(configReq)
    ##### End of script ####
pass


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print 'Usage: create_anp.py <hostname> <username> <password> <tenant_name>'
        sys.exit()
    else:
        hostname, username, password, tenant_name = sys.argv[1:]
        modir = apic_login(hostname, username, password)
        create_3tier_application(modir, tenant_name)
        modir.logout()
    pass
pass
