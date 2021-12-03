# coding:utf-8
from lxmaya_fnc.scripts import _mya_fnc_scp_utility, _mya_fnc_scp_texture


# scene export
def set_scene_export_by_any_scene_file(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxresolver.commands as rsv_commands
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    import lxshotgun_fnc.scripts as stg_fnc_scripts
    #
    option_opt = bsc_core.KeywordArgumentsOpt(option)
    #
    any_scene_file_path = option_opt.get('file')
    any_scene_file_path = utl_core.Path.set_map_to_platform(any_scene_file_path)
    #
    resolver = rsv_commands.get_resolver()
    rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=any_scene_file_path)
    if rsv_task_properties:
        _mya_fnc_scp_utility.set_export_check_run(rsv_task_properties)
        #
        user = option_opt.get('user') or utl_core.System.get_user_name()
        time_tag = option_opt.get('time_tag') or utl_core.System.get_time_tag()
        rsv_task_properties.set('user', user)
        rsv_task_properties.set('time_tag', time_tag)
        #
        branch = rsv_task_properties.get('branch')
        if branch == 'asset':
            step = rsv_task_properties.get('step')
            if step in ['mod', 'srf']:
                stg_fnc_scripts.set_version_log_module_result_trace(
                    rsv_task_properties,
                    'maya-scene-export',
                    'start'
                )
                #
                create_scene_src = option_opt.get('create_scene_src') or False
                if create_scene_src is True:
                    mya_dcc_objects.Scene.set_file_new()
                    set_asset_scene_src_create(rsv_task_properties)
                #
                any_scene_file = utl_dcc_objects.OsFile(any_scene_file_path)
                if any_scene_file.get_is_exists() is True:
                    mya_dcc_objects.Scene.set_file_open(any_scene_file_path)
                    # texture
                    with_texture = option_opt.get('with_texture') or False
                    if with_texture is True:
                        _mya_fnc_scp_texture.set_asset_texture_export(rsv_task_properties)
                    else:
                        # texture-tx
                        with_texture_tx = option_opt.get('with_texture_tx') or False
                        if with_texture_tx is True:
                            _mya_fnc_scp_texture.set_asset_texture_tx_export(rsv_task_properties)
                    # scene
                    with_scene = option_opt.get('with_scene') or False
                    if with_scene is True:
                        scene_file_path = set_asset_scene_export(rsv_task_properties)
                        mya_dcc_objects.Scene.set_file_open(scene_file_path)
                    # snapshot-preview
                    with_snapshot_preview = option_opt.get('with_snapshot_preview') or False
                    if with_snapshot_preview is True:
                        set_asset_scene_snapshot_preview_export(rsv_task_properties)
                    # render-preview
                    with_render_preview = option_opt.get('with_render_preview') or False
                    if with_render_preview is True:
                        pass
                        # set_asset_scene_render_preview_export(rsv_task_properties)
                    #
                    stg_fnc_scripts.set_version_log_module_result_trace(
                        rsv_task_properties,
                        'maya-scene-export',
                        'complete'
                    )
                else:
                    utl_core.Log.set_module_warning_trace(
                        'maya-scene-export-script-run',
                        u'file="{}" is non-exists'.format(any_scene_file_path)
                    )
            else:
                utl_core.Log.set_module_warning_trace(
                    'maya-scene-export-script-run',
                    u'file="{}" is not available'.format(any_scene_file_path)
                )


# create scene-src
def set_asset_scene_src_create(rsv_task_properties):
    import lxresolver.operators as rsv_operators
    #
    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    version = rsv_task_properties.get('version')
    #
    _mya_fnc_scp_utility.set_asset_workspace_create(rsv_task_properties)
    #
    scene_src_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_maya_src_file(
        version=version
    )
    mya_dcc_objects.Scene.set_file_save_to(scene_src_file_path)


