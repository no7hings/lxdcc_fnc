# coding:utf-8
from lxmaya_fnc import ma_fnc_abstract

from lxutil_prd import utl_prd_commands

from lxmaya_prd import ma_prd_objects

from lxmaya.dcc.dcc_objects import _mya_dcc_obj_dags


class Method(ma_fnc_abstract.AbsMyaChecker):
    NAMING_PATTERN = '*_grp'
    def __init__(self, *args):
        super(Method, self).__init__(*args)
    # Group-name is Non-match *_grp
    def _check_method_0(self, *args):
        obj, check_index = args
        #
        is_error = not obj.get_is_naming_match(self.NAMING_PATTERN)
        #
        self.set_error_obj_update(is_error, obj, check_index)
        #
        outputs = []
        return outputs
    # noinspection PyMethodMayBeStatic
    def _repair_method_0(self, *args):
        obj = args[0]
        obj._set_path_update_()
        if obj.get_is_exists():
            new_name = '{}_grp'.format(obj.name)
            obj.set_rename(new_name)
    # empty
    def _check_method_1(self, *args):
        obj, check_index = args
        #
        is_error = not obj.get_all_shape_paths()
        #
        self.set_error_obj_update(is_error, obj, check_index)
        #
        outputs = []
        return outputs
    # noinspection PyMethodMayBeStatic
    def _repair_method_1(self, *args):
        obj = args[0]
        obj._set_path_update_()
        if obj.get_is_exists():
            obj.set_delete()

    def set_check_run(self):
        self.set_restore()
        #
        self.EXCEPT_DCC_PATHS = []
        scene = utl_prd_commands.get_current_scene()
        entity_obj = scene.get_current_entity_obj()
        step_obj = scene.get_current_step_obj()
        # exclude entity and step groups
        if step_obj is not None:
            shot_opt = ma_prd_objects.ObjOpt(entity_obj)
            for i in shot_opt.get_dcc_group_paths():
                self.EXCEPT_DCC_PATHS.append(i)
            step_op = ma_prd_objects.ObjOpt(step_obj)
            for i in step_op.get_dcc_group_paths():
                self.EXCEPT_DCC_PATHS.append(i)
        #
        groups = _mya_dcc_obj_dags.Groups().get_custom_nodes(reference=False, exclude_paths=self.EXCEPT_DCC_PATHS)
        self._set_objs_check_(groups)
