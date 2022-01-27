# coding:utf-8


def set_camera_export_by_any_scene_file(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxresolver.commands as rsv_commands
    #
    import lxmaya.fnc.builders as mya_fnc_builders
    #
    option_opt = bsc_core.KeywordArgumentsOpt(option)
    #
    any_scene_file_path = option_opt.get('file')
    any_scene_file_path = utl_core.Path.set_map_to_platform(any_scene_file_path)
    #
    resolver = rsv_commands.get_resolver()
    rsv_task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=any_scene_file_path)
    if rsv_task_properties:
        user = option_opt.get('user') or utl_core.System.get_user_name()
        time_tag = option_opt.get('time_tag') or utl_core.System.get_time_tag()
        rsv_task_properties.set('user', user)
        rsv_task_properties.set('time_tag', time_tag)
        #
        project = rsv_task_properties.get('project')
        branch = rsv_task_properties.get('branch')
        if branch == 'asset':
            asset = rsv_task_properties.get('asset')
            mya_fnc_builders.AssetBuilder(
                option=dict(
                    project=project,
                    asset=asset,
                    with_model_geometry=True,
                    geometry_var_names=['hi'],
                )
            ).set_run()
            #
            with_camera_persp_abc = option_opt.get('with_camera_persp_abc') or False
            if with_camera_persp_abc is True:
                set_asset_camera_persp_abc_export(rsv_task_properties)


def set_asset_camera_persp_abc_export(rsv_task_properties):
    import lxresolver.operators as rsv_operators
    #
    import lxmaya.fnc.importers as mya_fnc_importers
    #
    import lxmaya.fnc.exporters as mya_fnc_exporters
    #
    import lxmaya.dcc.dcc_objects as mya_dcc_objects
    #
    root = rsv_task_properties.get('dcc.root')
    version = rsv_task_properties.get('version')
    #
    asset_scene_query = rsv_operators.RsvAssetSceneQuery(rsv_task_properties)
    camera_abc_file_path = asset_scene_query.get_camera_presp_abc_file(
        version=version
    )
    camera_transform, camera_shape = mya_fnc_exporters.CameraYamlExporter._set_camera_create_(
        root=root, persp_view=True
    )
    camera_locator_abc_file_path = '/l/resource/td/asset/abc/camera-locator.abc'
    #
    mya_fnc_importers.GeometryAbcImporter(
        file_path=camera_locator_abc_file_path,
        root='/cameras'
    ).set_run()
    mya_dcc_objects.Node(camera_transform).set_parent_path(
        '|cameras|camera_locator'
    )
    mya_fnc_exporters.GeometryAbcExporter(
        file_path=camera_abc_file_path,
        root='/cameras',
        frame=(1, 8)
    ).set_run()
