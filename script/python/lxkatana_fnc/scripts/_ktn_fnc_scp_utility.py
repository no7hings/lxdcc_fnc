# coding:utf-8


def set_asset_workspace_create(rsv_task_properties, use_preview_look_pass=True):
    import os
    #
    import fnmatch
    #
    from lxbasic import bsc_core
    #
    from lxutil import utl_core
    #
    import lxresolver.operators as rsv_operators
    #
    import lxkatana.fnc.builders as ktn_fnc_builders
    #
    import lxkatana.fnc.importers as ktn_fnc_importers
    #
    branch = rsv_task_properties.get('branch')
    root = rsv_task_properties.get('dcc.root')
    if branch == 'asset':
        rsv_asset_look_query = rsv_operators.RsvAssetLookQuery(rsv_task_properties)
        current_look_ass_file_path = rsv_asset_look_query.get_ass_file()
        if current_look_ass_file_path:
            ktn_workspace = ktn_fnc_builders.AssetWorkspaceBuilder()
            ktn_workspace.set_workspace_create()
            # geometry
            rsv_asset_geometry_query = rsv_operators.RsvAssetGeometryQuery(rsv_task_properties)
            # model
            current_geometry_usd_hi_file_path = rsv_asset_geometry_query.get_usd_hi_file()
            if current_geometry_usd_hi_file_path:
                ktn_workspace.set_geometry_usd_import(current_geometry_usd_hi_file_path)
            # groom
            groom_geometry_xgen_file_args = rsv_asset_geometry_query.get_xgen_file_args()
            if groom_geometry_xgen_file_args:
                for i_groom_geometry_xgen_file_path, i_groom_geometry_xgen_extend_variants in groom_geometry_xgen_file_args:
                    ktn_workspace.set_geometry_xgen_import(
                        i_groom_geometry_xgen_file_path,
                        i_groom_geometry_xgen_extend_variants
                    )
            # groom_geometry_usd_file_path = rsv_operators.RsvAssetUsdQuery(rsv_task_properties).get_groom_registry_file()
            # if groom_geometry_usd_file_path:
            #     ktn_workspace.set_groom_geometry_usd_import(groom_geometry_usd_file_path)
            # geometry-effect
            effect_geometry_usd_file_path = rsv_operators.RsvAssetUsdQuery(rsv_task_properties).get_effect_registry_file()
            if effect_geometry_usd_file_path:
                ktn_workspace.set_effect_usd_import(effect_geometry_usd_file_path)
            # default pass
            ktn_fnc_importers.LookAssImporter(
                file_path=current_look_ass_file_path,
                root='/root/materials',
            ).set_run()
            # other passes
            look_pass_names = []
            if use_preview_look_pass is True:
                look_yml__surface_anm__file_path = rsv_asset_look_query.get_yml_surface_anm_file()
                if look_yml__surface_anm__file_path is not None:
                    look_pass_names = ktn_fnc_importers.LookYamlImporter(
                        option=dict(
                            file=look_yml__surface_anm__file_path,
                            root=root
                        )
                    ).get_pass_names()
            else:
                look_klf_file_path = rsv_asset_look_query.get_klf_file()
                element_names = bsc_core.StorageZipFileOpt(look_klf_file_path).get_element_names()
                look_pass_names = [os.path.splitext(i)[0] for i in fnmatch.filter(element_names, '*.klf')]
            #
            if look_pass_names:
                g_p = utl_core.GuiProgressesRunner(maximum=len(look_pass_names))
                for i_look_pass_name in look_pass_names:
                    g_p.set_update()
                    #
                    if i_look_pass_name != 'default':
                        ktn_workspace.set_pass_add(i_look_pass_name)
                        i_look_ass_file_path = rsv_asset_look_query.get_ass_sub_file(
                            look_pass=i_look_pass_name
                        )
                        if i_look_ass_file_path:
                            ktn_fnc_importers.LookAssImporter(
                                file_path=i_look_ass_file_path,
                                root='/root/materials',
                                option=dict(
                                    look_pass=i_look_pass_name
                                )
                            ).set_run()
                #
                g_p.set_stop()
            return True
        else:
            utl_core.Log.set_module_warning_trace(
                'katana-scene-create',
                u'file="{}" is non-exists'.format(current_look_ass_file_path)
            )


