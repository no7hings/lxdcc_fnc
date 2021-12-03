# coding:utf-8
import lxkatana

lxkatana.set_reload()

import lxresolver.commands as rsv_commands

import lxkatana_fnc.scripts as ktn_fnc_scripts

resolver = rsv_commands.get_resolver()
#
scene_file_path = '/l/prod/cjd/publish/assets/chr/laohu_xiao/srf/surfacing/laohu_xiao.srf.surfacing.v021/scene/laohu_xiao.katana'

ktn_fnc_scripts.set_render_scene_create_by_any_scene_file(
    'file={}'.format(scene_file_path)
)