def set_asset_cfx_scene_src_create(rsv_task_properties):
    import lxresolver.operators as rsv_operators
    #
    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    version = rsv_task_properties.get('version')
    #
    _mya_fnc_scp_utility.set_asset_cfx_workspace_create(rsv_task_properties)
    #
    scene_src_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_maya_src_file(
        version=version
    )
    mya_dcc_objects.Scene.set_file_save_to(scene_src_file_path)


def set_asset_scene_export(rsv_task_properties):
    import lxresolver.operators as rsv_operators
    #
    import lxmaya.fnc.exporters as mya_fnc_exporters
    #
    version = rsv_task_properties.get('version')
    root = rsv_task_properties.get('dcc.root')
    #
    scene_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_maya_file(
        workspace='publish',
        version=version
    )
    mya_fnc_exporters.SceneExporter(
        file_path=scene_file_path,
        root=root,
        option=dict(
            with_xgen=True
        )
    ).set_run()
    return scene_file_path


def set_asset_camera_yml_export(rsv_task_properties):
    import lxresolver.operators as rsv_operators
    #
    import lxmaya.fnc.exporters as mya_fnc_exporter
    #
    root = rsv_task_properties.get('dcc.root')
    version = rsv_task_properties.get('version')
    #
    asset_scene_query = rsv_operators.RsvAssetSceneQuery(rsv_task_properties)
    camera_yml_file_path = asset_scene_query.get_camera_yml_file(
        version=version
    )
    #
    mya_fnc_exporter.CameraYamlExporter(
        option=dict(
            file=camera_yml_file_path,
            root=root
        )
    ).set_run()


def set_asset_camera_abc_export(rsv_task_properties):
    import lxresolver.operators as rsv_operators
    #
    import lxmaya.fnc.exporters as mya_fnc_exporter
    #
    root = rsv_task_properties.get('dcc.root')
    version = rsv_task_properties.get('version')
    asset_scene_query = rsv_operators.RsvAssetSceneQuery(rsv_task_properties)
    camera_abc_file_path = asset_scene_query.get_camera_presp_abc_file(
        version=version
    )
    print camera_abc_file_path


def set_asset_model_scene_import(rsv_task_properties):
    import lxresolver.operators as rsv_operators
    #
    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    branch = rsv_task_properties.get('branch')
    step = rsv_task_properties.get('step')
    if branch == 'asset':
        if step in ['mod', 'srf', 'rig']:
            maya_scene_file_path = rsv_operators.RsvAssetSceneQuery(rsv_task_properties).get_maya_file(
                step='mod',
                task='modeling',
                workspace='publish',
                version='latest'
            )
            if maya_scene_file_path:
                mya_dcc_objects.Scene.set_file_import(maya_scene_file_path)


def set_asset_scene_snapshot_preview_export(rsv_task_properties):
    import lxresolver.operators as rsv_operators
    #
    import lxmaya.fnc.exporters as mya_fnc_exporter
    #
    root = rsv_task_properties.get('dcc.root')
    version = rsv_task_properties.get('version')
    #
    asset_scene_query = rsv_operators.RsvAssetSceneQuery(rsv_task_properties)
    preview_mov_file_path = asset_scene_query.get_preview_mov_file(
        workspace='publish',
        version=version
    )
    #
    mya_fnc_exporter.PreviewExporter(
        file_path=preview_mov_file_path,
        root=root,
        option=dict(
            use_render=False,
            convert_to_dot_mov=True,
        )
    ).set_run()


def set_asset_scene_render_preview_export(rsv_task_properties):
    import lxresolver.operators as rsv_operators
    #
    import lxmaya.fnc.exporters as mya_fnc_exporter
    #
    root = rsv_task_properties.get('dcc.root')
    version = rsv_task_properties.get('version')
    #
    asset_scene_query = rsv_operators.RsvAssetSceneQuery(rsv_task_properties)
    preview_mov_file_path = asset_scene_query.get_preview_mov_file(
        workspace='publish',
        version=version
    )
    #
    mya_fnc_exporter.PreviewExporter(
        file_path=preview_mov_file_path,
        root=root,
        option=dict(
            use_render=True,
            convert_to_dot_mov=True,
        )
    ).set_run()
