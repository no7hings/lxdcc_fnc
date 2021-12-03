# coding:utf-8
from lxmaya_fnc import ma_fnc_abstract

from lxmaya.dcc.dcc_objects import _ma_dcc_obj_os

from lxmaya.dcc.dcc_xgn_objects import _ma_dcc_xgn_obj_utility


class Method(ma_fnc_abstract.AbsMyaChecker):
    def __init__(self, *args):
        super(Method, self).__init__(*args)
    # file exists
    def _check_method_0(self, *args):
        obj, check_index = args[:2]
        obj_path = obj.path
        #
        error_obj_files = []
        file_path = obj.get_port('fileTextureName').get()
        os_file = _ma_dcc_obj_os.OsFile(file_path)
        if os_file.get_is_exists() is False:
            error_obj_files.append(os_file)
        #
        is_error = self.set_error_obj_files_update(obj, check_index, error_obj_files)
        #
        outputs = []
        return outputs

    def _repair_method_0(self, *args):
        pass

    def set_check_run(self):
        self.set_restore()
        file_references = _ma_dcc_xgn_obj_utility.GroomFnc.get_grow_mesh_painter_file_nodes()
        self._set_objs_check_(file_references)
