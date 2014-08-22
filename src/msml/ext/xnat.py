# region gplv3preamble
# The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow
#
# MSML has been developed in the framework of 'SFB TRR 125 Cognition-Guided Surgery'
#
# If you use this software in academic work, please cite the paper:
# S. Suwelack, M. Stoll, S. Schalck, N.Schoch, R. Dillmann, R. Bendl, V. Heuveline and S. Speidel,
# The Medical Simulation Markup Language (MSML) - Simplifying the biomechanical modeling workflow,
#   Medicine Meets Virtual Reality (MMVR) 2014
#
# Copyright (C) 2013-2014 see Authors.txt
#
# If you have any questions please feel free to contact us at suwelack@kit.edu
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# endregion


__author__ = 'Alexadner Weigl'
__version__ = "0.1"
__date__ = "2014-08-20"

import os
import os.path
import urllib2
import tempfile
from ..log import error, warn, info, fatal, critical, debug
import requests
from .. import log

def xnat_get(filename, resource, project, host=None, subject=None, username=None, password=None, localname=None):
    """

    :param resource:
    :param project:
    :param host:
    :param subject:
    :param username:
    :param password:
    :param localname:
    :return:
    """
    username = username or os.environ['XNAT_USER']
    password = password or os.environ['XNAT_PASS']
    host = host or os.environ['XNAT_HOST']

    if localname and os.path.exists(localname):
        log.info("Download overjump, File exists locally")
        return

    base = host if host.startswith("http") else "https://%s" % host

    if subject:
        url = "{base}/data/archive/projects/{project}/subjects/{subject}/resources/{resource}/files/{file}"
    else:
        url = "{base}/data/archive/projects/{project}/resources/{resource}/files/{file}"

    url = url.format(resource=resource, project=project, base=base, file=filename, subject=subject)
    debug(url)
    auth = (username, password)

    if not localname:
        localname = tempfile.mktemp()

    with open(localname, 'w') as fp:
        resp = requests.get(url, auth=auth, verify=False)

        if resp.status_code != 200:
            raise BaseException('Error in Accessing: %s' % resp.url)

        fp.write(resp.content)

    return


def xnat_put(localname, resource, project, filename=None, host=None, deleteBeforePut = True,
             subject=None, username=None, password=None, _content=None,
             _format=None, _tags=None):
    """

    :param localname:
    :param resource:
    :param project:
    :param filename:
    :param host:
    :param deleteBeforePut:
    :param subject:
    :param username:
    :param password:
    :param _content:
    :param _format:
    :param _tags:
    :return:
    """

    username = username or os.environ['XNAT_USER']
    password = password or os.environ['XNAT_PASS']
    host = host or os.environ['XNAT_HOST']

    base = host if host.startswith("http") else "https://%s" % host

    if subject:
        url = "{base}/data/archive/projects/{project}/subjects/{subject}/resources/{resource}/files/{file}"
    else:
        url = "{base}/data/archive/projects/{project}/resources/{resource}/files/{file}"

    url = url.format(resource=resource, project=project, base=base, file=filename, subject=subject)
    auth = (username, password)

    p = {'inbody': None, 'content': _content, 'format': _format, 'tags': _tags}

    if deleteBeforePut:
        resp = requests.delete(url, verify = False, auth = auth)
        if resp.status_code != 200:
            raise BaseException("Could not delete file: %s " % resp.url)

    with open(localname, 'rb') as fp:
        #content = fp.read()
        f = {'FILE': fp}
        resp = requests.put(url, params=p, auth=auth, files = f,  verify=False)

        log.debug(resp.url)

        if resp.status_code != 200:
            debug(resp.request.headers)
            debug(resp.headers)
            log.fatal(resp.status_code)
            raise BaseException('Error in Accessing: %s' % resp.url)

    return


from pprint import pprint
