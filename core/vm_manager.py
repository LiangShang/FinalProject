

import keystoneclient.v2_0.client as ksclient
import novaclient.v1_1.client as nvclient
import glanceclient
import os
import exe_time


def get_keystone_creds():
    d = {}
    d['username'] = 'admin'
    d['password'] = 'password'
    d['auth_url'] = 'http://192.168.50.4:5000/v2.0/'
    d['tenant_name'] = 'demo'
    return d


def get_nova_creds():
    d = {}
    d['username'] = 'admin'
    d['api_key'] = 'password'
    d['auth_url'] = 'http://192.168.50.4:5000/v2.0/'
    d['project_id'] = 'demo'
    return d


def create_instance(vm_name, image_name, flavor_name):

    keystone_creds = get_keystone_creds()
    keystone = ksclient.Client(**keystone_creds)
    nova_creds = get_nova_creds()
    nova = nvclient.Client(**nova_creds)
    glance_endpoint = keystone.service_catalog.url_for(service_type='image',
                                                       endpoint_type='publicURL')
    glance = glanceclient.Client('1', glance_endpoint, token=keystone.auth_token)
    image = glance.images.find(name=image_name)
    flavor = nova.flavors.find(name=flavor_name)
    instance = nova.servers.create(name=vm_name, image=image, flavor=flavor)
    while instance.status == 'BUILD':
        exe_time.sleep(5)
        instance = nvclient.servers.get(instance.id)
        if instance.status == 'ACTIVE':
            return instance
        elif instance.status == 'ERROR':
            return None
