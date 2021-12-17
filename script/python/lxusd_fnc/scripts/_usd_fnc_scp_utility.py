# coding:utf-8


def set_usd_export_by_any_scene_file(option):
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxresolver.commands as rsv_commands
    #
    import lxshotgun_fnc.scripts as stg_fnc_scripts
    #
    option_opt = bsc_core.KeywordArgumentsOpt(option)
    #
    scene_file_path = option_opt.get('file')
    scene_file_path = utl_core.Path.set_map_to_platform(scene_file_path)
    #
    resolver = rsv_commands.get_resolver()
    task_properties = resolver.get_task_properties_by_any_scene_file_path(file_path=scene_file_path)
    if task_properties:
        branch = task_properties.get('branch')
        if branch == 'asset':
            stg_fnc_scripts.set_version_log_module_result_trace(
                task_properties,
                'usd-export',
                'start'
            )
            #
            with_geometry_uv_map_usd = option_opt.get('with_geometry_uv_map_usd') or False
            if with_geometry_uv_map_usd is True:
                set_asset_geometry_uv_map_usd_export(task_properties)
            #
            with_usd_set = option_opt.get('with_usd_set') or False
            if with_usd_set is True:
                set_asset_usd_set_export(task_properties)
            #
            stg_fnc_scripts.set_version_log_module_result_trace(
                task_properties,
                'usd-export',
                'complete'
            )
    else:
        utl_core.Log.set_module_warning_trace(
            'look-export',
            u'file="{}" is not available'.format(scene_file_path)
        )


def set_asset_geometry_uv_map_usd_export(task_properties):
    import lxresolver.operators as rsv_operators
    #
    import lxusd.fnc.exporters as usd_fnc_exporters
    #
    root = task_properties.get('dcc.root')
    workspace = 'publish'
    version = task_properties.get('version')
    #
    asset_geometry_rsv_query = rsv_operators.RsvAssetGeometryQuery(task_properties)
    # model geometry
    model_geometry_hi_usd_file_path = asset_geometry_rsv_query.get_usd_model_hi_file()
    # current geometry
    current_geometry_hi_usd_file_path = asset_geometry_rsv_query.get_usd_hi_file(
        workspace=workspace,
        version=version
    )
    # uv-map file
    geometry_usd_uv_map_file_path = asset_geometry_rsv_query.get_usd_uv_map_file(
        workspace=workspace,
        version=version
    )
    if geometry_usd_uv_map_file_path is not None:
        if model_geometry_hi_usd_file_path and current_geometry_hi_usd_file_path:
            if model_geometry_hi_usd_file_path != current_geometry_hi_usd_file_path:
                usd_fnc_exporters.GeometryUvMapExporter(
                    file_path=geometry_usd_uv_map_file_path,
                    root=root,
                    option=dict(
                        file_0=model_geometry_hi_usd_file_path,
                        file_1=current_geometry_hi_usd_file_path
                    )
                ).set_run()


def set_asset_geometry_uv_map_usd_link_export(task_properties):
    import lxresolver.operators as rsv_operators
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    version = task_properties.get('version')
    #
    asset_geometry_rsv_query = rsv_operators.RsvAssetGeometryQuery(task_properties)
    # uv-map file
    surface_geometry_usd_uv_map_file_path = asset_geometry_rsv_query.get_usd_surface_uv_map_file()
    if surface_geometry_usd_uv_map_file_path:
        current_geometry_usd_uv_map_file_path = asset_geometry_rsv_query.get_usd_uv_map_file(
            version=version
        )
        utl_dcc_objects.OsFile(current_geometry_usd_uv_map_file_path).set_directory_create()
        utl_dcc_objects.OsFile(surface_geometry_usd_uv_map_file_path).set_link_to(
            current_geometry_usd_uv_map_file_path, force=True
        )


def set_asset_usd_set_export(task_properties):
    import os
    #
    import fnmatch
    #
    from lxbasic import bsc_core
    #
    import lxutil.objects as utl_objects
    #
    import lxresolver.operators as rsv_operators
    #
    branch = task_properties.get('branch')
    if branch == 'asset':
        step = task_properties.get('step')
        if step in ['mod', 'srf']:
            task = task_properties.get('task')
            version = task_properties.get('version')
            #
            asset_look_rsv_query = rsv_operators.RsvAssetLookQuery(task_properties)
            asset_usd_rsv_query = rsv_operators.RsvAssetUsdQuery(task_properties)
            #
            look_klf_file_path = asset_look_rsv_query.get_klf_file(
                version=version
            )
            # usd-geometry-uv-map
            geometry_usd_uv_map_file_path = asset_usd_rsv_query.get_geometry_uv_map_look_file(
                version=version
            )
            # usd-look
            look_usd_file_path = asset_usd_rsv_query.get_look_file(
                version=version
            )
            look_properties_file_dict = asset_usd_rsv_query.get_look_properties_file_dict(
                version=version
            )
            element_names = bsc_core.ZipFileOpt(look_klf_file_path).get_element_names()
            look_pass_names = [os.path.splitext(i)[0] for i in fnmatch.filter(element_names, '*.klf')]
            if look_pass_names:
                utl_objects.DotUsdaFile(
                    file_path=look_usd_file_path
                ).set_surface_look_write(
                    look_root_name='look',
                    look_pass_name=look_pass_names[0],
                    look_pass_names=look_pass_names,
                    look_file_path=look_klf_file_path,
                    look_properties_file_dict=look_properties_file_dict
                )
            #
            usd_registry_file_path = asset_usd_rsv_query.get_registry_file(
                version=version
            )
            utl_objects.DotUsdaFile(
                file_path=usd_registry_file_path
            ).set_surface_registry_write(
                look_file_path=look_usd_file_path,
                uv_map_file_path=geometry_usd_uv_map_file_path,
            )
            #
            if task in ['modeling', 'surfacing', 'srf_anishading', 'srf_cfxshading']:
                # noinspection PyUnresolvedReferences
                import production.gen.record_set_registry as pgs
                pgs.run(usd_registry_file_path)