def set_asset_cfx_look_workspace_create(rsv_task_properties):
    from lxutil import utl_core
    #
    import lxresolver.operators as rsv_operators
    #
    import lxkatana.fnc.builders as ktn_fnc_builders
    #
    import lxkatana.fnc.importers as ktn_fnc_importers
    #
    branch = rsv_task_properties.get('branch')
    root = rsv_task_properties.get('dcc.root')
    if branch == 'asset':
        rsv_asset_look_query = rsv_operators.RsvAssetLookQuery(rsv_task_properties)
        look_ass__surface_anm__file_path = rsv_asset_look_query.get_ass_surface_anm_file()
        if look_ass__surface_anm__file_path:
            ktn_workspace = ktn_fnc_builders.AssetWorkspaceBuilder()
            ktn_workspace.set_workspace_create()
            # geometry
            rsv_asset_geometry_query = rsv_operators.RsvAssetGeometryQuery(rsv_task_properties)
            # geometry-model
            surface_geometry_usd_hi_file_path = rsv_asset_geometry_query.get_usd_surface_anm_hi_file()
            if surface_geometry_usd_hi_file_path:
                ktn_workspace.set_geometry_usd_import(surface_geometry_usd_hi_file_path)
            # geometry-groom
            groom_geometry_usd_file_path = rsv_operators.RsvAssetUsdQuery(rsv_task_properties).get_groom_registry_file()
            if groom_geometry_usd_file_path:
                ktn_workspace.set_groom_geometry_usd_import(groom_geometry_usd_file_path)
            # geometry-effect
            effect_geometry_usd_file_path = rsv_operators.RsvAssetUsdQuery(rsv_task_properties).get_effect_registry_file()
            if effect_geometry_usd_file_path:
                ktn_workspace.set_effect_usd_import(effect_geometry_usd_file_path)
            # default pass
            ktn_fnc_importers.LookAssImporter(
                file_path=look_ass__surface_anm__file_path,
                root='/root/materials',
                option=dict(
                    auto_occlusion_assign=True
                )
            ).set_run()
            # other passes
            look_yml__surface_anm__file_path = rsv_asset_look_query.get_yml_surface_anm_file()
            if look_yml__surface_anm__file_path is not None:
                look_pass_names = ktn_fnc_importers.LookYamlImporter(
                    option=dict(
                        file=look_yml__surface_anm__file_path,
                        root=root
                    )
                ).get_pass_names()
                if look_pass_names:
                    g_p = utl_core.GuiProgressesRunner(maximum=len(look_pass_names))
                    for i_look_pass_name in look_pass_names:
                        g_p.set_update()
                        #
                        if i_look_pass_name != 'default':
                            ktn_workspace.set_pass_add(i_look_pass_name)
                            i_look_ass__surface_anm__file_path = rsv_asset_look_query.get_ass_surface_anm_sub_file(
                                look_pass=i_look_pass_name
                            )
                            if i_look_ass__surface_anm__file_path:
                                ktn_fnc_importers.LookAssImporter(
                                    file_path=i_look_ass__surface_anm__file_path,
                                    root='/root/materials',
                                    option=dict(
                                        look_pass=i_look_pass_name,
                                        auto_occlusion_assign=True
                                    )
                                ).set_run()
                    #
                    g_p.set_stop()
            return True
        else:
            utl_core.Log.set_module_warning_trace(
                'katana-scene-create',
                u'file="{}" is non-exists'.format(look_ass__surface_anm__file_path)
            )


def set_work_look_ass_import(rsv_task_properties):
    from lxutil import utl_core
    #
    import lxutil.dcc.dcc_objects as utl_dcc_objects
    #
    import lxresolver.operators as rsv_operators
    #
    import lxkatana.fnc.importers as ktn_fnc_importers
    #
    work_look_ass_file_path = rsv_operators.RsvAssetLookQuery(rsv_task_properties).get_ass_work_file()
    #
    work_look_ass_file_obj = utl_dcc_objects.OsFile(work_look_ass_file_path)
    if work_look_ass_file_obj.get_is_exists() is True:
        ktn_fnc_importers.LookAssImporter(
            file_path=work_look_ass_file_path,
            root='/root/materials',
        ).set_run()
    else:
        utl_core.Log.set_module_warning_trace(
            'work-look-ass-import',
            'file="{}" is non-exists'.format(work_look_ass_file_path)
        )
