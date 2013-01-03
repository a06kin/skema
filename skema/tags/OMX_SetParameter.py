# Copyright (C) 2011-2013 Aratelia Limited - Juan A. Rubio
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

import sys
import skema.tag

from skema.omxil12 import *
from skema.omxil12 import OMX_AUDIO_PORTDEFINITIONTYPE
from skema.omxil12 import OMX_VIDEO_PORTDEFINITIONTYPE
from skema.omxil12 import OMX_IMAGE_PORTDEFINITIONTYPE
from skema.omxil12 import OMX_OTHER_PORTDEFINITIONTYPE

from skema.utils import log_line
from skema.utils import log_api
from skema.utils import log_result

from types import *
from ctypes import *
from xml.etree.ElementTree import ElementTree as et

class tag_OMX_SetParameter(skema.tag.SkemaTag):
    """

    """
    def run(self, element, context):
        indexstr = element.get('index')
        alias = element.get('alias')
        name = context.cnames[alias]
        portstr = element.get('port')

        log_api ("%s '%s' '%s:Port-%d'" \
                        % (element.tag, indexstr, name, int(portstr)))

        handle = context.handles[alias]
        index = get_il_enum_from_string(indexstr)
        param_type = skema.omxil12.__all_indexes__[indexstr]
        param_struct = param_type()
        param_struct.nSize = sizeof(param_type)

        if (portstr != None):
            param_struct.nPortIndex = int(portstr)

        if (handle != None):
            omxerror = OMX_GetParameter(handle, index, byref(param_struct))
            interror = int(omxerror & 0xffffffff)
            err = get_string_from_il_enum(interror, "OMX_Error")

            for name, val in param_type._fields_:
                for name2, val2 in element.items():
                    if (name2 == name):
                        setattr(param_struct, name, int(val2))

            omxerror = OMX_SetParameter(handle, index, byref(param_struct))
            interror = int(omxerror & 0xffffffff)
            domstr = ""
            err = get_string_from_il_enum(interror, "OMX_Error")
            log_line ()
            log_line ("%s" % param_struct.__class__.__name__, 1)
            for name, val in param_type._fields_:
                if (name == "nVersion"):
                    log_line ("%s -> '%08x'" \
                                    % (name, param_struct.nVersion.nVersion), 1)
                elif (name == "eDir"):
                    dirstr = get_string_from_il_enum \
                        (getattr(param_struct, name), "OMX_Dir")
                    log_line ("%s -> '%s'" % (name, dirstr), 1)
                elif (name == "eDomain"):
                    domstr = get_string_from_il_enum \
                        (getattr(param_struct, name), "OMX_PortDomain")
                    log_line ("%s -> '%s'" % (name, domstr), 1)
                elif (name == "format"):

                    if (domstr == "OMX_PortDomainAudio"):
                        param2_type = OMX_AUDIO_PORTDEFINITIONTYPE
                    elif (domstr == "OMX_PortDomainVideo"):
                        param2_type = OMX_VIDEO_PORTDEFINITIONTYPE
                    elif (domstr == "OMX_PortDomainImage"):
                        param2_type = OMX_IMAGE_PORTDEFINITIONTYPE
                    elif (domstr == "OMX_PortDomainOther"):
                        param2_type = OMX_OTHER_PORTDEFINITIONTYPE

                    log_line ("%s"  % param2_type.__name__, 2)
                    for name2, val2 in param2_type._fields_:
                        if (name2 == "eEncoding"):
                            encstr = get_string_from_il_enum \
                                (getattr(param_struct.format.audio, name2), \
                                     "OMX_AUDIO_Coding")
                            log_line ("%s -> '%s'" % (name2, encstr), 2)
                        else:
                            log_line ("%s -> '%s'" % (name2, getattr(\
                                        param_struct.format.audio, name2)), 2)
                else:
                    log_line ("%s -> '%s'" \
                        % (name, getattr(param_struct, name)), 1)

            log_result(element.tag, err)

tagobj = skema.tag.SkemaTag(tagname="OMX_SetParameter")