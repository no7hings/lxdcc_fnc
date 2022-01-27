# coding:utf-8
from lxmaya_fnc import ma_fnc_abstract

from lxmaya.dcc.dcc_objects import _mya_dcc_obj_dag, _mya_dcc_obj_dags, _mya_dcc_obj_geometry


class Method(ma_fnc_abstract.AbsMyaChecker):
    def __init__(self, *args):
        super(Method, self).__init__(*args)
    # non manifold edge
    def _check_method_0(self, *args):
        obj, check_index = args[:2]
        obj_path = obj.path
        #
        error_obj_comps = []
        comp_names = obj.get_edge_non_manifold_comp_names()
        if comp_names:
            for cmp_name in comp_names:
                component = obj.get_component(cmp_name)
                error_obj_comps.append(component)
        #
        is_error = self.set_error_obj_comps_update(obj, check_index, error_obj_comps)
        #
        outputs = []
        return outputs

    def _repair_method_0(self, *args):
        pass
    # non manifold vertex
    def _check_method_1(self, *args):
        obj, check_index = args[:2]
        obj_path = obj.path
        #
        error_obj_comps = []
        comp_names = obj.get_vertex_non_manifold_comp_names()
        if comp_names:
            for cmp_name in comp_names:
                component = obj.get_component(cmp_name)
                error_obj_comps.append(component)
        #
        is_error = self.set_error_obj_comps_update(obj, check_index, error_obj_comps)
        #
        outputs = []
        return outputs

    def _repair_method_1(self, *args):
        pass

    def set_check_run(self):
        self.set_restore()
        root = _mya_dcc_obj_dag.Group('|master|hi')
        mesh_paths = root.get_all_shape_paths(include_obj_type='mesh')
        mesh_objs = [_mya_dcc_obj_geometry.Mesh(i) for i in mesh_paths]
        self._set_objs_check_(mesh_objs)
