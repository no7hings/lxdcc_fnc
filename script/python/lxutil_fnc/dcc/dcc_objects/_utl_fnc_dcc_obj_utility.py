# coding:utf-8
import lxobj.core_objects as core_dcc_objects

import lxutil.dcc.dcc_objects as utl_dcc_objects

import lxutil.objects as utl_objects

from lxutil_fnc.dcc import utl_fnc_dcc_abstract


class Scene(utl_fnc_dcc_abstract.AbsObjScene):
    FILE_CLASS = utl_dcc_objects.OsFile
    UNIVERSE_CLASS = core_dcc_objects.ObjUniverse
    #
    CONFIGURE_CLASS = utl_objects.Configure
    def __init__(self):
        super(Scene, self).__init__()
