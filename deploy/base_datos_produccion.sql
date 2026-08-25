--
-- PostgreSQL database dump
--

\restrict kl6gpaCcvscOtvyCykTRz3q27oK5i6xmmenyIMvZblcYlCBixnUTDbxf24Up1eR

-- Dumped from database version 15.19
-- Dumped by pg_dump version 15.19

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE ONLY public.tickets_tickethistorial DROP CONSTRAINT tickets_tickethistorial_usuario_id_f0162cb5_fk_auth_user_id;
ALTER TABLE ONLY public.tickets_tickethistorial DROP CONSTRAINT tickets_tickethistorial_ticket_id_f4c39ded_fk_tickets_ticket_id;
ALTER TABLE ONLY public.tickets_ticket DROP CONSTRAINT tickets_ticket_solicitante_id_f155a8aa_fk_core_funcionario_id;
ALTER TABLE ONLY public.tickets_ticket DROP CONSTRAINT tickets_ticket_responsable_id_2e8d6597_fk_auth_user_id;
ALTER TABLE ONLY public.tickets_ticket DROP CONSTRAINT tickets_ticket_prioridad_id_7052ab00_fk_tickets_prioridad_id;
ALTER TABLE ONLY public.tickets_ticket DROP CONSTRAINT tickets_ticket_grupo_resolutor_id_1d35bb40_fk_tickets_g;
ALTER TABLE ONLY public.tickets_ticket DROP CONSTRAINT tickets_ticket_creador_id_b29e7e91_fk_auth_user_id;
ALTER TABLE ONLY public.tickets_ticket DROP CONSTRAINT tickets_ticket_categoria_id_0a1509bc_fk_tickets_categoria_id;
ALTER TABLE ONLY public.tickets_ticket DROP CONSTRAINT tickets_ticket_activo_id_c0497af8_fk_equipos_equipo_id;
ALTER TABLE ONLY public.tickets_notificacion DROP CONSTRAINT tickets_notificacion_usuario_id_3017c800_fk_auth_user_id;
ALTER TABLE ONLY public.tickets_notificacion DROP CONSTRAINT tickets_notificacion_ticket_id_cc82fb37_fk_tickets_ticket_id;
ALTER TABLE ONLY public.tickets_gruporesolutor_miembros DROP CONSTRAINT tickets_gruporesolut_user_id_1de6fdb9_fk_auth_user;
ALTER TABLE ONLY public.tickets_gruporesolutor_miembros DROP CONSTRAINT tickets_gruporesolut_gruporesolutor_id_df61e9b2_fk_tickets_g;
ALTER TABLE ONLY public.tickets_categoria DROP CONSTRAINT tickets_categoria_grupo_resolutor_id_55a94ded_fk_tickets_g;
ALTER TABLE ONLY public.tickets_archivoadjunto DROP CONSTRAINT tickets_archivoadjunto_ticket_id_89a738fe_fk_tickets_ticket_id;
ALTER TABLE ONLY public.tickets_archivoadjunto DROP CONSTRAINT tickets_archivoadjunto_subido_por_id_402143c0_fk_auth_user_id;
ALTER TABLE ONLY public.sla_slamatrix DROP CONSTRAINT sla_slamatrix_prioridad_id_7f7e1282_fk_tickets_prioridad_id;
ALTER TABLE ONLY public.redes_rangoip DROP CONSTRAINT redes_rangoip_piso_id_b2e65b73_fk_mantenedores_piso_id;
ALTER TABLE ONLY public.redes_pma DROP CONSTRAINT redes_pma_unidad_id_47dfdda1_fk_mantenedores_unidad_id;
ALTER TABLE ONLY public.redes_pma DROP CONSTRAINT redes_pma_edificio_piso_id_129d60bc_fk_mantenedores_piso_id;
ALTER TABLE ONLY public.redes_infraestructurared DROP CONSTRAINT redes_infraestructurared_pma_id_8c72b949_fk_redes_pma_id;
ALTER TABLE ONLY public.redes_infraestructurared DROP CONSTRAINT redes_infraestructur_vlan_id_d8834ba1_fk_mantenedo;
ALTER TABLE ONLY public.redes_infraestructurared DROP CONSTRAINT redes_infraestructur_unidad_id_46ee0fc9_fk_mantenedo;
ALTER TABLE ONLY public.redes_infraestructurared DROP CONSTRAINT redes_infraestructur_piso_id_96f56333_fk_mantenedo;
ALTER TABLE ONLY public.redes_infraestructurared DROP CONSTRAINT redes_infraestructur_institucion_id_9536b04f_fk_mantenedo;
ALTER TABLE ONLY public.redes_infraestructurared DROP CONSTRAINT redes_infraestructur_edificio_id_6743fa40_fk_mantenedo;
ALTER TABLE ONLY public.mantenedores_unidad DROP CONSTRAINT mantenedores_unidad_area_hospitalaria_id_9d70b06d_fk_mantenedo;
ALTER TABLE ONLY public.mantenedores_sector DROP CONSTRAINT mantenedores_sector_piso_id_5f130301_fk_mantenedores_piso_id;
ALTER TABLE ONLY public.mantenedores_recinto DROP CONSTRAINT mantenedores_recinto_unidad_id_875c2be4_fk_mantenedo;
ALTER TABLE ONLY public.mantenedores_recinto DROP CONSTRAINT mantenedores_recinto_sector_id_b4acf0c4_fk_mantenedo;
ALTER TABLE ONLY public.mantenedores_recinto DROP CONSTRAINT mantenedores_recinto_piso_id_297e1edf_fk_mantenedores_piso_id;
ALTER TABLE ONLY public.mantenedores_pma DROP CONSTRAINT mantenedores_pma_recinto_id_a42887d5_fk_mantenedores_recinto_id;
ALTER TABLE ONLY public.mantenedores_piso DROP CONSTRAINT mantenedores_piso_edificio_id_621ed362_fk_mantenedo;
ALTER TABLE ONLY public.mantenedores_modeloanexo DROP CONSTRAINT mantenedores_modeloa_marca_id_8855e9b9_fk_mantenedo;
ALTER TABLE ONLY public.mantenedores_modelo DROP CONSTRAINT mantenedores_modelo_marca_id_ab5df5a3_fk_mantenedores_marca_id;
ALTER TABLE ONLY public.mantenedores_edificio DROP CONSTRAINT mantenedores_edifici_institucion_id_18ca541d_fk_mantenedo;
ALTER TABLE ONLY public.equipos_equipo DROP CONSTRAINT equipos_equipo_so_id_c3e85b7b_fk_mantenedo;
ALTER TABLE ONLY public.equipos_equipo DROP CONSTRAINT equipos_equipo_proveedor_id_2c9fca71_fk_mantenedo;
ALTER TABLE ONLY public.equipos_equipo DROP CONSTRAINT equipos_equipo_pma_id_cd63491b_fk_mantenedores_pma_id;
ALTER TABLE ONLY public.equipos_equipo DROP CONSTRAINT equipos_equipo_modificado_por_id_f3676570_fk_auth_user_id;
ALTER TABLE ONLY public.equipos_equipo DROP CONSTRAINT equipos_equipo_modelo_id_1aeb07be_fk_mantenedores_modelo_id;
ALTER TABLE ONLY public.equipos_equipo DROP CONSTRAINT equipos_equipo_marca_id_f40af6dd_fk_mantenedores_marca_id;
ALTER TABLE ONLY public.equipos_equipo DROP CONSTRAINT equipos_equipo_estado_id_56fb76ff_fk_mantenedo;
ALTER TABLE ONLY public.equipos_equipo DROP CONSTRAINT equipos_equipo_articulo_id_8503937b_fk_mantenedores_articulo_id;
ALTER TABLE ONLY public.equipos_bitacoraopcion DROP CONSTRAINT equipos_bitacoraopcion_creado_por_id_6f47db54_fk_auth_user_id;
ALTER TABLE ONLY public.equipos_bitacoraequipo DROP CONSTRAINT equipos_bitacoraequipo_tecnico_id_e0b7c38a_fk_auth_user_id;
ALTER TABLE ONLY public.equipos_bitacoraequipo DROP CONSTRAINT equipos_bitacoraequipo_equipo_id_a0f57a1d_fk_equipos_equipo_id;
ALTER TABLE ONLY public.equipos_bitacoraequipo DROP CONSTRAINT equipos_bitacoraequi_solicitante_id_f5b2c848_fk_core_func;
ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id;
ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co;
ALTER TABLE ONLY public.correos_miembrogrupocorreo DROP CONSTRAINT correos_miembrogrupo_grupo_id_05325d71_fk_correos_g;
ALTER TABLE ONLY public.correos_correolog DROP CONSTRAINT correos_correolog_ticket_id_1790aa94_fk_tickets_ticket_id;
ALTER TABLE ONLY public.core_perfilusuario DROP CONSTRAINT core_perfilusuario_user_id_f33b9be3_fk_auth_user_id;
ALTER TABLE ONLY public.core_perfilusuario DROP CONSTRAINT core_perfilusuario_rol_id_dd0e25c8_fk_core_rol_id;
ALTER TABLE ONLY public.core_funcionario DROP CONSTRAINT core_funcionario_unidad_id_151a2b97_fk_mantenedores_unidad_id;
ALTER TABLE ONLY public.core_funcionario DROP CONSTRAINT core_funcionario_cargo_id_43291cdf_fk_mantenedores_cargo_id;
ALTER TABLE ONLY public.conocimiento_articuloconocimiento DROP CONSTRAINT conocimiento_articul_categoria_id_2331dc21_fk_conocimie;
ALTER TABLE ONLY public.axes_accessattemptexpiration DROP CONSTRAINT axes_accessattemptex_access_attempt_id_6b73a47a_fk_axes_acce;
ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id;
ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm;
ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id;
ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id;
ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
ALTER TABLE ONLY public.anexos_requerimientocambio DROP CONSTRAINT anexos_requerimientocambio_anexo_id_0e4ade28_fk_anexos_anexo_id;
ALTER TABLE ONLY public.anexos_anexo DROP CONSTRAINT anexos_anexo_unidad_id_cd2392a1_fk_mantenedores_unidad_id;
ALTER TABLE ONLY public.anexos_anexo DROP CONSTRAINT anexos_anexo_proveedor_id_358de8b5_fk_mantenedores_proveedor_id;
ALTER TABLE ONLY public.anexos_anexo DROP CONSTRAINT anexos_anexo_pma_id_b62bc2ba_fk_mantenedores_pma_id;
ALTER TABLE ONLY public.anexos_anexo DROP CONSTRAINT anexos_anexo_piso_id_d0bd0bc3_fk_mantenedores_piso_id;
ALTER TABLE ONLY public.anexos_anexo DROP CONSTRAINT anexos_anexo_modelo_anexo_id_1ce2338e_fk_mantenedo;
ALTER TABLE ONLY public.anexos_anexo DROP CONSTRAINT anexos_anexo_establecimiento_id_9d0fc07f_fk_mantenedo;
ALTER TABLE ONLY public.anexos_anexo DROP CONSTRAINT anexos_anexo_edificio_id_b9966609_fk_mantenedores_edificio_id;
ALTER TABLE ONLY public.anexos_anexo DROP CONSTRAINT anexos_anexo_creado_por_id_ea30cea2_fk_auth_user_id;
ALTER TABLE ONLY public.anexos_anexo DROP CONSTRAINT anexos_anexo_actualizado_por_id_f880f1ee_fk_auth_user_id;
ALTER TABLE ONLY public.actas_actadetalle DROP CONSTRAINT actas_actadetalle_unidad_id_4650aec0_fk_mantenedores_unidad_id;
ALTER TABLE ONLY public.actas_actadetalle DROP CONSTRAINT actas_actadetalle_piso_id_89ab3dd4_fk_mantenedores_piso_id;
ALTER TABLE ONLY public.actas_actadetalle DROP CONSTRAINT actas_actadetalle_edificio_id_1cb35d69_fk_mantenedo;
ALTER TABLE ONLY public.actas_actadetalle DROP CONSTRAINT actas_actadetalle_acta_id_73ddccab_fk_actas_acta_id;
ALTER TABLE ONLY public.actas_acta DROP CONSTRAINT actas_acta_encargado_id_285fabdc_fk_auth_user_id;
DROP INDEX public.visor_avisovisor_activo_b8721d10;
DROP INDEX public.utilidades_webapp_orden_7ff09a20;
DROP INDEX public.utilidades_webapp_nombre_e54f006d_like;
DROP INDEX public.utilidades_webapp_activo_031f3575;
DROP INDEX public.utilidades_pendiente_estado_0b3d1b98_like;
DROP INDEX public.utilidades_pendiente_estado_0b3d1b98;
DROP INDEX public.utilidades_checklistitem_orden_d93b2bc4;
DROP INDEX public.utilidades_checklistitem_activo_83f20ce1;
DROP INDEX public.utilidades_ayudarapida_titulo_6a589184_like;
DROP INDEX public.utilidades_ayudarapida_orden_bd4f41db;
DROP INDEX public.utilidades_ayudarapida_activo_6efa7b5f;
DROP INDEX public.tickets_tickethistorial_usuario_id_f0162cb5;
DROP INDEX public.tickets_tickethistorial_ticket_id_f4c39ded;
DROP INDEX public.tickets_ticket_solicitante_id_f155a8aa;
DROP INDEX public.tickets_ticket_responsable_id_2e8d6597;
DROP INDEX public.tickets_ticket_prioridad_id_7052ab00;
DROP INDEX public.tickets_ticket_grupo_resolutor_id_1d35bb40;
DROP INDEX public.tickets_ticket_creador_id_b29e7e91;
DROP INDEX public.tickets_ticket_correlativo_24ab8235_like;
DROP INDEX public.tickets_ticket_categoria_id_0a1509bc;
DROP INDEX public.tickets_ticket_activo_id_c0497af8;
DROP INDEX public.tickets_notificacion_usuario_id_3017c800;
DROP INDEX public.tickets_notificacion_ticket_id_cc82fb37;
DROP INDEX public.tickets_gruporesolutor_nombre_8e80652d_like;
DROP INDEX public.tickets_gruporesolutor_miembros_user_id_1de6fdb9;
DROP INDEX public.tickets_gruporesolutor_miembros_gruporesolutor_id_df61e9b2;
DROP INDEX public.tickets_categoria_grupo_resolutor_id_55a94ded;
DROP INDEX public.tickets_archivoadjunto_ticket_id_89a738fe;
DROP INDEX public.tickets_archivoadjunto_subido_por_id_402143c0;
DROP INDEX public.sla_slamatrix_prioridad_id_7f7e1282;
DROP INDEX public.redes_slaconfiguracion_activo_c29b1f63;
DROP INDEX public.redes_rangoip_piso_id_b2e65b73;
DROP INDEX public.redes_pma_unidad_id_47dfdda1;
DROP INDEX public.redes_pma_edificio_piso_id_129d60bc;
DROP INDEX public.redes_infraestructurared_vlan_id_d8834ba1;
DROP INDEX public.redes_infraestructurared_unidad_id_46ee0fc9;
DROP INDEX public.redes_infraestructurared_pma_id_8c72b949;
DROP INDEX public.redes_infraestructurared_piso_id_96f56333;
DROP INDEX public.redes_infraestructurared_institucion_id_9536b04f;
DROP INDEX public.redes_infraestructurared_estado_f16e86cf_like;
DROP INDEX public.redes_infraestructurared_estado_f16e86cf;
DROP INDEX public.redes_infraestructurared_edificio_id_6743fa40;
DROP INDEX public.mantenedores_vlan_nombre_a6704d49_like;
DROP INDEX public.mantenedores_vlan_activo_ea991839;
DROP INDEX public.mantenedores_unidad_area_hospitalaria_id_9d70b06d;
DROP INDEX public.mantenedores_unidad_activo_192414b9;
DROP INDEX public.mantenedores_sistemaoperativo_nombre_4c56e3e0_like;
DROP INDEX public.mantenedores_sistemaoperativo_activo_40a0c433;
DROP INDEX public.mantenedores_sector_piso_id_5f130301;
DROP INDEX public.mantenedores_sector_activo_ea5fc6c2;
DROP INDEX public.mantenedores_recinto_unidad_id_875c2be4;
DROP INDEX public.mantenedores_recinto_sector_id_b4acf0c4;
DROP INDEX public.mantenedores_recinto_piso_id_297e1edf;
DROP INDEX public.mantenedores_recinto_activo_08f773d8;
DROP INDEX public.mantenedores_proveedor_nombre_928de492_like;
DROP INDEX public.mantenedores_proveedor_activo_15465790;
DROP INDEX public.mantenedores_pma_recinto_id_a42887d5;
DROP INDEX public.mantenedores_pma_nombre_0288ea10_like;
DROP INDEX public.mantenedores_pma_activo_284d1f0f;
DROP INDEX public.mantenedores_piso_edificio_id_621ed362;
DROP INDEX public.mantenedores_piso_activo_690af811;
DROP INDEX public.mantenedores_modeloanexo_nombre_f4e991b0_like;
DROP INDEX public.mantenedores_modeloanexo_marca_id_8855e9b9;
DROP INDEX public.mantenedores_modeloanexo_activo_b27b2328;
DROP INDEX public.mantenedores_modelo_marca_id_ab5df5a3;
DROP INDEX public.mantenedores_modelo_activo_907cf0cd;
DROP INDEX public.mantenedores_marca_nombre_4799ada7_like;
DROP INDEX public.mantenedores_marca_activo_60f4c907;
DROP INDEX public.mantenedores_institucion_nombre_67b9b150_like;
DROP INDEX public.mantenedores_institucion_codigo_29d8552d_like;
DROP INDEX public.mantenedores_institucion_activo_de228f00;
DROP INDEX public.mantenedores_estadoequipo_nombre_492f21b4_like;
DROP INDEX public.mantenedores_estadoequipo_activo_89b4f79a;
DROP INDEX public.mantenedores_edificio_institucion_id_18ca541d;
DROP INDEX public.mantenedores_edificio_activo_a097f0fa;
DROP INDEX public.mantenedores_cargo_nombre_172da254_like;
DROP INDEX public.mantenedores_cargo_activo_fb5bae30;
DROP INDEX public.mantenedores_articulo_nombre_36f12c71_like;
DROP INDEX public.mantenedores_articulo_activo_94601add;
DROP INDEX public.mantenedores_areahospitalaria_nombre_064f9fe2_like;
DROP INDEX public.mantenedores_areahospitalaria_activo_77ef0249;
DROP INDEX public.idx_rangoip_piso;
DROP INDEX public.idx_rangoip_ip;
DROP INDEX public.idx_log_tabla_reg;
DROP INDEX public.idx_log_ip;
DROP INDEX public.idx_ipred_pma;
DROP INDEX public.idx_ipred_estado;
DROP INDEX public.idx_equipo_pma;
DROP INDEX public.idx_bitacora_tipo;
DROP INDEX public.idx_bitacora_tecnico;
DROP INDEX public.idx_bitacora_equipo;
DROP INDEX public.idx_anexo_numero;
DROP INDEX public.idx_anexo_estado;
DROP INDEX public.idx_anexo_edificio;
DROP INDEX public.idx_actadetalle_tipo_item;
DROP INDEX public.idx_acta_fecha;
DROP INDEX public.idx_acta_estado;
DROP INDEX public.equipos_equipo_so_id_c3e85b7b;
DROP INDEX public.equipos_equipo_serial_number_1e24bd7f_like;
DROP INDEX public.equipos_equipo_proveedor_id_2c9fca71;
DROP INDEX public.equipos_equipo_pma_id_cd63491b;
DROP INDEX public.equipos_equipo_num_inventario_7fc34ab8_like;
DROP INDEX public.equipos_equipo_modificado_por_id_f3676570;
DROP INDEX public.equipos_equipo_modelo_id_1aeb07be;
DROP INDEX public.equipos_equipo_marca_id_f40af6dd;
DROP INDEX public.equipos_equipo_estado_id_56fb76ff;
DROP INDEX public.equipos_equipo_articulo_id_8503937b;
DROP INDEX public.equipos_equ_serial__26fea4_idx;
DROP INDEX public.equipos_equ_estado__598d3b_idx;
DROP INDEX public.equipos_bitacoraopcion_tipo_2dc40b92_like;
DROP INDEX public.equipos_bitacoraopcion_tipo_2dc40b92;
DROP INDEX public.equipos_bitacoraopcion_orden_be457f2f;
DROP INDEX public.equipos_bitacoraopcion_creado_por_id_6f47db54;
DROP INDEX public.equipos_bitacoraopcion_activo_8ff983fc;
DROP INDEX public.equipos_bitacoraequipo_tecnico_id_e0b7c38a;
DROP INDEX public.equipos_bitacoraequipo_solicitante_id_f5b2c848;
DROP INDEX public.equipos_bitacoraequipo_equipo_id_a0f57a1d;
DROP INDEX public.django_session_session_key_c0390e0f_like;
DROP INDEX public.django_session_expire_date_a5c62663;
DROP INDEX public.django_celery_results_taskresult_task_id_de0d95bf_like;
DROP INDEX public.django_celery_results_groupresult_group_id_a085f1a9_like;
DROP INDEX public.django_celery_results_chordcounter_group_id_1f70858c_like;
DROP INDEX public.django_cele_worker_d54dd8_idx;
DROP INDEX public.django_cele_task_na_08aec9_idx;
DROP INDEX public.django_cele_status_9b6201_idx;
DROP INDEX public.django_cele_periodi_1993cf_idx;
DROP INDEX public.django_cele_date_do_f59aad_idx;
DROP INDEX public.django_cele_date_do_caae0e_idx;
DROP INDEX public.django_cele_date_cr_f04a50_idx;
DROP INDEX public.django_cele_date_cr_bd6c1d_idx;
DROP INDEX public.django_admin_log_user_id_c564eba6;
DROP INDEX public.django_admin_log_content_type_id_c4bce8eb;
DROP INDEX public.correos_miembrogrupocorreo_grupo_id_05325d71;
DROP INDEX public.correos_grupocorreo_nombre_885175f6_like;
DROP INDEX public.correos_credencialcorreo_email_04588194_like;
DROP INDEX public.correos_correolog_ticket_id_1790aa94;
DROP INDEX public.correos_cor_ticket__551fd6_idx;
DROP INDEX public.correos_cor_estado_41c840_idx;
DROP INDEX public.core_rol_orden_b482695e;
DROP INDEX public.core_rol_nombre_766ba3b6_like;
DROP INDEX public.core_rol_activo_8ec146ad;
DROP INDEX public.core_perfilusuario_rut_13bd4ad0_like;
DROP INDEX public.core_perfilusuario_rol_id_dd0e25c8;
DROP INDEX public.core_logauditoria_usuario_929eb424_like;
DROP INDEX public.core_logauditoria_usuario_929eb424;
DROP INDEX public.core_logauditoria_tabla_f0cfb57f_like;
DROP INDEX public.core_logauditoria_tabla_f0cfb57f;
DROP INDEX public.core_logauditoria_registro_id_34747d4a_like;
DROP INDEX public.core_logauditoria_registro_id_34747d4a;
DROP INDEX public.core_logauditoria_fecha_registro_bdd4ceca;
DROP INDEX public.core_logauditoria_accion_473925e9_like;
DROP INDEX public.core_logauditoria_accion_473925e9;
DROP INDEX public.core_funcionario_unidad_id_151a2b97;
DROP INDEX public.core_funcionario_rut_6ce3638d_like;
DROP INDEX public.core_funcionario_cargo_id_43291cdf;
DROP INDEX public.conocimiento_categoriaconocimiento_nombre_fd098266_like;
DROP INDEX public.conocimiento_articuloconocimiento_categoria_id_2331dc21;
DROP INDEX public.axes_accesslog_username_df93064b_like;
DROP INDEX public.axes_accesslog_username_df93064b;
DROP INDEX public.axes_accesslog_user_agent_0e659004_like;
DROP INDEX public.axes_accesslog_user_agent_0e659004;
DROP INDEX public.axes_accesslog_ip_address_86b417e5;
DROP INDEX public.axes_accessfailurelog_username_a8b7e8a4_like;
DROP INDEX public.axes_accessfailurelog_username_a8b7e8a4;
DROP INDEX public.axes_accessfailurelog_user_agent_ea145dda_like;
DROP INDEX public.axes_accessfailurelog_user_agent_ea145dda;
DROP INDEX public.axes_accessfailurelog_ip_address_2e9f5a7f;
DROP INDEX public.axes_accessattempt_username_3f2d4ca0_like;
DROP INDEX public.axes_accessattempt_username_3f2d4ca0;
DROP INDEX public.axes_accessattempt_user_agent_ad89678b_like;
DROP INDEX public.axes_accessattempt_user_agent_ad89678b;
DROP INDEX public.axes_accessattempt_ip_address_10922d9c;
DROP INDEX public.auth_user_username_6821ab7c_like;
DROP INDEX public.auth_user_user_permissions_user_id_a95ead1b;
DROP INDEX public.auth_user_user_permissions_permission_id_1fbb5f2c;
DROP INDEX public.auth_user_groups_user_id_6a12ed8b;
DROP INDEX public.auth_user_groups_group_id_97559544;
DROP INDEX public.auth_permission_content_type_id_2f476e4b;
DROP INDEX public.auth_group_permissions_permission_id_84c5c92e;
DROP INDEX public.auth_group_permissions_group_id_b120cbf9;
DROP INDEX public.auth_group_name_a6ea08ec_like;
DROP INDEX public.anexos_requerimientocambio_anexo_id_0e4ade28;
DROP INDEX public.anexos_anexo_unidad_id_cd2392a1;
DROP INDEX public.anexos_anexo_serial_number_0e9f324c_like;
DROP INDEX public.anexos_anexo_proveedor_id_358de8b5;
DROP INDEX public.anexos_anexo_pma_id_b62bc2ba;
DROP INDEX public.anexos_anexo_piso_id_d0bd0bc3;
DROP INDEX public.anexos_anexo_numero_anexo_bc584d6f_like;
DROP INDEX public.anexos_anexo_modelo_anexo_id_1ce2338e;
DROP INDEX public.anexos_anexo_estado_bb9fa0d9_like;
DROP INDEX public.anexos_anexo_estado_bb9fa0d9;
DROP INDEX public.anexos_anexo_establecimiento_id_9d0fc07f;
DROP INDEX public.anexos_anexo_edificio_id_b9966609;
DROP INDEX public.anexos_anexo_creado_por_id_ea30cea2;
DROP INDEX public.anexos_anexo_actualizado_por_id_f880f1ee;
DROP INDEX public.actas_actadetalle_unidad_id_4650aec0;
DROP INDEX public.actas_actadetalle_piso_id_89ab3dd4;
DROP INDEX public.actas_actadetalle_edificio_id_1cb35d69;
DROP INDEX public.actas_actadetalle_acta_id_73ddccab;
DROP INDEX public.actas_acta_estado_e12ae8fb_like;
DROP INDEX public.actas_acta_estado_e12ae8fb;
DROP INDEX public.actas_acta_encargado_id_285fabdc;
DROP INDEX public.actas_acta_codigo_2760a1b3_like;
ALTER TABLE ONLY public.visor_avisovisor DROP CONSTRAINT visor_avisovisor_pkey;
ALTER TABLE ONLY public.utilidades_webapp DROP CONSTRAINT utilidades_webapp_pkey;
ALTER TABLE ONLY public.utilidades_webapp DROP CONSTRAINT utilidades_webapp_nombre_key;
ALTER TABLE ONLY public.utilidades_pendiente DROP CONSTRAINT utilidades_pendiente_pkey;
ALTER TABLE ONLY public.utilidades_checklistitem DROP CONSTRAINT utilidades_checklistitem_pkey;
ALTER TABLE ONLY public.utilidades_ayudarapida DROP CONSTRAINT utilidades_ayudarapida_titulo_key;
ALTER TABLE ONLY public.utilidades_ayudarapida DROP CONSTRAINT utilidades_ayudarapida_pkey;
ALTER TABLE ONLY public.redes_pma DROP CONSTRAINT uniq_pma_codigo_piso;
ALTER TABLE ONLY public.mantenedores_piso DROP CONSTRAINT uniq_piso_edificio_nombre;
ALTER TABLE ONLY public.mantenedores_modelo DROP CONSTRAINT uniq_modelo_marca_nombre;
ALTER TABLE ONLY public.correos_miembrogrupocorreo DROP CONSTRAINT uniq_miembro_grupo_email;
ALTER TABLE ONLY public.mantenedores_edificio DROP CONSTRAINT uniq_edificio_nombre_institucion;
ALTER TABLE ONLY public.equipos_bitacoraopcion DROP CONSTRAINT uniq_bitacora_opcion_tipo_nombre;
ALTER TABLE ONLY public.tickets_tickethistorial DROP CONSTRAINT tickets_tickethistorial_pkey;
ALTER TABLE ONLY public.tickets_ticket DROP CONSTRAINT tickets_ticket_pkey;
ALTER TABLE ONLY public.tickets_ticket DROP CONSTRAINT tickets_ticket_correlativo_key;
ALTER TABLE ONLY public.tickets_prioridad DROP CONSTRAINT tickets_prioridad_pkey;
ALTER TABLE ONLY public.tickets_notificacion DROP CONSTRAINT tickets_notificacion_pkey;
ALTER TABLE ONLY public.tickets_gruporesolutor DROP CONSTRAINT tickets_gruporesolutor_pkey;
ALTER TABLE ONLY public.tickets_gruporesolutor DROP CONSTRAINT tickets_gruporesolutor_nombre_key;
ALTER TABLE ONLY public.tickets_gruporesolutor_miembros DROP CONSTRAINT tickets_gruporesolutor_miembros_pkey;
ALTER TABLE ONLY public.tickets_gruporesolutor_miembros DROP CONSTRAINT tickets_gruporesolutor_m_gruporesolutor_id_user_i_bf921b40_uniq;
ALTER TABLE ONLY public.tickets_categoria DROP CONSTRAINT tickets_categoria_pkey;
ALTER TABLE ONLY public.tickets_archivoadjunto DROP CONSTRAINT tickets_archivoadjunto_pkey;
ALTER TABLE ONLY public.sla_slamatrix DROP CONSTRAINT sla_slamatrix_pkey;
ALTER TABLE ONLY public.sla_slamatrix DROP CONSTRAINT sla_slamatrix_impacto_urgencia_5bc9bf0b_uniq;
ALTER TABLE ONLY public.redes_slaconfiguracion DROP CONSTRAINT redes_slaconfiguracion_pkey;
ALTER TABLE ONLY public.redes_rangoip DROP CONSTRAINT redes_rangoip_pkey;
ALTER TABLE ONLY public.redes_pma DROP CONSTRAINT redes_pma_pkey;
ALTER TABLE ONLY public.redes_infraestructurared DROP CONSTRAINT redes_infraestructurared_pkey;
ALTER TABLE ONLY public.redes_infraestructurared DROP CONSTRAINT redes_infraestructurared_ip_direccion_key;
ALTER TABLE ONLY public.mantenedores_vlan DROP CONSTRAINT mantenedores_vlan_pkey;
ALTER TABLE ONLY public.mantenedores_vlan DROP CONSTRAINT mantenedores_vlan_nombre_key;
ALTER TABLE ONLY public.mantenedores_unidad DROP CONSTRAINT mantenedores_unidad_pkey;
ALTER TABLE ONLY public.mantenedores_sistemaoperativo DROP CONSTRAINT mantenedores_sistemaoperativo_pkey;
ALTER TABLE ONLY public.mantenedores_sistemaoperativo DROP CONSTRAINT mantenedores_sistemaoperativo_nombre_key;
ALTER TABLE ONLY public.mantenedores_sector DROP CONSTRAINT mantenedores_sector_pkey;
ALTER TABLE ONLY public.mantenedores_recinto DROP CONSTRAINT mantenedores_recinto_pkey;
ALTER TABLE ONLY public.mantenedores_proveedor DROP CONSTRAINT mantenedores_proveedor_pkey;
ALTER TABLE ONLY public.mantenedores_proveedor DROP CONSTRAINT mantenedores_proveedor_nombre_key;
ALTER TABLE ONLY public.mantenedores_pma DROP CONSTRAINT mantenedores_pma_pkey;
ALTER TABLE ONLY public.mantenedores_pma DROP CONSTRAINT mantenedores_pma_nombre_key;
ALTER TABLE ONLY public.mantenedores_piso DROP CONSTRAINT mantenedores_piso_pkey;
ALTER TABLE ONLY public.mantenedores_modeloanexo DROP CONSTRAINT mantenedores_modeloanexo_pkey;
ALTER TABLE ONLY public.mantenedores_modeloanexo DROP CONSTRAINT mantenedores_modeloanexo_nombre_key;
ALTER TABLE ONLY public.mantenedores_modelo DROP CONSTRAINT mantenedores_modelo_pkey;
ALTER TABLE ONLY public.mantenedores_marca DROP CONSTRAINT mantenedores_marca_pkey;
ALTER TABLE ONLY public.mantenedores_marca DROP CONSTRAINT mantenedores_marca_nombre_key;
ALTER TABLE ONLY public.mantenedores_institucion DROP CONSTRAINT mantenedores_institucion_pkey;
ALTER TABLE ONLY public.mantenedores_institucion DROP CONSTRAINT mantenedores_institucion_nombre_key;
ALTER TABLE ONLY public.mantenedores_institucion DROP CONSTRAINT mantenedores_institucion_codigo_key;
ALTER TABLE ONLY public.mantenedores_estadoequipo DROP CONSTRAINT mantenedores_estadoequipo_pkey;
ALTER TABLE ONLY public.mantenedores_estadoequipo DROP CONSTRAINT mantenedores_estadoequipo_nombre_key;
ALTER TABLE ONLY public.mantenedores_edificio DROP CONSTRAINT mantenedores_edificio_pkey;
ALTER TABLE ONLY public.mantenedores_cargo DROP CONSTRAINT mantenedores_cargo_pkey;
ALTER TABLE ONLY public.mantenedores_cargo DROP CONSTRAINT mantenedores_cargo_nombre_key;
ALTER TABLE ONLY public.mantenedores_articulo DROP CONSTRAINT mantenedores_articulo_pkey;
ALTER TABLE ONLY public.mantenedores_articulo DROP CONSTRAINT mantenedores_articulo_nombre_key;
ALTER TABLE ONLY public.mantenedores_areahospitalaria DROP CONSTRAINT mantenedores_areahospitalaria_pkey;
ALTER TABLE ONLY public.mantenedores_areahospitalaria DROP CONSTRAINT mantenedores_areahospitalaria_nombre_key;
ALTER TABLE ONLY public.equipos_equipo DROP CONSTRAINT equipos_equipo_serial_number_key;
ALTER TABLE ONLY public.equipos_equipo DROP CONSTRAINT equipos_equipo_pkey;
ALTER TABLE ONLY public.equipos_equipo DROP CONSTRAINT equipos_equipo_num_inventario_key;
ALTER TABLE ONLY public.equipos_bitacoraopcion DROP CONSTRAINT equipos_bitacoraopcion_pkey;
ALTER TABLE ONLY public.equipos_bitacoraequipo DROP CONSTRAINT equipos_bitacoraequipo_pkey;
ALTER TABLE ONLY public.django_session DROP CONSTRAINT django_session_pkey;
ALTER TABLE ONLY public.django_migrations DROP CONSTRAINT django_migrations_pkey;
ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_pkey;
ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq;
ALTER TABLE ONLY public.django_celery_results_taskresult DROP CONSTRAINT django_celery_results_taskresult_task_id_key;
ALTER TABLE ONLY public.django_celery_results_taskresult DROP CONSTRAINT django_celery_results_taskresult_pkey;
ALTER TABLE ONLY public.django_celery_results_groupresult DROP CONSTRAINT django_celery_results_groupresult_pkey;
ALTER TABLE ONLY public.django_celery_results_groupresult DROP CONSTRAINT django_celery_results_groupresult_group_id_key;
ALTER TABLE ONLY public.django_celery_results_chordcounter DROP CONSTRAINT django_celery_results_chordcounter_pkey;
ALTER TABLE ONLY public.django_celery_results_chordcounter DROP CONSTRAINT django_celery_results_chordcounter_group_id_key;
ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_pkey;
ALTER TABLE ONLY public.correos_miembrogrupocorreo DROP CONSTRAINT correos_miembrogrupocorreo_pkey;
ALTER TABLE ONLY public.correos_grupocorreo DROP CONSTRAINT correos_grupocorreo_pkey;
ALTER TABLE ONLY public.correos_grupocorreo DROP CONSTRAINT correos_grupocorreo_nombre_key;
ALTER TABLE ONLY public.correos_credencialcorreo DROP CONSTRAINT correos_credencialcorreo_pkey;
ALTER TABLE ONLY public.correos_credencialcorreo DROP CONSTRAINT correos_credencialcorreo_email_key;
ALTER TABLE ONLY public.correos_correolog DROP CONSTRAINT correos_correolog_pkey;
ALTER TABLE ONLY public.correos_configuracionsmtp DROP CONSTRAINT correos_configuracionsmtp_pkey;
ALTER TABLE ONLY public.core_rol DROP CONSTRAINT core_rol_pkey;
ALTER TABLE ONLY public.core_rol DROP CONSTRAINT core_rol_nombre_key;
ALTER TABLE ONLY public.core_perfilusuario DROP CONSTRAINT core_perfilusuario_user_id_key;
ALTER TABLE ONLY public.core_perfilusuario DROP CONSTRAINT core_perfilusuario_rut_key;
ALTER TABLE ONLY public.core_perfilusuario DROP CONSTRAINT core_perfilusuario_pkey;
ALTER TABLE ONLY public.core_logauditoria DROP CONSTRAINT core_logauditoria_pkey;
ALTER TABLE ONLY public.core_funcionario DROP CONSTRAINT core_funcionario_rut_key;
ALTER TABLE ONLY public.core_funcionario DROP CONSTRAINT core_funcionario_pkey;
ALTER TABLE ONLY public.conocimiento_categoriaconocimiento DROP CONSTRAINT conocimiento_categoriaconocimiento_pkey;
ALTER TABLE ONLY public.conocimiento_categoriaconocimiento DROP CONSTRAINT conocimiento_categoriaconocimiento_nombre_key;
ALTER TABLE ONLY public.conocimiento_articuloconocimiento DROP CONSTRAINT conocimiento_articuloconocimiento_pkey;
ALTER TABLE ONLY public.axes_accesslog DROP CONSTRAINT axes_accesslog_pkey;
ALTER TABLE ONLY public.axes_accessfailurelog DROP CONSTRAINT axes_accessfailurelog_pkey;
ALTER TABLE ONLY public.axes_accessattemptexpiration DROP CONSTRAINT axes_accessattemptexpiration_pkey;
ALTER TABLE ONLY public.axes_accessattempt DROP CONSTRAINT axes_accessattempt_username_ip_address_user_agent_8ea22282_uniq;
ALTER TABLE ONLY public.axes_accessattempt DROP CONSTRAINT axes_accessattempt_pkey;
ALTER TABLE ONLY public.auth_user DROP CONSTRAINT auth_user_username_key;
ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq;
ALTER TABLE ONLY public.auth_user_user_permissions DROP CONSTRAINT auth_user_user_permissions_pkey;
ALTER TABLE ONLY public.auth_user DROP CONSTRAINT auth_user_pkey;
ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq;
ALTER TABLE ONLY public.auth_user_groups DROP CONSTRAINT auth_user_groups_pkey;
ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_pkey;
ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq;
ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_pkey;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_pkey;
ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_name_key;
ALTER TABLE ONLY public.anexos_requerimientocambio DROP CONSTRAINT anexos_requerimientocambio_pkey;
ALTER TABLE ONLY public.anexos_anexo DROP CONSTRAINT anexos_anexo_serial_number_key;
ALTER TABLE ONLY public.anexos_anexo DROP CONSTRAINT anexos_anexo_pkey;
ALTER TABLE ONLY public.anexos_anexo DROP CONSTRAINT anexos_anexo_numero_anexo_key;
ALTER TABLE ONLY public.actas_actadetalle DROP CONSTRAINT actas_actadetalle_pkey;
ALTER TABLE ONLY public.actas_acta DROP CONSTRAINT actas_acta_pkey;
ALTER TABLE ONLY public.actas_acta DROP CONSTRAINT actas_acta_codigo_key;
DROP TABLE public.visor_avisovisor;
DROP TABLE public.utilidades_webapp;
DROP TABLE public.utilidades_pendiente;
DROP TABLE public.utilidades_checklistitem;
DROP TABLE public.utilidades_ayudarapida;
DROP TABLE public.tickets_tickethistorial;
DROP TABLE public.tickets_ticket;
DROP TABLE public.tickets_prioridad;
DROP TABLE public.tickets_notificacion;
DROP TABLE public.tickets_gruporesolutor_miembros;
DROP TABLE public.tickets_gruporesolutor;
DROP TABLE public.tickets_categoria;
DROP TABLE public.tickets_archivoadjunto;
DROP TABLE public.sla_slamatrix;
DROP TABLE public.redes_slaconfiguracion;
DROP TABLE public.redes_rangoip;
DROP TABLE public.redes_pma;
DROP TABLE public.redes_infraestructurared;
DROP TABLE public.mantenedores_vlan;
DROP TABLE public.mantenedores_unidad;
DROP TABLE public.mantenedores_sistemaoperativo;
DROP TABLE public.mantenedores_sector;
DROP TABLE public.mantenedores_recinto;
DROP TABLE public.mantenedores_proveedor;
DROP TABLE public.mantenedores_pma;
DROP TABLE public.mantenedores_piso;
DROP TABLE public.mantenedores_modeloanexo;
DROP TABLE public.mantenedores_modelo;
DROP TABLE public.mantenedores_marca;
DROP TABLE public.mantenedores_institucion;
DROP TABLE public.mantenedores_estadoequipo;
DROP TABLE public.mantenedores_edificio;
DROP TABLE public.mantenedores_cargo;
DROP TABLE public.mantenedores_articulo;
DROP TABLE public.mantenedores_areahospitalaria;
DROP TABLE public.equipos_equipo;
DROP TABLE public.equipos_bitacoraopcion;
DROP TABLE public.equipos_bitacoraequipo;
DROP TABLE public.django_session;
DROP TABLE public.django_migrations;
DROP TABLE public.django_content_type;
DROP TABLE public.django_celery_results_taskresult;
DROP TABLE public.django_celery_results_groupresult;
DROP TABLE public.django_celery_results_chordcounter;
DROP TABLE public.django_admin_log;
DROP TABLE public.correos_miembrogrupocorreo;
DROP TABLE public.correos_grupocorreo;
DROP TABLE public.correos_credencialcorreo;
DROP TABLE public.correos_correolog;
DROP TABLE public.correos_configuracionsmtp;
DROP TABLE public.core_rol;
DROP TABLE public.core_perfilusuario;
DROP TABLE public.core_logauditoria;
DROP TABLE public.core_funcionario;
DROP TABLE public.conocimiento_categoriaconocimiento;
DROP TABLE public.conocimiento_articuloconocimiento;
DROP TABLE public.axes_accesslog;
DROP TABLE public.axes_accessfailurelog;
DROP TABLE public.axes_accessattemptexpiration;
DROP TABLE public.axes_accessattempt;
DROP TABLE public.auth_user_user_permissions;
DROP TABLE public.auth_user_groups;
DROP TABLE public.auth_user;
DROP TABLE public.auth_permission;
DROP TABLE public.auth_group_permissions;
DROP TABLE public.auth_group;
DROP TABLE public.anexos_requerimientocambio;
DROP TABLE public.anexos_anexo;
DROP TABLE public.actas_actadetalle;
DROP TABLE public.actas_acta;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: actas_acta; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.actas_acta (
    id bigint NOT NULL,
    codigo character varying(20) NOT NULL,
    receptor_nombre character varying(100) NOT NULL,
    receptor_rut character varying(20),
    receptor_cargo character varying(100),
    receptor_unidad character varying(100),
    observaciones text,
    fecha timestamp with time zone NOT NULL,
    pdf_generado character varying(100),
    pdf_firmado character varying(100),
    firma_receptor character varying(100),
    firma_encargado character varying(100),
    timbre_encargado character varying(100),
    email_receptor character varying(254),
    estado character varying(20) NOT NULL,
    fecha_envio timestamp with time zone,
    encargado_id integer NOT NULL
);


ALTER TABLE public.actas_acta OWNER TO ticsystem_admin;

--
-- Name: actas_acta_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.actas_acta ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.actas_acta_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: actas_actadetalle; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.actas_actadetalle (
    id bigint NOT NULL,
    tipo_item character varying(20) NOT NULL,
    id_item integer NOT NULL,
    articulo character varying(100),
    serie character varying(100),
    pma_lugar character varying(255),
    estado character varying(255),
    acta_id bigint NOT NULL,
    edificio_id bigint,
    piso_id bigint,
    unidad_id bigint,
    CONSTRAINT actas_actadetalle_id_item_check CHECK ((id_item >= 0))
);


ALTER TABLE public.actas_actadetalle OWNER TO ticsystem_admin;

--
-- Name: actas_actadetalle_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.actas_actadetalle ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.actas_actadetalle_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: anexos_anexo; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.anexos_anexo (
    id bigint NOT NULL,
    numero_anexo character varying(50) NOT NULL,
    marca character varying(50) NOT NULL,
    modelo character varying(50) NOT NULL,
    estado character varying(20) NOT NULL,
    serial_number character varying(100) NOT NULL,
    ip inet,
    comentario text,
    foto character varying(100),
    grupo character varying(50),
    creado_en timestamp with time zone NOT NULL,
    actualizado_en timestamp with time zone NOT NULL,
    actualizado_por_id integer,
    creado_por_id integer,
    edificio_id bigint,
    establecimiento_id bigint,
    modelo_anexo_id bigint,
    piso_id bigint,
    proveedor_id bigint,
    unidad_id bigint,
    pma_id bigint,
    numero_inventario character varying(50)
);


ALTER TABLE public.anexos_anexo OWNER TO ticsystem_admin;

--
-- Name: anexos_anexo_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.anexos_anexo ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.anexos_anexo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: anexos_requerimientocambio; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.anexos_requerimientocambio (
    id bigint NOT NULL,
    tipo character varying(100),
    sub_requerimiento character varying(100),
    accion character varying(100),
    nombre_usuario_req character varying(100),
    ubicacion_req character varying(100),
    estado_req character varying(100),
    grupo_captura character varying(100),
    cambiar_dos_anexos boolean NOT NULL,
    numero_anexo_cambio character varying(50),
    cascada boolean NOT NULL,
    observacion text,
    fecha timestamp with time zone NOT NULL,
    anexo_id bigint NOT NULL
);


ALTER TABLE public.anexos_requerimientocambio OWNER TO ticsystem_admin;

--
-- Name: anexos_requerimientocambio_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.anexos_requerimientocambio ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.anexos_requerimientocambio_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO ticsystem_admin;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO ticsystem_admin;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO ticsystem_admin;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO ticsystem_admin;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO ticsystem_admin;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.auth_user_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.auth_user ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO ticsystem_admin;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.auth_user_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: axes_accessattempt; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.axes_accessattempt (
    id integer NOT NULL,
    user_agent character varying(255) NOT NULL,
    ip_address inet,
    username character varying(255),
    http_accept character varying(1025) NOT NULL,
    path_info character varying(255) NOT NULL,
    attempt_time timestamp with time zone NOT NULL,
    get_data text NOT NULL,
    post_data text NOT NULL,
    failures_since_start integer NOT NULL,
    CONSTRAINT axes_accessattempt_failures_since_start_check CHECK ((failures_since_start >= 0))
);


ALTER TABLE public.axes_accessattempt OWNER TO ticsystem_admin;

--
-- Name: axes_accessattempt_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.axes_accessattempt ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.axes_accessattempt_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: axes_accessattemptexpiration; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.axes_accessattemptexpiration (
    access_attempt_id integer NOT NULL,
    expires_at timestamp with time zone NOT NULL
);


ALTER TABLE public.axes_accessattemptexpiration OWNER TO ticsystem_admin;

--
-- Name: axes_accessfailurelog; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.axes_accessfailurelog (
    id integer NOT NULL,
    user_agent character varying(255) NOT NULL,
    ip_address inet,
    username character varying(255),
    http_accept character varying(1025) NOT NULL,
    path_info character varying(255) NOT NULL,
    attempt_time timestamp with time zone NOT NULL,
    locked_out boolean NOT NULL
);


ALTER TABLE public.axes_accessfailurelog OWNER TO ticsystem_admin;

--
-- Name: axes_accessfailurelog_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.axes_accessfailurelog ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.axes_accessfailurelog_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: axes_accesslog; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.axes_accesslog (
    id integer NOT NULL,
    user_agent character varying(255) NOT NULL,
    ip_address inet,
    username character varying(255),
    http_accept character varying(1025) NOT NULL,
    path_info character varying(255) NOT NULL,
    attempt_time timestamp with time zone NOT NULL,
    logout_time timestamp with time zone,
    session_hash character varying(64) NOT NULL
);


ALTER TABLE public.axes_accesslog OWNER TO ticsystem_admin;

--
-- Name: axes_accesslog_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.axes_accesslog ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.axes_accesslog_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: conocimiento_articuloconocimiento; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.conocimiento_articuloconocimiento (
    id bigint NOT NULL,
    titulo character varying(200) NOT NULL,
    sintomas text NOT NULL,
    solucion text NOT NULL,
    es_error_conocido boolean NOT NULL,
    creado_en timestamp with time zone NOT NULL,
    actualizado_en timestamp with time zone NOT NULL,
    categoria_id bigint
);


ALTER TABLE public.conocimiento_articuloconocimiento OWNER TO ticsystem_admin;

--
-- Name: conocimiento_articuloconocimiento_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.conocimiento_articuloconocimiento ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.conocimiento_articuloconocimiento_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: conocimiento_categoriaconocimiento; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.conocimiento_categoriaconocimiento (
    id bigint NOT NULL,
    nombre character varying(100) NOT NULL
);


ALTER TABLE public.conocimiento_categoriaconocimiento OWNER TO ticsystem_admin;

--
-- Name: conocimiento_categoriaconocimiento_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.conocimiento_categoriaconocimiento ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.conocimiento_categoriaconocimiento_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: core_funcionario; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.core_funcionario (
    id bigint NOT NULL,
    rut character varying(20) NOT NULL,
    nombres character varying(150) NOT NULL,
    apellidos character varying(150) NOT NULL,
    correo character varying(150),
    cargo_id bigint,
    fecha_registro timestamp with time zone NOT NULL,
    unidad_id bigint,
    cargo_old character varying(100)
);


ALTER TABLE public.core_funcionario OWNER TO ticsystem_admin;

--
-- Name: core_funcionario_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.core_funcionario ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.core_funcionario_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: core_logauditoria; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.core_logauditoria (
    id bigint NOT NULL,
    usuario character varying(150),
    accion character varying(10) NOT NULL,
    tabla character varying(100) NOT NULL,
    registro_id character varying(100),
    detalles text NOT NULL,
    ip_address inet,
    fecha_registro timestamp with time zone NOT NULL
);


ALTER TABLE public.core_logauditoria OWNER TO ticsystem_admin;

--
-- Name: core_logauditoria_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.core_logauditoria ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.core_logauditoria_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: core_perfilusuario; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.core_perfilusuario (
    id bigint NOT NULL,
    unidad character varying(100) NOT NULL,
    cargo character varying(100) NOT NULL,
    grado character varying(20) NOT NULL,
    rut character varying(20) NOT NULL,
    telefono character varying(20),
    foto character varying(100),
    fecha_registro timestamp with time zone NOT NULL,
    user_id integer NOT NULL,
    rol_id bigint
);


ALTER TABLE public.core_perfilusuario OWNER TO ticsystem_admin;

--
-- Name: core_perfilusuario_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.core_perfilusuario ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.core_perfilusuario_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: core_rol; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.core_rol (
    id bigint NOT NULL,
    nombre character varying(80) NOT NULL,
    descripcion character varying(255),
    permisos jsonb NOT NULL,
    activo boolean NOT NULL,
    orden integer NOT NULL,
    creado_por character varying(120),
    actualizado_por character varying(120),
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL,
    icono character varying(50),
    is_system boolean NOT NULL
);


ALTER TABLE public.core_rol OWNER TO ticsystem_admin;

--
-- Name: core_rol_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.core_rol ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.core_rol_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: correos_configuracionsmtp; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.correos_configuracionsmtp (
    id bigint NOT NULL,
    host character varying(150) NOT NULL,
    puerto integer NOT NULL,
    usuario character varying(150),
    password character varying(255),
    use_tls boolean NOT NULL,
    remitente_por_defecto character varying(254),
    fecha_actualizacion timestamp with time zone NOT NULL
);


ALTER TABLE public.correos_configuracionsmtp OWNER TO ticsystem_admin;

--
-- Name: correos_configuracionsmtp_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.correos_configuracionsmtp ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.correos_configuracionsmtp_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: correos_correolog; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.correos_correolog (
    id bigint NOT NULL,
    tipo character varying(20) NOT NULL,
    destinatario character varying(254) NOT NULL,
    asunto character varying(255) NOT NULL,
    estado character varying(10) NOT NULL,
    intentos smallint NOT NULL,
    error_detalle text NOT NULL,
    reenviado_manualmente boolean NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_ultimo_intento timestamp with time zone,
    ticket_id bigint,
    CONSTRAINT correos_correolog_intentos_check CHECK ((intentos >= 0))
);


ALTER TABLE public.correos_correolog OWNER TO ticsystem_admin;

--
-- Name: correos_correolog_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.correos_correolog ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.correos_correolog_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: correos_credencialcorreo; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.correos_credencialcorreo (
    id bigint NOT NULL,
    email character varying(254) NOT NULL,
    propietario character varying(150),
    departamento character varying(100),
    activo boolean NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL
);


ALTER TABLE public.correos_credencialcorreo OWNER TO ticsystem_admin;

--
-- Name: correos_credencialcorreo_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.correos_credencialcorreo ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.correos_credencialcorreo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: correos_grupocorreo; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.correos_grupocorreo (
    id bigint NOT NULL,
    nombre character varying(120) NOT NULL,
    descripcion character varying(255),
    orden integer NOT NULL,
    activo boolean NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL
);


ALTER TABLE public.correos_grupocorreo OWNER TO ticsystem_admin;

--
-- Name: correos_grupocorreo_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.correos_grupocorreo ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.correos_grupocorreo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: correos_miembrogrupocorreo; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.correos_miembrogrupocorreo (
    id bigint NOT NULL,
    email character varying(254) NOT NULL,
    grupo_id bigint NOT NULL
);


ALTER TABLE public.correos_miembrogrupocorreo OWNER TO ticsystem_admin;

--
-- Name: correos_miembrogrupocorreo_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.correos_miembrogrupocorreo ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.correos_miembrogrupocorreo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO ticsystem_admin;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_celery_results_chordcounter; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.django_celery_results_chordcounter (
    id integer NOT NULL,
    group_id character varying(255) NOT NULL,
    sub_tasks text NOT NULL,
    count integer NOT NULL,
    CONSTRAINT django_celery_results_chordcounter_count_check CHECK ((count >= 0))
);


ALTER TABLE public.django_celery_results_chordcounter OWNER TO ticsystem_admin;

--
-- Name: django_celery_results_chordcounter_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.django_celery_results_chordcounter ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_celery_results_chordcounter_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_celery_results_groupresult; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.django_celery_results_groupresult (
    id integer NOT NULL,
    group_id character varying(255) NOT NULL,
    date_created timestamp with time zone NOT NULL,
    date_done timestamp with time zone NOT NULL,
    content_type character varying(128) NOT NULL,
    content_encoding character varying(64) NOT NULL,
    result text
);


ALTER TABLE public.django_celery_results_groupresult OWNER TO ticsystem_admin;

--
-- Name: django_celery_results_groupresult_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.django_celery_results_groupresult ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_celery_results_groupresult_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_celery_results_taskresult; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.django_celery_results_taskresult (
    id integer NOT NULL,
    task_id character varying(255) NOT NULL,
    status character varying(50) NOT NULL,
    content_type character varying(128) NOT NULL,
    content_encoding character varying(64) NOT NULL,
    result text,
    date_done timestamp with time zone NOT NULL,
    traceback text,
    meta text,
    task_args text,
    task_kwargs text,
    task_name character varying(255),
    worker character varying(100),
    date_created timestamp with time zone NOT NULL,
    periodic_task_name character varying(255),
    date_started timestamp with time zone
);


ALTER TABLE public.django_celery_results_taskresult OWNER TO ticsystem_admin;

--
-- Name: django_celery_results_taskresult_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.django_celery_results_taskresult ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_celery_results_taskresult_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO ticsystem_admin;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO ticsystem_admin;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO ticsystem_admin;

--
-- Name: equipos_bitacoraequipo; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.equipos_bitacoraequipo (
    id bigint NOT NULL,
    fecha_mantenimiento timestamp with time zone NOT NULL,
    fecha_devolucion timestamp with time zone,
    solicitante_id bigint,
    falla_reportada text,
    actividades_realizadas text,
    servicio_unidad character varying(100),
    tipo_registro character varying(30) NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    tecnico_id integer NOT NULL,
    equipo_id bigint NOT NULL
);


ALTER TABLE public.equipos_bitacoraequipo OWNER TO ticsystem_admin;

--
-- Name: equipos_bitacoraequipo_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.equipos_bitacoraequipo ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.equipos_bitacoraequipo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: equipos_bitacoraopcion; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.equipos_bitacoraopcion (
    id bigint NOT NULL,
    tipo character varying(20) NOT NULL,
    nombre character varying(255) NOT NULL,
    activo boolean NOT NULL,
    orden integer NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL,
    creado_por_id integer
);


ALTER TABLE public.equipos_bitacoraopcion OWNER TO ticsystem_admin;

--
-- Name: equipos_bitacoraopcion_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.equipos_bitacoraopcion ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.equipos_bitacoraopcion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: equipos_equipo; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.equipos_equipo (
    id bigint NOT NULL,
    imagen character varying(100),
    correlativo character varying(50),
    orden_interno integer,
    serie_corta character varying(100),
    estado_candado character varying(100),
    serial_number character varying(100),
    ip inet,
    anexo character varying(50),
    usuario character varying(150),
    office character varying(100),
    activador character varying(150),
    pmalugar character varying(100),
    comentario text,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_modificacion timestamp with time zone NOT NULL,
    articulo_id bigint NOT NULL,
    estado_id bigint NOT NULL,
    marca_id bigint NOT NULL,
    modelo_id bigint NOT NULL,
    modificado_por_id integer,
    pma_id bigint,
    proveedor_id bigint,
    so_id bigint,
    fecha_compra date,
    mac_address character varying(100),
    orden_compra character varying(100),
    patch_panel character varying(100),
    puerto_red character varying(50),
    switch_ip character varying(100),
    vencimiento_garantia date,
    num_inventario character varying(80)
);


ALTER TABLE public.equipos_equipo OWNER TO ticsystem_admin;

--
-- Name: equipos_equipo_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.equipos_equipo ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.equipos_equipo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mantenedores_areahospitalaria; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.mantenedores_areahospitalaria (
    id bigint NOT NULL,
    activo boolean NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL,
    nombre character varying(150) NOT NULL
);


ALTER TABLE public.mantenedores_areahospitalaria OWNER TO ticsystem_admin;

--
-- Name: mantenedores_areahospitalaria_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.mantenedores_areahospitalaria ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mantenedores_areahospitalaria_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mantenedores_articulo; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.mantenedores_articulo (
    id bigint NOT NULL,
    activo boolean NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL,
    nombre character varying(80) NOT NULL,
    imagen character varying(100)
);


ALTER TABLE public.mantenedores_articulo OWNER TO ticsystem_admin;

--
-- Name: mantenedores_articulo_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.mantenedores_articulo ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mantenedores_articulo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mantenedores_cargo; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.mantenedores_cargo (
    id bigint NOT NULL,
    activo boolean NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL,
    nombre character varying(150) NOT NULL
);


ALTER TABLE public.mantenedores_cargo OWNER TO ticsystem_admin;

--
-- Name: mantenedores_cargo_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.mantenedores_cargo ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mantenedores_cargo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mantenedores_edificio; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.mantenedores_edificio (
    id bigint NOT NULL,
    activo boolean NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL,
    nombre character varying(120) NOT NULL,
    institucion_id bigint
);


ALTER TABLE public.mantenedores_edificio OWNER TO ticsystem_admin;

--
-- Name: mantenedores_edificio_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.mantenedores_edificio ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mantenedores_edificio_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mantenedores_estadoequipo; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.mantenedores_estadoequipo (
    id bigint NOT NULL,
    activo boolean NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL,
    nombre character varying(80) NOT NULL,
    color_hex character varying(20) NOT NULL
);


ALTER TABLE public.mantenedores_estadoequipo OWNER TO ticsystem_admin;

--
-- Name: mantenedores_estadoequipo_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.mantenedores_estadoequipo ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mantenedores_estadoequipo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mantenedores_institucion; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.mantenedores_institucion (
    id bigint NOT NULL,
    activo boolean NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL,
    codigo character varying(20) NOT NULL,
    nombre character varying(150) NOT NULL
);


ALTER TABLE public.mantenedores_institucion OWNER TO ticsystem_admin;

--
-- Name: mantenedores_institucion_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.mantenedores_institucion ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mantenedores_institucion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mantenedores_marca; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.mantenedores_marca (
    id bigint NOT NULL,
    activo boolean NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL,
    nombre character varying(80) NOT NULL
);


ALTER TABLE public.mantenedores_marca OWNER TO ticsystem_admin;

--
-- Name: mantenedores_marca_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.mantenedores_marca ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mantenedores_marca_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mantenedores_modelo; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.mantenedores_modelo (
    id bigint NOT NULL,
    activo boolean NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL,
    nombre character varying(150) NOT NULL,
    imagen character varying(100),
    marca_id bigint NOT NULL
);


ALTER TABLE public.mantenedores_modelo OWNER TO ticsystem_admin;

--
-- Name: mantenedores_modelo_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.mantenedores_modelo ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mantenedores_modelo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mantenedores_modeloanexo; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.mantenedores_modeloanexo (
    id bigint NOT NULL,
    activo boolean NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL,
    nombre character varying(100) NOT NULL,
    imagen character varying(100),
    marca_id bigint
);


ALTER TABLE public.mantenedores_modeloanexo OWNER TO ticsystem_admin;

--
-- Name: mantenedores_modeloanexo_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.mantenedores_modeloanexo ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mantenedores_modeloanexo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mantenedores_piso; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.mantenedores_piso (
    id bigint NOT NULL,
    activo boolean NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL,
    nombre character varying(50) NOT NULL,
    alias character varying(50),
    edificio_id bigint NOT NULL
);


ALTER TABLE public.mantenedores_piso OWNER TO ticsystem_admin;

--
-- Name: mantenedores_piso_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.mantenedores_piso ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mantenedores_piso_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mantenedores_pma; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.mantenedores_pma (
    id bigint NOT NULL,
    activo boolean NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL,
    nombre character varying(50) NOT NULL,
    recinto_id bigint NOT NULL
);


ALTER TABLE public.mantenedores_pma OWNER TO ticsystem_admin;

--
-- Name: mantenedores_pma_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.mantenedores_pma ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mantenedores_pma_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mantenedores_proveedor; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.mantenedores_proveedor (
    id bigint NOT NULL,
    activo boolean NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL,
    nombre character varying(120) NOT NULL,
    contacto character varying(100),
    telefono character varying(50),
    email character varying(120),
    direccion character varying(255),
    rut character varying(12)
);


ALTER TABLE public.mantenedores_proveedor OWNER TO ticsystem_admin;

--
-- Name: mantenedores_proveedor_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.mantenedores_proveedor ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mantenedores_proveedor_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mantenedores_recinto; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.mantenedores_recinto (
    id bigint NOT NULL,
    activo boolean NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL,
    nombre character varying(150) NOT NULL,
    piso_id bigint,
    sector_id bigint,
    unidad_id bigint
);


ALTER TABLE public.mantenedores_recinto OWNER TO ticsystem_admin;

--
-- Name: mantenedores_recinto_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.mantenedores_recinto ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mantenedores_recinto_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mantenedores_sector; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.mantenedores_sector (
    id bigint NOT NULL,
    activo boolean NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL,
    nombre character varying(50) NOT NULL,
    piso_id bigint
);


ALTER TABLE public.mantenedores_sector OWNER TO ticsystem_admin;

--
-- Name: mantenedores_sector_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.mantenedores_sector ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mantenedores_sector_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mantenedores_sistemaoperativo; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.mantenedores_sistemaoperativo (
    id bigint NOT NULL,
    activo boolean NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL,
    nombre character varying(80) NOT NULL
);


ALTER TABLE public.mantenedores_sistemaoperativo OWNER TO ticsystem_admin;

--
-- Name: mantenedores_sistemaoperativo_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.mantenedores_sistemaoperativo ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mantenedores_sistemaoperativo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mantenedores_unidad; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.mantenedores_unidad (
    id bigint NOT NULL,
    activo boolean NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL,
    nombre character varying(150) NOT NULL,
    area_hospitalaria_id bigint
);


ALTER TABLE public.mantenedores_unidad OWNER TO ticsystem_admin;

--
-- Name: mantenedores_unidad_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.mantenedores_unidad ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mantenedores_unidad_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mantenedores_vlan; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.mantenedores_vlan (
    id bigint NOT NULL,
    activo boolean NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL,
    nombre character varying(50) NOT NULL,
    descripcion character varying(255)
);


ALTER TABLE public.mantenedores_vlan OWNER TO ticsystem_admin;

--
-- Name: mantenedores_vlan_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.mantenedores_vlan ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.mantenedores_vlan_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: redes_infraestructurared; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.redes_infraestructurared (
    id bigint NOT NULL,
    ip_direccion inet NOT NULL,
    switch_ip inet,
    switch_port character varying(20),
    estado character varying(20) NOT NULL,
    sector character varying(100),
    mac character varying(20),
    rack character varying(100),
    patch_panel character varying(100),
    edificio_id bigint,
    institucion_id bigint,
    piso_id bigint,
    unidad_id bigint,
    vlan_id bigint,
    pma_id bigint
);


ALTER TABLE public.redes_infraestructurared OWNER TO ticsystem_admin;

--
-- Name: redes_infraestructurared_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.redes_infraestructurared ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.redes_infraestructurared_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: redes_pma; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.redes_pma (
    id bigint NOT NULL,
    codigo character varying(50) NOT NULL,
    estado character varying(20) NOT NULL,
    descripcion text,
    edificio_piso_id bigint NOT NULL,
    unidad_id bigint
);


ALTER TABLE public.redes_pma OWNER TO ticsystem_admin;

--
-- Name: redes_pma_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.redes_pma ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.redes_pma_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: redes_rangoip; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.redes_rangoip (
    id bigint NOT NULL,
    unidad character varying(200) NOT NULL,
    ubicacion character varying(200) NOT NULL,
    pma character varying(100) NOT NULL,
    rack character varying(100) NOT NULL,
    dato character varying(100) NOT NULL,
    rango character varying(50) NOT NULL,
    ip inet NOT NULL,
    estado boolean NOT NULL,
    comentario text NOT NULL,
    piso_id bigint NOT NULL
);


ALTER TABLE public.redes_rangoip OWNER TO ticsystem_admin;

--
-- Name: redes_rangoip_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.redes_rangoip ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.redes_rangoip_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: redes_slaconfiguracion; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.redes_slaconfiguracion (
    id bigint NOT NULL,
    nombre character varying(120) NOT NULL,
    horas_objetivo integer NOT NULL,
    alerta_porcentaje integer NOT NULL,
    activo boolean NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL
);


ALTER TABLE public.redes_slaconfiguracion OWNER TO ticsystem_admin;

--
-- Name: redes_slaconfiguracion_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.redes_slaconfiguracion ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.redes_slaconfiguracion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: sla_slamatrix; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.sla_slamatrix (
    id bigint NOT NULL,
    impacto integer NOT NULL,
    urgencia integer NOT NULL,
    tiempo_respuesta_minutos integer NOT NULL,
    tiempo_resolucion_horas integer NOT NULL,
    prioridad_id bigint NOT NULL
);


ALTER TABLE public.sla_slamatrix OWNER TO ticsystem_admin;

--
-- Name: sla_slamatrix_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.sla_slamatrix ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.sla_slamatrix_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: tickets_archivoadjunto; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.tickets_archivoadjunto (
    id bigint NOT NULL,
    archivo character varying(100) NOT NULL,
    fecha_subida timestamp with time zone NOT NULL,
    subido_por_id integer NOT NULL,
    ticket_id bigint NOT NULL
);


ALTER TABLE public.tickets_archivoadjunto OWNER TO ticsystem_admin;

--
-- Name: tickets_archivoadjunto_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.tickets_archivoadjunto ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.tickets_archivoadjunto_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: tickets_categoria; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.tickets_categoria (
    id bigint NOT NULL,
    nombre character varying(100) NOT NULL,
    activa boolean NOT NULL,
    grupo_resolutor_id bigint
);


ALTER TABLE public.tickets_categoria OWNER TO ticsystem_admin;

--
-- Name: tickets_categoria_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.tickets_categoria ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.tickets_categoria_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: tickets_gruporesolutor; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.tickets_gruporesolutor (
    id bigint NOT NULL,
    nombre character varying(100) NOT NULL,
    descripcion text,
    activo boolean NOT NULL,
    icono character varying(50),
    is_system boolean NOT NULL
);


ALTER TABLE public.tickets_gruporesolutor OWNER TO ticsystem_admin;

--
-- Name: tickets_gruporesolutor_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.tickets_gruporesolutor ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.tickets_gruporesolutor_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: tickets_gruporesolutor_miembros; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.tickets_gruporesolutor_miembros (
    id bigint NOT NULL,
    gruporesolutor_id bigint NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.tickets_gruporesolutor_miembros OWNER TO ticsystem_admin;

--
-- Name: tickets_gruporesolutor_miembros_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.tickets_gruporesolutor_miembros ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.tickets_gruporesolutor_miembros_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: tickets_notificacion; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.tickets_notificacion (
    id bigint NOT NULL,
    mensaje character varying(255) NOT NULL,
    leida boolean NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    ticket_id bigint,
    usuario_id integer NOT NULL
);


ALTER TABLE public.tickets_notificacion OWNER TO ticsystem_admin;

--
-- Name: tickets_notificacion_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.tickets_notificacion ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.tickets_notificacion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: tickets_prioridad; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.tickets_prioridad (
    id bigint NOT NULL,
    nombre character varying(50) NOT NULL,
    sla_horas integer NOT NULL,
    color_hex character varying(20) NOT NULL
);


ALTER TABLE public.tickets_prioridad OWNER TO ticsystem_admin;

--
-- Name: tickets_prioridad_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.tickets_prioridad ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.tickets_prioridad_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: tickets_ticket; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.tickets_ticket (
    id bigint NOT NULL,
    correlativo character varying(20) NOT NULL,
    estado character varying(30) NOT NULL,
    descripcion text NOT NULL,
    diagnostico text,
    solucion text,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_asignacion timestamp with time zone,
    fecha_cierre timestamp with time zone,
    activo_id bigint,
    categoria_id bigint,
    prioridad_id bigint,
    responsable_id integer,
    solicitante_id bigint NOT NULL,
    creador_id integer,
    fecha_vencimiento_sla timestamp with time zone,
    impacto integer NOT NULL,
    tipo character varying(20) NOT NULL,
    urgencia integer NOT NULL,
    grupo_resolutor_id bigint,
    anexo_contacto character varying(50),
    correo_contacto character varying(150)
);


ALTER TABLE public.tickets_ticket OWNER TO ticsystem_admin;

--
-- Name: tickets_ticket_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.tickets_ticket ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.tickets_ticket_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: tickets_tickethistorial; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.tickets_tickethistorial (
    id bigint NOT NULL,
    accion character varying(255) NOT NULL,
    valor_anterior text,
    valor_nuevo text,
    comentario text,
    fecha timestamp with time zone NOT NULL,
    ticket_id bigint NOT NULL,
    usuario_id integer NOT NULL
);


ALTER TABLE public.tickets_tickethistorial OWNER TO ticsystem_admin;

--
-- Name: tickets_tickethistorial_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.tickets_tickethistorial ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.tickets_tickethistorial_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: utilidades_ayudarapida; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.utilidades_ayudarapida (
    id bigint NOT NULL,
    titulo character varying(200) NOT NULL,
    contenido text NOT NULL,
    categoria character varying(100),
    activo boolean NOT NULL,
    orden integer NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL
);


ALTER TABLE public.utilidades_ayudarapida OWNER TO ticsystem_admin;

--
-- Name: utilidades_ayudarapida_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.utilidades_ayudarapida ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.utilidades_ayudarapida_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: utilidades_checklistitem; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.utilidades_checklistitem (
    id bigint NOT NULL,
    task_name character varying(255) NOT NULL,
    is_completed boolean NOT NULL,
    activo boolean NOT NULL,
    orden integer NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL
);


ALTER TABLE public.utilidades_checklistitem OWNER TO ticsystem_admin;

--
-- Name: utilidades_checklistitem_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.utilidades_checklistitem ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.utilidades_checklistitem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: utilidades_pendiente; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.utilidades_pendiente (
    id bigint NOT NULL,
    titulo character varying(255) NOT NULL,
    link character varying(255) NOT NULL,
    estado character varying(20) NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_cierre timestamp with time zone,
    fecha_programada timestamp with time zone
);


ALTER TABLE public.utilidades_pendiente OWNER TO ticsystem_admin;

--
-- Name: utilidades_pendiente_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.utilidades_pendiente ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.utilidades_pendiente_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: utilidades_webapp; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.utilidades_webapp (
    id bigint NOT NULL,
    nombre character varying(180) NOT NULL,
    url character varying(200) NOT NULL,
    icono character varying(100) NOT NULL,
    descripcion character varying(255),
    activo boolean NOT NULL,
    orden integer NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL
);


ALTER TABLE public.utilidades_webapp OWNER TO ticsystem_admin;

--
-- Name: utilidades_webapp_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.utilidades_webapp ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.utilidades_webapp_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: visor_avisovisor; Type: TABLE; Schema: public; Owner: ticsystem_admin
--

CREATE TABLE public.visor_avisovisor (
    id bigint NOT NULL,
    titulo character varying(200) NOT NULL,
    mensaje text NOT NULL,
    activo boolean NOT NULL,
    fecha_creacion timestamp with time zone NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL
);


ALTER TABLE public.visor_avisovisor OWNER TO ticsystem_admin;

--
-- Name: visor_avisovisor_id_seq; Type: SEQUENCE; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE public.visor_avisovisor ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.visor_avisovisor_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: actas_acta; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.actas_acta (id, codigo, receptor_nombre, receptor_rut, receptor_cargo, receptor_unidad, observaciones, fecha, pdf_generado, pdf_firmado, firma_receptor, firma_encargado, timbre_encargado, email_receptor, estado, fecha_envio, encargado_id) FROM stdin;
\.


--
-- Data for Name: actas_actadetalle; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.actas_actadetalle (id, tipo_item, id_item, articulo, serie, pma_lugar, estado, acta_id, edificio_id, piso_id, unidad_id) FROM stdin;
\.


--
-- Data for Name: anexos_anexo; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.anexos_anexo (id, numero_anexo, marca, modelo, estado, serial_number, ip, comentario, foto, grupo, creado_en, actualizado_en, actualizado_por_id, creado_por_id, edificio_id, establecimiento_id, modelo_anexo_id, piso_id, proveedor_id, unidad_id, pma_id, numero_inventario) FROM stdin;
\.


--
-- Data for Name: anexos_requerimientocambio; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.anexos_requerimientocambio (id, tipo, sub_requerimiento, accion, nombre_usuario_req, ubicacion_req, estado_req, grupo_captura, cambiar_dos_anexos, numero_anexo_cambio, cascada, observacion, fecha, anexo_id) FROM stdin;
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.auth_group (id, name) FROM stdin;
1	Mesa de Ayuda
2	Técnicos Terreno
3	Super Administrador
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
1	3	1
2	3	2
3	3	3
4	3	4
5	3	5
6	3	6
7	3	7
8	3	8
9	3	9
10	3	10
11	3	11
12	3	12
13	3	13
14	3	14
15	3	15
16	3	16
17	3	17
18	3	18
19	3	19
20	3	20
21	3	21
22	3	22
23	3	23
24	3	24
25	3	25
26	3	26
27	3	27
28	3	28
29	3	29
30	3	30
31	3	31
32	3	32
33	3	33
34	3	34
35	3	35
36	3	36
37	3	37
38	3	38
39	3	39
40	3	40
41	3	41
42	3	42
43	3	43
44	3	44
45	3	45
46	3	46
47	3	47
48	3	48
49	3	49
50	3	50
51	3	51
52	3	52
53	3	53
54	3	54
55	3	55
56	3	56
57	3	57
58	3	58
59	3	59
60	3	60
61	3	61
62	3	62
63	3	63
64	3	64
65	3	65
66	3	66
67	3	67
68	3	68
69	3	69
70	3	70
71	3	71
72	3	72
73	3	73
74	3	74
75	3	75
76	3	76
77	3	77
78	3	78
79	3	79
80	3	80
81	3	81
82	3	82
83	3	83
84	3	84
85	3	85
86	3	86
87	3	87
88	3	88
89	3	89
90	3	90
91	3	91
92	3	92
93	3	93
94	3	94
95	3	95
96	3	96
97	3	97
98	3	98
99	3	99
100	3	100
101	3	101
102	3	102
103	3	103
104	3	104
105	3	105
106	3	106
107	3	107
108	3	108
109	3	109
110	3	110
111	3	111
112	3	112
113	3	113
114	3	114
115	3	115
116	3	116
117	3	117
118	3	118
119	3	119
120	3	120
121	3	121
122	3	122
123	3	123
124	3	124
125	3	125
126	3	126
127	3	127
128	3	128
129	3	129
130	3	130
131	3	131
132	3	132
133	3	133
134	3	134
135	3	135
136	3	136
137	3	137
138	3	138
139	3	139
140	3	140
141	3	141
142	3	142
143	3	143
144	3	144
145	3	145
146	3	146
147	3	147
148	3	148
149	3	149
150	3	150
151	3	151
152	3	152
153	3	153
154	3	154
155	3	155
156	3	156
157	3	157
158	3	158
159	3	159
160	3	160
161	3	161
162	3	162
163	3	163
164	3	164
165	3	165
166	3	166
167	3	167
168	3	168
169	3	169
170	3	170
171	3	171
172	3	172
173	3	173
174	3	174
175	3	175
176	3	176
177	3	177
178	3	178
179	3	179
180	3	180
181	3	181
182	3	182
183	3	183
184	3	184
185	3	185
186	3	186
187	3	187
188	3	188
189	3	189
190	3	190
191	3	191
192	3	192
193	3	193
194	3	194
195	3	195
196	3	196
197	3	197
198	3	198
199	3	199
200	3	200
201	3	201
202	3	202
203	3	203
204	3	204
205	3	205
206	3	206
207	3	207
208	3	208
209	3	209
210	3	210
211	3	211
212	3	212
213	3	213
214	3	214
215	3	215
216	3	216
217	3	217
218	3	218
219	3	219
220	3	220
221	3	221
222	3	222
223	3	223
224	3	224
225	3	225
226	3	226
227	3	227
228	3	228
229	3	229
230	3	230
231	3	231
232	3	232
233	3	233
234	3	234
235	3	235
236	3	236
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	3	add_permission
6	Can change permission	3	change_permission
7	Can delete permission	3	delete_permission
8	Can view permission	3	view_permission
9	Can add group	2	add_group
10	Can change group	2	change_group
11	Can delete group	2	delete_group
12	Can view group	2	view_group
13	Can add user	4	add_user
14	Can change user	4	change_user
15	Can delete user	4	delete_user
16	Can view user	4	view_user
17	Can add content type	5	add_contenttype
18	Can change content type	5	change_contenttype
19	Can delete content type	5	delete_contenttype
20	Can view content type	5	view_contenttype
21	Can add session	6	add_session
22	Can change session	6	change_session
23	Can delete session	6	delete_session
24	Can view session	6	view_session
25	Can add access attempt	7	add_accessattempt
26	Can change access attempt	7	change_accessattempt
27	Can delete access attempt	7	delete_accessattempt
28	Can view access attempt	7	view_accessattempt
29	Can add access log	10	add_accesslog
30	Can change access log	10	change_accesslog
31	Can delete access log	10	delete_accesslog
32	Can view access log	10	view_accesslog
33	Can add access failure	9	add_accessfailurelog
34	Can change access failure	9	change_accessfailurelog
35	Can delete access failure	9	delete_accessfailurelog
36	Can view access failure	9	view_accessfailurelog
37	Can add access attempt expiration	8	add_accessattemptexpiration
38	Can change access attempt expiration	8	change_accessattemptexpiration
39	Can delete access attempt expiration	8	delete_accessattemptexpiration
40	Can view access attempt expiration	8	view_accessattemptexpiration
41	Can add task result	13	add_taskresult
42	Can change task result	13	change_taskresult
43	Can delete task result	13	delete_taskresult
44	Can view task result	13	view_taskresult
45	Can add chord counter	11	add_chordcounter
46	Can change chord counter	11	change_chordcounter
47	Can delete chord counter	11	delete_chordcounter
48	Can view chord counter	11	view_chordcounter
49	Can add group result	12	add_groupresult
50	Can change group result	12	change_groupresult
51	Can delete group result	12	delete_groupresult
52	Can view group result	12	view_groupresult
53	Can add Rol	17	add_rol
54	Can change Rol	17	change_rol
55	Can delete Rol	17	delete_rol
56	Can view Rol	17	view_rol
57	Can add Log de AuditorÃ­a	15	add_logauditoria
58	Can change Log de AuditorÃ­a	15	change_logauditoria
59	Can delete Log de AuditorÃ­a	15	delete_logauditoria
60	Can view Log de AuditorÃ­a	15	view_logauditoria
61	Can add Perfil de Usuario	16	add_perfilusuario
62	Can change Perfil de Usuario	16	change_perfilusuario
63	Can delete Perfil de Usuario	16	delete_perfilusuario
64	Can view Perfil de Usuario	16	view_perfilusuario
65	Can add Funcionario	14	add_funcionario
66	Can change Funcionario	14	change_funcionario
67	Can delete Funcionario	14	delete_funcionario
68	Can view Funcionario	14	view_funcionario
69	Can add Área Hospitalaria	18	add_areahospitalaria
70	Can change Área Hospitalaria	18	change_areahospitalaria
71	Can delete Área Hospitalaria	18	delete_areahospitalaria
72	Can view Área Hospitalaria	18	view_areahospitalaria
73	Can add Artículo	19	add_articulo
74	Can change Artículo	19	change_articulo
75	Can delete Artículo	19	delete_articulo
76	Can view Artículo	19	view_articulo
77	Can add Estado de Equipo	22	add_estadoequipo
78	Can change Estado de Equipo	22	change_estadoequipo
79	Can delete Estado de Equipo	22	delete_estadoequipo
80	Can view Estado de Equipo	22	view_estadoequipo
81	Can add Institución	23	add_institucion
82	Can change Institución	23	change_institucion
83	Can delete Institución	23	delete_institucion
84	Can view Institución	23	view_institucion
85	Can add Marca	24	add_marca
86	Can change Marca	24	change_marca
87	Can delete Marca	24	delete_marca
88	Can view Marca	24	view_marca
89	Can add Modelo de Anexo	26	add_modeloanexo
90	Can change Modelo de Anexo	26	change_modeloanexo
91	Can delete Modelo de Anexo	26	delete_modeloanexo
92	Can view Modelo de Anexo	26	view_modeloanexo
93	Can add Proveedor	29	add_proveedor
94	Can change Proveedor	29	change_proveedor
95	Can delete Proveedor	29	delete_proveedor
96	Can view Proveedor	29	view_proveedor
97	Can add Sistema Operativo	32	add_sistemaoperativo
98	Can change Sistema Operativo	32	change_sistemaoperativo
99	Can delete Sistema Operativo	32	delete_sistemaoperativo
100	Can view Sistema Operativo	32	view_sistemaoperativo
101	Can add VLAN	34	add_vlan
102	Can change VLAN	34	change_vlan
103	Can delete VLAN	34	delete_vlan
104	Can view VLAN	34	view_vlan
105	Can add Edificio	21	add_edificio
106	Can change Edificio	21	change_edificio
107	Can delete Edificio	21	delete_edificio
108	Can view Edificio	21	view_edificio
109	Can add Modelo	25	add_modelo
110	Can change Modelo	25	change_modelo
111	Can delete Modelo	25	delete_modelo
112	Can view Modelo	25	view_modelo
113	Can add Piso	27	add_piso
114	Can change Piso	27	change_piso
115	Can delete Piso	27	delete_piso
116	Can view Piso	27	view_piso
117	Can add Recinto	30	add_recinto
118	Can change Recinto	30	change_recinto
119	Can delete Recinto	30	delete_recinto
120	Can view Recinto	30	view_recinto
121	Can add PMA	28	add_pma
122	Can change PMA	28	change_pma
123	Can delete PMA	28	delete_pma
124	Can view PMA	28	view_pma
125	Can add Sector	31	add_sector
126	Can change Sector	31	change_sector
127	Can delete Sector	31	delete_sector
128	Can view Sector	31	view_sector
129	Can add Unidad / Servicio	33	add_unidad
130	Can change Unidad / Servicio	33	change_unidad
131	Can delete Unidad / Servicio	33	delete_unidad
132	Can view Unidad / Servicio	33	view_unidad
133	Can add Cargo	20	add_cargo
134	Can change Cargo	20	change_cargo
135	Can delete Cargo	20	delete_cargo
136	Can view Cargo	20	view_cargo
137	Can add Equipo	37	add_equipo
138	Can change Equipo	37	change_equipo
139	Can delete Equipo	37	delete_equipo
140	Can view Equipo	37	view_equipo
141	Can add Registro de Bitácora	35	add_bitacoraequipo
142	Can change Registro de Bitácora	35	change_bitacoraequipo
143	Can delete Registro de Bitácora	35	delete_bitacoraequipo
144	Can view Registro de Bitácora	35	view_bitacoraequipo
145	Can add Opción de Bitácora	36	add_bitacoraopcion
146	Can change Opción de Bitácora	36	change_bitacoraopcion
147	Can delete Opción de Bitácora	36	delete_bitacoraopcion
148	Can view Opción de Bitácora	36	view_bitacoraopcion
149	Can add Anexo	38	add_anexo
150	Can change Anexo	38	change_anexo
151	Can delete Anexo	38	delete_anexo
152	Can view Anexo	38	view_anexo
153	Can add Requerimiento de Cambio	39	add_requerimientocambio
154	Can change Requerimiento de Cambio	39	change_requerimientocambio
155	Can delete Requerimiento de Cambio	39	delete_requerimientocambio
156	Can view Requerimiento de Cambio	39	view_requerimientocambio
157	Can add Acta de Entrega	40	add_acta
158	Can change Acta de Entrega	40	change_acta
159	Can delete Acta de Entrega	40	delete_acta
160	Can view Acta de Entrega	40	view_acta
161	Can add Detalle de Acta	41	add_actadetalle
162	Can change Detalle de Acta	41	change_actadetalle
163	Can delete Detalle de Acta	41	delete_actadetalle
164	Can view Detalle de Acta	41	view_actadetalle
165	Can add Categoría	43	add_categoria
166	Can change Categoría	43	change_categoria
167	Can delete Categoría	43	delete_categoria
168	Can view Categoría	43	view_categoria
169	Can add Prioridad	46	add_prioridad
170	Can change Prioridad	46	change_prioridad
171	Can delete Prioridad	46	delete_prioridad
172	Can view Prioridad	46	view_prioridad
173	Can add Ticket	47	add_ticket
174	Can change Ticket	47	change_ticket
175	Can delete Ticket	47	delete_ticket
176	Can view Ticket	47	view_ticket
177	Can add Archivo Adjunto	42	add_archivoadjunto
178	Can change Archivo Adjunto	42	change_archivoadjunto
179	Can delete Archivo Adjunto	42	delete_archivoadjunto
180	Can view Archivo Adjunto	42	view_archivoadjunto
181	Can add Historial de Ticket	48	add_tickethistorial
182	Can change Historial de Ticket	48	change_tickethistorial
183	Can delete Historial de Ticket	48	delete_tickethistorial
184	Can view Historial de Ticket	48	view_tickethistorial
185	Can add Grupo Resolutor	44	add_gruporesolutor
186	Can change Grupo Resolutor	44	change_gruporesolutor
187	Can delete Grupo Resolutor	44	delete_gruporesolutor
188	Can view Grupo Resolutor	44	view_gruporesolutor
189	Can add Notificación	45	add_notificacion
190	Can change Notificación	45	change_notificacion
191	Can delete Notificación	45	delete_notificacion
192	Can view Notificación	45	view_notificacion
193	Can add Matriz SLA	49	add_slamatrix
194	Can change Matriz SLA	49	change_slamatrix
195	Can delete Matriz SLA	49	delete_slamatrix
196	Can view Matriz SLA	49	view_slamatrix
197	Can add Credencial de Correo	52	add_credencialcorreo
198	Can change Credencial de Correo	52	change_credencialcorreo
199	Can delete Credencial de Correo	52	delete_credencialcorreo
200	Can view Credencial de Correo	52	view_credencialcorreo
201	Can add Grupo de Correo	53	add_grupocorreo
202	Can change Grupo de Correo	53	change_grupocorreo
203	Can delete Grupo de Correo	53	delete_grupocorreo
204	Can view Grupo de Correo	53	view_grupocorreo
205	Can add Miembro de Grupo	54	add_miembrogrupocorreo
206	Can change Miembro de Grupo	54	change_miembrogrupocorreo
207	Can delete Miembro de Grupo	54	delete_miembrogrupocorreo
208	Can view Miembro de Grupo	54	view_miembrogrupocorreo
209	Can add Configuración SMTP	50	add_configuracionsmtp
210	Can change Configuración SMTP	50	change_configuracionsmtp
211	Can delete Configuración SMTP	50	delete_configuracionsmtp
212	Can view Configuración SMTP	50	view_configuracionsmtp
213	Can add Log de Correo	51	add_correolog
214	Can change Log de Correo	51	change_correolog
215	Can delete Log de Correo	51	delete_correolog
216	Can view Log de Correo	51	view_correolog
217	Can add Ayuda Rápida	55	add_ayudarapida
218	Can change Ayuda Rápida	55	change_ayudarapida
219	Can delete Ayuda Rápida	55	delete_ayudarapida
220	Can view Ayuda Rápida	55	view_ayudarapida
221	Can add Ítem de Checklist	56	add_checklistitem
222	Can change Ítem de Checklist	56	change_checklistitem
223	Can delete Ítem de Checklist	56	delete_checklistitem
224	Can view Ítem de Checklist	56	view_checklistitem
225	Can add Pendiente	57	add_pendiente
226	Can change Pendiente	57	change_pendiente
227	Can delete Pendiente	57	delete_pendiente
228	Can view Pendiente	57	view_pendiente
229	Can add Web App / Acceso	58	add_webapp
230	Can change Web App / Acceso	58	change_webapp
231	Can delete Web App / Acceso	58	delete_webapp
232	Can view Web App / Acceso	58	view_webapp
233	Can add Aviso del Visor	59	add_avisovisor
234	Can change Aviso del Visor	59	change_avisovisor
235	Can delete Aviso del Visor	59	delete_avisovisor
236	Can view Aviso del Visor	59	view_avisovisor
237	Can add Configuración SLA	63	add_slaconfiguracion
238	Can change Configuración SLA	63	change_slaconfiguracion
239	Can delete Configuración SLA	63	delete_slaconfiguracion
240	Can view Configuración SLA	63	view_slaconfiguracion
241	Can add PMA	61	add_pma
242	Can change PMA	61	change_pma
243	Can delete PMA	61	delete_pma
244	Can view PMA	61	view_pma
245	Can add IP de Red	60	add_infraestructurared
246	Can change IP de Red	60	change_infraestructurared
247	Can delete IP de Red	60	delete_infraestructurared
248	Can view IP de Red	60	view_infraestructurared
249	Can add Rango de IP	62	add_rangoip
250	Can change Rango de IP	62	change_rangoip
251	Can delete Rango de IP	62	delete_rangoip
252	Can view Rango de IP	62	view_rangoip
253	Can add Categoría de Conocimiento	65	add_categoriaconocimiento
254	Can change Categoría de Conocimiento	65	change_categoriaconocimiento
255	Can delete Categoría de Conocimiento	65	delete_categoriaconocimiento
256	Can view Categoría de Conocimiento	65	view_categoriaconocimiento
257	Can add Artículo de Conocimiento	64	add_articuloconocimiento
258	Can change Artículo de Conocimiento	64	change_articuloconocimiento
259	Can delete Artículo de Conocimiento	64	delete_articuloconocimiento
260	Can view Artículo de Conocimiento	64	view_articuloconocimiento
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
2	pbkdf2_sha256$1200000$7HNyAQvfxLA9GkbPp8dWV2$5JRNlllNrYvfXM4oA1CAma0McK1RkMDAIBQ++PPALP4=	2026-08-25 01:14:32.15206+00	t	16233406-9	REINALDO	GOMEZ	mr.reinaldo.g@redsalud.gob.cl	t	t	2026-07-09 01:03:15.143+00
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
1	2	3
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: axes_accessattempt; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.axes_accessattempt (id, user_agent, ip_address, username, http_accept, path_info, attempt_time, get_data, post_data, failures_since_start) FROM stdin;
\.


--
-- Data for Name: axes_accessattemptexpiration; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.axes_accessattemptexpiration (access_attempt_id, expires_at) FROM stdin;
\.


--
-- Data for Name: axes_accessfailurelog; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.axes_accessfailurelog (id, user_agent, ip_address, username, http_accept, path_info, attempt_time, locked_out) FROM stdin;
\.


--
-- Data for Name: axes_accesslog; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.axes_accesslog (id, user_agent, ip_address, username, http_accept, path_info, attempt_time, logout_time, session_hash) FROM stdin;
1	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-14 23:03:14.950209+00	\N	af57a789827c533684d9cee5b20222739ce2e1fdc9cfc8612ebc89750c4588ef
2	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-14 23:07:31.001438+00	\N	54217dabfcc5b990a2b0b876e7ba0a9fda337149f36953c1ad97058494a1afb2
3	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-14 23:12:21.389321+00	\N	160599c9c8a31ffca5e24c56a401be2f4c1df72b724758d9a7eeb4beacf44b14
4	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-14 23:16:41.415772+00	2026-07-15 00:15:18.009178+00	8927652c749e46edbb05e92cfe9f9d2c0241f7bd09b1311d574d70b9b6c93be8
5	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-15 00:15:48.44178+00	2026-07-15 03:00:00.654281+00	938d2037876c3ba3056cef71176424d22b6289bdbcb1bead48524c97d8995dbd
6	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-15 03:08:41.956117+00	2026-07-15 03:08:46.660309+00	f013d7128ab5d38227902454d5807e0fd91e28201ca1516e0415ad6c76f126d4
7	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-15 03:09:33.767456+00	2026-07-15 03:16:17.328632+00	ca80d70e8ab56ecd1fca9cd8c1d5f287baaed9d24c42c20d3845db1b1c6a5c69
8	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-15 03:16:51.540545+00	2026-07-15 03:16:54.011527+00	0c2d512266e064fbdbfe7b6c81a97f06e18fb6db65bc13d82ae41b16c3d3ad47
9	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-15 03:17:52.516253+00	2026-07-15 03:49:57.954794+00	452caec218530eec4ed37a46da802a908cda6eaaf7608b7ef07e4bfa6226d99a
10	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-15 03:50:04.706881+00	2026-07-15 03:53:46.438889+00	16c6ff523b59cf0e2e3dda2d64f4df3e3b08a516009baccfe4fbfac058aa4bd7
11	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-15 12:40:33.481666+00	2026-07-15 12:43:37.846502+00	280430b6b8d93578210e6ad1399c074e7a4a2b09135b9a6d1cec6ec52c891a22
12	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-15 12:56:15.364675+00	2026-07-15 14:18:17.355861+00	e8fec7ba0408301c8596b76c85dc5443a53dd8602e8f556c88f0eb74a3ef6ba2
13	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-15 14:18:22.726584+00	2026-07-15 14:19:36.475859+00	23c2d859d8eb7d1d2d2c307d9a04553cf3ff85b04c1c76f7067f35ab08d91e29
14	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-15 14:28:33.012586+00	2026-07-15 14:28:50.509163+00	1c7b6ffd7829fbb79296873a6aa48423a3a4e3cac6f861a83161b718e70d8e2d
15	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-15 14:29:19.586526+00	2026-07-17 03:55:46.049283+00	d6916cdffe171af827adcf7258e3eb6e012d8d7101f8f3a7c340eb48da99fc5d
16	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-16 16:12:41.432254+00	2026-07-16 19:51:47.531024+00	8b3ff7e29d6ab752b1c534c0f765b29fff6a7bb36f569441b4688390597fcdd4
18	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-19 00:48:24.289829+00	2026-07-19 04:32:08.243508+00	8a75637e8d23b1659a40771f9d2ff74a09cbc48513d51888321c39f4f9b69a9c
19	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-19 15:35:28.125073+00	2026-07-19 16:23:32.613056+00	e696118293612ed765ba037b48a8ca7f8a6212388bb321d5c7c989641afc8a6e
20	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-19 16:24:06.772335+00	2026-07-19 23:17:50.855778+00	276afe9d396855325aedc58d36d8feb3e3c85743ebf481f0301a4e7426883e5a
21	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-19 23:18:05.518114+00	2026-07-19 23:26:44.825963+00	32acc455aafc52ade44e2538cf5f6327ea95efdb71042e2b8de9c51695d97c91
22	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	24028352-2	application/json, text/javascript, */*; q=0.01	/login/	2026-07-19 23:26:52.235018+00	2026-07-19 23:27:14.508044+00	3faa288e491ddb92cbec55e27e4437bf228b8c8e970dcd5f41f4038cc27878f1
23	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-19 23:27:24.765323+00	2026-07-19 23:28:46.491363+00	3f93411d1d8f6e641d5d0d5f397731d83da0c4c95db704eaeb5ee16dc44a2c1c
24	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	24028352-2	application/json, text/javascript, */*; q=0.01	/login/	2026-07-19 23:28:56.098323+00	2026-07-19 23:29:37.327069+00	49bbdf31e7d6f42562d3f2534c49db9f98539861674cde6ed60d016c7ad4ae6e
25	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-19 23:29:47.295332+00	2026-07-19 23:40:27.112615+00	9e96b853299213f2f0842856fc40c7077d93da586b4193ee49a8cb1cfe017326
26	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	24028352-2	application/json, text/javascript, */*; q=0.01	/login/	2026-07-19 23:40:40.022242+00	2026-07-19 23:41:23.905411+00	dbb4956c085f956076076434f99513148b97f8e591fd78c916865cda14cefd6d
27	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-19 23:41:32.16008+00	2026-07-19 23:53:50.180754+00	69bbc55fdddba072de874e959aab25792c778dad1a24b39e4baf6b008f3eeaf8
28	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-19 23:53:57.635171+00	2026-07-19 23:55:14.636306+00	2660319b61ef85f443b4530bc9c6e5a3ff9d4a73344dbfe7f7d0248067fcfb76
29	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	24028352-2	application/json, text/javascript, */*; q=0.01	/login/	2026-07-19 23:55:30.907614+00	2026-07-20 00:25:06.42251+00	3bfd37faf9a220bd0ebf6e41179bfe3f1259ed1d6d7d870ef383ec8d09f2c16b
30	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-20 00:25:18.819382+00	2026-07-20 00:46:05.227285+00	db221950d8434a3d602b7e5bc5df101ce3a785c20740d3fb92c80f29a74924ff
31	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	24028352-2	application/json, text/javascript, */*; q=0.01	/login/	2026-07-20 00:46:17.718716+00	2026-07-20 00:46:28.468179+00	c54da6609a1ae0e9809b2567e4e85ef1d78c40a21c7f60c3e6f2d61ba31d9560
32	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-20 00:46:38.502577+00	2026-07-20 00:46:54.898975+00	5f00b23af082b43411c3fb14a507167d73632aa38386273d93fc504281134ab9
33	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-20 00:47:13.204793+00	2026-07-20 00:49:51.809987+00	0dd156e803413132109c9e9ab53e982fa7b7a7fcd5579ec3d99c7953d20ddcbe
34	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	24028352-2	application/json, text/javascript, */*; q=0.01	/login/	2026-07-20 00:50:01.506324+00	2026-07-20 01:02:03.805128+00	74cd4f0a927777de1b3c24843f78cfeeaf6902ac47dff6c67a1a3c4694957f8a
35	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	8325648-6	application/json, text/javascript, */*; q=0.01	/login/	2026-07-20 01:02:14.964234+00	2026-07-20 01:02:37.613138+00	04044a20440c141e9ee716c827f88b85da6b6e884d533b8c46c97d0fda9c1c0c
36	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-20 01:03:16.064436+00	2026-07-20 01:03:56.386407+00	fa5b681c8a9b81719b03f8be335ff5831fb59b3add58765cb910460e505f37d3
37	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	24186567-3	application/json, text/javascript, */*; q=0.01	/login/	2026-07-20 01:04:03.17699+00	2026-07-20 01:04:16.689073+00	52001c44f7a04a9b97bd32010e3eafae41a5e2cdd305f9083e21f646f254627b
38	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	13549881-5	application/json, text/javascript, */*; q=0.01	/login/	2026-07-20 01:04:26.317484+00	2026-07-20 01:05:30.918809+00	2005c69fb161204e94a46bf8ba3a702942f5f7f23e3ec3cf7ed11165b6b25869
39	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	24186567-3	application/json, text/javascript, */*; q=0.01	/login/	2026-07-20 01:05:42.710112+00	2026-07-20 01:06:57.561469+00	92fb626ba7236256a75961aef94801e6d52245a534672c51cc631d1c75a2fe41
40	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	24028352-2	application/json, text/javascript, */*; q=0.01	/login/	2026-07-20 01:07:10.608802+00	2026-07-20 01:40:12.462854+00	8b4d24c6dddeae51eaf8caa830d7fe0dbe926ec05f25a2aa3efdf45bc3a4e7f6
17	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-16 19:51:57.986752+00	2026-07-21 14:58:54.974311+00	0d2881d3175766d9fb345c72f945dac7690fc6a5ae384306b1cafaff09dfcafd
41	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-20 01:40:20.10771+00	2026-07-20 03:02:03.478699+00	0fbeff2862fa2c041a5769c7e7a8e73ecafd19e0b53fef65db3ef452ead25167
42	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	24028352-2	application/json, text/javascript, */*; q=0.01	/login/	2026-07-20 03:02:12.089309+00	2026-07-20 22:59:15.468061+00	1acf57b48b1aa2698885319481f76c44b962d44a0e3a27d563192239eddf61b7
44	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-20 23:22:47.622413+00	2026-07-20 23:23:22.641222+00	6f4491b78888dbdcf28cb3baeaefd5bc63d13e0ee6bb71c3ed052ef8cfdb7fa1
45	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-20 23:24:40.826621+00	2026-07-20 23:24:49.051665+00	b7d215fdde895f12bd08d37ecd73e8eae4436f48493e49a54fa16eda8c3bb4e8
46	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-20 23:31:30.425368+00	2026-07-20 23:31:36.2457+00	51ee8701068bc34fb5a576a69ea507abdc00d32b47cd3cf0d93f52c2d246397c
47	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-20 23:32:33.346609+00	2026-07-20 23:34:53.323566+00	23414590aade9b2433009a46f6a44ec263493799799ec2f1ba21a7e295bbae0d
48	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-20 23:39:18.205214+00	2026-07-21 01:02:09.616639+00	51e8d4eb94928f6e3be43c000b116727e5d90292f15b3f6936c664fc8c091908
49	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-21 01:02:17.035805+00	2026-07-21 01:52:20.732852+00	839366553e0bd6b5c5ceefb35d3a1b78d55fd475cc17fac9f1d13460dfd51e72
50	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-21 01:52:32.590409+00	2026-07-21 02:49:54.370686+00	2c47290288bbcca763b97c2dcbf0035c7b04c7c515b7672c0d6d53fa0b828209
51	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	24028352-2	application/json, text/javascript, */*; q=0.01	/login/	2026-07-21 02:50:05.395298+00	2026-07-21 02:50:28.842306+00	3980ed2672decdc9a4ece8a81f8c2b14203dc0b34ca0e58f715b2dfa1214bb2d
53	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-22 00:17:29.889307+00	\N	a75ab78747a1c87caf499d007bfd75262e864e995348890bd3f505039ea530ba
52	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-21 21:28:16.18343+00	2026-07-22 01:56:16.079446+00	7b3aa352e9a6d33a942fb3add1b61133fd59d4fe665b4a65bee1538eb1d20e5b
55	Mozilla/5.0 (iPhone; CPU iPhone OS 18_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.4 Mobile/15E148 Safari/604.1	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-22 02:36:50.016124+00	\N	a8f7304f87c3c9d521c4cdfc51bca0e52c73614043462dfa7792cc954778efd2
43	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-20 14:35:08.034377+00	2026-07-24 04:26:43.254926+00	9fce43edbc475df282bfcec0d5e0646d1d15327e32912bdfc286fa9cade709e4
54	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-22 01:57:33.787192+00	2026-07-24 13:23:23.708219+00	26ba4d643e35827cb44b67bda590e78f21f224f9d85bf95011c0670e43596429
56	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-22 16:13:05.630942+00	\N	f8295d828b28c3fecb710a18f18dcea6c3b01d9f5b47d4a39946f06debc69ed3
57	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-23 01:06:19.133985+00	2026-07-23 01:49:39.120952+00	290ed8328a6f92e6ef2d13c25e95e65c40bfd7a0787d0b4a1407add21127a137
58	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-23 01:49:48.533385+00	\N	954ea90c9e4487e41029f80176a49c9fb6b849e0cbc37ce5561ea195518bf662
59	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-24 04:27:03.083377+00	\N	22e85dc1662f8df3d09ed0a6539f76da779627d1880b64b8b97987e9cf35977e
60	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-24 13:23:45.29252+00	2026-07-24 13:24:35.078633+00	1603ade55d1d6947df0960b8eca3ead79ef992221bdf50c5598148b18937873d
61	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-24 13:24:57.901035+00	2026-07-24 13:25:20.795976+00	0d89b171c6083d5032eaaf66516ed7f3cffe3f96da97a6e15354bd6fba13ab26
62	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-24 13:26:16.731083+00	2026-07-24 13:28:31.216141+00	22740c16737172be0b7f4407352e8088e3bf9ecbcc83861705a15ae2c74f9f95
63	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	17944996-K	application/json, text/javascript, */*; q=0.01	/login/	2026-07-24 13:28:44.193724+00	2026-07-24 13:40:33.528692+00	8e9be97f1686fae5d7859812ca7337332e57913dd586797eb5381996516658ea
64	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-24 13:40:45.987096+00	2026-07-24 13:58:09.685434+00	7a3d10a7453fa187c81846f9dcb98684f804446c3e23205c9ccb298ea04acce6
65	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	17944996-K	application/json, text/javascript, */*; q=0.01	/login/	2026-07-24 13:58:16.639683+00	2026-07-24 14:01:50.607288+00	bcbe435a4bd77c014303a2664e83dec65b49a8d8b978a6fb0460abf39c49daa9
66	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	17944996-K	application/json, text/javascript, */*; q=0.01	/login/	2026-07-24 14:02:07.692361+00	2026-07-24 14:02:30.554455+00	76a6efd10449f8bdf644414743171502961e27d9938fdfe8e67ed2f99a6c04f1
67	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	17944996-K	application/json, text/javascript, */*; q=0.01	/login/	2026-07-24 14:02:41.101013+00	2026-07-24 14:02:50.188714+00	a5d29c78d8d90d5a77be35a441d41b22f5a1cf0fa73158477586733d9f835839
68	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-24 14:02:55.675871+00	2026-07-24 14:03:18.722921+00	15f7b4835e972adc232bf78ac9e04d9023a453e06b629b5eb85a5af8be5b3461
69	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	17944996-K	application/json, text/javascript, */*; q=0.01	/login/	2026-07-24 14:03:46.215113+00	2026-07-24 14:05:37.689092+00	b52e514e844d72a1361320884a0d6dff30218ca552a6277ad34f7d571e06f020
70	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	17944996-K	application/json, text/javascript, */*; q=0.01	/login/	2026-07-24 14:06:01.127095+00	\N	317eb7454cdc26c027ce370790718bcda22c7b67a21e1fedfcc1013f31de555e
71	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	17944996-K	application/json, text/javascript, */*; q=0.01	/login/	2026-07-24 14:10:19.487931+00	\N	a8ba6f8ccb527617512c2e9162628a77b2dc458e144a5f355b10abc5d15b8bd4
72	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	17944996-K	application/json, text/javascript, */*; q=0.01	/login/	2026-07-24 14:10:58.038383+00	2026-07-24 14:30:25.898822+00	447c2ffcb90fa827c315844668f658bb960447730c9fcceff65817d5c2f1229e
74	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	17944996-K	application/json, text/javascript, */*; q=0.01	/login/	2026-07-24 17:10:23.309997+00	\N	f1296852e3907e6d893de49cb0ad37bec844773f813efe9f226cb8dca68468df
73	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	17944996-K	application/json, text/javascript, */*; q=0.01	/login/	2026-07-24 14:32:14.330371+00	2026-07-24 17:54:17.361409+00	d50287e85c31ecc9f5eeb9b4dd7c01087e941b834d365660f61e67dac85226e0
75	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-24 17:54:29.501798+00	2026-07-24 17:56:28.112767+00	e698639943598f87178d3f87a647fdc461df148ac7697633f5c898fb0db237f3
76	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36	\N	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-07-30 01:55:33.647208+00	\N	aa67ff62d3571d237869f773754ae40df2fa44497295a9779494f7aa30baa44f
77	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 Edg/149.0.0.0	\N	17944996-K	application/json, text/javascript, */*; q=0.01	/login/	2026-08-04 14:24:13.133642+00	2026-08-04 14:29:52.801472+00	24c7194767189030c39dced814386b615d2ce04734325cd9db2a8317ce213e1a
78	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36	172.18.0.4	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-08-24 14:37:19.694719+00	2026-08-24 14:37:25.583244+00	39363d83aa2867cbef4129d5cf3eefc3fc88db0806a3b06b1203b92059368c92
79	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36	172.18.0.4	24028352-2	application/json, text/javascript, */*; q=0.01	/login/	2026-08-24 14:39:34.593449+00	2026-08-24 14:40:38.832736+00	3ca1213ebc51b3215f87dcb513d3cefdc5786b9ab3fe9eb46c8a93b093ec23b8
80	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36	172.18.0.4	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-08-24 14:40:48.61885+00	\N	8343a6f9cb35465f18e322effa08d54e430f50964bca529c9dd6cd7a8f7721bb
81	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36	172.18.0.4	16233406-9	application/json, text/javascript, */*; q=0.01	/login/	2026-08-25 01:14:32.134301+00	\N	70493bbf55a9c23eacbf1b393329ab6656e65ca4c4fda50c32fefdfd501ce852
\.


--
-- Data for Name: conocimiento_articuloconocimiento; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.conocimiento_articuloconocimiento (id, titulo, sintomas, solucion, es_error_conocido, creado_en, actualizado_en, categoria_id) FROM stdin;
\.


--
-- Data for Name: conocimiento_categoriaconocimiento; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.conocimiento_categoriaconocimiento (id, nombre) FROM stdin;
\.


--
-- Data for Name: core_funcionario; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.core_funcionario (id, rut, nombres, apellidos, correo, cargo_id, fecha_registro, unidad_id, cargo_old) FROM stdin;
\.


--
-- Data for Name: core_logauditoria; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.core_logauditoria (id, usuario, accion, tabla, registro_id, detalles, ip_address, fecha_registro) FROM stdin;
1	16233406-9	LOGIN_FAIL	User	\N	Intento fallido de inicio de sesión para el usuario: 16233406-9	186.67.112.146	2026-08-24 14:26:10.143074+00
2	16233406-9	LOGIN_FAIL	User	\N	Intento fallido de inicio de sesión para el usuario: 16233406-9	186.67.112.146	2026-08-24 14:26:16.637771+00
3	16233406-9	LOGIN_FAIL	User	\N	Intento fallido de inicio de sesión para el usuario: 16233406-9	186.67.112.146	2026-08-24 14:26:21.843334+00
4	24028352-2	LOGIN_FAIL	User	\N	Intento fallido de inicio de sesión para el usuario: 24028352-2	186.67.112.146	2026-08-24 14:26:31.110144+00
5	24028352-2	LOGIN_FAIL	User	\N	Intento fallido de inicio de sesión para el usuario: 24028352-2	186.67.112.146	2026-08-24 14:29:17.101836+00
6	24028352-2	LOGIN_FAIL	User	\N	Intento fallido de inicio de sesión para el usuario: 24028352-2	186.67.112.146	2026-08-24 14:31:16.372885+00
7	16233406-9	LOGIN_FAIL	User	\N	Intento fallido de inicio de sesión para el usuario: 16233406-9	186.67.112.146	2026-08-24 14:31:29.515812+00
8	16233406-9	LOGIN_FAIL	User	\N	Intento fallido de inicio de sesión para el usuario: 16233406-9	200.39.136.193	2026-08-24 14:32:00.021357+00
9	16233406-9	LOGIN_FAIL	User	\N	Intento fallido de inicio de sesión para el usuario: 16233406-9	186.67.112.146	2026-08-24 14:34:02.694269+00
638	16233406-9	LOGIN_OK	User	2	Inicio de sesión exitoso mediante AJAX	186.67.112.146	2026-08-24 14:37:19.717442+00
639	16233406-9	ACCESO	Dashboard	\N	El usuario accedió al módulo: Dashboard	186.67.112.146	2026-08-24 14:37:20.081079+00
640	16233406-9	CREAR	Logout	\N	Petición POST a /logout/	186.67.112.146	2026-08-24 14:37:24.928283+00
641	16233406-9	LOGOUT	User	\N	Cierre de sesión exitoso (POST)	186.67.112.146	2026-08-24 14:37:25.610913+00
642	24028352-2	LOGIN_FAIL	User	\N	Intento fallido de inicio de sesión para el usuario: 24028352-2	186.67.112.146	2026-08-24 14:37:36.799378+00
643	24028352-2	LOGIN_FAIL	User	\N	Intento fallido de inicio de sesión para el usuario: 24028352-2	186.67.112.146	2026-08-24 14:37:48.214005+00
644	16233406-9	LOGIN_FAIL	User	\N	Intento fallido de inicio de sesión para el usuario: 16233406-9	186.67.112.146	2026-08-24 14:38:35.103763+00
645	16233406-9	LOGIN_FAIL	User	\N	Intento fallido de inicio de sesión para el usuario: 16233406-9	186.67.112.146	2026-08-24 14:38:47.304419+00
646	24028352-2	LOGIN_FAIL	User	\N	Intento fallido de inicio de sesión para el usuario: 24028352-2	186.67.112.146	2026-08-24 14:39:07.983656+00
647	24028352-2	LOGIN_OK	User	21	Inicio de sesión exitoso mediante AJAX	186.67.112.146	2026-08-24 14:39:34.631478+00
648	24028352-2	ACCESO	Dashboard	\N	El usuario accedió al módulo: Dashboard	186.67.112.146	2026-08-24 14:39:34.819939+00
649	24028352-2	CREAR	Logout	\N	Petición POST a /logout/	186.67.112.146	2026-08-24 14:40:38.822983+00
650	24028352-2	LOGOUT	User	\N	Cierre de sesión exitoso (POST)	186.67.112.146	2026-08-24 14:40:38.847504+00
651	16233406-9	LOGIN_FAIL	User	\N	Intento fallido de inicio de sesión para el usuario: 16233406-9	186.67.112.146	2026-08-24 14:40:45.164056+00
652	16233406-9	LOGIN_OK	User	2	Inicio de sesión exitoso mediante AJAX	186.67.112.146	2026-08-24 14:40:48.641446+00
653	16233406-9	ACCESO	Dashboard	\N	El usuario accedió al módulo: Dashboard	186.67.112.146	2026-08-24 14:40:48.848321+00
654	16233406-9	ACCESO	Tickets	\N	El usuario accedió al módulo: Tickets	186.67.112.146	2026-08-24 14:40:50.680491+00
655	16233406-9	ACCESO	Usuarios	\N	El usuario accedió al módulo: Usuarios	186.67.112.146	2026-08-24 14:40:53.091611+00
656	16233406-9	CREAR	Usuarios	\N	Petición POST a /api/usuarios/	186.67.112.146	2026-08-24 14:40:53.65047+00
657	16233406-9	ACCESO	Equipos	\N	El usuario accedió al módulo: Equipos	186.67.112.146	2026-08-24 14:41:09.347612+00
658	16233406-9	CREAR	Equipos	\N	Petición POST a /equipos/api/	186.67.112.146	2026-08-24 14:41:10.364777+00
659	16233406-9	ACCESO	Mantenedores	\N	El usuario accedió al módulo: Mantenedores	186.67.112.146	2026-08-24 14:43:40.300905+00
660	16233406-9	CREAR	Mantenedores	\N	Petición POST a /mantenedores/api/	186.67.112.146	2026-08-24 14:43:44.608862+00
661	16233406-9	CREAR	Mantenedores	\N	Petición POST a /mantenedores/api/	186.67.112.146	2026-08-24 14:43:45.683061+00
662	16233406-9	CREAR	Mantenedores	\N	Petición POST a /mantenedores/api/	186.67.112.146	2026-08-24 14:43:46.122804+00
663	16233406-9	CREAR	Mantenedores	\N	Petición POST a /mantenedores/api/	186.67.112.146	2026-08-24 14:43:47.816786+00
664	16233406-9	CREAR	Mantenedores	\N	Petición POST a /mantenedores/api/	186.67.112.146	2026-08-24 14:43:54.085988+00
665	16233406-9	ACCESO	Usuarios	\N	El usuario accedió al módulo: Usuarios	186.67.112.146	2026-08-24 14:48:12.507528+00
666	16233406-9	CREAR	Usuarios	\N	Petición POST a /api/usuarios/	186.67.112.146	2026-08-24 14:48:14.93769+00
667	16233406-9	ACCESO	Mantenedores	\N	El usuario accedió al módulo: Mantenedores	186.67.112.146	2026-08-24 14:48:44.029157+00
668	16233406-9	CREAR	Mantenedores	\N	Petición POST a /mantenedores/api/	186.67.112.146	2026-08-24 14:48:47.627808+00
669	16233406-9	CREAR	Mantenedores	\N	Petición POST a /mantenedores/api/	186.67.112.146	2026-08-24 14:49:12.446072+00
670	16233406-9	CREAR	Mantenedores	\N	Petición POST a /mantenedores/api/	186.67.112.146	2026-08-24 14:49:13.234337+00
671	16233406-9	CREAR	Mantenedores	\N	Petición POST a /mantenedores/api/	186.67.112.146	2026-08-24 14:49:14.922293+00
672	16233406-9	CREAR	Mantenedores	\N	Petición POST a /mantenedores/api/	186.67.112.146	2026-08-24 14:49:16.642523+00
673	16233406-9	CREAR	Mantenedores	\N	Petición POST a /mantenedores/api/	186.67.112.146	2026-08-24 14:53:06.752966+00
674	16233406-9	CREAR	Mantenedores	\N	Petición POST a /mantenedores/api/	186.67.112.146	2026-08-24 14:53:07.093967+00
675	16233406-9	CREAR	Mantenedores	\N	Petición POST a /mantenedores/api/	186.67.112.146	2026-08-24 14:53:09.110785+00
676	16233406-9	LOGIN_FAIL	User	\N	Intento fallido de inicio de sesión para el usuario: 16233406-9	200.39.136.193	2026-08-25 01:14:28.767134+00
677	16233406-9	LOGIN_OK	User	2	Inicio de sesión exitoso mediante AJAX	200.39.136.193	2026-08-25 01:14:32.159031+00
678	16233406-9	ACCESO	Dashboard	\N	El usuario accedió al módulo: Dashboard	200.39.136.193	2026-08-25 01:14:32.306678+00
679	16233406-9	ACCESO	Roles	\N	El usuario accedió al módulo: Roles	200.39.136.193	2026-08-25 01:14:51.83089+00
680	16233406-9	ACCESO	Correos/configuracion	\N	El usuario accedió al módulo: Correos/configuracion	200.39.136.193	2026-08-25 01:15:07.268858+00
681	16233406-9	ACCESO	Sla	\N	El usuario accedió al módulo: Sla	200.39.136.193	2026-08-25 01:17:19.233212+00
\.


--
-- Data for Name: core_perfilusuario; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.core_perfilusuario (id, unidad, cargo, grado, rut, telefono, foto, fecha_registro, user_id, rol_id) FROM stdin;
\.


--
-- Data for Name: core_rol; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.core_rol (id, nombre, descripcion, permisos, activo, orden, creado_por, actualizado_por, fecha_creacion, fecha_actualizacion, icono, is_system) FROM stdin;
1	Super Administrador	Acceso total a todos los módulos y configuración	{"VER_ACTAS": true, "VER_ANEXOS": true, "VER_INICIO": true, "VER_EQUIPOS": true, "VER_TICKETS": true, "VER_REPORTES": true, "VER_USUARIOS": true, "GESTIONAR_ACTAS": true, "GESTIONAR_ROLES": true, "GESTIONAR_ANEXOS": true, "VER_MANTENEDORES": true, "GESTIONAR_EQUIPOS": true, "GESTIONAR_TICKETS": true, "GESTIONAR_USUARIOS": true, "GESTIONAR_MANTENEDORES": true}	t	1	\N	\N	2026-07-12 23:39:52.976+00	2026-07-20 01:44:55.828274+00	fas fa-key	t
14	Mesa de Ayuda	Atención de Nivel 1, creación y derivación de tickets	{"VER_INICIO": true, "VER_TICKETS": true, "GESTIONAR_TICKETS": true}	t	0	\N	\N	2026-07-20 01:44:55.838224+00	2026-07-21 01:06:47.923667+00	fas fa-headset	t
10	Técnico Nivel 2	Técnico que va a terreno a resolver incidentes y tickets	{"VER_INICIO": true, "VER_EQUIPOS": true, "VER_TICKETS": true, "RECIBIR_TICKETS": true}	t	0	\N	\N	2026-07-19 20:51:32.471176+00	2026-07-19 20:52:09.57434+00	fas fa-tools	f
\.


--
-- Data for Name: correos_configuracionsmtp; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.correos_configuracionsmtp (id, host, puerto, usuario, password, use_tls, remitente_por_defecto, fecha_actualizacion) FROM stdin;
1	servidor SMTP	587	usuario@usuario.cl	123456	t	usuario@usuario.cl	2026-07-24 13:27:36.735379+00
\.


--
-- Data for Name: correos_correolog; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.correos_correolog (id, tipo, destinatario, asunto, estado, intentos, error_detalle, reenviado_manualmente, fecha_creacion, fecha_ultimo_intento, ticket_id) FROM stdin;
\.


--
-- Data for Name: correos_credencialcorreo; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.correos_credencialcorreo (id, email, propietario, departamento, activo, fecha_creacion) FROM stdin;
\.


--
-- Data for Name: correos_grupocorreo; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.correos_grupocorreo (id, nombre, descripcion, orden, activo, fecha_creacion, fecha_actualizacion) FROM stdin;
\.


--
-- Data for Name: correos_miembrogrupocorreo; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.correos_miembrogrupocorreo (id, email, grupo_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_celery_results_chordcounter; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.django_celery_results_chordcounter (id, group_id, sub_tasks, count) FROM stdin;
\.


--
-- Data for Name: django_celery_results_groupresult; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.django_celery_results_groupresult (id, group_id, date_created, date_done, content_type, content_encoding, result) FROM stdin;
\.


--
-- Data for Name: django_celery_results_taskresult; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.django_celery_results_taskresult (id, task_id, status, content_type, content_encoding, result, date_done, traceback, meta, task_args, task_kwargs, task_name, worker, date_created, periodic_task_name, date_started) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	group
3	auth	permission
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	axes	accessattempt
8	axes	accessattemptexpiration
9	axes	accessfailurelog
10	axes	accesslog
11	django_celery_results	chordcounter
12	django_celery_results	groupresult
13	django_celery_results	taskresult
14	core	funcionario
15	core	logauditoria
16	core	perfilusuario
17	core	rol
18	mantenedores	areahospitalaria
19	mantenedores	articulo
20	mantenedores	cargo
21	mantenedores	edificio
22	mantenedores	estadoequipo
23	mantenedores	institucion
24	mantenedores	marca
25	mantenedores	modelo
26	mantenedores	modeloanexo
27	mantenedores	piso
28	mantenedores	pma
29	mantenedores	proveedor
30	mantenedores	recinto
31	mantenedores	sector
32	mantenedores	sistemaoperativo
33	mantenedores	unidad
34	mantenedores	vlan
35	equipos	bitacoraequipo
36	equipos	bitacoraopcion
37	equipos	equipo
38	anexos	anexo
39	anexos	requerimientocambio
40	actas	acta
41	actas	actadetalle
42	tickets	archivoadjunto
43	tickets	categoria
44	tickets	gruporesolutor
45	tickets	notificacion
46	tickets	prioridad
47	tickets	ticket
48	tickets	tickethistorial
49	sla	slamatrix
50	correos	configuracionsmtp
51	correos	correolog
52	correos	credencialcorreo
53	correos	grupocorreo
54	correos	miembrogrupocorreo
55	utilidades	ayudarapida
56	utilidades	checklistitem
57	utilidades	pendiente
58	utilidades	webapp
59	visor	avisovisor
60	redes	infraestructurared
61	redes	pma
62	redes	rangoip
63	redes	slaconfiguracion
64	conocimiento	articuloconocimiento
65	conocimiento	categoriaconocimiento
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	mantenedores	0001_initial	2026-08-24 14:20:15.869895+00
2	contenttypes	0001_initial	2026-08-24 14:20:15.899285+00
3	auth	0001_initial	2026-08-24 14:20:16.290867+00
4	actas	0001_initial	2026-08-24 14:20:16.57822+00
5	admin	0001_initial	2026-08-24 14:20:16.756441+00
6	admin	0002_logentry_remove_auto_add	2026-08-24 14:20:16.777238+00
7	admin	0003_logentry_add_action_flag_choices	2026-08-24 14:20:16.80028+00
8	mantenedores	0002_proveedor_rut	2026-08-24 14:20:16.810713+00
9	mantenedores	0003_articulo_imagen	2026-08-24 14:20:16.825276+00
10	mantenedores	0004_cargo	2026-08-24 14:20:16.89495+00
11	mantenedores	0005_alter_piso_edificio_alter_pma_recinto_and_more	2026-08-24 14:20:17.140268+00
12	mantenedores	0006_modeloanexo_marca	2026-08-24 14:20:17.164982+00
13	anexos	0001_initial	2026-08-24 14:20:17.672778+00
14	anexos	0002_remove_anexo_pma_lugar_anexo_pma	2026-08-24 14:20:17.798982+00
15	anexos	0003_anexo_numero_inventario	2026-08-24 14:20:17.859024+00
16	contenttypes	0002_remove_content_type_name	2026-08-24 14:20:17.942816+00
17	auth	0002_alter_permission_name_max_length	2026-08-24 14:20:18.003686+00
18	auth	0003_alter_user_email_max_length	2026-08-24 14:20:18.035703+00
19	auth	0004_alter_user_username_opts	2026-08-24 14:20:18.203429+00
20	auth	0005_alter_user_last_login_null	2026-08-24 14:20:18.232453+00
21	auth	0006_require_contenttypes_0002	2026-08-24 14:20:18.237919+00
22	auth	0007_alter_validators_add_error_messages	2026-08-24 14:20:18.268084+00
23	auth	0008_alter_user_username_max_length	2026-08-24 14:20:18.312434+00
24	auth	0009_alter_user_last_name_max_length	2026-08-24 14:20:18.339762+00
25	auth	0010_alter_group_name_max_length	2026-08-24 14:20:18.394695+00
26	auth	0011_update_proxy_permissions	2026-08-24 14:20:18.447808+00
27	auth	0012_alter_user_first_name_max_length	2026-08-24 14:20:18.47725+00
28	axes	0001_initial	2026-08-24 14:20:18.525151+00
29	axes	0002_auto_20151217_2044	2026-08-24 14:20:18.688114+00
30	axes	0003_auto_20160322_0929	2026-08-24 14:20:18.730198+00
31	axes	0004_auto_20181024_1538	2026-08-24 14:20:18.771393+00
32	axes	0005_remove_accessattempt_trusted	2026-08-24 14:20:18.784658+00
33	axes	0006_remove_accesslog_trusted	2026-08-24 14:20:18.797722+00
34	axes	0007_alter_accessattempt_unique_together	2026-08-24 14:20:18.881129+00
35	axes	0008_accessfailurelog	2026-08-24 14:20:19.024939+00
36	axes	0009_add_session_hash	2026-08-24 14:20:19.041768+00
37	axes	0010_accessattemptexpiration	2026-08-24 14:20:19.087097+00
38	conocimiento	0001_initial	2026-08-24 14:20:19.180526+00
39	core	0001_initial	2026-08-24 14:20:19.76279+00
40	core	0002_funcionario	2026-08-24 14:20:19.892478+00
41	core	0003_funcionario_cargo_old_alter_funcionario_cargo	2026-08-24 14:20:20.030262+00
42	core	0004_alter_logauditoria_options_alter_funcionario_cargo_and_more	2026-08-24 14:20:20.413082+00
43	core	0005_rol_icono	2026-08-24 14:20:20.428185+00
44	core	0006_rol_is_system	2026-08-24 14:20:20.442274+00
45	equipos	0001_initial	2026-08-24 14:20:21.348992+00
46	tickets	0001_initial	2026-08-24 14:20:21.954685+00
47	tickets	0002_ticket_creador_ticket_fecha_vencimiento_sla_and_more	2026-08-24 14:20:22.707941+00
48	tickets	0003_gruporesolutor_categoria_grupo_resolutor_and_more	2026-08-24 14:20:23.096865+00
49	tickets	0004_ticket_anexo_contacto	2026-08-24 14:20:23.174304+00
50	tickets	0005_alter_ticket_solicitante	2026-08-24 14:20:23.417772+00
51	tickets	0006_alter_categoria_grupo_resolutor_and_more	2026-08-24 14:20:23.596991+00
52	tickets	0007_ticket_correo_contacto	2026-08-24 14:20:23.670682+00
53	tickets	0008_gruporesolutor_icono	2026-08-24 14:20:23.742124+00
54	tickets	0009_gruporesolutor_is_system	2026-08-24 14:20:23.80137+00
55	tickets	0010_notificacion	2026-08-24 14:20:23.918146+00
56	correos	0001_initial	2026-08-24 14:20:24.054913+00
57	correos	0002_configuracionsmtp	2026-08-24 14:20:24.086073+00
58	correos	0003_correolog	2026-08-24 14:20:24.250652+00
59	django_celery_results	0001_initial	2026-08-24 14:20:24.302978+00
60	django_celery_results	0002_add_task_name_args_kwargs	2026-08-24 14:20:24.333121+00
61	django_celery_results	0003_auto_20181106_1101	2026-08-24 14:20:24.352216+00
62	django_celery_results	0004_auto_20190516_0412	2026-08-24 14:20:24.487504+00
63	django_celery_results	0005_taskresult_worker	2026-08-24 14:20:24.518796+00
64	django_celery_results	0006_taskresult_date_created	2026-08-24 14:20:24.659226+00
65	django_celery_results	0007_remove_taskresult_hidden	2026-08-24 14:20:24.672004+00
66	django_celery_results	0008_chordcounter	2026-08-24 14:20:24.797268+00
67	django_celery_results	0009_groupresult	2026-08-24 14:20:25.215419+00
68	django_celery_results	0010_remove_duplicate_indices	2026-08-24 14:20:25.243937+00
69	django_celery_results	0011_taskresult_periodic_task_name	2026-08-24 14:20:25.25652+00
70	django_celery_results	0012_taskresult_date_started	2026-08-24 14:20:25.27275+00
71	django_celery_results	0013_taskresult_django_cele_periodi_1993cf_idx	2026-08-24 14:20:25.294817+00
72	django_celery_results	0014_alter_taskresult_status	2026-08-24 14:20:25.308509+00
73	equipos	0002_alter_bitacoraequipo_tipo_registro	2026-08-24 14:20:25.372341+00
74	equipos	0003_alter_bitacoraequipo_solicitante	2026-08-24 14:20:25.88511+00
75	equipos	0004_alter_bitacoraequipo_fecha_devolucion_and_more	2026-08-24 14:20:26.315002+00
76	equipos	0005_equipo_fecha_compra_equipo_mac_address_and_more	2026-08-24 14:20:26.734017+00
77	equipos	0006_add_num_inventario	2026-08-24 14:20:26.885635+00
78	redes	0001_initial	2026-08-24 14:20:27.723056+00
79	sessions	0001_initial	2026-08-24 14:20:27.801009+00
80	sla	0001_initial	2026-08-24 14:20:27.949924+00
81	utilidades	0001_initial	2026-08-24 14:20:28.243465+00
82	visor	0001_initial	2026-08-24 14:20:28.327713+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
fm8q3014gdrnk942qgkjod7qex65itw3	.eJxVjMEOwiAQRP-FsyGk4Lp49O43kGVZpGogKe2p8d9tkx70NMm8N7OqQMtcwtJlCmNSVzWo028XiV9Sd5CeVB9Nc6vzNEa9K_qgXd9bkvftcP8OCvWyrSWzERC0lJ3PsGUUdAiOs8MMTNbDBdkbipzsYPDsEIkkskGEzOrzBQdzOLU:1wmMpG:UCoufWt0Ua96JRiufCRbCNyjI3-jx-qg7n8H8hbsk80	2026-08-05 02:36:50.032136+00
ng0ncycoql241jvwgj4drq20dxxsjhq0	.eJxVjMEOwiAQRP-FsyGk4Lp49O43kGVZpGogKe2p8d9tkx70NMm8N7OqQMtcwtJlCmNSVzWo028XiV9Sd5CeVB9Nc6vzNEa9K_qgXd9bkvftcP8OCvWyrSWzERC0lJ3PsGUUdAiOs8MMTNbDBdkbipzsYPDsEIkkskGEzOrzBQdzOLU:1wmZZB:l5voVjFGAZXjAhZop7WIReG5Iyydl6qitJs7oqhJ46w	2026-08-05 16:13:05.653103+00
y0i54hlyuzedijdt1l9b17mruh4f31rm	.eJxVjMEOwiAQRP-FsyGk4Lp49O43kGVZpGogKe2p8d9tkx70NMm8N7OqQMtcwtJlCmNSVzWo028XiV9Sd5CeVB9Nc6vzNEa9K_qgXd9bkvftcP8OCvWyrSWzERC0lJ3PsGUUdAiOs8MMTNbDBdkbipzsYPDsEIkkskGEzOrzBQdzOLU:1wmiZI:Ad9bMnA4lcgF3krwNvdS3xroI-iMlo117z315n7zG3s	2026-08-06 01:49:48.544492+00
aunsw2v1om7ea6dim1ynp6v6pb46nop2	.eJxVjMEOwiAQRP-FsyGk4Lp49O43kGVZpGogKe2p8d9tkx70NMm8N7OqQMtcwtJlCmNSVzWo028XiV9Sd5CeVB9Nc6vzNEa9K_qgXd9bkvftcP8OCvWyrSWzERC0lJ3PsGUUdAiOs8MMTNbDBdkbipzsYPDsEIkkskGEzOrzBQdzOLU:1wn7V1:BH4bwzSvQBxWHl2szGodbGP2eZAW3NBKeMGhqxDrbEU	2026-08-07 04:27:03.103981+00
x86oqxgyh3tzux4r8t635fbns40qswhi	.eJxVjEEOwiAQRe_C2hAYKFiX7nsGMgyDVA0kpV0Z765NutDtf-_9lwi4rSVsnZcwJ3ERAOL0O0akB9edpDvWW5PU6rrMUe6KPGiXU0v8vB7u30HBXr41ae9VJEN5ZJtVzD4j0llrYDYIPABn1C4qUMqOhMSoLQ_OOANIZMX7AzKXOPw:1wnGXJ:Y5O_9ERDJmH1oeRF_eN7e7HFD-AAyTGGx7Qn1vFdN10	2026-08-07 14:06:01.160522+00
k1dimd2vohsi3a9nl5uz9lxep3wfxlm6	.eJxVjEEOwiAQRe_C2hAYKFiX7nsGMgyDVA0kpV0Z765NutDtf-_9lwi4rSVsnZcwJ3ERAOL0O0akB9edpDvWW5PU6rrMUe6KPGiXU0v8vB7u30HBXr41ae9VJEN5ZJtVzD4j0llrYDYIPABn1C4qUMqOhMSoLQ_OOANIZMX7AzKXOPw:1wnGbT:251k8mqEVsMFJBTKgiEah-j-r9slxu6K9TIxUMg3Bp8	2026-08-07 14:10:19.566552+00
akrx8qwsi6hyzjxq3jhkwiezku2iual9	.eJxVjEEOwiAQRe_C2hAYKFiX7nsGMgyDVA0kpV0Z765NutDtf-_9lwi4rSVsnZcwJ3ERAOL0O0akB9edpDvWW5PU6rrMUe6KPGiXU0v8vB7u30HBXr41ae9VJEN5ZJtVzD4j0llrYDYIPABn1C4qUMqOhMSoLQ_OOANIZMX7AzKXOPw:1wnJPj:T620XURS8vbkJ6bNoZk5EO-mp6D6hG9U7tRfsU1I590	2026-08-07 17:10:23.327472+00
xvxz54jn7uvhqtmqqpemge76ygxebmlv	.eJxVjMEOwiAQRP-FsyGk4Lp49O43kGVZpGogKe2p8d9tkx70NMm8N7OqQMtcwtJlCmNSVzWo028XiV9Sd5CeVB9Nc6vzNEa9K_qgXd9bkvftcP8OCvWyrSWzERC0lJ3PsGUUdAiOs8MMTNbDBdkbipzsYPDsEIkkskGEzOrzBQdzOLU:1wpFzh:4D7jnpAdbaLmXUAZUbw0LaYUUxi9B6vxRSQ_tEL3wqM	2026-08-13 01:55:33.669204+00
dxads9zxdd7wgks13rkmotfytu3r4cf1	.eJxVjMEOwiAQRP-FsyGk4Lp49O43kGVZpGogKe2p8d9tkx70NMm8N7OqQMtcwtJlCmNSVzWo028XiV9Sd5CeVB9Nc6vzNEa9K_qgXd9bkvftcP8OCvWyrSWzERC0lJ3PsGUUdAiOs8MMTNbDBdkbipzsYPDsEIkkskGEzOrzBQdzOLU:1wmKeP:eUaajVhb9XnKwgJsQAudQEM097GB5CRdutHcyMrCq8I	2026-08-05 00:17:29.96236+00
vs34wvsbmuz7ttwz37oaci7mvx8m1mx7	.eJxVjDsOwjAQBe_iGlk4jn-U9DmDtfbu4gCypTipEHeHSCmgfTPzXiLCtpa4dVrijOIiBnH63RLkB9Ud4B3qrcnc6rrMSe6KPGiXU0N6Xg_376BAL986cLIuB-PQ-3MwShvUPHifXLaOfSCLeaRRQRhZGe-YMwA4IICgbSLx_gDg1ziR:1wyVqy:G_i9j2sDWpiRw1BzljUZ9MT1zQx4S14Ysn54Ji4BMcA	2026-09-07 14:40:48.64563+00
vy2j2f2ypbut23lh2jm7fi0ok3fiitc2	.eJxVjDsOwjAQBe_iGlk4jn-U9DmDtfbu4gCypTipEHeHSCmgfTPzXiLCtpa4dVrijOIiBnH63RLkB9Ud4B3qrcnc6rrMSe6KPGiXU0N6Xg_376BAL986cLIuB-PQ-3MwShvUPHifXLaOfSCLeaRRQRhZGe-YMwA4IICgbSLx_gDg1ziR:1wyfkG:ZeQTRFF81Gwvs-nhidbq_F0vbbrL5bzgBgyyYiUUgmY	2026-09-08 01:14:32.165503+00
\.


--
-- Data for Name: equipos_bitacoraequipo; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.equipos_bitacoraequipo (id, fecha_mantenimiento, fecha_devolucion, solicitante_id, falla_reportada, actividades_realizadas, servicio_unidad, tipo_registro, fecha_creacion, tecnico_id, equipo_id) FROM stdin;
\.


--
-- Data for Name: equipos_bitacoraopcion; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.equipos_bitacoraopcion (id, tipo, nombre, activo, orden, fecha_creacion, fecha_actualizacion, creado_por_id) FROM stdin;
1	FALLA	Actualización de Perfil/Status del Activo	t	10	2026-07-14 01:16:37.53+00	2026-07-14 01:16:37.53+00	\N
2	FALLA	Disco con sectores malos.	t	20	2026-07-14 01:16:37.534+00	2026-07-14 01:16:37.534+00	\N
3	FALLA	Disco duro al 100% con 4 GB de RAM.	t	30	2026-07-14 01:16:37.538+00	2026-07-14 01:16:37.538+00	\N
4	FALLA	Disco lleno	t	40	2026-07-14 01:16:37.541+00	2026-07-14 01:16:37.541+00	\N
5	FALLA	Equipo abre multiples ventanas.	t	50	2026-07-14 01:16:37.544+00	2026-07-14 01:16:37.544+00	\N
6	FALLA	Equipo con Bitlocker	t	60	2026-07-14 01:16:37.548+00	2026-07-14 01:16:37.548+00	\N
7	FALLA	Equipo con disco duro danado	t	70	2026-07-14 01:16:37.551+00	2026-07-14 01:16:37.551+00	\N
8	FALLA	Equipo con falla	t	80	2026-07-14 01:16:37.554+00	2026-07-14 01:16:37.554+00	\N
9	FALLA	Equipo con funcionamiento erratico	t	90	2026-07-14 01:16:37.556+00	2026-07-14 01:16:37.556+00	\N
10	FALLA	Equipo con pantallazo azul.	t	100	2026-07-14 01:16:37.559+00	2026-07-14 01:16:37.559+00	\N
11	FALLA	Equipo con SO corrupto	t	110	2026-07-14 01:16:37.562+00	2026-07-14 01:16:37.562+00	\N
12	FALLA	Equipo con sospecha de virus	t	120	2026-07-14 01:16:37.564+00	2026-07-14 01:16:37.564+00	\N
13	FALLA	Equipo con ventilador acelerado	t	130	2026-07-14 01:16:37.567+00	2026-07-14 01:16:37.567+00	\N
14	FALLA	Equipo con Windos 7	t	140	2026-07-14 01:16:37.57+00	2026-07-14 01:16:37.57+00	\N
15	FALLA	Equipo desactualizado	t	150	2026-07-14 01:16:37.573+00	2026-07-14 01:16:37.573+00	\N
16	FALLA	Equipo desactualizado y sin WiFi	t	160	2026-07-14 01:16:37.576+00	2026-07-14 01:16:37.576+00	\N
17	FALLA	Equipo lento	t	170	2026-07-14 01:16:37.578+00	2026-07-14 01:16:37.578+00	\N
18	FALLA	Equipo muy lento	t	180	2026-07-14 01:16:37.581+00	2026-07-14 01:16:37.581+00	\N
19	FALLA	Equipo no arranca	t	190	2026-07-14 01:16:37.584+00	2026-07-14 01:16:37.584+00	\N
20	FALLA	Equipo no arranca (pantalla azul)	t	200	2026-07-14 01:16:37.587+00	2026-07-14 01:16:37.587+00	\N
21	FALLA	Equipo no arranca. Disco danado.	t	210	2026-07-14 01:16:37.59+00	2026-07-14 01:16:37.59+00	\N
22	FALLA	Equipo no detecta el ventilador de la CPU	t	220	2026-07-14 01:16:37.593+00	2026-07-14 01:16:37.593+00	\N
23	FALLA	Equipo no puede instalar actualizaciones.	t	230	2026-07-14 01:16:37.596+00	2026-07-14 01:16:37.596+00	\N
24	FALLA	Equipo pierde la hora y fecha.	t	240	2026-07-14 01:16:37.598+00	2026-07-14 01:16:37.598+00	\N
25	FALLA	Equipo quemado	t	250	2026-07-14 01:16:37.601+00	2026-07-14 01:16:37.601+00	\N
26	FALLA	Equipo reasignado	t	260	2026-07-14 01:16:37.603+00	2026-07-14 01:16:37.603+00	\N
27	FALLA	Equipo reemplazado (UCFH)	t	270	2026-07-14 01:16:37.607+00	2026-07-14 01:16:37.607+00	\N
28	FALLA	Equipo reemplazado por AIO	t	280	2026-07-14 01:16:37.61+00	2026-07-14 01:16:37.61+00	\N
29	FALLA	Equipo reemplazado por AIO HP	t	290	2026-07-14 01:16:37.612+00	2026-07-14 01:16:37.612+00	\N
30	FALLA	Equipo se apago y no enciende pantalla	t	300	2026-07-14 01:16:37.615+00	2026-07-14 01:16:37.615+00	\N
31	FALLA	Equipo sin Office	t	310	2026-07-14 01:16:37.617+00	2026-07-14 01:16:37.617+00	\N
32	FALLA	Etiquetadora	t	320	2026-07-14 01:16:37.62+00	2026-07-14 01:16:37.62+00	\N
33	FALLA	Etiquetadora No detecta el rollo	t	330	2026-07-14 01:16:37.622+00	2026-07-14 01:16:37.622+00	\N
34	FALLA	No funciona pantalla tactil	t	340	2026-07-14 01:16:37.625+00	2026-07-14 01:16:37.625+00	\N
35	FALLA	Problemas con Word	t	350	2026-07-14 01:16:37.627+00	2026-07-14 01:16:37.627+00	\N
36	FALLA	Reemplazado por HP ProOne 440 G9	t	360	2026-07-14 01:16:37.63+00	2026-07-14 01:16:37.63+00	\N
37	FALLA	Tablet Fusion5	t	370	2026-07-14 01:16:37.633+00	2026-07-14 01:16:37.633+00	\N
38	FALLA	Agente antivirus	t	380	2026-07-14 01:16:37.636+00	2026-07-14 01:16:37.636+00	\N
\.


--
-- Data for Name: equipos_equipo; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.equipos_equipo (id, imagen, correlativo, orden_interno, serie_corta, estado_candado, serial_number, ip, anexo, usuario, office, activador, pmalugar, comentario, fecha_creacion, fecha_modificacion, articulo_id, estado_id, marca_id, modelo_id, modificado_por_id, pma_id, proveedor_id, so_id, fecha_compra, mac_address, orden_compra, patch_panel, puerto_red, switch_ip, vencimiento_garantia, num_inventario) FROM stdin;
\.


--
-- Data for Name: mantenedores_areahospitalaria; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.mantenedores_areahospitalaria (id, activo, fecha_creacion, fecha_actualizacion, nombre) FROM stdin;
17	t	2026-07-14 23:08:32.604053+00	2026-07-14 23:08:43.491089+00	Mesa De Ayuda
8	t	2026-07-09 01:38:22.633+00	2026-07-09 01:38:22.633+00	APOYO CLINICO ATENCION DIRECTA
9	t	2026-07-09 01:38:22.7+00	2026-07-09 01:38:22.7+00	ATENCION ABIERTA
10	t	2026-07-09 01:38:23.049+00	2026-07-09 01:38:23.049+00	AREAS DISPONIBLES
11	t	2026-07-09 01:38:23.342+00	2026-07-09 01:38:23.342+00	ATENCION CERRADA
12	t	2026-07-09 01:38:24.047+00	2026-07-09 01:38:24.047+00	AREA ADMINISTRATIVA
13	t	2026-07-09 01:38:24.266+00	2026-07-09 01:38:24.266+00	APOYO CLINICO ATENCION INDIRECTA
14	t	2026-07-09 01:38:24.574+00	2026-07-09 01:38:24.574+00	APOYO GENERAL LOGISTICO
\.


--
-- Data for Name: mantenedores_articulo; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.mantenedores_articulo (id, activo, fecha_creacion, fecha_actualizacion, nombre, imagen) FROM stdin;
4	t	2026-07-15 03:26:49.298886+00	2026-07-15 03:26:49.298907+00	Impresoras	
3	t	2026-07-10 01:45:28.926+00	2026-07-10 01:45:28.926+00	All In One	
5	t	2026-07-15 02:50:11.769+00	2026-07-15 02:50:11.769+00	Impresora Laser	
\.


--
-- Data for Name: mantenedores_cargo; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.mantenedores_cargo (id, activo, fecha_creacion, fecha_actualizacion, nombre) FROM stdin;
3	t	2026-07-12 18:26:54.897+00	2026-07-12 18:26:54.897+00	Subrogante
5	t	2026-07-12 22:59:07.997+00	2026-07-12 22:59:07.997+00	Médico Jefe de Servicio
6	t	2026-07-12 22:59:08+00	2026-07-12 22:59:08+00	Médico Especialista
7	t	2026-07-12 22:59:08.003+00	2026-07-12 22:59:08.003+00	Médico General / EDF
8	t	2026-07-12 22:59:08.005+00	2026-07-12 22:59:08.005+00	Enfermero/a Clínico
9	t	2026-07-12 22:59:08.008+00	2026-07-12 22:59:08.008+00	Enfermero/a Supervisor(a)
10	t	2026-07-12 22:59:08.011+00	2026-07-12 22:59:08.011+00	TENS
11	t	2026-07-12 22:59:08.013+00	2026-07-12 22:59:08.013+00	Profesional Clínico
12	t	2026-07-12 22:59:08.016+00	2026-07-12 22:59:08.016+00	Auxiliar de Servicio
13	t	2026-07-12 22:59:08.019+00	2026-07-12 22:59:08.019+00	Director / Subdirector
14	t	2026-07-12 22:59:08.021+00	2026-07-12 22:59:08.021+00	Profesional Administrativo
15	t	2026-07-12 22:59:08.024+00	2026-07-12 22:59:08.024+00	Técnico Administrativo
16	t	2026-07-12 22:59:08.026+00	2026-07-12 22:59:08.026+00	Administrativo de SOME
17	t	2026-07-12 22:59:08.029+00	2026-07-12 22:59:08.029+00	Coordinador(a) / Encargado(a)
18	t	2026-07-12 22:59:08.031+00	2026-07-12 22:59:08.031+00	Operador(a) de Mesa de Ayuda
19	t	2026-07-12 23:01:03.721+00	2026-07-12 23:07:57.941+00	Jefatura
\.


--
-- Data for Name: mantenedores_edificio; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.mantenedores_edificio (id, activo, fecha_creacion, fecha_actualizacion, nombre, institucion_id) FROM stdin;
2	t	2026-07-09 01:38:22.626+00	2026-07-09 01:38:22.626+00	Edificio Principal	2
\.


--
-- Data for Name: mantenedores_estadoequipo; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.mantenedores_estadoequipo (id, activo, fecha_creacion, fecha_actualizacion, nombre, color_hex) FROM stdin;
6	t	2026-07-09 01:41:31.537+00	2026-07-09 02:08:24.091+00	En Inventario	#17a2b8
3	t	2026-07-09 01:41:31.53+00	2026-07-17 00:32:25.996501+00	Soporte	#ffb900
2	t	2026-07-09 01:41:31.527+00	2026-07-17 00:32:26.001097+00	Funcional	#107c10
5	t	2026-07-09 01:41:31.535+00	2026-07-17 00:32:26.005915+00	No Funcional	#d13438
7	t	2026-07-09 01:41:31.54+00	2026-07-16 22:19:09.716+00	Baja	#a4262c
8	t	2026-07-11 23:59:31.158+00	2026-07-16 22:19:09.713+00	Operativo	#107c10
9	t	2026-07-16 22:19:09.71+00	2026-07-16 22:19:09.718+00	En Bodega	#797775
\.


--
-- Data for Name: mantenedores_institucion; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.mantenedores_institucion (id, activo, fecha_creacion, fecha_actualizacion, codigo, nombre) FROM stdin;
2	t	2026-07-09 01:38:22.624+00	2026-07-09 01:38:22.624+00	HMM	Hospital Marga Marga
\.


--
-- Data for Name: mantenedores_marca; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.mantenedores_marca (id, activo, fecha_creacion, fecha_actualizacion, nombre) FROM stdin;
4	t	2026-07-15 03:27:06.506154+00	2026-07-15 03:27:06.506176+00	Brother
1	t	2026-07-09 00:59:19.958+00	2026-07-09 00:59:19.958+00	Genérica
2	t	2026-07-10 01:22:02.249+00	2026-07-12 03:59:30.414+00	Lenovo
3	t	2026-07-15 02:50:11.774+00	2026-07-15 02:50:11.774+00	HP
\.


--
-- Data for Name: mantenedores_modelo; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.mantenedores_modelo (id, activo, fecha_creacion, fecha_actualizacion, nombre, imagen, marca_id) FROM stdin;
1	t	2026-07-09 00:59:19.959+00	2026-07-12 00:47:41.245+00	Genérico	modelos/sinimagen_UbcvfDn.png	1
2	t	2026-07-10 01:44:47.781+00	2026-07-11 01:17:20.621+00	Thinkcentre Neo 50a 24 Gen 4	modelos/Lenovo.png	2
4	t	2026-07-15 02:50:11.778+00	2026-07-15 02:50:11.778+00	LaserJet Pro M404n		3
\.


--
-- Data for Name: mantenedores_modeloanexo; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.mantenedores_modeloanexo (id, activo, fecha_creacion, fecha_actualizacion, nombre, imagen, marca_id) FROM stdin;
2	t	2026-07-15 00:52:41.852823+00	2026-07-15 00:52:41.852847+00	CP-3905	modelos_anexos/CP-3905.jpg	3
3	t	2026-07-15 01:17:16.680444+00	2026-07-15 01:17:16.680467+00	CP-7841	modelos_anexos/CP-7841.png	3
4	t	2026-07-15 01:17:36.457628+00	2026-07-15 01:17:36.457652+00	IP-PHONE7911	modelos_anexos/IPPhone7911.jpg	3
5	t	2026-07-15 01:17:52.348048+00	2026-07-15 01:17:52.348073+00	IP-PHONE7962	modelos_anexos/IPPhone7962.png	3
\.


--
-- Data for Name: mantenedores_piso; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.mantenedores_piso (id, activo, fecha_creacion, fecha_actualizacion, nombre, alias, edificio_id) FROM stdin;
9	t	2026-07-09 01:38:22.628+00	2026-07-09 01:38:22.628+00	1	\N	2
10	t	2026-07-09 01:38:22.856+00	2026-07-09 01:38:22.856+00	2	\N	2
11	t	2026-07-09 01:38:23.118+00	2026-07-09 01:38:23.118+00	3	\N	2
12	t	2026-07-09 01:38:23.314+00	2026-07-09 01:38:23.314+00	4	\N	2
13	t	2026-07-09 01:38:23.339+00	2026-07-09 01:38:23.34+00	5	\N	2
14	t	2026-07-09 01:38:23.545+00	2026-07-09 01:38:23.545+00	6	\N	2
15	t	2026-07-09 01:38:24.047+00	2026-07-09 01:38:24.047+00	Auditorio	\N	2
16	t	2026-07-09 01:38:24.822+00	2026-07-09 01:38:24.822+00	7	\N	2
\.


--
-- Data for Name: mantenedores_pma; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.mantenedores_pma (id, activo, fecha_creacion, fecha_actualizacion, nombre, recinto_id) FROM stdin;
507	t	2026-07-09 01:38:22.636+00	2026-07-09 01:38:22.636+00	J-1-24	203
508	t	2026-07-09 01:38:22.652+00	2026-07-09 01:38:22.652+00	J-1-16	204
509	t	2026-07-09 01:38:22.658+00	2026-07-09 01:38:22.658+00	J-1-36	205
510	t	2026-07-09 01:38:22.661+00	2026-07-09 01:38:22.661+00	J-1-10	206
511	t	2026-07-09 01:38:22.664+00	2026-07-09 01:38:22.664+00	J-1-11	207
512	t	2026-07-09 01:38:22.667+00	2026-07-09 01:38:22.667+00	J-1-35	208
513	t	2026-07-09 01:38:22.67+00	2026-07-09 01:38:22.67+00	J-1-2	209
514	t	2026-07-09 01:38:22.682+00	2026-07-09 01:38:22.682+00	J-1-34	210
515	t	2026-07-09 01:38:22.685+00	2026-07-09 01:38:22.685+00	J-1-1	211
516	t	2026-07-09 01:38:22.688+00	2026-07-09 01:38:22.688+00	J-1-7	212
517	t	2026-07-09 01:38:22.691+00	2026-07-09 01:38:22.691+00	J-1-9	212
518	t	2026-07-09 01:38:22.694+00	2026-07-09 01:38:22.694+00	J-1-8	212
519	t	2026-07-09 01:38:22.697+00	2026-07-09 01:38:22.697+00	J-1-6	212
520	t	2026-07-09 01:38:22.702+00	2026-07-09 01:38:22.702+00	J-1-46	210
521	t	2026-07-09 01:38:22.705+00	2026-07-09 01:38:22.705+00	J-1-47	213
522	t	2026-07-09 01:38:22.708+00	2026-07-09 01:38:22.708+00	J-1-5	214
523	t	2026-07-09 01:38:22.714+00	2026-07-09 01:38:22.715+00	E-1-1	215
524	t	2026-07-09 01:38:22.727+00	2026-07-09 01:38:22.727+00	J-1-44	216
525	t	2026-07-09 01:38:22.745+00	2026-07-09 01:38:22.745+00	E-1-48	217
526	t	2026-07-09 01:38:22.748+00	2026-07-09 01:38:22.748+00	E-1-49	218
527	t	2026-07-09 01:38:22.751+00	2026-07-09 01:38:22.751+00	E-1-43	219
528	t	2026-07-09 01:38:22.768+00	2026-07-09 01:38:22.768+00	E-1-57	220
529	t	2026-07-09 01:38:22.771+00	2026-07-09 01:38:22.771+00	E-1-45	220
530	t	2026-07-09 01:38:22.777+00	2026-07-09 01:38:22.777+00	E-1-11	221
531	t	2026-07-09 01:38:22.78+00	2026-07-09 01:38:22.78+00	E-1-21	222
532	t	2026-07-09 01:38:22.783+00	2026-07-09 01:38:22.783+00	E-1-33	223
533	t	2026-07-09 01:38:22.786+00	2026-07-09 01:38:22.786+00	E-1-10	224
534	t	2026-07-09 01:38:22.789+00	2026-07-09 01:38:22.789+00	E-1-6	225
535	t	2026-07-09 01:38:22.791+00	2026-07-09 01:38:22.791+00	E-1-5	225
536	t	2026-07-09 01:38:22.794+00	2026-07-09 01:38:22.794+00	E-1-7	225
537	t	2026-07-09 01:38:22.797+00	2026-07-09 01:38:22.797+00	E-1-25	226
538	t	2026-07-09 01:38:22.801+00	2026-07-09 01:38:22.801+00	E-1-22	227
539	t	2026-07-09 01:38:22.804+00	2026-07-09 01:38:22.804+00	E-1-18	228
540	t	2026-07-09 01:38:22.806+00	2026-07-09 01:38:22.806+00	E-1-20	229
541	t	2026-07-09 01:38:22.809+00	2026-07-09 01:38:22.809+00	E-1-3	230
542	t	2026-07-09 01:38:22.812+00	2026-07-09 01:38:22.812+00	E-1-47	230
543	t	2026-07-09 01:38:22.815+00	2026-07-09 01:38:22.815+00	E-1-38	220
544	t	2026-07-09 01:38:22.819+00	2026-07-09 01:38:22.819+00	E-1-46	210
545	t	2026-07-09 01:38:22.822+00	2026-07-09 01:38:22.822+00	E-1-23	231
546	t	2026-07-09 01:38:22.824+00	2026-07-09 01:38:22.824+00	E-1-24	231
547	t	2026-07-09 01:38:22.828+00	2026-07-09 01:38:22.828+00	E-1-17	232
548	t	2026-07-09 01:38:22.831+00	2026-07-09 01:38:22.831+00	E-1-8	233
549	t	2026-07-09 01:38:22.833+00	2026-07-09 01:38:22.833+00	E-1-9	233
550	t	2026-07-09 01:38:22.836+00	2026-07-09 01:38:22.836+00	E-1-19	234
551	t	2026-07-09 01:38:22.839+00	2026-07-09 01:38:22.839+00	E-1-37	235
552	t	2026-07-09 01:38:22.842+00	2026-07-09 01:38:22.842+00	E-1-12	221
553	t	2026-07-09 01:38:22.845+00	2026-07-09 01:38:22.845+00	E-1-13	221
554	t	2026-07-09 01:38:22.848+00	2026-07-09 01:38:22.848+00	E-1-14	221
555	t	2026-07-09 01:38:22.851+00	2026-07-09 01:38:22.851+00	E-1-15	221
556	t	2026-07-09 01:38:22.854+00	2026-07-09 01:38:22.854+00	E-1-16	221
557	t	2026-07-09 01:38:22.865+00	2026-07-09 01:38:22.865+00	J-2-11	236
558	t	2026-07-09 01:38:22.877+00	2026-07-09 01:38:22.877+00	J-2-32	209
559	t	2026-07-09 01:38:22.88+00	2026-07-09 01:38:22.88+00	J-2-23	237
560	t	2026-07-09 01:38:22.883+00	2026-07-09 01:38:22.883+00	J-2-58	226
561	t	2026-07-09 01:38:22.886+00	2026-07-09 01:38:22.886+00	J-2-52	238
562	t	2026-07-09 01:38:22.889+00	2026-07-09 01:38:22.889+00	J-2-51	238
563	t	2026-07-09 01:38:22.892+00	2026-07-09 01:38:22.892+00	J-2-61	238
564	t	2026-07-09 01:38:22.895+00	2026-07-09 01:38:22.895+00	J-2-48	238
565	t	2026-07-09 01:38:22.898+00	2026-07-09 01:38:22.898+00	J-2-56	239
566	t	2026-07-09 01:38:22.901+00	2026-07-09 01:38:22.901+00	J-2-63	220
567	t	2026-07-09 01:38:22.903+00	2026-07-09 01:38:22.903+00	J-2-30	220
568	t	2026-07-09 01:38:22.906+00	2026-07-09 01:38:22.906+00	J-2-6	237
569	t	2026-07-09 01:38:22.909+00	2026-07-09 01:38:22.909+00	J-2-7	237
570	t	2026-07-09 01:38:22.912+00	2026-07-09 01:38:22.912+00	J-2-9	240
571	t	2026-07-09 01:38:22.915+00	2026-07-09 01:38:22.915+00	J-2-8	241
572	t	2026-07-09 01:38:22.918+00	2026-07-09 01:38:22.918+00	J-2-47	238
573	t	2026-07-09 01:38:22.921+00	2026-07-09 01:38:22.921+00	J-2-49	238
574	t	2026-07-09 01:38:22.924+00	2026-07-09 01:38:22.924+00	J-2-46	238
575	t	2026-07-09 01:38:22.927+00	2026-07-09 01:38:22.927+00	J-2-50	238
576	t	2026-07-09 01:38:22.93+00	2026-07-09 01:38:22.93+00	J-2-13	242
577	t	2026-07-09 01:38:22.936+00	2026-07-09 01:38:22.936+00	J-2-5	243
578	t	2026-07-09 01:38:22.938+00	2026-07-09 01:38:22.938+00	J-2-12	210
579	t	2026-07-09 01:38:22.943+00	2026-07-09 01:38:22.943+00	J-2-34	244
580	t	2026-07-09 01:38:22.955+00	2026-07-09 01:38:22.955+00	J-2-68	245
581	t	2026-07-09 01:38:22.957+00	2026-07-09 01:38:22.957+00	J-2-67	245
582	t	2026-07-09 01:38:22.961+00	2026-07-09 01:38:22.961+00	J-2-66	246
583	t	2026-07-09 01:38:22.963+00	2026-07-09 01:38:22.963+00	J-2-40	210
584	t	2026-07-09 01:38:22.966+00	2026-07-09 01:38:22.966+00	J-2-39	247
585	t	2026-07-09 01:38:22.975+00	2026-07-09 01:38:22.975+00	J-2-33	248
586	t	2026-07-09 01:38:22.981+00	2026-07-09 01:38:22.981+00	J-2-43	230
587	t	2026-07-09 01:38:22.983+00	2026-07-09 01:38:22.983+00	J-2-3	214
588	t	2026-07-09 01:38:22.99+00	2026-07-09 01:38:22.99+00	E-2-2	249
589	t	2026-07-09 01:38:23.002+00	2026-07-09 01:38:23.002+00	E-2-60	226
590	t	2026-07-09 01:38:23.006+00	2026-07-09 01:38:23.006+00	E-2-59	212
591	t	2026-07-09 01:38:23.009+00	2026-07-09 01:38:23.009+00	E-2-58	212
592	t	2026-07-09 01:38:23.013+00	2026-07-09 01:38:23.013+00	E-2-57	250
593	t	2026-07-09 01:38:23.016+00	2026-07-09 01:38:23.016+00	E-2-61	251
594	t	2026-07-09 01:38:23.038+00	2026-07-09 01:38:23.038+00	E-2-24	252
595	t	2026-07-09 01:38:23.041+00	2026-07-09 01:38:23.041+00	E-2-52	230
596	t	2026-07-09 01:38:23.044+00	2026-07-09 01:38:23.044+00	E-2-55	220
597	t	2026-07-09 01:38:23.047+00	2026-07-09 01:38:23.047+00	E-2-4	230
598	t	2026-07-09 01:38:23.05+00	2026-07-09 01:38:23.05+00	E-2-1	253
599	t	2026-07-09 01:38:23.053+00	2026-07-09 01:38:23.053+00	E-2-14	231
600	t	2026-07-09 01:38:23.056+00	2026-07-09 01:38:23.056+00	E-2-13	231
601	t	2026-07-09 01:38:23.059+00	2026-07-09 01:38:23.059+00	E-2-9	254
602	t	2026-07-09 01:38:23.062+00	2026-07-09 01:38:23.062+00	E-2-8	254
603	t	2026-07-09 01:38:23.065+00	2026-07-09 01:38:23.065+00	E-2-7	255
604	t	2026-07-09 01:38:23.068+00	2026-07-09 01:38:23.068+00	E-2-6	252
605	t	2026-07-09 01:38:23.071+00	2026-07-09 01:38:23.071+00	E-2-12	256
606	t	2026-07-09 01:38:23.074+00	2026-07-09 01:38:23.074+00	E-2-11	256
607	t	2026-07-09 01:38:23.077+00	2026-07-09 01:38:23.077+00	E-2-25	257
608	t	2026-07-09 01:38:23.08+00	2026-07-09 01:38:23.08+00	E-2-15	226
609	t	2026-07-09 01:38:23.083+00	2026-07-09 01:38:23.083+00	E-2-17	220
610	t	2026-07-09 01:38:23.089+00	2026-07-09 01:38:23.089+00	E-2-44	258
611	t	2026-07-09 01:38:23.092+00	2026-07-09 01:38:23.092+00	E-2-45	231
612	t	2026-07-09 01:38:23.095+00	2026-07-09 01:38:23.095+00	E-2-37	225
613	t	2026-07-09 01:38:23.098+00	2026-07-09 01:38:23.098+00	E-2-39	225
614	t	2026-07-09 01:38:23.101+00	2026-07-09 01:38:23.101+00	E-2-38	225
615	t	2026-07-09 01:38:23.104+00	2026-07-09 01:38:23.104+00	E-2-40	259
616	t	2026-07-09 01:38:23.106+00	2026-07-09 01:38:23.107+00	E-2-41	259
617	t	2026-07-09 01:38:23.11+00	2026-07-09 01:38:23.11+00	E-2-42	260
618	t	2026-07-09 01:38:23.113+00	2026-07-09 01:38:23.113+00	E-2-43	261
619	t	2026-07-09 01:38:23.115+00	2026-07-09 01:38:23.115+00	E-2-10	262
620	t	2026-07-09 01:38:23.122+00	2026-07-09 01:38:23.122+00	J-3-2	263
621	t	2026-07-09 01:38:23.134+00	2026-07-09 01:38:23.134+00	J-3-42	264
622	t	2026-07-09 01:38:23.143+00	2026-07-09 01:38:23.143+00	J-3-51	265
623	t	2026-07-09 01:38:23.145+00	2026-07-09 01:38:23.145+00	J-3-38	226
624	t	2026-07-09 01:38:23.148+00	2026-07-09 01:38:23.148+00	J-3-41	264
625	t	2026-07-09 01:38:23.156+00	2026-07-09 01:38:23.156+00	J-3-50	266
626	t	2026-07-09 01:38:23.159+00	2026-07-09 01:38:23.159+00	J-3-60	267
627	t	2026-07-09 01:38:23.163+00	2026-07-09 01:38:23.163+00	J-3-61	268
628	t	2026-07-09 01:38:23.169+00	2026-07-09 01:38:23.169+00	J-3-27	269
629	t	2026-07-09 01:38:23.175+00	2026-07-09 01:38:23.175+00	J-3-14	209
630	t	2026-07-09 01:38:23.181+00	2026-07-09 01:38:23.181+00	J-3-31	270
631	t	2026-07-09 01:38:23.184+00	2026-07-09 01:38:23.184+00	J-3-6	271
632	t	2026-07-09 01:38:23.187+00	2026-07-09 01:38:23.187+00	J-3-3	272
633	t	2026-07-09 01:38:23.19+00	2026-07-09 01:38:23.19+00	J-3-26	211
634	t	2026-07-09 01:38:23.193+00	2026-07-09 01:38:23.193+00	J-3-35	273
635	t	2026-07-09 01:38:23.195+00	2026-07-09 01:38:23.195+00	J-3-37	220
636	t	2026-07-09 01:38:23.198+00	2026-07-09 01:38:23.198+00	E-3-50	226
637	t	2026-07-09 01:38:23.202+00	2026-07-09 01:38:23.202+00	E-3-58	274
638	t	2026-07-09 01:38:23.205+00	2026-07-09 01:38:23.205+00	E-3-45	275
639	t	2026-07-09 01:38:23.207+00	2026-07-09 01:38:23.207+00	E-3-56	230
640	t	2026-07-09 01:38:23.21+00	2026-07-09 01:38:23.21+00	E-3-57	220
641	t	2026-07-09 01:38:23.213+00	2026-07-09 01:38:23.213+00	E-3-46	275
642	t	2026-07-09 01:38:23.216+00	2026-07-09 01:38:23.216+00	E-3-47	275
643	t	2026-07-09 01:38:23.22+00	2026-07-09 01:38:23.22+00	E-3-48	275
644	t	2026-07-09 01:38:23.224+00	2026-07-09 01:38:23.224+00	E-3-49	275
645	t	2026-07-09 01:38:23.227+00	2026-07-09 01:38:23.227+00	E-3-44	275
646	t	2026-07-09 01:38:23.23+00	2026-07-09 01:38:23.23+00	E-3-17	225
647	t	2026-07-09 01:38:23.233+00	2026-07-09 01:38:23.233+00	E-3-9	225
648	t	2026-07-09 01:38:23.236+00	2026-07-09 01:38:23.236+00	E-3-32	259
649	t	2026-07-09 01:38:23.239+00	2026-07-09 01:38:23.239+00	E-3-52	276
650	t	2026-07-09 01:38:23.242+00	2026-07-09 01:38:23.242+00	E-3-2	230
651	t	2026-07-09 01:38:23.245+00	2026-07-09 01:38:23.245+00	E-3-40	220
652	t	2026-07-09 01:38:23.248+00	2026-07-09 01:38:23.248+00	E-3-24	231
653	t	2026-07-09 01:38:23.251+00	2026-07-09 01:38:23.251+00	E-3-25	231
654	t	2026-07-09 01:38:23.254+00	2026-07-09 01:38:23.254+00	E-3-10	225
655	t	2026-07-09 01:38:23.257+00	2026-07-09 01:38:23.257+00	E-3-11	225
656	t	2026-07-09 01:38:23.26+00	2026-07-09 01:38:23.26+00	E-3-8	225
657	t	2026-07-09 01:38:23.263+00	2026-07-09 01:38:23.263+00	E-3-7	225
658	t	2026-07-09 01:38:23.266+00	2026-07-09 01:38:23.266+00	E-3-6	225
659	t	2026-07-09 01:38:23.269+00	2026-07-09 01:38:23.269+00	E-3-5	225
660	t	2026-07-09 01:38:23.272+00	2026-07-09 01:38:23.272+00	E-3-4	225
661	t	2026-07-09 01:38:23.275+00	2026-07-09 01:38:23.275+00	E-3-15	225
662	t	2026-07-09 01:38:23.278+00	2026-07-09 01:38:23.278+00	E-3-16	225
663	t	2026-07-09 01:38:23.283+00	2026-07-09 01:38:23.283+00	E-3-19	277
664	t	2026-07-09 01:38:23.286+00	2026-07-09 01:38:23.286+00	E-3-18	278
665	t	2026-07-09 01:38:23.288+00	2026-07-09 01:38:23.288+00	E-3-23	279
666	t	2026-07-09 01:38:23.292+00	2026-07-09 01:38:23.292+00	E-3-37	280
667	t	2026-07-09 01:38:23.294+00	2026-07-09 01:38:23.294+00	E-3-12	225
668	t	2026-07-09 01:38:23.297+00	2026-07-09 01:38:23.297+00	E-3-13	225
669	t	2026-07-09 01:38:23.3+00	2026-07-09 01:38:23.3+00	E-3-14	225
670	t	2026-07-09 01:38:23.303+00	2026-07-09 01:38:23.303+00	E-3-22	281
671	t	2026-07-09 01:38:23.306+00	2026-07-09 01:38:23.306+00	E-3-21	282
672	t	2026-07-09 01:38:23.309+00	2026-07-09 01:38:23.309+00	E-3-20	283
673	t	2026-07-09 01:38:23.312+00	2026-07-09 01:38:23.312+00	E-3-41	226
674	t	2026-07-09 01:38:23.343+00	2026-07-09 01:38:23.343+00	M-5-17	209
675	t	2026-07-09 01:38:23.35+00	2026-07-09 01:38:23.35+00	M-5-18	284
676	t	2026-07-09 01:38:23.352+00	2026-07-09 01:38:23.352+00	M-5-55	285
677	t	2026-07-09 01:38:23.355+00	2026-07-09 01:38:23.355+00	M-5-54	285
678	t	2026-07-09 01:38:23.358+00	2026-07-09 01:38:23.358+00	M-5-25	265
679	t	2026-07-09 01:38:23.361+00	2026-07-09 01:38:23.361+00	M-5-49	286
680	t	2026-07-09 01:38:23.364+00	2026-07-09 01:38:23.364+00	M-5-50	287
681	t	2026-07-09 01:38:23.367+00	2026-07-09 01:38:23.367+00	M-5-21	287
682	t	2026-07-09 01:38:23.37+00	2026-07-09 01:38:23.37+00	M-5-22	287
683	t	2026-07-09 01:38:23.373+00	2026-07-09 01:38:23.373+00	M-5-42	288
684	t	2026-07-09 01:38:23.378+00	2026-07-09 01:38:23.378+00	M-5-32	264
685	t	2026-07-09 01:38:23.387+00	2026-07-09 01:38:23.387+00	M-5-19	289
686	t	2026-07-09 01:38:23.39+00	2026-07-09 01:38:23.39+00	M-5-20	287
687	t	2026-07-09 01:38:23.393+00	2026-07-09 01:38:23.393+00	M-5-9	220
688	t	2026-07-09 01:38:23.399+00	2026-07-09 01:38:23.399+00	M-5-4	290
689	t	2026-07-09 01:38:23.402+00	2026-07-09 01:38:23.402+00	M-5-27	291
690	t	2026-07-09 01:38:23.404+00	2026-07-09 01:38:23.404+00	M-5-26	291
691	t	2026-07-09 01:38:23.407+00	2026-07-09 01:38:23.407+00	M-5-15	250
692	t	2026-07-09 01:38:23.41+00	2026-07-09 01:38:23.41+00	N-5-44	291
693	t	2026-07-09 01:38:23.413+00	2026-07-09 01:38:23.413+00	N-5-8	291
694	t	2026-07-09 01:38:23.416+00	2026-07-09 01:38:23.416+00	N-5-11	250
695	t	2026-07-09 01:38:23.419+00	2026-07-09 01:38:23.419+00	N-5-13	287
696	t	2026-07-09 01:38:23.422+00	2026-07-09 01:38:23.422+00	N-5-10	287
697	t	2026-07-09 01:38:23.425+00	2026-07-09 01:38:23.425+00	N-5-14	287
698	t	2026-07-09 01:38:23.428+00	2026-07-09 01:38:23.428+00	N-5-67	285
699	t	2026-07-09 01:38:23.43+00	2026-07-09 01:38:23.43+00	N-5-38	288
700	t	2026-07-09 01:38:23.436+00	2026-07-09 01:38:23.436+00	N-5-35	264
701	t	2026-07-09 01:38:23.444+00	2026-07-09 01:38:23.444+00	N-5-68	285
702	t	2026-07-09 01:38:23.447+00	2026-07-09 01:38:23.447+00	N-5-69	285
703	t	2026-07-09 01:38:23.45+00	2026-07-09 01:38:23.45+00	N-5-46	287
704	t	2026-07-09 01:38:23.452+00	2026-07-09 01:38:23.452+00	N-5-45	287
705	t	2026-07-09 01:38:23.456+00	2026-07-09 01:38:23.456+00	N-5-19	287
706	t	2026-07-09 01:38:23.458+00	2026-07-09 01:38:23.458+00	N-5-47	287
707	t	2026-07-09 01:38:23.461+00	2026-07-09 01:38:23.461+00	N-5-20	287
708	t	2026-07-09 01:38:23.464+00	2026-07-09 01:38:23.464+00	N-5-18	287
709	t	2026-07-09 01:38:23.466+00	2026-07-09 01:38:23.466+00	N-5-21	265
710	t	2026-07-09 01:38:23.47+00	2026-07-09 01:38:23.47+00	N-5-16	284
711	t	2026-07-09 01:38:23.472+00	2026-07-09 01:38:23.472+00	N-5-43	209
712	t	2026-07-09 01:38:23.478+00	2026-07-09 01:38:23.478+00	N-5-37	209
713	t	2026-07-09 01:38:23.483+00	2026-07-09 01:38:23.483+00	N-5-17	284
714	t	2026-07-09 01:38:23.486+00	2026-07-09 01:38:23.486+00	O-5-18	291
715	t	2026-07-09 01:38:23.489+00	2026-07-09 01:38:23.489+00	O-5-6	250
716	t	2026-07-09 01:38:23.492+00	2026-07-09 01:38:23.492+00	O-5-17	291
717	t	2026-07-09 01:38:23.495+00	2026-07-09 01:38:23.495+00	O-5-14	287
718	t	2026-07-09 01:38:23.498+00	2026-07-09 01:38:23.498+00	O-5-27	287
719	t	2026-07-09 01:38:23.501+00	2026-07-09 01:38:23.501+00	O-5-10	287
720	t	2026-07-09 01:38:23.503+00	2026-07-09 01:38:23.503+00	O-5-49	285
721	t	2026-07-09 01:38:23.506+00	2026-07-09 01:38:23.506+00	O-5-50	285
722	t	2026-07-09 01:38:23.509+00	2026-07-09 01:38:23.509+00	O-5-51	285
723	t	2026-07-09 01:38:23.512+00	2026-07-09 01:38:23.512+00	O-5-19	264
724	t	2026-07-09 01:38:23.52+00	2026-07-09 01:38:23.52+00	O-5-28	288
725	t	2026-07-09 01:38:23.526+00	2026-07-09 01:38:23.526+00	O-5-31	287
726	t	2026-07-09 01:38:23.529+00	2026-07-09 01:38:23.529+00	O-5-12	287
727	t	2026-07-09 01:38:23.531+00	2026-07-09 01:38:23.531+00	O-5-15	265
728	t	2026-07-09 01:38:23.534+00	2026-07-09 01:38:23.534+00	O-5-8	287
729	t	2026-07-09 01:38:23.537+00	2026-07-09 01:38:23.537+00	O-5-29	287
730	t	2026-07-09 01:38:23.54+00	2026-07-09 01:38:23.54+00	O-5-9	287
731	t	2026-07-09 01:38:23.542+00	2026-07-09 01:38:23.542+00	O-5-30	287
732	t	2026-07-09 01:38:23.55+00	2026-07-09 01:38:23.55+00	M-6-7	209
733	t	2026-07-09 01:38:23.555+00	2026-07-09 01:38:23.555+00	M-6-8	284
734	t	2026-07-09 01:38:23.558+00	2026-07-09 01:38:23.558+00	M-6-11	286
735	t	2026-07-09 01:38:23.561+00	2026-07-09 01:38:23.561+00	M-6-12	286
736	t	2026-07-09 01:38:23.564+00	2026-07-09 01:38:23.564+00	M-6-16	265
737	t	2026-07-09 01:38:23.566+00	2026-07-09 01:38:23.567+00	M-6-13	286
738	t	2026-07-09 01:38:23.569+00	2026-07-09 01:38:23.569+00	M-6-30	286
739	t	2026-07-09 01:38:23.572+00	2026-07-09 01:38:23.572+00	M-6-39	286
740	t	2026-07-09 01:38:23.575+00	2026-07-09 01:38:23.575+00	M-6-60	285
741	t	2026-07-09 01:38:23.578+00	2026-07-09 01:38:23.578+00	M-6-34	288
742	t	2026-07-09 01:38:23.584+00	2026-07-09 01:38:23.584+00	M-6-20	264
743	t	2026-07-09 01:38:23.592+00	2026-07-09 01:38:23.592+00	M-6-61	285
744	t	2026-07-09 01:38:23.595+00	2026-07-09 01:38:23.595+00	M-6-62	285
745	t	2026-07-09 01:38:23.598+00	2026-07-09 01:38:23.598+00	M-6-32	286
746	t	2026-07-09 01:38:23.6+00	2026-07-09 01:38:23.6+00	M-6-33	286
747	t	2026-07-09 01:38:23.604+00	2026-07-09 01:38:23.604+00	M-6-2	292
748	t	2026-07-09 01:38:23.607+00	2026-07-09 01:38:23.607+00	M-6-4	293
749	t	2026-07-09 01:38:23.611+00	2026-07-09 01:38:23.611+00	M-6-9	286
750	t	2026-07-09 01:38:23.614+00	2026-07-09 01:38:23.614+00	M-6-31	286
751	t	2026-07-09 01:38:23.617+00	2026-07-09 01:38:23.617+00	M-6-10	286
752	t	2026-07-09 01:38:23.62+00	2026-07-09 01:38:23.62+00	M-6-18	291
753	t	2026-07-09 01:38:23.623+00	2026-07-09 01:38:23.623+00	M-6-17	291
754	t	2026-07-09 01:38:23.625+00	2026-07-09 01:38:23.625+00	M-6-5	250
755	t	2026-07-09 01:38:23.628+00	2026-07-09 01:38:23.628+00	N-6-42	291
756	t	2026-07-09 01:38:23.631+00	2026-07-09 01:38:23.631+00	N-6-51	291
757	t	2026-07-09 01:38:23.634+00	2026-07-09 01:38:23.634+00	N-6-44	250
758	t	2026-07-09 01:38:23.637+00	2026-07-09 01:38:23.637+00	N-6-67	285
759	t	2026-07-09 01:38:23.639+00	2026-07-09 01:38:23.639+00	N-6-27	288
760	t	2026-07-09 01:38:23.645+00	2026-07-09 01:38:23.645+00	N-6-25	264
761	t	2026-07-09 01:38:23.654+00	2026-07-09 01:38:23.654+00	N-6-68	285
762	t	2026-07-09 01:38:23.657+00	2026-07-09 01:38:23.657+00	N-6-69	285
763	t	2026-07-09 01:38:23.66+00	2026-07-09 01:38:23.66+00	N-6-33	287
764	t	2026-07-09 01:38:23.663+00	2026-07-09 01:38:23.663+00	N-6-13	287
765	t	2026-07-09 01:38:23.666+00	2026-07-09 01:38:23.666+00	N-6-35	287
766	t	2026-07-09 01:38:23.669+00	2026-07-09 01:38:23.669+00	N-6-14	287
767	t	2026-07-09 01:38:23.671+00	2026-07-09 01:38:23.671+00	N-6-12	287
768	t	2026-07-09 01:38:23.674+00	2026-07-09 01:38:23.674+00	N-6-15	265
769	t	2026-07-09 01:38:23.677+00	2026-07-09 01:38:23.677+00	N-6-10	284
770	t	2026-07-09 01:38:23.68+00	2026-07-09 01:38:23.68+00	N-6-32	209
771	t	2026-07-09 01:38:23.686+00	2026-07-09 01:38:23.686+00	N-6-26	209
772	t	2026-07-09 01:38:23.691+00	2026-07-09 01:38:23.691+00	N-6-11	284
773	t	2026-07-09 01:38:23.694+00	2026-07-09 01:38:23.694+00	O-6-17	291
774	t	2026-07-09 01:38:23.697+00	2026-07-09 01:38:23.697+00	O-6-6	250
775	t	2026-07-09 01:38:23.7+00	2026-07-09 01:38:23.7+00	O-6-16	291
776	t	2026-07-09 01:38:23.702+00	2026-07-09 01:38:23.702+00	O-6-13	287
777	t	2026-07-09 01:38:23.705+00	2026-07-09 01:38:23.705+00	O-6-26	287
778	t	2026-07-09 01:38:23.708+00	2026-07-09 01:38:23.708+00	O-6-10	287
779	t	2026-07-09 01:38:23.711+00	2026-07-09 01:38:23.711+00	O-6-43	285
780	t	2026-07-09 01:38:23.714+00	2026-07-09 01:38:23.714+00	O-6-44	285
781	t	2026-07-09 01:38:23.717+00	2026-07-09 01:38:23.717+00	O-6-45	285
782	t	2026-07-09 01:38:23.719+00	2026-07-09 01:38:23.719+00	O-6-18	264
783	t	2026-07-09 01:38:23.728+00	2026-07-09 01:38:23.728+00	O-6-27	288
784	t	2026-07-09 01:38:23.736+00	2026-07-09 01:38:23.736+00	O-6-11	287
785	t	2026-07-09 01:38:23.739+00	2026-07-09 01:38:23.739+00	O-6-14	265
786	t	2026-07-09 01:38:23.742+00	2026-07-09 01:38:23.742+00	O-6-8	287
787	t	2026-07-09 01:38:23.744+00	2026-07-09 01:38:23.744+00	O-6-29	287
788	t	2026-07-09 01:38:23.747+00	2026-07-09 01:38:23.747+00	O-6-9	287
789	t	2026-07-09 01:38:23.75+00	2026-07-09 01:38:23.75+00	O-6-28	287
790	t	2026-07-09 01:38:23.757+00	2026-07-09 01:38:23.757+00	D-1-59	294
791	t	2026-07-09 01:38:23.774+00	2026-07-09 01:38:23.774+00	D-1-60	294
792	t	2026-07-09 01:38:23.78+00	2026-07-09 01:38:23.78+00	D-1-58	295
793	t	2026-07-09 01:38:23.785+00	2026-07-09 01:38:23.785+00	D-1-57	296
794	t	2026-07-09 01:38:23.79+00	2026-07-09 01:38:23.79+00	D-1-61	297
795	t	2026-07-09 01:38:23.795+00	2026-07-09 01:38:23.795+00	D-1-56	296
796	t	2026-07-09 01:38:23.834+00	2026-07-09 01:38:23.834+00	D-1-22	298
797	t	2026-07-09 01:38:23.836+00	2026-07-09 01:38:23.836+00	D-1-18	299
798	t	2026-07-09 01:38:23.839+00	2026-07-09 01:38:23.839+00	D-1-17	300
799	t	2026-07-09 01:38:23.842+00	2026-07-09 01:38:23.842+00	D-1-16	301
800	t	2026-07-09 01:38:23.845+00	2026-07-09 01:38:23.845+00	D-1-15	302
801	t	2026-07-09 01:38:23.847+00	2026-07-09 01:38:23.847+00	D-1-13	250
802	t	2026-07-09 01:38:23.858+00	2026-07-09 01:38:23.858+00	D-1-49	303
803	t	2026-07-09 01:38:23.864+00	2026-07-09 01:38:23.864+00	D-1-53	304
804	t	2026-07-09 01:38:23.872+00	2026-07-09 01:38:23.872+00	D-1-24	250
805	t	2026-07-09 01:38:23.877+00	2026-07-09 01:38:23.877+00	D-1-23	305
806	t	2026-07-09 01:38:23.88+00	2026-07-09 01:38:23.88+00	D-1-14	306
807	t	2026-07-09 01:38:23.882+00	2026-07-09 01:38:23.883+00	D-1-19	226
808	t	2026-07-09 01:38:23.885+00	2026-07-09 01:38:23.885+00	D-1-48	307
809	t	2026-07-09 01:38:23.918+00	2026-07-09 01:38:23.918+00	D-1-51	308
810	t	2026-07-09 01:38:23.929+00	2026-07-09 01:38:23.929+00	D-1-45	309
811	t	2026-07-09 01:38:23.945+00	2026-07-09 01:38:23.945+00	D-1-46	310
812	t	2026-07-09 01:38:23.956+00	2026-07-09 01:38:23.956+00	D-1-29	311
813	t	2026-07-09 01:38:23.959+00	2026-07-09 01:38:23.959+00	D-1-11	250
814	t	2026-07-09 01:38:23.964+00	2026-07-09 01:38:23.964+00	D-1-28	311
815	t	2026-07-09 01:38:23.967+00	2026-07-09 01:38:23.967+00	D-1-44	210
816	t	2026-07-09 01:38:23.97+00	2026-07-09 01:38:23.97+00	D-1-39	312
817	t	2026-07-09 01:38:23.981+00	2026-07-09 01:38:23.981+00	D-1-38	313
818	t	2026-07-09 01:38:23.995+00	2026-07-09 01:38:23.995+00	D-1-43	314
819	t	2026-07-09 01:38:24.006+00	2026-07-09 01:38:24.006+00	D-1-37	315
820	t	2026-07-09 01:38:24.017+00	2026-07-09 01:38:24.017+00	D-1-54	316
821	t	2026-07-09 01:38:24.02+00	2026-07-09 01:38:24.02+00	D-1-55	317
822	t	2026-07-09 01:38:24.025+00	2026-07-09 01:38:24.025+00	D-1-40	318
823	t	2026-07-09 01:38:24.036+00	2026-07-09 01:38:24.036+00	D-1-41	319
824	t	2026-07-09 01:38:24.041+00	2026-07-09 01:38:24.041+00	D-1-42	320
825	t	2026-07-09 01:38:24.049+00	2026-07-09 01:38:24.049+00	A-3-7	321
826	t	2026-07-09 01:38:24.052+00	2026-07-09 01:38:24.052+00	A-3-5	322
827	t	2026-07-09 01:38:24.075+00	2026-07-09 01:38:24.075+00	A-3-4	284
828	t	2026-07-09 01:38:24.078+00	2026-07-09 01:38:24.078+00	A-1-10	323
829	t	2026-07-09 01:38:24.084+00	2026-07-09 01:38:24.084+00	A-1-9	324
830	t	2026-07-09 01:38:24.095+00	2026-07-09 01:38:24.095+00	A-1-8	324
831	t	2026-07-09 01:38:24.124+00	2026-07-09 01:38:24.124+00	A-1-12	250
832	t	2026-07-09 01:38:24.13+00	2026-07-09 01:38:24.13+00	A-1-6	325
833	t	2026-07-09 01:38:24.147+00	2026-07-09 01:38:24.147+00	A-2-2	326
834	t	2026-07-09 01:38:24.15+00	2026-07-09 01:38:24.15+00	NA	327
835	t	2026-07-09 01:38:24.152+00	2026-07-09 01:38:24.152+00	A-3-8	328
836	t	2026-07-09 01:38:24.155+00	2026-07-09 01:38:24.155+00	A-1-17	329
837	t	2026-07-09 01:38:24.178+00	2026-07-09 01:38:24.178+00	A-1-19	330
838	t	2026-07-09 01:38:24.188+00	2026-07-09 01:38:24.188+00	A-1-14	331
839	t	2026-07-09 01:38:24.199+00	2026-07-09 01:38:24.199+00	A-1-15	332
840	t	2026-07-09 01:38:24.208+00	2026-07-09 01:38:24.208+00	A-1-13	333
841	t	2026-07-09 01:38:24.213+00	2026-07-09 01:38:24.213+00	A-1-16	334
842	t	2026-07-09 01:38:24.257+00	2026-07-09 01:38:24.257+00	A-3-2	226
843	t	2026-07-09 01:38:24.261+00	2026-07-09 01:38:24.261+00	A-3-3	226
844	t	2026-07-09 01:38:24.263+00	2026-07-09 01:38:24.263+00	A-3-6	284
845	t	2026-07-09 01:38:24.268+00	2026-07-09 01:38:24.268+00	G-2-1	335
846	t	2026-07-09 01:38:24.27+00	2026-07-09 01:38:24.27+00	G-3-12	336
847	t	2026-07-09 01:38:24.273+00	2026-07-09 01:38:24.273+00	G-3-19	337
848	t	2026-07-09 01:38:24.276+00	2026-07-09 01:38:24.276+00	G-3-5	338
849	t	2026-07-09 01:38:24.282+00	2026-07-09 01:38:24.282+00	G-3-6	339
850	t	2026-07-09 01:38:24.288+00	2026-07-09 01:38:24.288+00	G-3-7	340
851	t	2026-07-09 01:38:24.291+00	2026-07-09 01:38:24.291+00	G-3-8	341
852	t	2026-07-09 01:38:24.296+00	2026-07-09 01:38:24.296+00	G-3-2	342
853	t	2026-07-09 01:38:24.302+00	2026-07-09 01:38:24.302+00	G-3-3	226
854	t	2026-07-09 01:38:24.304+00	2026-07-09 01:38:24.304+00	G-3-1	213
855	t	2026-07-09 01:38:24.311+00	2026-07-09 01:38:24.311+00	G-3-52	343
856	t	2026-07-09 01:38:24.313+00	2026-07-09 01:38:24.313+00	G-3-50	337
857	t	2026-07-09 01:38:24.316+00	2026-07-09 01:38:24.316+00	G-3-54	344
858	t	2026-07-09 01:38:24.319+00	2026-07-09 01:38:24.319+00	G-3-51	345
859	t	2026-07-09 01:38:24.322+00	2026-07-09 01:38:24.322+00	B-3-45	209
860	t	2026-07-09 01:38:24.328+00	2026-07-09 01:38:24.328+00	B-3-10	346
861	t	2026-07-09 01:38:24.337+00	2026-07-09 01:38:24.337+00	B-3-17	347
862	t	2026-07-09 01:38:24.34+00	2026-07-09 01:38:24.34+00	B-3-35	348
863	t	2026-07-09 01:38:24.348+00	2026-07-09 01:38:24.348+00	B-3-2	349
864	t	2026-07-09 01:38:24.351+00	2026-07-09 01:38:24.351+00	B-3-23	226
865	t	2026-07-09 01:38:24.354+00	2026-07-09 01:38:24.354+00	B-3-21	209
866	t	2026-07-09 01:38:24.365+00	2026-07-09 01:38:24.365+00	B-3-3	291
867	t	2026-07-09 01:38:24.368+00	2026-07-09 01:38:24.368+00	I-3-4	350
868	t	2026-07-09 01:38:24.373+00	2026-07-09 01:38:24.373+00	H-3-61	351
869	t	2026-07-09 01:38:24.381+00	2026-07-09 01:38:24.381+00	H-3-29	347
870	t	2026-07-09 01:38:24.393+00	2026-07-09 01:38:24.393+00	H-3-27	352
871	t	2026-07-09 01:38:24.402+00	2026-07-09 01:38:24.402+00	H-3-28	351
872	t	2026-07-09 01:38:24.41+00	2026-07-09 01:38:24.41+00	H-3-57	291
873	t	2026-07-09 01:38:24.413+00	2026-07-09 01:38:24.413+00	H-3-30	347
874	t	2026-07-09 01:38:24.424+00	2026-07-09 01:38:24.424+00	H-3-58	349
875	t	2026-07-09 01:38:24.427+00	2026-07-09 01:38:24.427+00	I-1-4	353
876	t	2026-07-09 01:38:24.43+00	2026-07-09 01:38:24.43+00	I-3-5	354
877	t	2026-07-09 01:38:24.436+00	2026-07-09 01:38:24.436+00	I-3-55	284
878	t	2026-07-09 01:38:24.438+00	2026-07-09 01:38:24.438+00	I-3-31	347
879	t	2026-07-09 01:38:24.45+00	2026-07-09 01:38:24.45+00	I-3-1	291
880	t	2026-07-09 01:38:24.453+00	2026-07-09 01:38:24.453+00	I-3-57	349
881	t	2026-07-09 01:38:24.456+00	2026-07-09 01:38:24.456+00	I-3-29	352
882	t	2026-07-09 01:38:24.464+00	2026-07-09 01:38:24.464+00	I-3-30	351
883	t	2026-07-09 01:38:24.473+00	2026-07-09 01:38:24.473+00	I-3-62	351
884	t	2026-07-09 01:38:24.481+00	2026-07-09 01:38:24.481+00	I-3-32	347
885	t	2026-07-09 01:38:24.493+00	2026-07-09 01:38:24.493+00	G-3-30	220
886	t	2026-07-09 01:38:24.499+00	2026-07-09 01:38:24.499+00	G-3-48	355
887	t	2026-07-09 01:38:24.502+00	2026-07-09 01:38:24.502+00	G-3-36	356
888	t	2026-07-09 01:38:24.505+00	2026-07-09 01:38:24.505+00	G-3-47	357
889	t	2026-07-09 01:38:24.508+00	2026-07-09 01:38:24.508+00	G-3-29	337
890	t	2026-07-09 01:38:24.514+00	2026-07-09 01:38:24.514+00	G-3-34	358
891	t	2026-07-09 01:38:24.517+00	2026-07-09 01:38:24.517+00	G-3-45	359
892	t	2026-07-09 01:38:24.519+00	2026-07-09 01:38:24.519+00	G-3-37	360
893	t	2026-07-09 01:38:24.528+00	2026-07-09 01:38:24.528+00	G-3-33	361
894	t	2026-07-09 01:38:24.534+00	2026-07-09 01:38:24.534+00	G-3-35	362
895	t	2026-07-09 01:38:24.575+00	2026-07-09 01:38:24.575+00	H-2-23	365
896	t	2026-07-09 01:38:24.578+00	2026-07-09 01:38:24.578+00	H-2-24	365
897	t	2026-07-09 01:38:24.581+00	2026-07-09 01:38:24.581+00	H-2-15	366
898	t	2026-07-09 01:38:24.584+00	2026-07-09 01:38:24.584+00	H-2-19	367
899	t	2026-07-09 01:38:24.59+00	2026-07-09 01:38:24.59+00	H-2-27	369
900	t	2026-07-09 01:38:24.593+00	2026-07-09 01:38:24.593+00	H-2-18	370
901	t	2026-07-09 01:38:24.596+00	2026-07-09 01:38:24.596+00	H-2-25	213
902	t	2026-07-09 01:38:24.598+00	2026-07-09 01:38:24.598+00	H-2-20	269
903	t	2026-07-09 01:38:24.604+00	2026-07-09 01:38:24.604+00	H-2-48	371
904	t	2026-07-09 01:38:24.607+00	2026-07-09 01:38:24.607+00	H-2-32	372
905	t	2026-07-09 01:38:24.61+00	2026-07-09 01:38:24.61+00	H-2-46	373
906	t	2026-07-09 01:38:24.613+00	2026-07-09 01:38:24.613+00	H-2-31	374
907	t	2026-07-09 01:38:24.616+00	2026-07-09 01:38:24.616+00	H-2-34	375
908	t	2026-07-09 01:38:24.619+00	2026-07-09 01:38:24.619+00	H-2-35	375
909	t	2026-07-09 01:38:24.622+00	2026-07-09 01:38:24.622+00	H-2-47	269
910	t	2026-07-09 01:38:24.624+00	2026-07-09 01:38:24.624+00	H-2-28	213
911	t	2026-07-09 01:38:24.627+00	2026-07-09 01:38:24.627+00	H-2-42	209
912	t	2026-07-09 01:38:24.63+00	2026-07-09 01:38:24.63+00	H-2-43	209
913	t	2026-07-09 01:38:24.633+00	2026-07-09 01:38:24.633+00	H-2-44	209
914	t	2026-07-09 01:38:24.636+00	2026-07-09 01:38:24.636+00	H-2-45	209
915	t	2026-07-09 01:38:24.648+00	2026-07-09 01:38:24.648+00	H-2-49	209
916	t	2026-07-09 01:38:24.651+00	2026-07-09 01:38:24.651+00	H-2-29	376
917	t	2026-07-09 01:38:24.654+00	2026-07-09 01:38:24.654+00	H-2-1	377
918	t	2026-07-09 01:38:24.659+00	2026-07-09 01:38:24.659+00	H-2-13	378
919	t	2026-07-09 01:38:24.662+00	2026-07-09 01:38:24.662+00	H-2-3	379
920	t	2026-07-09 01:38:24.667+00	2026-07-09 01:38:24.667+00	I-2-4	380
921	t	2026-07-09 01:38:24.674+00	2026-07-09 01:38:24.674+00	H-2-5	381
922	t	2026-07-09 01:38:24.679+00	2026-07-09 01:38:24.679+00	H-2-11	382
923	t	2026-07-09 01:38:24.685+00	2026-07-09 01:38:24.685+00	H-2-4	383
924	t	2026-07-09 01:38:24.687+00	2026-07-09 01:38:24.687+00	H-2-2	209
925	t	2026-07-09 01:38:24.719+00	2026-07-09 01:38:24.719+00	H-2-14	384
926	t	2026-07-09 01:38:24.724+00	2026-07-09 01:38:24.724+00	H-2-12	385
927	t	2026-07-09 01:38:24.747+00	2026-07-09 01:38:24.747+00	D-2-57	265
928	t	2026-07-09 01:38:24.75+00	2026-07-09 01:38:24.75+00	D-2-50	386
929	t	2026-07-09 01:38:24.753+00	2026-07-09 01:38:24.753+00	D-2-56	387
930	t	2026-07-09 01:38:24.756+00	2026-07-09 01:38:24.756+00	D-2-2	209
931	t	2026-07-09 01:38:24.762+00	2026-07-09 01:38:24.762+00	D-2-21	226
932	t	2026-07-09 01:38:24.765+00	2026-07-09 01:38:24.765+00	D-2-1	389
933	t	2026-07-09 01:38:24.768+00	2026-07-09 01:38:24.768+00	D-2-19	390
934	t	2026-07-09 01:38:24.77+00	2026-07-09 01:38:24.77+00	D-2-16	390
935	t	2026-07-09 01:38:24.773+00	2026-07-09 01:38:24.773+00	D-2-23	391
936	t	2026-07-09 01:38:24.776+00	2026-07-09 01:38:24.776+00	D-2-7	392
937	t	2026-07-09 01:38:24.779+00	2026-07-09 01:38:24.779+00	D-2-20	393
938	t	2026-07-09 01:38:24.782+00	2026-07-09 01:38:24.782+00	D-2-18	390
939	t	2026-07-09 01:38:24.785+00	2026-07-09 01:38:24.785+00	D-2-41	394
940	t	2026-07-09 01:38:24.787+00	2026-07-09 01:38:24.787+00	D-2-42	394
941	t	2026-07-09 01:38:24.79+00	2026-07-09 01:38:24.79+00	D-2-45	395
942	t	2026-07-09 01:38:24.793+00	2026-07-09 01:38:24.793+00	I-2-3	396
943	t	2026-07-09 01:38:24.798+00	2026-07-09 01:38:24.798+00	I-2-5	378
944	t	2026-07-09 01:38:24.801+00	2026-07-09 01:38:24.801+00	G-2-5	397
945	t	2026-07-09 01:38:24.804+00	2026-07-09 01:38:24.804+00	G-2-6	398
946	t	2026-07-09 01:38:24.806+00	2026-07-09 01:38:24.806+00	G-2-7	399
947	t	2026-07-09 01:38:24.809+00	2026-07-09 01:38:24.809+00	G-2-9	213
948	t	2026-07-09 01:38:24.812+00	2026-07-09 01:38:24.812+00	G-2-10	269
949	t	2026-07-09 01:38:24.815+00	2026-07-09 01:38:24.815+00	H-2-56	400
950	t	2026-07-09 01:38:24.817+00	2026-07-09 01:38:24.817+00	H-2-55	401
951	t	2026-07-09 01:38:24.82+00	2026-07-09 01:38:24.82+00	H-2-57	402
952	t	2026-07-09 01:38:24.824+00	2026-07-09 01:38:24.824+00	M-7-43	403
953	t	2026-07-09 01:38:24.827+00	2026-07-09 01:38:24.827+00	M-7-6	403
954	t	2026-07-09 01:38:24.83+00	2026-07-09 01:38:24.83+00	M-7-7	403
955	t	2026-07-09 01:38:24.832+00	2026-07-09 01:38:24.832+00	M-7-8	403
956	t	2026-07-09 01:38:24.835+00	2026-07-09 01:38:24.835+00	M-7-47	265
957	t	2026-07-09 01:38:24.838+00	2026-07-09 01:38:24.838+00	M-7-9	403
958	t	2026-07-09 01:38:24.841+00	2026-07-09 01:38:24.841+00	M-7-10	403
959	t	2026-07-09 01:38:24.844+00	2026-07-09 01:38:24.844+00	M-7-11	403
960	t	2026-07-09 01:38:24.847+00	2026-07-09 01:38:24.847+00	M-7-12	403
961	t	2026-07-09 01:38:24.85+00	2026-07-09 01:38:24.85+00	M-7-29	288
962	t	2026-07-09 01:38:24.857+00	2026-07-09 01:38:24.857+00	M-7-22	264
963	t	2026-07-09 01:38:24.865+00	2026-07-09 01:38:24.865+00	M-7-13	403
964	t	2026-07-09 01:38:24.868+00	2026-07-09 01:38:24.868+00	M-7-14	403
965	t	2026-07-09 01:38:24.871+00	2026-07-09 01:38:24.871+00	M-7-15	403
966	t	2026-07-09 01:38:24.878+00	2026-07-09 01:38:24.878+00	M-7-16	403
967	t	2026-07-09 01:38:24.881+00	2026-07-09 01:38:24.881+00	M-7-4	404
968	t	2026-07-09 01:38:24.89+00	2026-07-09 01:38:24.89+00	M-7-17	403
969	t	2026-07-09 01:38:24.893+00	2026-07-09 01:38:24.893+00	M-7-18	403
970	t	2026-07-09 01:38:24.896+00	2026-07-09 01:38:24.896+00	M-7-5	403
971	t	2026-07-09 01:38:24.899+00	2026-07-09 01:38:24.899+00	M-7-35	291
972	t	2026-07-09 01:38:24.902+00	2026-07-09 01:38:24.902+00	M-7-19	250
973	t	2026-07-09 01:38:24.905+00	2026-07-09 01:38:24.905+00	N-7-43	291
974	t	2026-07-09 01:38:24.908+00	2026-07-09 01:38:24.908+00	N-7-52	291
975	t	2026-07-09 01:38:24.91+00	2026-07-09 01:38:24.91+00	N-7-45	250
976	t	2026-07-09 01:38:24.913+00	2026-07-09 01:38:24.913+00	N-7-40	287
977	t	2026-07-09 01:38:24.916+00	2026-07-09 01:38:24.916+00	N-7-41	287
978	t	2026-07-09 01:38:24.919+00	2026-07-09 01:38:24.919+00	N-7-42	287
979	t	2026-07-09 01:38:24.922+00	2026-07-09 01:38:24.922+00	N-7-67	285
980	t	2026-07-09 01:38:24.925+00	2026-07-09 01:38:24.925+00	N-7-26	288
981	t	2026-07-09 01:38:24.934+00	2026-07-09 01:38:24.934+00	N-7-24	264
982	t	2026-07-09 01:38:24.941+00	2026-07-09 01:38:24.941+00	N-7-68	285
983	t	2026-07-09 01:38:24.944+00	2026-07-09 01:38:24.944+00	N-7-69	285
984	t	2026-07-09 01:38:24.946+00	2026-07-09 01:38:24.946+00	N-7-33	287
985	t	2026-07-09 01:38:24.949+00	2026-07-09 01:38:24.949+00	N-7-32	287
986	t	2026-07-09 01:38:24.952+00	2026-07-09 01:38:24.952+00	N-7-12	287
987	t	2026-07-09 01:38:24.955+00	2026-07-09 01:38:24.955+00	N-7-34	287
988	t	2026-07-09 01:38:24.958+00	2026-07-09 01:38:24.958+00	N-7-13	287
989	t	2026-07-09 01:38:24.961+00	2026-07-09 01:38:24.961+00	N-7-11	287
990	t	2026-07-09 01:38:24.964+00	2026-07-09 01:38:24.964+00	N-7-14	265
991	t	2026-07-09 01:38:24.967+00	2026-07-09 01:38:24.967+00	N-7-9	284
992	t	2026-07-09 01:38:24.969+00	2026-07-09 01:38:24.969+00	N-7-31	209
993	t	2026-07-09 01:38:24.975+00	2026-07-09 01:38:24.975+00	N-7-25	209
994	t	2026-07-09 01:38:24.979+00	2026-07-09 01:38:24.979+00	N-7-10	284
995	t	2026-07-09 01:38:24.982+00	2026-07-09 01:38:24.982+00	O-7-17	291
996	t	2026-07-09 01:38:24.985+00	2026-07-09 01:38:24.985+00	O-7-6	250
997	t	2026-07-09 01:38:24.988+00	2026-07-09 01:38:24.988+00	O-7-16	291
998	t	2026-07-09 01:38:24.991+00	2026-07-09 01:38:24.991+00	O-7-13	287
999	t	2026-07-09 01:38:24.994+00	2026-07-09 01:38:24.994+00	O-7-25	287
1000	t	2026-07-09 01:38:24.997+00	2026-07-09 01:38:24.997+00	O-7-10	287
1001	t	2026-07-09 01:38:25+00	2026-07-09 01:38:25+00	O-7-49	285
1002	t	2026-07-09 01:38:25.003+00	2026-07-09 01:38:25.003+00	O-7-50	285
1003	t	2026-07-09 01:38:25.006+00	2026-07-09 01:38:25.006+00	O-7-51	285
1004	t	2026-07-09 01:38:25.008+00	2026-07-09 01:38:25.008+00	O-7-18	264
1005	t	2026-07-09 01:38:25.019+00	2026-07-09 01:38:25.019+00	O-7-26	288
1006	t	2026-07-09 01:38:25.025+00	2026-07-09 01:38:25.025+00	O-7-29	287
1007	t	2026-07-09 01:38:25.029+00	2026-07-09 01:38:25.029+00	O-7-11	287
1008	t	2026-07-09 01:38:25.032+00	2026-07-09 01:38:25.032+00	O-7-14	265
1009	t	2026-07-09 01:38:25.035+00	2026-07-09 01:38:25.035+00	O-7-8	287
1010	t	2026-07-09 01:38:25.037+00	2026-07-09 01:38:25.037+00	O-7-28	287
1011	t	2026-07-09 01:38:25.04+00	2026-07-09 01:38:25.04+00	O-7-9	287
1012	t	2026-07-09 01:38:25.043+00	2026-07-09 01:38:25.043+00	O-7-27	287
\.


--
-- Data for Name: mantenedores_proveedor; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.mantenedores_proveedor (id, activo, fecha_creacion, fecha_actualizacion, nombre, contacto, telefono, email, direccion, rut) FROM stdin;
1	t	2026-07-11 01:17:55.935+00	2026-07-11 01:17:55.935+00	Telefonica	Reinaldo Gomez	949253333	reinaldog.gomez@redsaludo.gob.cl	Calle Street 12	\N
\.


--
-- Data for Name: mantenedores_recinto; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.mantenedores_recinto (id, activo, fecha_creacion, fecha_actualizacion, nombre, piso_id, sector_id, unidad_id) FROM stdin;
203	t	2026-07-09 01:38:22.635+00	2026-07-09 01:38:22.635+00	Cubículos Electro Tratamiento	9	8	42
204	t	2026-07-09 01:38:22.652+00	2026-07-09 01:38:22.652+00	Gimnasio Rehabilitación	9	8	42
205	t	2026-07-09 01:38:22.658+00	2026-07-09 01:38:22.658+00	Sala Estimulación Cognitiva	9	8	42
206	t	2026-07-09 01:38:22.661+00	2026-07-09 01:38:22.661+00	Sala Terapia Ocupacional	9	8	42
207	t	2026-07-09 01:38:22.664+00	2026-07-09 01:38:22.664+00	Taller Actividades Vida Diaria	9	8	42
208	t	2026-07-09 01:38:22.667+00	2026-07-09 01:38:22.667+00	Sala NANEAS	9	8	42
209	t	2026-07-09 01:38:22.67+00	2026-07-09 01:38:22.67+00	Oficina Modular	9	8	42
210	t	2026-07-09 01:38:22.682+00	2026-07-09 01:38:22.682+00	Sala Entrevista	9	8	42
211	t	2026-07-09 01:38:22.685+00	2026-07-09 01:38:22.685+00	Secretaria y Recepción	9	8	42
212	t	2026-07-09 01:38:22.688+00	2026-07-09 01:38:22.688+00	Box Consulta	9	8	42
213	t	2026-07-09 01:38:22.705+00	2026-07-09 01:38:22.705+00	Secretaria	9	8	43
214	t	2026-07-09 01:38:22.708+00	2026-07-09 01:38:22.708+00	Modulo de Admisión y Recaudación	9	8	42
215	t	2026-07-09 01:38:22.714+00	2026-07-09 01:38:22.714+00	Modulo Información y Agenda Medica	9	8	44
216	t	2026-07-09 01:38:22.727+00	2026-07-09 01:38:22.727+00	Oficina Modular (Hospitaliazación domiciliaria)	9	8	43
217	t	2026-07-09 01:38:22.744+00	2026-07-09 01:38:22.744+00	Sala Toma Muestras Adulto	9	9	45
218	t	2026-07-09 01:38:22.747+00	2026-07-09 01:38:22.747+00	Sala Toma Muestras Infantil	9	9	45
219	t	2026-07-09 01:38:22.75+00	2026-07-09 01:38:22.75+00	Modulos Despacho Farmacia	9	9	45
220	t	2026-07-09 01:38:22.768+00	2026-07-09 01:38:22.768+00	Oficina Administrativa	9	9	45
221	t	2026-07-09 01:38:22.777+00	2026-07-09 01:38:22.777+00	Box Consulta Prof. No Medico Indif.	9	9	46
222	t	2026-07-09 01:38:22.78+00	2026-07-09 01:38:22.78+00	Sala Procedimientos - Camara Silente	9	9	46
223	t	2026-07-09 01:38:22.783+00	2026-07-09 01:38:22.783+00	Sala Procedimientos - Octavo Par	9	9	46
224	t	2026-07-09 01:38:22.785+00	2026-07-09 01:38:22.785+00	Box Consulta Otorrino.	9	9	46
225	t	2026-07-09 01:38:22.788+00	2026-07-09 01:38:22.788+00	Box Consulta Medica Indiferenciada	9	9	46
226	t	2026-07-09 01:38:22.797+00	2026-07-09 01:38:22.797+00	Sala Reuniones 12 Personas	9	9	46
227	t	2026-07-09 01:38:22.8+00	2026-07-09 01:38:22.8+00	Sala Procedimientos - Traumatologia	9	9	46
228	t	2026-07-09 01:38:22.803+00	2026-07-09 01:38:22.803+00	Sala Procedimientos - Dermatologia	9	9	46
229	t	2026-07-09 01:38:22.806+00	2026-07-09 01:38:22.806+00	Sala Procedimientos - Laser (Oftalmo.)	9	9	46
230	t	2026-07-09 01:38:22.809+00	2026-07-09 01:38:22.809+00	Modulo de Admision y Recaudacion	9	9	46
231	t	2026-07-09 01:38:22.821+00	2026-07-09 01:38:22.821+00	Sala Preparacion Pacientes	9	9	46
232	t	2026-07-09 01:38:22.827+00	2026-07-09 01:38:22.827+00	Box Consulta Tecnologo Oftalmo.	9	9	46
233	t	2026-07-09 01:38:22.83+00	2026-07-09 01:38:22.83+00	Box Consulta Oftalmologia	9	9	46
234	t	2026-07-09 01:38:22.836+00	2026-07-09 01:38:22.836+00	Sala Procedimientos - Oftalmologia 2	9	9	46
235	t	2026-07-09 01:38:22.839+00	2026-07-09 01:38:22.839+00	Sala Procedimientos - Oftalmologia 1	9	9	46
236	t	2026-07-09 01:38:22.865+00	2026-07-09 01:38:22.865+00	Sala Informes	10	8	47
237	t	2026-07-09 01:38:22.88+00	2026-07-09 01:38:22.88+00	Sala Procedimientos - Endoscopia	10	8	47
238	t	2026-07-09 01:38:22.886+00	2026-07-09 01:38:22.886+00	Box Odontologia	10	8	48
239	t	2026-07-09 01:38:22.898+00	2026-07-09 01:38:22.898+00	Sala de Impresiones	10	8	48
240	t	2026-07-09 01:38:22.912+00	2026-07-09 01:38:22.912+00	Cistoscopia	10	8	47
241	t	2026-07-09 01:38:22.915+00	2026-07-09 01:38:22.915+00	Disponible (Proced. Endoscopia)	10	8	47
242	t	2026-07-09 01:38:22.93+00	2026-07-09 01:38:22.93+00	Estación Enfermería	10	8	47
243	t	2026-07-09 01:38:22.935+00	2026-07-09 01:38:22.935+00	Sala Preparación Pacientes	10	8	47
244	t	2026-07-09 01:38:22.943+00	2026-07-09 01:38:22.943+00	Oficina Gestion Agenda Medica	10	8	49
245	t	2026-07-09 01:38:22.954+00	2026-07-09 01:38:22.954+00	Control RX Dental	10	8	48
246	t	2026-07-09 01:38:22.96+00	2026-07-09 01:38:22.96+00	Control RX Dental Ortopantomografo	10	8	48
247	t	2026-07-09 01:38:22.966+00	2026-07-09 01:38:22.966+00	Oficina Secretarias At. Abierta	10	8	49
248	t	2026-07-09 01:38:22.975+00	2026-07-09 01:38:22.975+00	Oficina Jefatura At. Abierta y Admision	10	8	49
249	t	2026-07-09 01:38:22.989+00	2026-07-09 01:38:22.989+00	Oficina Gestion Archivo	10	8	49
250	t	2026-07-09 01:38:23.012+00	2026-07-09 01:38:23.012+00	Secretaria y Recepcion	10	9	50
251	t	2026-07-09 01:38:23.016+00	2026-07-09 01:38:23.016+00	Archivo	10	9	50
252	t	2026-07-09 01:38:23.037+00	2026-07-09 01:38:23.037+00	Box Consulta Ginecologia	10	9	51
253	t	2026-07-09 01:38:23.05+00	2026-07-09 01:38:23.05+00	Vacunatorio	10	9	53
254	t	2026-07-09 01:38:23.059+00	2026-07-09 01:38:23.059+00	Box Consulta Matrona	10	9	51
255	t	2026-07-09 01:38:23.065+00	2026-07-09 01:38:23.065+00	Box Consulta Obstetricia	10	9	51
256	t	2026-07-09 01:38:23.071+00	2026-07-09 01:38:23.071+00	Sala Procedimientos - Eco tomografia G-O	10	9	51
257	t	2026-07-09 01:38:23.077+00	2026-07-09 01:38:23.077+00	Box Ecotomogr. G-O	10	9	51
258	t	2026-07-09 01:38:23.088+00	2026-07-09 01:38:23.088+00	Sala Procedimientos Indiferenciados Infantil	10	9	52
259	t	2026-07-09 01:38:23.103+00	2026-07-09 01:38:23.103+00	Box Consulta Fonoaudiologo	10	9	52
260	t	2026-07-09 01:38:23.109+00	2026-07-09 01:38:23.109+00	Sala Procedimientos - Broncopulmonar 1	10	9	52
261	t	2026-07-09 01:38:23.112+00	2026-07-09 01:38:23.112+00	Sala Procedimientos - Broncopulmonar 2	10	9	52
262	t	2026-07-09 01:38:23.115+00	2026-07-09 01:38:23.115+00	Sala Procedimientos - Gineco-Obstetra	10	9	51
263	t	2026-07-09 01:38:23.122+00	2026-07-09 01:38:23.122+00	Estación Monitoreo	11	8	54
264	t	2026-07-09 01:38:23.134+00	2026-07-09 01:38:23.134+00	Estacion Enfermeria	11	8	55
265	t	2026-07-09 01:38:23.142+00	2026-07-09 01:38:23.142+00	Sala Procedimientos	11	8	55
266	t	2026-07-09 01:38:23.155+00	2026-07-09 01:38:23.155+00	Box Profesional Multiple	11	8	55
267	t	2026-07-09 01:38:23.159+00	2026-07-09 01:38:23.159+00	Box Poli Del Dolor	11	8	55
268	t	2026-07-09 01:38:23.162+00	2026-07-09 01:38:23.162+00	Oficina Poli Del Dolor	11	8	55
269	t	2026-07-09 01:38:23.169+00	2026-07-09 01:38:23.169+00	Oficina Jefatura	11	8	54
270	t	2026-07-09 01:38:23.18+00	2026-07-09 01:38:23.18+00	Sala Procedimientos - Hemodiálisis	11	8	54
271	t	2026-07-09 01:38:23.183+00	2026-07-09 01:38:23.183+00	Sala Procedimientos - Peritoneodialisis	11	8	54
272	t	2026-07-09 01:38:23.186+00	2026-07-09 01:38:23.186+00	Box Evaluación	11	8	54
273	t	2026-07-09 01:38:23.192+00	2026-07-09 01:38:23.192+00	Modulo Admision y Secretaria	11	8	55
274	t	2026-07-09 01:38:23.201+00	2026-07-09 01:38:23.201+00	Sala Gessel	11	9	56
275	t	2026-07-09 01:38:23.204+00	2026-07-09 01:38:23.204+00	Box Consulta Prof. No Medico	11	9	56
276	t	2026-07-09 01:38:23.239+00	2026-07-09 01:38:23.239+00	Sala Preparacion Pacientes y Procedimientos	11	9	56
277	t	2026-07-09 01:38:23.282+00	2026-07-09 01:38:23.282+00	Sala Procedimientos Ecocarfiograma	11	9	57
278	t	2026-07-09 01:38:23.285+00	2026-07-09 01:38:23.285+00	Sala Procedimientos Electrocarfiograma	11	9	57
279	t	2026-07-09 01:38:23.288+00	2026-07-09 01:38:23.288+00	Sala Procedimientos Indeferenciados Adultos	11	9	57
280	t	2026-07-09 01:38:23.291+00	2026-07-09 01:38:23.291+00	Sala Procedimientos Indiferenciada	11	9	57
281	t	2026-07-09 01:38:23.303+00	2026-07-09 01:38:23.303+00	Sala Procedimientos - Neurologia 3	11	9	57
282	t	2026-07-09 01:38:23.306+00	2026-07-09 01:38:23.306+00	Sala Procedimientos - Neurologia 1	11	9	57
283	t	2026-07-09 01:38:23.309+00	2026-07-09 01:38:23.309+00	Sala Procedimientos - Test Esfuerzo	11	9	57
284	t	2026-07-09 01:38:23.349+00	2026-07-09 01:38:23.349+00	Sala Reuniones 20 Personas	13	10	58
285	t	2026-07-09 01:38:23.352+00	2026-07-09 01:38:23.352+00	Esclusa	13	10	58
286	t	2026-07-09 01:38:23.361+00	2026-07-09 01:38:23.361+00	Sala Hospitalizacion 2 Camas	13	10	58
287	t	2026-07-09 01:38:23.364+00	2026-07-09 01:38:23.364+00	Sala Hospitalizacion 3 Camas	13	10	58
288	t	2026-07-09 01:38:23.372+00	2026-07-09 01:38:23.372+00	Trabajo Medico	13	10	58
289	t	2026-07-09 01:38:23.386+00	2026-07-09 01:38:23.386+00	Sala Hospitalizacion 6 Camas	13	10	58
290	t	2026-07-09 01:38:23.398+00	2026-07-09 01:38:23.398+00	Oficina Docente	13	10	59
291	t	2026-07-09 01:38:23.401+00	2026-07-09 01:38:23.401+00	Sala Entrevista Familiares	13	10	58
292	t	2026-07-09 01:38:23.603+00	2026-07-09 01:38:23.603+00	Sala Entrevista Chile Crece Contigo	14	10	62
293	t	2026-07-09 01:38:23.606+00	2026-07-09 01:38:23.606+00	Oficina Chile Crece Contigo	14	10	62
294	t	2026-07-09 01:38:23.757+00	2026-07-09 01:38:23.757+00	Oficina Calidad de Vida Laboral	9	9	63
295	t	2026-07-09 01:38:23.779+00	2026-07-09 01:38:23.779+00	DO	9	9	63
296	t	2026-07-09 01:38:23.785+00	2026-07-09 01:38:23.785+00	Oficina Personal y Rentas	9	9	63
297	t	2026-07-09 01:38:23.79+00	2026-07-09 01:38:23.79+00	Oficina Analisis y Planificacion	9	9	63
298	t	2026-07-09 01:38:23.833+00	2026-07-09 01:38:23.833+00	Oficina SD RRHH	9	9	64
299	t	2026-07-09 01:38:23.836+00	2026-07-09 01:38:23.836+00	Oficina SD Gestion Administrativa	9	9	64
300	t	2026-07-09 01:38:23.839+00	2026-07-09 01:38:23.839+00	Oficina SD Atencion Usuario y Part. Social	9	9	64
301	t	2026-07-09 01:38:23.842+00	2026-07-09 01:38:23.842+00	Oficina SD Gestion del Cuidado	9	9	64
302	t	2026-07-09 01:38:23.844+00	2026-07-09 01:38:23.844+00	Oficina SD Medico Asistencial	9	9	64
303	t	2026-07-09 01:38:23.858+00	2026-07-09 01:38:23.858+00	Oficina Abastecimiento	9	9	65
304	t	2026-07-09 01:38:23.863+00	2026-07-09 01:38:23.863+00	Oficina Abastecimiento o abogados	9	9	65
305	t	2026-07-09 01:38:23.877+00	2026-07-09 01:38:23.877+00	Oficina SD Operaciones	9	9	64
306	t	2026-07-09 01:38:23.879+00	2026-07-09 01:38:23.879+00	Oficina Director	9	9	64
307	t	2026-07-09 01:38:23.885+00	2026-07-09 01:38:23.885+00	Oficina Contabilidad	9	9	65
308	t	2026-07-09 01:38:23.917+00	2026-07-09 01:38:23.917+00	Oficina Presupuesto	9	9	65
309	t	2026-07-09 01:38:23.928+00	2026-07-09 01:38:23.928+00	Oficina Comercializacion y Recaudacion	9	9	65
310	t	2026-07-09 01:38:23.944+00	2026-07-09 01:38:23.944+00	Oficina Tesoreria	9	9	65
311	t	2026-07-09 01:38:23.956+00	2026-07-09 01:38:23.956+00	Sala Reuniones 6 Personas	9	9	66
312	t	2026-07-09 01:38:23.97+00	2026-07-09 01:38:23.97+00	Atención Psicosocial Integral	9	9	67
313	t	2026-07-09 01:38:23.981+00	2026-07-09 01:38:23.981+00	Oficina Servicio Social	9	9	67
314	t	2026-07-09 01:38:23.995+00	2026-07-09 01:38:23.995+00	Oficina Programas Humaniz.	9	9	67
315	t	2026-07-09 01:38:24.006+00	2026-07-09 01:38:24.006+00	Oficina Participacion Social	9	9	67
316	t	2026-07-09 01:38:24.016+00	2026-07-09 01:38:24.016+00	Caja	9	9	65
317	t	2026-07-09 01:38:24.019+00	2026-07-09 01:38:24.019+00	Oficina Procura	9	9	68
318	t	2026-07-09 01:38:24.025+00	2026-07-09 01:38:24.025+00	Oficina OIRS	9	9	67
319	t	2026-07-09 01:38:24.036+00	2026-07-09 01:38:24.036+00	Modulos OIRS Atencion Cerrada	9	9	67
320	t	2026-07-09 01:38:24.041+00	2026-07-09 01:38:24.041+00	Modulos OIRS Atencion Abierta	9	9	67
321	t	2026-07-09 01:38:24.048+00	2026-07-09 01:38:24.048+00	Sala Capacitacion	15	13	69
322	t	2026-07-09 01:38:24.051+00	2026-07-09 01:38:24.051+00	Unidad de Capacitación y Reclutamiento	15	13	69
323	t	2026-07-09 01:38:24.078+00	2026-07-09 01:38:24.078+00	Listo pero disponible	15	13	68
324	t	2026-07-09 01:38:24.083+00	2026-07-09 01:38:24.083+00	Oficina Gestion GES	15	13	68
325	t	2026-07-09 01:38:24.129+00	2026-07-09 01:38:24.129+00	Oficina Gestion del Cuidado	15	13	71
326	t	2026-07-09 01:38:24.146+00	2026-07-09 01:38:24.146+00	Sala Lectura y Puesto Trabajo Encargado	15	13	69
327	t	2026-07-09 01:38:24.149+00	2026-07-09 01:38:24.149+00	Sala Expositor	15	13	69
328	t	2026-07-09 01:38:24.152+00	2026-07-09 01:38:24.152+00	Sala Video Conferencia	15	13	69
329	t	2026-07-09 01:38:24.155+00	2026-07-09 01:38:24.155+00	Oficina Gestion Calidad y Segu. Paciente	15	13	70
330	t	2026-07-09 01:38:24.178+00	2026-07-09 01:38:24.178+00	Oficina Epidemiologia	15	13	70
331	t	2026-07-09 01:38:24.188+00	2026-07-09 01:38:24.188+00	Oficina Auditores	15	13	70
332	t	2026-07-09 01:38:24.199+00	2026-07-09 01:38:24.199+00	Oficina Comunicaciones	15	13	70
333	t	2026-07-09 01:38:24.207+00	2026-07-09 01:38:24.208+00	Oficina Asesores Juridicos (se cambian a otro recinto)	15	13	70
334	t	2026-07-09 01:38:24.213+00	2026-07-09 01:38:24.213+00	Oficina Control de Gestion	15	13	70
335	t	2026-07-09 01:38:24.267+00	2026-07-09 01:38:24.267+00	Sala Espera Deudos	11	14	72
336	t	2026-07-09 01:38:24.27+00	2026-07-09 01:38:24.27+00	Oficina	11	14	72
337	t	2026-07-09 01:38:24.273+00	2026-07-09 01:38:24.273+00	Recepción Muestras	11	14	72
338	t	2026-07-09 01:38:24.276+00	2026-07-09 01:38:24.276+00	Sala Macroscopias	11	14	72
339	t	2026-07-09 01:38:24.282+00	2026-07-09 01:38:24.282+00	Sala Corte y Tinción	11	14	72
340	t	2026-07-09 01:38:24.287+00	2026-07-09 01:38:24.287+00	Sala Citodiagnost. e Histología	11	14	72
341	t	2026-07-09 01:38:24.29+00	2026-07-09 01:38:24.29+00	Sala Microscopia	11	14	72
342	t	2026-07-09 01:38:24.296+00	2026-07-09 01:38:24.296+00	Oficina Modular Patólogos	11	14	72
343	t	2026-07-09 01:38:24.31+00	2026-07-09 01:38:24.31+00	Laboratorio Inmunohematoligia	11	14	73
344	t	2026-07-09 01:38:24.316+00	2026-07-09 01:38:24.316+00	Despacho Transfusiones	11	14	73
345	t	2026-07-09 01:38:24.319+00	2026-07-09 01:38:24.319+00	Sala Conserv. Componentes Sanguineos	11	14	73
346	t	2026-07-09 01:38:24.328+00	2026-07-09 01:38:24.328+00	Estacion Enfermeria y Monitoreo Neonatologia	11	14	74
347	t	2026-07-09 01:38:24.336+00	2026-07-09 01:38:24.336+00	Sala Evolucion Paciente	11	14	74
348	t	2026-07-09 01:38:24.339+00	2026-07-09 01:38:24.339+00	Estacion Enfermeria y Monitoreo UTI Infantil	11	14	74
349	t	2026-07-09 01:38:24.348+00	2026-07-09 01:38:24.348+00	Secretaria y Admision	11	14	74
350	t	2026-07-09 01:38:24.368+00	2026-07-09 01:38:24.368+00	Oficina Modular UCI	11	14	75
351	t	2026-07-09 01:38:24.373+00	2026-07-09 01:38:24.373+00	Estacion Enfermeria y Monitoreo UTI	11	14	75
352	t	2026-07-09 01:38:24.393+00	2026-07-09 01:38:24.393+00	Estacion Enfermeria y Monitoreo UCI	11	14	75
353	t	2026-07-09 01:38:24.427+00	2026-07-09 01:38:24.427+00	PROCURA	11	14	75
354	t	2026-07-09 01:38:24.43+00	2026-07-09 01:38:24.43+00	Oficina Modular UTI	11	14	75
355	t	2026-07-09 01:38:24.499+00	2026-07-09 01:38:24.499+00	IFI	11	14	76
356	t	2026-07-09 01:38:24.502+00	2026-07-09 01:38:24.502+00	Microscopia	11	14	76
357	t	2026-07-09 01:38:24.505+00	2026-07-09 01:38:24.505+00	Sala Descont. y Lavado	11	14	76
358	t	2026-07-09 01:38:24.514+00	2026-07-09 01:38:24.514+00	Área Preanalítica Sucia	11	14	76
359	t	2026-07-09 01:38:24.516+00	2026-07-09 01:38:24.516+00	Parasitología + TBC	11	14	76
360	t	2026-07-09 01:38:24.519+00	2026-07-09 01:38:24.519+00	Bacteriología	11	14	76
361	t	2026-07-09 01:38:24.528+00	2026-07-09 01:38:24.528+00	Área Preanalítica Limpia	11	14	76
362	t	2026-07-09 01:38:24.533+00	2026-07-09 01:38:24.533+00	Área Equipamiento Automatizado	11	14	76
363	t	2026-07-09 01:38:24.567+00	2026-07-09 01:38:24.567+00	Extracción	11	14	76
364	t	2026-07-09 01:38:24.57+00	2026-07-09 01:38:24.57+00	Lectura	11	14	76
365	t	2026-07-09 01:38:24.574+00	2026-07-09 01:38:24.574+00	Pool Tecnicos	10	14	77
366	t	2026-07-09 01:38:24.581+00	2026-07-09 01:38:24.581+00	Equipos de Prueba	10	14	77
367	t	2026-07-09 01:38:24.584+00	2026-07-09 01:38:24.584+00	Entrega Equipos	10	14	77
368	t	2026-07-09 01:38:24.586+00	2026-07-09 01:38:24.586+00	Supervisor Serv. Tecnico Interno	10	14	77
369	t	2026-07-09 01:38:24.59+00	2026-07-09 01:38:24.59+00	Supervisor Serv. Tecnico Externo	10	14	77
370	t	2026-07-09 01:38:24.592+00	2026-07-09 01:38:24.592+00	Recepcion Equipos	10	14	77
371	t	2026-07-09 01:38:24.604+00	2026-07-09 01:38:24.604+00	Bodega Activa	10	14	78
372	t	2026-07-09 01:38:24.607+00	2026-07-09 01:38:24.607+00	Sala Preparaciones No Esteriles	10	14	78
373	t	2026-07-09 01:38:24.61+00	2026-07-09 01:38:24.61+00	Bodega Vacunas	10	14	78
374	t	2026-07-09 01:38:24.613+00	2026-07-09 01:38:24.613+00	Sala Dispensacion	10	14	78
375	t	2026-07-09 01:38:24.616+00	2026-07-09 01:38:24.616+00	Recepcion y Despacho Carros Distribucion	10	14	78
376	t	2026-07-09 01:38:24.65+00	2026-07-09 01:38:24.65+00	Bodega Farmacos Controlados	10	14	78
377	t	2026-07-09 01:38:24.653+00	2026-07-09 01:38:24.653+00	Bodega Otros Farmacos	10	14	79
378	t	2026-07-09 01:38:24.659+00	2026-07-09 01:38:24.659+00	Recepcion Bodega	10	14	79
379	t	2026-07-09 01:38:24.661+00	2026-07-09 01:38:24.661+00	Bodega Insumos	10	14	79
380	t	2026-07-09 01:38:24.666+00	2026-07-09 01:38:24.666+00	Oficina Economato	10	14	79
381	t	2026-07-09 01:38:24.674+00	2026-07-09 01:38:24.674+00	Despacho Carros Distribucion	10	14	79
382	t	2026-07-09 01:38:24.679+00	2026-07-09 01:38:24.679+00	Oficina Insumos	10	14	79
383	t	2026-07-09 01:38:24.684+00	2026-07-09 01:38:24.684+00	Bodega Programas	10	14	79
384	t	2026-07-09 01:38:24.718+00	2026-07-09 01:38:24.718+00	Oficina Jefe Compras	10	14	79
385	t	2026-07-09 01:38:24.724+00	2026-07-09 01:38:24.724+00	Oficina Compras	10	14	79
386	t	2026-07-09 01:38:24.75+00	2026-07-09 01:38:24.75+00	Control TAC	10	14	80
387	t	2026-07-09 01:38:24.753+00	2026-07-09 01:38:24.753+00	Sala Preparación y Recuperación TAC	10	14	80
388	t	2026-07-09 01:38:24.758+00	2026-07-09 01:38:24.758+00	Oficina SUPERVISOR	10	14	80
389	t	2026-07-09 01:38:24.764+00	2026-07-09 01:38:24.764+00	Secretaria y Transcripción	10	14	80
390	t	2026-07-09 01:38:24.767+00	2026-07-09 01:38:24.767+00	Sala Ecotomografía	10	14	80
391	t	2026-07-09 01:38:24.773+00	2026-07-09 01:38:24.773+00	Control Mamografía	10	14	80
392	t	2026-07-09 01:38:24.776+00	2026-07-09 01:38:24.776+00	Modulo Admisión y Recaudación	10	14	80
393	t	2026-07-09 01:38:24.779+00	2026-07-09 01:38:24.779+00	Sala Mamografía	10	14	80
394	t	2026-07-09 01:38:24.784+00	2026-07-09 01:38:24.784+00	Control Rayos Osteopulmonar	10	14	80
395	t	2026-07-09 01:38:24.79+00	2026-07-09 01:38:24.79+00	control rayos osteopulmonar	10	14	80
396	t	2026-07-09 01:38:24.793+00	2026-07-09 01:38:24.793+00	Bodega Economato	10	\N	79
397	t	2026-07-09 01:38:24.801+00	2026-07-09 01:38:24.801+00	Taller Electricidad	10	\N	81
398	t	2026-07-09 01:38:24.803+00	2026-07-09 01:38:24.803+00	Taller Gasfiteria	10	\N	81
399	t	2026-07-09 01:38:24.806+00	2026-07-09 01:38:24.806+00	Taller Soldadura	10	\N	81
400	t	2026-07-09 01:38:24.814+00	2026-07-09 01:38:24.814+00	Taller Pintura	10	\N	81
401	t	2026-07-09 01:38:24.817+00	2026-07-09 01:38:24.817+00	Taller Carpinteria	10	\N	81
402	t	2026-07-09 01:38:24.82+00	2026-07-09 01:38:24.82+00	Bodega Pañol	10	\N	81
403	t	2026-07-09 01:38:24.824+00	2026-07-09 01:38:24.824+00	Sala Hospitalizacion 1 Cama	16	14	82
404	t	2026-07-09 01:38:24.881+00	2026-07-09 01:38:24.881+00	Oficina Admision y Recaudacion	16	14	82
\.


--
-- Data for Name: mantenedores_sector; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.mantenedores_sector (id, activo, fecha_creacion, fecha_actualizacion, nombre, piso_id) FROM stdin;
8	t	2026-07-09 01:38:22.635+00	2026-07-09 01:38:22.635+00	SUR	9
9	t	2026-07-09 01:38:22.744+00	2026-07-09 01:38:22.744+00	NORTE	9
10	t	2026-07-09 01:38:23.343+00	2026-07-09 01:38:23.343+00	A	13
11	t	2026-07-09 01:38:23.41+00	2026-07-09 01:38:23.41+00	B	13
12	t	2026-07-09 01:38:23.486+00	2026-07-09 01:38:23.486+00	C	13
13	t	2026-07-09 01:38:24.048+00	2026-07-09 01:38:24.048+00	AU	15
14	t	2026-07-09 01:38:24.267+00	2026-07-09 01:38:24.267+00	EP	11
\.


--
-- Data for Name: mantenedores_sistemaoperativo; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.mantenedores_sistemaoperativo (id, activo, fecha_creacion, fecha_actualizacion, nombre) FROM stdin;
1	t	2026-07-10 02:26:54.651+00	2026-07-10 02:26:54.651+00	Windows 11 Pro
\.


--
-- Data for Name: mantenedores_unidad; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.mantenedores_unidad (id, activo, fecha_creacion, fecha_actualizacion, nombre, area_hospitalaria_id) FROM stdin;
84	t	2026-07-19 04:21:56.424208+00	2026-07-19 16:21:21.414131+00	UNIDAD QA	\N
42	t	2026-07-09 01:38:22.634+00	2026-07-19 16:20:31.389+00	UNIDAD DE MEDICINA FISICA	8
43	t	2026-07-09 01:38:22.701+00	2026-07-19 16:20:31.362+00	HOSPITALIZACION DOMICILIARIA	9
44	t	2026-07-09 01:38:22.714+00	2026-07-19 16:20:31.325+00	ACCESO ATENCION ABIERTA	9
45	t	2026-07-09 01:38:22.744+00	2026-07-19 16:20:31.36+00	FARMACIA Y TOMA DE MUESTRAS	9
46	t	2026-07-09 01:38:22.776+00	2026-07-19 16:20:31.336+00	CONSULTAS Y PROCEDIMIENTOS ADULTO - INFANTIL	9
47	t	2026-07-09 01:38:22.864+00	2026-07-19 16:20:31.351+00	ENDOSCOPIA Y GASTROENTEROLOGIA	8
48	t	2026-07-09 01:38:22.883+00	2026-07-19 16:20:31.393+00	UNIDAD DE ODONTOLOGIA	9
49	t	2026-07-09 01:38:22.942+00	2026-07-19 16:20:31.328+00	ADMINISTRACION ATENCION ABIERTA	9
50	t	2026-07-09 01:38:23.001+00	2026-07-19 16:20:31.37+00	PRAIS	9
51	t	2026-07-09 01:38:23.037+00	2026-07-19 16:20:31.337+00	CONSULTAS Y PROCEDIMIENTOS DE LA MUJER	9
52	t	2026-07-09 01:38:23.04+00	2026-07-19 16:20:31.341+00	CONSULTAS Y PROCEDIMIENTOS INFANTIL	9
53	t	2026-07-09 01:38:23.05+00	2026-07-19 16:20:31.349+00	DISPONIBLE	10
54	t	2026-07-09 01:38:23.121+00	2026-07-19 16:20:31.345+00	DIALISIS	8
55	t	2026-07-09 01:38:23.133+00	2026-07-19 16:20:31.399+00	UNIDAD MEDICINA AMBULATORIA	9
56	t	2026-07-09 01:38:23.198+00	2026-07-19 16:20:31.343+00	CONSULTAS Y PROCEDIMIENTOS SALUD MENTAL	9
57	t	2026-07-09 01:38:23.23+00	2026-07-19 16:20:31.339+00	CONSULTAS Y PROCEDIMIENTOS DEL ADULTO	9
58	t	2026-07-09 01:38:23.343+00	2026-07-19 16:20:31.397+00	UNIDAD INFANTIL	11
59	t	2026-07-09 01:38:23.392+00	2026-07-19 16:20:31.356+00	ESCUELA HOSPITALARIA	11
60	t	2026-07-09 01:38:23.41+00	2026-07-19 16:20:31.395+00	UNIDAD DEL ADULTO	11
61	t	2026-07-09 01:38:23.549+00	2026-07-19 16:20:31.387+00	UNIDAD DE LA MUJER	11
62	t	2026-07-09 01:38:23.603+00	2026-07-19 16:20:31.334+00	CHILE CRECE CONTIGO	11
63	t	2026-07-09 01:38:23.756+00	2026-07-19 16:20:31.381+00	SD RECURSOS HUMANOS	\N
64	t	2026-07-09 01:38:23.833+00	2026-07-19 16:20:31.347+00	DIRECCION	\N
65	t	2026-07-09 01:38:23.858+00	2026-07-19 16:20:31.375+00	SD GESTION ADMINISTRATIVA	\N
66	t	2026-07-09 01:38:23.955+00	2026-07-19 16:20:31.372+00	RECINTOS DE APOYO	\N
67	t	2026-07-09 01:38:23.966+00	2026-07-19 16:20:31.374+00	SD ATENCION USUARIO Y PARTICIPACION SOCIAL	\N
68	t	2026-07-09 01:38:24.019+00	2026-07-19 16:20:31.379+00	SD MEDICO ASISTENCIAL	\N
69	t	2026-07-09 01:38:24.048+00	2026-07-19 16:20:31.332+00	BIBLIOTECA - AUDITORIO	12
70	t	2026-07-09 01:38:24.123+00	2026-07-19 16:20:31.385+00	UNIDAD DE APOYO A LA GESTION	12
71	t	2026-07-09 01:38:24.129+00	2026-07-19 16:20:31.377+00	SD GESTION DEL CUIDADO	12
72	t	2026-07-09 01:38:24.266+00	2026-07-19 16:20:31.33+00	ANATOMIA PATOLOGICA	13
73	t	2026-07-09 01:38:24.31+00	2026-07-19 16:20:31.391+00	UNIDAD DE MEDICINA TRANSFUSIONAL	13
74	t	2026-07-09 01:38:24.322+00	2026-07-19 16:20:31.403+00	UPC INFANTIL Y UNIDAD NEONATOLOGIA	11
75	t	2026-07-09 01:38:24.367+00	2026-07-19 16:20:31.401+00	UPC ADULTO	11
76	t	2026-07-09 01:38:24.493+00	2026-07-19 16:20:31.366+00	LABORATORIO	13
77	t	2026-07-09 01:38:24.574+00	2026-07-19 16:20:31.354+00	EQUIPOS MEDICOS	14
78	t	2026-07-09 01:38:24.604+00	2026-07-19 16:20:31.358+00	FARMACIA	14
79	t	2026-07-09 01:38:24.653+00	2026-07-19 16:20:31.321+00	ABASTECIMIENTO	14
80	t	2026-07-09 01:38:24.747+00	2026-07-19 16:20:31.364+00	IMAGENOLOGIA	8
81	t	2026-07-09 01:38:24.8+00	2026-07-19 16:20:31.383+00	SERVICIOS GENERALES	14
82	t	2026-07-09 01:38:24.823+00	2026-07-19 16:20:31.368+00	PENSIONADO	11
83	t	2026-07-19 04:18:44.606+00	2026-07-19 16:20:31.405+00	UNIDAD QA	\N
\.


--
-- Data for Name: mantenedores_vlan; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.mantenedores_vlan (id, activo, fecha_creacion, fecha_actualizacion, nombre, descripcion) FROM stdin;
\.


--
-- Data for Name: redes_infraestructurared; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.redes_infraestructurared (id, ip_direccion, switch_ip, switch_port, estado, sector, mac, rack, patch_panel, edificio_id, institucion_id, piso_id, unidad_id, vlan_id, pma_id) FROM stdin;
\.


--
-- Data for Name: redes_pma; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.redes_pma (id, codigo, estado, descripcion, edificio_piso_id, unidad_id) FROM stdin;
\.


--
-- Data for Name: redes_rangoip; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.redes_rangoip (id, unidad, ubicacion, pma, rack, dato, rango, ip, estado, comentario, piso_id) FROM stdin;
\.


--
-- Data for Name: redes_slaconfiguracion; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.redes_slaconfiguracion (id, nombre, horas_objetivo, alerta_porcentaje, activo, fecha_creacion, fecha_actualizacion) FROM stdin;
\.


--
-- Data for Name: sla_slamatrix; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.sla_slamatrix (id, impacto, urgencia, tiempo_respuesta_minutos, tiempo_resolucion_horas, prioridad_id) FROM stdin;
\.


--
-- Data for Name: tickets_archivoadjunto; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.tickets_archivoadjunto (id, archivo, fecha_subida, subido_por_id, ticket_id) FROM stdin;
\.


--
-- Data for Name: tickets_categoria; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.tickets_categoria (id, nombre, activa, grupo_resolutor_id) FROM stdin;
7	Hardware	t	\N
8	Software	t	\N
9	Redes	t	\N
10	Soporte General	t	\N
11	Insumos	t	\N
\.


--
-- Data for Name: tickets_gruporesolutor; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.tickets_gruporesolutor (id, nombre, descripcion, activo, icono, is_system) FROM stdin;
10	Soporte Software	Atención de incidentes y requerimientos de software y sistemas informáticos.	t	ms-Icon--Group	f
11	Soporte Hardware	Mantenimiento y reparación de equipos físicos e impresoras.	t	ms-Icon--Group	f
12	Sistemas Médicos	Soporte de sistemas clínicos, HIS, LIS y equipos médicos digitalizados.	t	ms-Icon--Group	f
13	Infraestructura y Redes	Soporte a servidores, conectividad, redes y telefonía.	t	ms-Icon--Group	f
14	Mesa de Ayuda (Derivación)	Primer nivel de atención, filtro y derivación de tickets.	t	ms-Icon--Group	f
15	Soporte Nivel 1	Grupo de Soporte Nivel 1	t	ms-Icon--Group	f
16	Soporte Nivel 2	Grupo de Soporte Nivel 2	t	ms-Icon--Group	f
17	Redes y Comunicaciones	Grupo de Redes y Comunicaciones	t	ms-Icon--Group	f
18	Sistemas Clínicos	Grupo de Sistemas Clínicos	t	ms-Icon--Group	f
19	Mantenimiento Hardware	Grupo de Mantenimiento Hardware	t	ms-Icon--Group	f
\.


--
-- Data for Name: tickets_gruporesolutor_miembros; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.tickets_gruporesolutor_miembros (id, gruporesolutor_id, user_id) FROM stdin;
\.


--
-- Data for Name: tickets_notificacion; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.tickets_notificacion (id, mensaje, leida, fecha_creacion, ticket_id, usuario_id) FROM stdin;
\.


--
-- Data for Name: tickets_prioridad; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.tickets_prioridad (id, nombre, sla_horas, color_hex) FROM stdin;
1	Baja	48	#3b82f6
2	Media	24	#eab308
3	Alta	8	#f97316
4	Crítica	2	#ef4444
5	Media QA	24	#eab308
\.


--
-- Data for Name: tickets_ticket; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.tickets_ticket (id, correlativo, estado, descripcion, diagnostico, solucion, fecha_creacion, fecha_asignacion, fecha_cierre, activo_id, categoria_id, prioridad_id, responsable_id, solicitante_id, creador_id, fecha_vencimiento_sla, impacto, tipo, urgencia, grupo_resolutor_id, anexo_contacto, correo_contacto) FROM stdin;
\.


--
-- Data for Name: tickets_tickethistorial; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.tickets_tickethistorial (id, accion, valor_anterior, valor_nuevo, comentario, fecha, ticket_id, usuario_id) FROM stdin;
\.


--
-- Data for Name: utilidades_ayudarapida; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.utilidades_ayudarapida (id, titulo, contenido, categoria, activo, orden, fecha_creacion, fecha_actualizacion) FROM stdin;
\.


--
-- Data for Name: utilidades_checklistitem; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.utilidades_checklistitem (id, task_name, is_completed, activo, orden, fecha_actualizacion) FROM stdin;
\.


--
-- Data for Name: utilidades_pendiente; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.utilidades_pendiente (id, titulo, link, estado, fecha_creacion, fecha_cierre, fecha_programada) FROM stdin;
\.


--
-- Data for Name: utilidades_webapp; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.utilidades_webapp (id, nombre, url, icono, descripcion, activo, orden, fecha_actualizacion) FROM stdin;
\.


--
-- Data for Name: visor_avisovisor; Type: TABLE DATA; Schema: public; Owner: ticsystem_admin
--

COPY public.visor_avisovisor (id, titulo, mensaje, activo, fecha_creacion, fecha_actualizacion) FROM stdin;
\.


--
-- Name: actas_acta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.actas_acta_id_seq', 10, true);


--
-- Name: actas_actadetalle_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.actas_actadetalle_id_seq', 16, true);


--
-- Name: anexos_anexo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.anexos_anexo_id_seq', 2, true);


--
-- Name: anexos_requerimientocambio_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.anexos_requerimientocambio_id_seq', 1, false);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 3, true);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 236, true);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 244, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 4, true);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 32, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: axes_accessattempt_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.axes_accessattempt_id_seq', 38, true);


--
-- Name: axes_accessfailurelog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.axes_accessfailurelog_id_seq', 1, false);


--
-- Name: axes_accesslog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.axes_accesslog_id_seq', 81, true);


--
-- Name: conocimiento_articuloconocimiento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.conocimiento_articuloconocimiento_id_seq', 1, false);


--
-- Name: conocimiento_categoriaconocimiento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.conocimiento_categoriaconocimiento_id_seq', 1, false);


--
-- Name: core_funcionario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.core_funcionario_id_seq', 22, true);


--
-- Name: core_logauditoria_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.core_logauditoria_id_seq', 681, true);


--
-- Name: core_perfilusuario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.core_perfilusuario_id_seq', 19, true);


--
-- Name: core_rol_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.core_rol_id_seq', 16, true);


--
-- Name: correos_configuracionsmtp_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.correos_configuracionsmtp_id_seq', 1, false);


--
-- Name: correos_correolog_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.correos_correolog_id_seq', 1, false);


--
-- Name: correos_credencialcorreo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.correos_credencialcorreo_id_seq', 1, false);


--
-- Name: correos_grupocorreo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.correos_grupocorreo_id_seq', 1, false);


--
-- Name: correos_miembrogrupocorreo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.correos_miembrogrupocorreo_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_celery_results_chordcounter_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.django_celery_results_chordcounter_id_seq', 1, false);


--
-- Name: django_celery_results_groupresult_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.django_celery_results_groupresult_id_seq', 1, false);


--
-- Name: django_celery_results_taskresult_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.django_celery_results_taskresult_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 61, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 67, true);


--
-- Name: equipos_bitacoraequipo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.equipos_bitacoraequipo_id_seq', 28, true);


--
-- Name: equipos_bitacoraopcion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.equipos_bitacoraopcion_id_seq', 38, true);


--
-- Name: equipos_equipo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.equipos_equipo_id_seq', 3542, true);


--
-- Name: mantenedores_areahospitalaria_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.mantenedores_areahospitalaria_id_seq', 17, true);


--
-- Name: mantenedores_articulo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.mantenedores_articulo_id_seq', 5, true);


--
-- Name: mantenedores_cargo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.mantenedores_cargo_id_seq', 19, true);


--
-- Name: mantenedores_edificio_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.mantenedores_edificio_id_seq', 2, true);


--
-- Name: mantenedores_estadoequipo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.mantenedores_estadoequipo_id_seq', 9, true);


--
-- Name: mantenedores_institucion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.mantenedores_institucion_id_seq', 2, true);


--
-- Name: mantenedores_marca_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.mantenedores_marca_id_seq', 4, true);


--
-- Name: mantenedores_modelo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.mantenedores_modelo_id_seq', 4, true);


--
-- Name: mantenedores_modeloanexo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.mantenedores_modeloanexo_id_seq', 5, true);


--
-- Name: mantenedores_piso_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.mantenedores_piso_id_seq', 16, true);


--
-- Name: mantenedores_pma_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.mantenedores_pma_id_seq', 1012, true);


--
-- Name: mantenedores_proveedor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.mantenedores_proveedor_id_seq', 1, true);


--
-- Name: mantenedores_recinto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.mantenedores_recinto_id_seq', 404, true);


--
-- Name: mantenedores_sector_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.mantenedores_sector_id_seq', 14, true);


--
-- Name: mantenedores_sistemaoperativo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.mantenedores_sistemaoperativo_id_seq', 1, true);


--
-- Name: mantenedores_unidad_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.mantenedores_unidad_id_seq', 84, true);


--
-- Name: mantenedores_vlan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.mantenedores_vlan_id_seq', 1, false);


--
-- Name: redes_infraestructurared_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.redes_infraestructurared_id_seq', 1, false);


--
-- Name: redes_pma_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.redes_pma_id_seq', 1, false);


--
-- Name: redes_rangoip_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.redes_rangoip_id_seq', 1, false);


--
-- Name: redes_slaconfiguracion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.redes_slaconfiguracion_id_seq', 1, false);


--
-- Name: sla_slamatrix_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.sla_slamatrix_id_seq', 12, true);


--
-- Name: tickets_archivoadjunto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.tickets_archivoadjunto_id_seq', 1, false);


--
-- Name: tickets_categoria_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.tickets_categoria_id_seq', 11, true);


--
-- Name: tickets_gruporesolutor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.tickets_gruporesolutor_id_seq', 19, true);


--
-- Name: tickets_gruporesolutor_miembros_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.tickets_gruporesolutor_miembros_id_seq', 55, true);


--
-- Name: tickets_notificacion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.tickets_notificacion_id_seq', 2, true);


--
-- Name: tickets_prioridad_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.tickets_prioridad_id_seq', 5, true);


--
-- Name: tickets_ticket_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.tickets_ticket_id_seq', 64, true);


--
-- Name: tickets_tickethistorial_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.tickets_tickethistorial_id_seq', 164, true);


--
-- Name: utilidades_ayudarapida_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.utilidades_ayudarapida_id_seq', 1, false);


--
-- Name: utilidades_checklistitem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.utilidades_checklistitem_id_seq', 1, false);


--
-- Name: utilidades_pendiente_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.utilidades_pendiente_id_seq', 1, false);


--
-- Name: utilidades_webapp_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.utilidades_webapp_id_seq', 1, false);


--
-- Name: visor_avisovisor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ticsystem_admin
--

SELECT pg_catalog.setval('public.visor_avisovisor_id_seq', 1, false);


--
-- Name: actas_acta actas_acta_codigo_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.actas_acta
    ADD CONSTRAINT actas_acta_codigo_key UNIQUE (codigo);


--
-- Name: actas_acta actas_acta_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.actas_acta
    ADD CONSTRAINT actas_acta_pkey PRIMARY KEY (id);


--
-- Name: actas_actadetalle actas_actadetalle_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.actas_actadetalle
    ADD CONSTRAINT actas_actadetalle_pkey PRIMARY KEY (id);


--
-- Name: anexos_anexo anexos_anexo_numero_anexo_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.anexos_anexo
    ADD CONSTRAINT anexos_anexo_numero_anexo_key UNIQUE (numero_anexo);


--
-- Name: anexos_anexo anexos_anexo_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.anexos_anexo
    ADD CONSTRAINT anexos_anexo_pkey PRIMARY KEY (id);


--
-- Name: anexos_anexo anexos_anexo_serial_number_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.anexos_anexo
    ADD CONSTRAINT anexos_anexo_serial_number_key UNIQUE (serial_number);


--
-- Name: anexos_requerimientocambio anexos_requerimientocambio_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.anexos_requerimientocambio
    ADD CONSTRAINT anexos_requerimientocambio_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: axes_accessattempt axes_accessattempt_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.axes_accessattempt
    ADD CONSTRAINT axes_accessattempt_pkey PRIMARY KEY (id);


--
-- Name: axes_accessattempt axes_accessattempt_username_ip_address_user_agent_8ea22282_uniq; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.axes_accessattempt
    ADD CONSTRAINT axes_accessattempt_username_ip_address_user_agent_8ea22282_uniq UNIQUE (username, ip_address, user_agent);


--
-- Name: axes_accessattemptexpiration axes_accessattemptexpiration_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.axes_accessattemptexpiration
    ADD CONSTRAINT axes_accessattemptexpiration_pkey PRIMARY KEY (access_attempt_id);


--
-- Name: axes_accessfailurelog axes_accessfailurelog_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.axes_accessfailurelog
    ADD CONSTRAINT axes_accessfailurelog_pkey PRIMARY KEY (id);


--
-- Name: axes_accesslog axes_accesslog_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.axes_accesslog
    ADD CONSTRAINT axes_accesslog_pkey PRIMARY KEY (id);


--
-- Name: conocimiento_articuloconocimiento conocimiento_articuloconocimiento_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.conocimiento_articuloconocimiento
    ADD CONSTRAINT conocimiento_articuloconocimiento_pkey PRIMARY KEY (id);


--
-- Name: conocimiento_categoriaconocimiento conocimiento_categoriaconocimiento_nombre_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.conocimiento_categoriaconocimiento
    ADD CONSTRAINT conocimiento_categoriaconocimiento_nombre_key UNIQUE (nombre);


--
-- Name: conocimiento_categoriaconocimiento conocimiento_categoriaconocimiento_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.conocimiento_categoriaconocimiento
    ADD CONSTRAINT conocimiento_categoriaconocimiento_pkey PRIMARY KEY (id);


--
-- Name: core_funcionario core_funcionario_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.core_funcionario
    ADD CONSTRAINT core_funcionario_pkey PRIMARY KEY (id);


--
-- Name: core_funcionario core_funcionario_rut_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.core_funcionario
    ADD CONSTRAINT core_funcionario_rut_key UNIQUE (rut);


--
-- Name: core_logauditoria core_logauditoria_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.core_logauditoria
    ADD CONSTRAINT core_logauditoria_pkey PRIMARY KEY (id);


--
-- Name: core_perfilusuario core_perfilusuario_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.core_perfilusuario
    ADD CONSTRAINT core_perfilusuario_pkey PRIMARY KEY (id);


--
-- Name: core_perfilusuario core_perfilusuario_rut_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.core_perfilusuario
    ADD CONSTRAINT core_perfilusuario_rut_key UNIQUE (rut);


--
-- Name: core_perfilusuario core_perfilusuario_user_id_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.core_perfilusuario
    ADD CONSTRAINT core_perfilusuario_user_id_key UNIQUE (user_id);


--
-- Name: core_rol core_rol_nombre_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.core_rol
    ADD CONSTRAINT core_rol_nombre_key UNIQUE (nombre);


--
-- Name: core_rol core_rol_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.core_rol
    ADD CONSTRAINT core_rol_pkey PRIMARY KEY (id);


--
-- Name: correos_configuracionsmtp correos_configuracionsmtp_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.correos_configuracionsmtp
    ADD CONSTRAINT correos_configuracionsmtp_pkey PRIMARY KEY (id);


--
-- Name: correos_correolog correos_correolog_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.correos_correolog
    ADD CONSTRAINT correos_correolog_pkey PRIMARY KEY (id);


--
-- Name: correos_credencialcorreo correos_credencialcorreo_email_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.correos_credencialcorreo
    ADD CONSTRAINT correos_credencialcorreo_email_key UNIQUE (email);


--
-- Name: correos_credencialcorreo correos_credencialcorreo_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.correos_credencialcorreo
    ADD CONSTRAINT correos_credencialcorreo_pkey PRIMARY KEY (id);


--
-- Name: correos_grupocorreo correos_grupocorreo_nombre_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.correos_grupocorreo
    ADD CONSTRAINT correos_grupocorreo_nombre_key UNIQUE (nombre);


--
-- Name: correos_grupocorreo correos_grupocorreo_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.correos_grupocorreo
    ADD CONSTRAINT correos_grupocorreo_pkey PRIMARY KEY (id);


--
-- Name: correos_miembrogrupocorreo correos_miembrogrupocorreo_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.correos_miembrogrupocorreo
    ADD CONSTRAINT correos_miembrogrupocorreo_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_celery_results_chordcounter django_celery_results_chordcounter_group_id_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.django_celery_results_chordcounter
    ADD CONSTRAINT django_celery_results_chordcounter_group_id_key UNIQUE (group_id);


--
-- Name: django_celery_results_chordcounter django_celery_results_chordcounter_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.django_celery_results_chordcounter
    ADD CONSTRAINT django_celery_results_chordcounter_pkey PRIMARY KEY (id);


--
-- Name: django_celery_results_groupresult django_celery_results_groupresult_group_id_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.django_celery_results_groupresult
    ADD CONSTRAINT django_celery_results_groupresult_group_id_key UNIQUE (group_id);


--
-- Name: django_celery_results_groupresult django_celery_results_groupresult_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.django_celery_results_groupresult
    ADD CONSTRAINT django_celery_results_groupresult_pkey PRIMARY KEY (id);


--
-- Name: django_celery_results_taskresult django_celery_results_taskresult_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.django_celery_results_taskresult
    ADD CONSTRAINT django_celery_results_taskresult_pkey PRIMARY KEY (id);


--
-- Name: django_celery_results_taskresult django_celery_results_taskresult_task_id_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.django_celery_results_taskresult
    ADD CONSTRAINT django_celery_results_taskresult_task_id_key UNIQUE (task_id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: equipos_bitacoraequipo equipos_bitacoraequipo_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.equipos_bitacoraequipo
    ADD CONSTRAINT equipos_bitacoraequipo_pkey PRIMARY KEY (id);


--
-- Name: equipos_bitacoraopcion equipos_bitacoraopcion_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.equipos_bitacoraopcion
    ADD CONSTRAINT equipos_bitacoraopcion_pkey PRIMARY KEY (id);


--
-- Name: equipos_equipo equipos_equipo_num_inventario_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.equipos_equipo
    ADD CONSTRAINT equipos_equipo_num_inventario_key UNIQUE (num_inventario);


--
-- Name: equipos_equipo equipos_equipo_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.equipos_equipo
    ADD CONSTRAINT equipos_equipo_pkey PRIMARY KEY (id);


--
-- Name: equipos_equipo equipos_equipo_serial_number_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.equipos_equipo
    ADD CONSTRAINT equipos_equipo_serial_number_key UNIQUE (serial_number);


--
-- Name: mantenedores_areahospitalaria mantenedores_areahospitalaria_nombre_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_areahospitalaria
    ADD CONSTRAINT mantenedores_areahospitalaria_nombre_key UNIQUE (nombre);


--
-- Name: mantenedores_areahospitalaria mantenedores_areahospitalaria_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_areahospitalaria
    ADD CONSTRAINT mantenedores_areahospitalaria_pkey PRIMARY KEY (id);


--
-- Name: mantenedores_articulo mantenedores_articulo_nombre_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_articulo
    ADD CONSTRAINT mantenedores_articulo_nombre_key UNIQUE (nombre);


--
-- Name: mantenedores_articulo mantenedores_articulo_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_articulo
    ADD CONSTRAINT mantenedores_articulo_pkey PRIMARY KEY (id);


--
-- Name: mantenedores_cargo mantenedores_cargo_nombre_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_cargo
    ADD CONSTRAINT mantenedores_cargo_nombre_key UNIQUE (nombre);


--
-- Name: mantenedores_cargo mantenedores_cargo_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_cargo
    ADD CONSTRAINT mantenedores_cargo_pkey PRIMARY KEY (id);


--
-- Name: mantenedores_edificio mantenedores_edificio_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_edificio
    ADD CONSTRAINT mantenedores_edificio_pkey PRIMARY KEY (id);


--
-- Name: mantenedores_estadoequipo mantenedores_estadoequipo_nombre_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_estadoequipo
    ADD CONSTRAINT mantenedores_estadoequipo_nombre_key UNIQUE (nombre);


--
-- Name: mantenedores_estadoequipo mantenedores_estadoequipo_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_estadoequipo
    ADD CONSTRAINT mantenedores_estadoequipo_pkey PRIMARY KEY (id);


--
-- Name: mantenedores_institucion mantenedores_institucion_codigo_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_institucion
    ADD CONSTRAINT mantenedores_institucion_codigo_key UNIQUE (codigo);


--
-- Name: mantenedores_institucion mantenedores_institucion_nombre_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_institucion
    ADD CONSTRAINT mantenedores_institucion_nombre_key UNIQUE (nombre);


--
-- Name: mantenedores_institucion mantenedores_institucion_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_institucion
    ADD CONSTRAINT mantenedores_institucion_pkey PRIMARY KEY (id);


--
-- Name: mantenedores_marca mantenedores_marca_nombre_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_marca
    ADD CONSTRAINT mantenedores_marca_nombre_key UNIQUE (nombre);


--
-- Name: mantenedores_marca mantenedores_marca_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_marca
    ADD CONSTRAINT mantenedores_marca_pkey PRIMARY KEY (id);


--
-- Name: mantenedores_modelo mantenedores_modelo_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_modelo
    ADD CONSTRAINT mantenedores_modelo_pkey PRIMARY KEY (id);


--
-- Name: mantenedores_modeloanexo mantenedores_modeloanexo_nombre_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_modeloanexo
    ADD CONSTRAINT mantenedores_modeloanexo_nombre_key UNIQUE (nombre);


--
-- Name: mantenedores_modeloanexo mantenedores_modeloanexo_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_modeloanexo
    ADD CONSTRAINT mantenedores_modeloanexo_pkey PRIMARY KEY (id);


--
-- Name: mantenedores_piso mantenedores_piso_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_piso
    ADD CONSTRAINT mantenedores_piso_pkey PRIMARY KEY (id);


--
-- Name: mantenedores_pma mantenedores_pma_nombre_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_pma
    ADD CONSTRAINT mantenedores_pma_nombre_key UNIQUE (nombre);


--
-- Name: mantenedores_pma mantenedores_pma_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_pma
    ADD CONSTRAINT mantenedores_pma_pkey PRIMARY KEY (id);


--
-- Name: mantenedores_proveedor mantenedores_proveedor_nombre_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_proveedor
    ADD CONSTRAINT mantenedores_proveedor_nombre_key UNIQUE (nombre);


--
-- Name: mantenedores_proveedor mantenedores_proveedor_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_proveedor
    ADD CONSTRAINT mantenedores_proveedor_pkey PRIMARY KEY (id);


--
-- Name: mantenedores_recinto mantenedores_recinto_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_recinto
    ADD CONSTRAINT mantenedores_recinto_pkey PRIMARY KEY (id);


--
-- Name: mantenedores_sector mantenedores_sector_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_sector
    ADD CONSTRAINT mantenedores_sector_pkey PRIMARY KEY (id);


--
-- Name: mantenedores_sistemaoperativo mantenedores_sistemaoperativo_nombre_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_sistemaoperativo
    ADD CONSTRAINT mantenedores_sistemaoperativo_nombre_key UNIQUE (nombre);


--
-- Name: mantenedores_sistemaoperativo mantenedores_sistemaoperativo_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_sistemaoperativo
    ADD CONSTRAINT mantenedores_sistemaoperativo_pkey PRIMARY KEY (id);


--
-- Name: mantenedores_unidad mantenedores_unidad_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_unidad
    ADD CONSTRAINT mantenedores_unidad_pkey PRIMARY KEY (id);


--
-- Name: mantenedores_vlan mantenedores_vlan_nombre_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_vlan
    ADD CONSTRAINT mantenedores_vlan_nombre_key UNIQUE (nombre);


--
-- Name: mantenedores_vlan mantenedores_vlan_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_vlan
    ADD CONSTRAINT mantenedores_vlan_pkey PRIMARY KEY (id);


--
-- Name: redes_infraestructurared redes_infraestructurared_ip_direccion_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.redes_infraestructurared
    ADD CONSTRAINT redes_infraestructurared_ip_direccion_key UNIQUE (ip_direccion);


--
-- Name: redes_infraestructurared redes_infraestructurared_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.redes_infraestructurared
    ADD CONSTRAINT redes_infraestructurared_pkey PRIMARY KEY (id);


--
-- Name: redes_pma redes_pma_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.redes_pma
    ADD CONSTRAINT redes_pma_pkey PRIMARY KEY (id);


--
-- Name: redes_rangoip redes_rangoip_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.redes_rangoip
    ADD CONSTRAINT redes_rangoip_pkey PRIMARY KEY (id);


--
-- Name: redes_slaconfiguracion redes_slaconfiguracion_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.redes_slaconfiguracion
    ADD CONSTRAINT redes_slaconfiguracion_pkey PRIMARY KEY (id);


--
-- Name: sla_slamatrix sla_slamatrix_impacto_urgencia_5bc9bf0b_uniq; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.sla_slamatrix
    ADD CONSTRAINT sla_slamatrix_impacto_urgencia_5bc9bf0b_uniq UNIQUE (impacto, urgencia);


--
-- Name: sla_slamatrix sla_slamatrix_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.sla_slamatrix
    ADD CONSTRAINT sla_slamatrix_pkey PRIMARY KEY (id);


--
-- Name: tickets_archivoadjunto tickets_archivoadjunto_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.tickets_archivoadjunto
    ADD CONSTRAINT tickets_archivoadjunto_pkey PRIMARY KEY (id);


--
-- Name: tickets_categoria tickets_categoria_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.tickets_categoria
    ADD CONSTRAINT tickets_categoria_pkey PRIMARY KEY (id);


--
-- Name: tickets_gruporesolutor_miembros tickets_gruporesolutor_m_gruporesolutor_id_user_i_bf921b40_uniq; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.tickets_gruporesolutor_miembros
    ADD CONSTRAINT tickets_gruporesolutor_m_gruporesolutor_id_user_i_bf921b40_uniq UNIQUE (gruporesolutor_id, user_id);


--
-- Name: tickets_gruporesolutor_miembros tickets_gruporesolutor_miembros_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.tickets_gruporesolutor_miembros
    ADD CONSTRAINT tickets_gruporesolutor_miembros_pkey PRIMARY KEY (id);


--
-- Name: tickets_gruporesolutor tickets_gruporesolutor_nombre_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.tickets_gruporesolutor
    ADD CONSTRAINT tickets_gruporesolutor_nombre_key UNIQUE (nombre);


--
-- Name: tickets_gruporesolutor tickets_gruporesolutor_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.tickets_gruporesolutor
    ADD CONSTRAINT tickets_gruporesolutor_pkey PRIMARY KEY (id);


--
-- Name: tickets_notificacion tickets_notificacion_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.tickets_notificacion
    ADD CONSTRAINT tickets_notificacion_pkey PRIMARY KEY (id);


--
-- Name: tickets_prioridad tickets_prioridad_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.tickets_prioridad
    ADD CONSTRAINT tickets_prioridad_pkey PRIMARY KEY (id);


--
-- Name: tickets_ticket tickets_ticket_correlativo_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.tickets_ticket
    ADD CONSTRAINT tickets_ticket_correlativo_key UNIQUE (correlativo);


--
-- Name: tickets_ticket tickets_ticket_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.tickets_ticket
    ADD CONSTRAINT tickets_ticket_pkey PRIMARY KEY (id);


--
-- Name: tickets_tickethistorial tickets_tickethistorial_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.tickets_tickethistorial
    ADD CONSTRAINT tickets_tickethistorial_pkey PRIMARY KEY (id);


--
-- Name: equipos_bitacoraopcion uniq_bitacora_opcion_tipo_nombre; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.equipos_bitacoraopcion
    ADD CONSTRAINT uniq_bitacora_opcion_tipo_nombre UNIQUE (tipo, nombre);


--
-- Name: mantenedores_edificio uniq_edificio_nombre_institucion; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_edificio
    ADD CONSTRAINT uniq_edificio_nombre_institucion UNIQUE (nombre, institucion_id);


--
-- Name: correos_miembrogrupocorreo uniq_miembro_grupo_email; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.correos_miembrogrupocorreo
    ADD CONSTRAINT uniq_miembro_grupo_email UNIQUE (grupo_id, email);


--
-- Name: mantenedores_modelo uniq_modelo_marca_nombre; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_modelo
    ADD CONSTRAINT uniq_modelo_marca_nombre UNIQUE (marca_id, nombre);


--
-- Name: mantenedores_piso uniq_piso_edificio_nombre; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_piso
    ADD CONSTRAINT uniq_piso_edificio_nombre UNIQUE (edificio_id, nombre);


--
-- Name: redes_pma uniq_pma_codigo_piso; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.redes_pma
    ADD CONSTRAINT uniq_pma_codigo_piso UNIQUE (codigo, edificio_piso_id);


--
-- Name: utilidades_ayudarapida utilidades_ayudarapida_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.utilidades_ayudarapida
    ADD CONSTRAINT utilidades_ayudarapida_pkey PRIMARY KEY (id);


--
-- Name: utilidades_ayudarapida utilidades_ayudarapida_titulo_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.utilidades_ayudarapida
    ADD CONSTRAINT utilidades_ayudarapida_titulo_key UNIQUE (titulo);


--
-- Name: utilidades_checklistitem utilidades_checklistitem_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.utilidades_checklistitem
    ADD CONSTRAINT utilidades_checklistitem_pkey PRIMARY KEY (id);


--
-- Name: utilidades_pendiente utilidades_pendiente_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.utilidades_pendiente
    ADD CONSTRAINT utilidades_pendiente_pkey PRIMARY KEY (id);


--
-- Name: utilidades_webapp utilidades_webapp_nombre_key; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.utilidades_webapp
    ADD CONSTRAINT utilidades_webapp_nombre_key UNIQUE (nombre);


--
-- Name: utilidades_webapp utilidades_webapp_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.utilidades_webapp
    ADD CONSTRAINT utilidades_webapp_pkey PRIMARY KEY (id);


--
-- Name: visor_avisovisor visor_avisovisor_pkey; Type: CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.visor_avisovisor
    ADD CONSTRAINT visor_avisovisor_pkey PRIMARY KEY (id);


--
-- Name: actas_acta_codigo_2760a1b3_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX actas_acta_codigo_2760a1b3_like ON public.actas_acta USING btree (codigo varchar_pattern_ops);


--
-- Name: actas_acta_encargado_id_285fabdc; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX actas_acta_encargado_id_285fabdc ON public.actas_acta USING btree (encargado_id);


--
-- Name: actas_acta_estado_e12ae8fb; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX actas_acta_estado_e12ae8fb ON public.actas_acta USING btree (estado);


--
-- Name: actas_acta_estado_e12ae8fb_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX actas_acta_estado_e12ae8fb_like ON public.actas_acta USING btree (estado varchar_pattern_ops);


--
-- Name: actas_actadetalle_acta_id_73ddccab; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX actas_actadetalle_acta_id_73ddccab ON public.actas_actadetalle USING btree (acta_id);


--
-- Name: actas_actadetalle_edificio_id_1cb35d69; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX actas_actadetalle_edificio_id_1cb35d69 ON public.actas_actadetalle USING btree (edificio_id);


--
-- Name: actas_actadetalle_piso_id_89ab3dd4; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX actas_actadetalle_piso_id_89ab3dd4 ON public.actas_actadetalle USING btree (piso_id);


--
-- Name: actas_actadetalle_unidad_id_4650aec0; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX actas_actadetalle_unidad_id_4650aec0 ON public.actas_actadetalle USING btree (unidad_id);


--
-- Name: anexos_anexo_actualizado_por_id_f880f1ee; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX anexos_anexo_actualizado_por_id_f880f1ee ON public.anexos_anexo USING btree (actualizado_por_id);


--
-- Name: anexos_anexo_creado_por_id_ea30cea2; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX anexos_anexo_creado_por_id_ea30cea2 ON public.anexos_anexo USING btree (creado_por_id);


--
-- Name: anexos_anexo_edificio_id_b9966609; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX anexos_anexo_edificio_id_b9966609 ON public.anexos_anexo USING btree (edificio_id);


--
-- Name: anexos_anexo_establecimiento_id_9d0fc07f; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX anexos_anexo_establecimiento_id_9d0fc07f ON public.anexos_anexo USING btree (establecimiento_id);


--
-- Name: anexos_anexo_estado_bb9fa0d9; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX anexos_anexo_estado_bb9fa0d9 ON public.anexos_anexo USING btree (estado);


--
-- Name: anexos_anexo_estado_bb9fa0d9_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX anexos_anexo_estado_bb9fa0d9_like ON public.anexos_anexo USING btree (estado varchar_pattern_ops);


--
-- Name: anexos_anexo_modelo_anexo_id_1ce2338e; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX anexos_anexo_modelo_anexo_id_1ce2338e ON public.anexos_anexo USING btree (modelo_anexo_id);


--
-- Name: anexos_anexo_numero_anexo_bc584d6f_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX anexos_anexo_numero_anexo_bc584d6f_like ON public.anexos_anexo USING btree (numero_anexo varchar_pattern_ops);


--
-- Name: anexos_anexo_piso_id_d0bd0bc3; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX anexos_anexo_piso_id_d0bd0bc3 ON public.anexos_anexo USING btree (piso_id);


--
-- Name: anexos_anexo_pma_id_b62bc2ba; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX anexos_anexo_pma_id_b62bc2ba ON public.anexos_anexo USING btree (pma_id);


--
-- Name: anexos_anexo_proveedor_id_358de8b5; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX anexos_anexo_proveedor_id_358de8b5 ON public.anexos_anexo USING btree (proveedor_id);


--
-- Name: anexos_anexo_serial_number_0e9f324c_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX anexos_anexo_serial_number_0e9f324c_like ON public.anexos_anexo USING btree (serial_number varchar_pattern_ops);


--
-- Name: anexos_anexo_unidad_id_cd2392a1; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX anexos_anexo_unidad_id_cd2392a1 ON public.anexos_anexo USING btree (unidad_id);


--
-- Name: anexos_requerimientocambio_anexo_id_0e4ade28; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX anexos_requerimientocambio_anexo_id_0e4ade28 ON public.anexos_requerimientocambio USING btree (anexo_id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: axes_accessattempt_ip_address_10922d9c; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX axes_accessattempt_ip_address_10922d9c ON public.axes_accessattempt USING btree (ip_address);


--
-- Name: axes_accessattempt_user_agent_ad89678b; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX axes_accessattempt_user_agent_ad89678b ON public.axes_accessattempt USING btree (user_agent);


--
-- Name: axes_accessattempt_user_agent_ad89678b_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX axes_accessattempt_user_agent_ad89678b_like ON public.axes_accessattempt USING btree (user_agent varchar_pattern_ops);


--
-- Name: axes_accessattempt_username_3f2d4ca0; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX axes_accessattempt_username_3f2d4ca0 ON public.axes_accessattempt USING btree (username);


--
-- Name: axes_accessattempt_username_3f2d4ca0_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX axes_accessattempt_username_3f2d4ca0_like ON public.axes_accessattempt USING btree (username varchar_pattern_ops);


--
-- Name: axes_accessfailurelog_ip_address_2e9f5a7f; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX axes_accessfailurelog_ip_address_2e9f5a7f ON public.axes_accessfailurelog USING btree (ip_address);


--
-- Name: axes_accessfailurelog_user_agent_ea145dda; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX axes_accessfailurelog_user_agent_ea145dda ON public.axes_accessfailurelog USING btree (user_agent);


--
-- Name: axes_accessfailurelog_user_agent_ea145dda_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX axes_accessfailurelog_user_agent_ea145dda_like ON public.axes_accessfailurelog USING btree (user_agent varchar_pattern_ops);


--
-- Name: axes_accessfailurelog_username_a8b7e8a4; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX axes_accessfailurelog_username_a8b7e8a4 ON public.axes_accessfailurelog USING btree (username);


--
-- Name: axes_accessfailurelog_username_a8b7e8a4_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX axes_accessfailurelog_username_a8b7e8a4_like ON public.axes_accessfailurelog USING btree (username varchar_pattern_ops);


--
-- Name: axes_accesslog_ip_address_86b417e5; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX axes_accesslog_ip_address_86b417e5 ON public.axes_accesslog USING btree (ip_address);


--
-- Name: axes_accesslog_user_agent_0e659004; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX axes_accesslog_user_agent_0e659004 ON public.axes_accesslog USING btree (user_agent);


--
-- Name: axes_accesslog_user_agent_0e659004_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX axes_accesslog_user_agent_0e659004_like ON public.axes_accesslog USING btree (user_agent varchar_pattern_ops);


--
-- Name: axes_accesslog_username_df93064b; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX axes_accesslog_username_df93064b ON public.axes_accesslog USING btree (username);


--
-- Name: axes_accesslog_username_df93064b_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX axes_accesslog_username_df93064b_like ON public.axes_accesslog USING btree (username varchar_pattern_ops);


--
-- Name: conocimiento_articuloconocimiento_categoria_id_2331dc21; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX conocimiento_articuloconocimiento_categoria_id_2331dc21 ON public.conocimiento_articuloconocimiento USING btree (categoria_id);


--
-- Name: conocimiento_categoriaconocimiento_nombre_fd098266_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX conocimiento_categoriaconocimiento_nombre_fd098266_like ON public.conocimiento_categoriaconocimiento USING btree (nombre varchar_pattern_ops);


--
-- Name: core_funcionario_cargo_id_43291cdf; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX core_funcionario_cargo_id_43291cdf ON public.core_funcionario USING btree (cargo_id);


--
-- Name: core_funcionario_rut_6ce3638d_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX core_funcionario_rut_6ce3638d_like ON public.core_funcionario USING btree (rut varchar_pattern_ops);


--
-- Name: core_funcionario_unidad_id_151a2b97; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX core_funcionario_unidad_id_151a2b97 ON public.core_funcionario USING btree (unidad_id);


--
-- Name: core_logauditoria_accion_473925e9; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX core_logauditoria_accion_473925e9 ON public.core_logauditoria USING btree (accion);


--
-- Name: core_logauditoria_accion_473925e9_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX core_logauditoria_accion_473925e9_like ON public.core_logauditoria USING btree (accion varchar_pattern_ops);


--
-- Name: core_logauditoria_fecha_registro_bdd4ceca; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX core_logauditoria_fecha_registro_bdd4ceca ON public.core_logauditoria USING btree (fecha_registro);


--
-- Name: core_logauditoria_registro_id_34747d4a; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX core_logauditoria_registro_id_34747d4a ON public.core_logauditoria USING btree (registro_id);


--
-- Name: core_logauditoria_registro_id_34747d4a_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX core_logauditoria_registro_id_34747d4a_like ON public.core_logauditoria USING btree (registro_id varchar_pattern_ops);


--
-- Name: core_logauditoria_tabla_f0cfb57f; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX core_logauditoria_tabla_f0cfb57f ON public.core_logauditoria USING btree (tabla);


--
-- Name: core_logauditoria_tabla_f0cfb57f_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX core_logauditoria_tabla_f0cfb57f_like ON public.core_logauditoria USING btree (tabla varchar_pattern_ops);


--
-- Name: core_logauditoria_usuario_929eb424; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX core_logauditoria_usuario_929eb424 ON public.core_logauditoria USING btree (usuario);


--
-- Name: core_logauditoria_usuario_929eb424_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX core_logauditoria_usuario_929eb424_like ON public.core_logauditoria USING btree (usuario varchar_pattern_ops);


--
-- Name: core_perfilusuario_rol_id_dd0e25c8; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX core_perfilusuario_rol_id_dd0e25c8 ON public.core_perfilusuario USING btree (rol_id);


--
-- Name: core_perfilusuario_rut_13bd4ad0_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX core_perfilusuario_rut_13bd4ad0_like ON public.core_perfilusuario USING btree (rut varchar_pattern_ops);


--
-- Name: core_rol_activo_8ec146ad; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX core_rol_activo_8ec146ad ON public.core_rol USING btree (activo);


--
-- Name: core_rol_nombre_766ba3b6_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX core_rol_nombre_766ba3b6_like ON public.core_rol USING btree (nombre varchar_pattern_ops);


--
-- Name: core_rol_orden_b482695e; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX core_rol_orden_b482695e ON public.core_rol USING btree (orden);


--
-- Name: correos_cor_estado_41c840_idx; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX correos_cor_estado_41c840_idx ON public.correos_correolog USING btree (estado, fecha_creacion);


--
-- Name: correos_cor_ticket__551fd6_idx; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX correos_cor_ticket__551fd6_idx ON public.correos_correolog USING btree (ticket_id);


--
-- Name: correos_correolog_ticket_id_1790aa94; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX correos_correolog_ticket_id_1790aa94 ON public.correos_correolog USING btree (ticket_id);


--
-- Name: correos_credencialcorreo_email_04588194_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX correos_credencialcorreo_email_04588194_like ON public.correos_credencialcorreo USING btree (email varchar_pattern_ops);


--
-- Name: correos_grupocorreo_nombre_885175f6_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX correos_grupocorreo_nombre_885175f6_like ON public.correos_grupocorreo USING btree (nombre varchar_pattern_ops);


--
-- Name: correos_miembrogrupocorreo_grupo_id_05325d71; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX correos_miembrogrupocorreo_grupo_id_05325d71 ON public.correos_miembrogrupocorreo USING btree (grupo_id);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_cele_date_cr_bd6c1d_idx; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX django_cele_date_cr_bd6c1d_idx ON public.django_celery_results_groupresult USING btree (date_created);


--
-- Name: django_cele_date_cr_f04a50_idx; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX django_cele_date_cr_f04a50_idx ON public.django_celery_results_taskresult USING btree (date_created);


--
-- Name: django_cele_date_do_caae0e_idx; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX django_cele_date_do_caae0e_idx ON public.django_celery_results_groupresult USING btree (date_done);


--
-- Name: django_cele_date_do_f59aad_idx; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX django_cele_date_do_f59aad_idx ON public.django_celery_results_taskresult USING btree (date_done);


--
-- Name: django_cele_periodi_1993cf_idx; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX django_cele_periodi_1993cf_idx ON public.django_celery_results_taskresult USING btree (periodic_task_name);


--
-- Name: django_cele_status_9b6201_idx; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX django_cele_status_9b6201_idx ON public.django_celery_results_taskresult USING btree (status);


--
-- Name: django_cele_task_na_08aec9_idx; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX django_cele_task_na_08aec9_idx ON public.django_celery_results_taskresult USING btree (task_name);


--
-- Name: django_cele_worker_d54dd8_idx; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX django_cele_worker_d54dd8_idx ON public.django_celery_results_taskresult USING btree (worker);


--
-- Name: django_celery_results_chordcounter_group_id_1f70858c_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX django_celery_results_chordcounter_group_id_1f70858c_like ON public.django_celery_results_chordcounter USING btree (group_id varchar_pattern_ops);


--
-- Name: django_celery_results_groupresult_group_id_a085f1a9_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX django_celery_results_groupresult_group_id_a085f1a9_like ON public.django_celery_results_groupresult USING btree (group_id varchar_pattern_ops);


--
-- Name: django_celery_results_taskresult_task_id_de0d95bf_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX django_celery_results_taskresult_task_id_de0d95bf_like ON public.django_celery_results_taskresult USING btree (task_id varchar_pattern_ops);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: equipos_bitacoraequipo_equipo_id_a0f57a1d; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX equipos_bitacoraequipo_equipo_id_a0f57a1d ON public.equipos_bitacoraequipo USING btree (equipo_id);


--
-- Name: equipos_bitacoraequipo_solicitante_id_f5b2c848; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX equipos_bitacoraequipo_solicitante_id_f5b2c848 ON public.equipos_bitacoraequipo USING btree (solicitante_id);


--
-- Name: equipos_bitacoraequipo_tecnico_id_e0b7c38a; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX equipos_bitacoraequipo_tecnico_id_e0b7c38a ON public.equipos_bitacoraequipo USING btree (tecnico_id);


--
-- Name: equipos_bitacoraopcion_activo_8ff983fc; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX equipos_bitacoraopcion_activo_8ff983fc ON public.equipos_bitacoraopcion USING btree (activo);


--
-- Name: equipos_bitacoraopcion_creado_por_id_6f47db54; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX equipos_bitacoraopcion_creado_por_id_6f47db54 ON public.equipos_bitacoraopcion USING btree (creado_por_id);


--
-- Name: equipos_bitacoraopcion_orden_be457f2f; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX equipos_bitacoraopcion_orden_be457f2f ON public.equipos_bitacoraopcion USING btree (orden);


--
-- Name: equipos_bitacoraopcion_tipo_2dc40b92; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX equipos_bitacoraopcion_tipo_2dc40b92 ON public.equipos_bitacoraopcion USING btree (tipo);


--
-- Name: equipos_bitacoraopcion_tipo_2dc40b92_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX equipos_bitacoraopcion_tipo_2dc40b92_like ON public.equipos_bitacoraopcion USING btree (tipo varchar_pattern_ops);


--
-- Name: equipos_equ_estado__598d3b_idx; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX equipos_equ_estado__598d3b_idx ON public.equipos_equipo USING btree (estado_id);


--
-- Name: equipos_equ_serial__26fea4_idx; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX equipos_equ_serial__26fea4_idx ON public.equipos_equipo USING btree (serial_number);


--
-- Name: equipos_equipo_articulo_id_8503937b; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX equipos_equipo_articulo_id_8503937b ON public.equipos_equipo USING btree (articulo_id);


--
-- Name: equipos_equipo_estado_id_56fb76ff; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX equipos_equipo_estado_id_56fb76ff ON public.equipos_equipo USING btree (estado_id);


--
-- Name: equipos_equipo_marca_id_f40af6dd; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX equipos_equipo_marca_id_f40af6dd ON public.equipos_equipo USING btree (marca_id);


--
-- Name: equipos_equipo_modelo_id_1aeb07be; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX equipos_equipo_modelo_id_1aeb07be ON public.equipos_equipo USING btree (modelo_id);


--
-- Name: equipos_equipo_modificado_por_id_f3676570; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX equipos_equipo_modificado_por_id_f3676570 ON public.equipos_equipo USING btree (modificado_por_id);


--
-- Name: equipos_equipo_num_inventario_7fc34ab8_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX equipos_equipo_num_inventario_7fc34ab8_like ON public.equipos_equipo USING btree (num_inventario varchar_pattern_ops);


--
-- Name: equipos_equipo_pma_id_cd63491b; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX equipos_equipo_pma_id_cd63491b ON public.equipos_equipo USING btree (pma_id);


--
-- Name: equipos_equipo_proveedor_id_2c9fca71; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX equipos_equipo_proveedor_id_2c9fca71 ON public.equipos_equipo USING btree (proveedor_id);


--
-- Name: equipos_equipo_serial_number_1e24bd7f_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX equipos_equipo_serial_number_1e24bd7f_like ON public.equipos_equipo USING btree (serial_number varchar_pattern_ops);


--
-- Name: equipos_equipo_so_id_c3e85b7b; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX equipos_equipo_so_id_c3e85b7b ON public.equipos_equipo USING btree (so_id);


--
-- Name: idx_acta_estado; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX idx_acta_estado ON public.actas_acta USING btree (estado);


--
-- Name: idx_acta_fecha; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX idx_acta_fecha ON public.actas_acta USING btree (fecha);


--
-- Name: idx_actadetalle_tipo_item; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX idx_actadetalle_tipo_item ON public.actas_actadetalle USING btree (tipo_item, id_item);


--
-- Name: idx_anexo_edificio; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX idx_anexo_edificio ON public.anexos_anexo USING btree (edificio_id);


--
-- Name: idx_anexo_estado; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX idx_anexo_estado ON public.anexos_anexo USING btree (estado);


--
-- Name: idx_anexo_numero; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX idx_anexo_numero ON public.anexos_anexo USING btree (numero_anexo);


--
-- Name: idx_bitacora_equipo; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX idx_bitacora_equipo ON public.equipos_bitacoraequipo USING btree (equipo_id);


--
-- Name: idx_bitacora_tecnico; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX idx_bitacora_tecnico ON public.equipos_bitacoraequipo USING btree (tecnico_id);


--
-- Name: idx_bitacora_tipo; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX idx_bitacora_tipo ON public.equipos_bitacoraequipo USING btree (tipo_registro);


--
-- Name: idx_equipo_pma; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX idx_equipo_pma ON public.equipos_equipo USING btree (pma_id);


--
-- Name: idx_ipred_estado; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX idx_ipred_estado ON public.redes_infraestructurared USING btree (estado);


--
-- Name: idx_ipred_pma; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX idx_ipred_pma ON public.redes_infraestructurared USING btree (pma_id);


--
-- Name: idx_log_ip; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX idx_log_ip ON public.core_logauditoria USING btree (ip_address);


--
-- Name: idx_log_tabla_reg; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX idx_log_tabla_reg ON public.core_logauditoria USING btree (tabla, registro_id);


--
-- Name: idx_rangoip_ip; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX idx_rangoip_ip ON public.redes_rangoip USING btree (ip);


--
-- Name: idx_rangoip_piso; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX idx_rangoip_piso ON public.redes_rangoip USING btree (piso_id);


--
-- Name: mantenedores_areahospitalaria_activo_77ef0249; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_areahospitalaria_activo_77ef0249 ON public.mantenedores_areahospitalaria USING btree (activo);


--
-- Name: mantenedores_areahospitalaria_nombre_064f9fe2_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_areahospitalaria_nombre_064f9fe2_like ON public.mantenedores_areahospitalaria USING btree (nombre varchar_pattern_ops);


--
-- Name: mantenedores_articulo_activo_94601add; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_articulo_activo_94601add ON public.mantenedores_articulo USING btree (activo);


--
-- Name: mantenedores_articulo_nombre_36f12c71_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_articulo_nombre_36f12c71_like ON public.mantenedores_articulo USING btree (nombre varchar_pattern_ops);


--
-- Name: mantenedores_cargo_activo_fb5bae30; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_cargo_activo_fb5bae30 ON public.mantenedores_cargo USING btree (activo);


--
-- Name: mantenedores_cargo_nombre_172da254_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_cargo_nombre_172da254_like ON public.mantenedores_cargo USING btree (nombre varchar_pattern_ops);


--
-- Name: mantenedores_edificio_activo_a097f0fa; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_edificio_activo_a097f0fa ON public.mantenedores_edificio USING btree (activo);


--
-- Name: mantenedores_edificio_institucion_id_18ca541d; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_edificio_institucion_id_18ca541d ON public.mantenedores_edificio USING btree (institucion_id);


--
-- Name: mantenedores_estadoequipo_activo_89b4f79a; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_estadoequipo_activo_89b4f79a ON public.mantenedores_estadoequipo USING btree (activo);


--
-- Name: mantenedores_estadoequipo_nombre_492f21b4_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_estadoequipo_nombre_492f21b4_like ON public.mantenedores_estadoequipo USING btree (nombre varchar_pattern_ops);


--
-- Name: mantenedores_institucion_activo_de228f00; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_institucion_activo_de228f00 ON public.mantenedores_institucion USING btree (activo);


--
-- Name: mantenedores_institucion_codigo_29d8552d_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_institucion_codigo_29d8552d_like ON public.mantenedores_institucion USING btree (codigo varchar_pattern_ops);


--
-- Name: mantenedores_institucion_nombre_67b9b150_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_institucion_nombre_67b9b150_like ON public.mantenedores_institucion USING btree (nombre varchar_pattern_ops);


--
-- Name: mantenedores_marca_activo_60f4c907; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_marca_activo_60f4c907 ON public.mantenedores_marca USING btree (activo);


--
-- Name: mantenedores_marca_nombre_4799ada7_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_marca_nombre_4799ada7_like ON public.mantenedores_marca USING btree (nombre varchar_pattern_ops);


--
-- Name: mantenedores_modelo_activo_907cf0cd; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_modelo_activo_907cf0cd ON public.mantenedores_modelo USING btree (activo);


--
-- Name: mantenedores_modelo_marca_id_ab5df5a3; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_modelo_marca_id_ab5df5a3 ON public.mantenedores_modelo USING btree (marca_id);


--
-- Name: mantenedores_modeloanexo_activo_b27b2328; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_modeloanexo_activo_b27b2328 ON public.mantenedores_modeloanexo USING btree (activo);


--
-- Name: mantenedores_modeloanexo_marca_id_8855e9b9; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_modeloanexo_marca_id_8855e9b9 ON public.mantenedores_modeloanexo USING btree (marca_id);


--
-- Name: mantenedores_modeloanexo_nombre_f4e991b0_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_modeloanexo_nombre_f4e991b0_like ON public.mantenedores_modeloanexo USING btree (nombre varchar_pattern_ops);


--
-- Name: mantenedores_piso_activo_690af811; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_piso_activo_690af811 ON public.mantenedores_piso USING btree (activo);


--
-- Name: mantenedores_piso_edificio_id_621ed362; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_piso_edificio_id_621ed362 ON public.mantenedores_piso USING btree (edificio_id);


--
-- Name: mantenedores_pma_activo_284d1f0f; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_pma_activo_284d1f0f ON public.mantenedores_pma USING btree (activo);


--
-- Name: mantenedores_pma_nombre_0288ea10_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_pma_nombre_0288ea10_like ON public.mantenedores_pma USING btree (nombre varchar_pattern_ops);


--
-- Name: mantenedores_pma_recinto_id_a42887d5; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_pma_recinto_id_a42887d5 ON public.mantenedores_pma USING btree (recinto_id);


--
-- Name: mantenedores_proveedor_activo_15465790; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_proveedor_activo_15465790 ON public.mantenedores_proveedor USING btree (activo);


--
-- Name: mantenedores_proveedor_nombre_928de492_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_proveedor_nombre_928de492_like ON public.mantenedores_proveedor USING btree (nombre varchar_pattern_ops);


--
-- Name: mantenedores_recinto_activo_08f773d8; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_recinto_activo_08f773d8 ON public.mantenedores_recinto USING btree (activo);


--
-- Name: mantenedores_recinto_piso_id_297e1edf; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_recinto_piso_id_297e1edf ON public.mantenedores_recinto USING btree (piso_id);


--
-- Name: mantenedores_recinto_sector_id_b4acf0c4; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_recinto_sector_id_b4acf0c4 ON public.mantenedores_recinto USING btree (sector_id);


--
-- Name: mantenedores_recinto_unidad_id_875c2be4; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_recinto_unidad_id_875c2be4 ON public.mantenedores_recinto USING btree (unidad_id);


--
-- Name: mantenedores_sector_activo_ea5fc6c2; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_sector_activo_ea5fc6c2 ON public.mantenedores_sector USING btree (activo);


--
-- Name: mantenedores_sector_piso_id_5f130301; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_sector_piso_id_5f130301 ON public.mantenedores_sector USING btree (piso_id);


--
-- Name: mantenedores_sistemaoperativo_activo_40a0c433; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_sistemaoperativo_activo_40a0c433 ON public.mantenedores_sistemaoperativo USING btree (activo);


--
-- Name: mantenedores_sistemaoperativo_nombre_4c56e3e0_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_sistemaoperativo_nombre_4c56e3e0_like ON public.mantenedores_sistemaoperativo USING btree (nombre varchar_pattern_ops);


--
-- Name: mantenedores_unidad_activo_192414b9; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_unidad_activo_192414b9 ON public.mantenedores_unidad USING btree (activo);


--
-- Name: mantenedores_unidad_area_hospitalaria_id_9d70b06d; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_unidad_area_hospitalaria_id_9d70b06d ON public.mantenedores_unidad USING btree (area_hospitalaria_id);


--
-- Name: mantenedores_vlan_activo_ea991839; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_vlan_activo_ea991839 ON public.mantenedores_vlan USING btree (activo);


--
-- Name: mantenedores_vlan_nombre_a6704d49_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX mantenedores_vlan_nombre_a6704d49_like ON public.mantenedores_vlan USING btree (nombre varchar_pattern_ops);


--
-- Name: redes_infraestructurared_edificio_id_6743fa40; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX redes_infraestructurared_edificio_id_6743fa40 ON public.redes_infraestructurared USING btree (edificio_id);


--
-- Name: redes_infraestructurared_estado_f16e86cf; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX redes_infraestructurared_estado_f16e86cf ON public.redes_infraestructurared USING btree (estado);


--
-- Name: redes_infraestructurared_estado_f16e86cf_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX redes_infraestructurared_estado_f16e86cf_like ON public.redes_infraestructurared USING btree (estado varchar_pattern_ops);


--
-- Name: redes_infraestructurared_institucion_id_9536b04f; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX redes_infraestructurared_institucion_id_9536b04f ON public.redes_infraestructurared USING btree (institucion_id);


--
-- Name: redes_infraestructurared_piso_id_96f56333; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX redes_infraestructurared_piso_id_96f56333 ON public.redes_infraestructurared USING btree (piso_id);


--
-- Name: redes_infraestructurared_pma_id_8c72b949; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX redes_infraestructurared_pma_id_8c72b949 ON public.redes_infraestructurared USING btree (pma_id);


--
-- Name: redes_infraestructurared_unidad_id_46ee0fc9; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX redes_infraestructurared_unidad_id_46ee0fc9 ON public.redes_infraestructurared USING btree (unidad_id);


--
-- Name: redes_infraestructurared_vlan_id_d8834ba1; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX redes_infraestructurared_vlan_id_d8834ba1 ON public.redes_infraestructurared USING btree (vlan_id);


--
-- Name: redes_pma_edificio_piso_id_129d60bc; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX redes_pma_edificio_piso_id_129d60bc ON public.redes_pma USING btree (edificio_piso_id);


--
-- Name: redes_pma_unidad_id_47dfdda1; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX redes_pma_unidad_id_47dfdda1 ON public.redes_pma USING btree (unidad_id);


--
-- Name: redes_rangoip_piso_id_b2e65b73; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX redes_rangoip_piso_id_b2e65b73 ON public.redes_rangoip USING btree (piso_id);


--
-- Name: redes_slaconfiguracion_activo_c29b1f63; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX redes_slaconfiguracion_activo_c29b1f63 ON public.redes_slaconfiguracion USING btree (activo);


--
-- Name: sla_slamatrix_prioridad_id_7f7e1282; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX sla_slamatrix_prioridad_id_7f7e1282 ON public.sla_slamatrix USING btree (prioridad_id);


--
-- Name: tickets_archivoadjunto_subido_por_id_402143c0; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX tickets_archivoadjunto_subido_por_id_402143c0 ON public.tickets_archivoadjunto USING btree (subido_por_id);


--
-- Name: tickets_archivoadjunto_ticket_id_89a738fe; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX tickets_archivoadjunto_ticket_id_89a738fe ON public.tickets_archivoadjunto USING btree (ticket_id);


--
-- Name: tickets_categoria_grupo_resolutor_id_55a94ded; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX tickets_categoria_grupo_resolutor_id_55a94ded ON public.tickets_categoria USING btree (grupo_resolutor_id);


--
-- Name: tickets_gruporesolutor_miembros_gruporesolutor_id_df61e9b2; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX tickets_gruporesolutor_miembros_gruporesolutor_id_df61e9b2 ON public.tickets_gruporesolutor_miembros USING btree (gruporesolutor_id);


--
-- Name: tickets_gruporesolutor_miembros_user_id_1de6fdb9; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX tickets_gruporesolutor_miembros_user_id_1de6fdb9 ON public.tickets_gruporesolutor_miembros USING btree (user_id);


--
-- Name: tickets_gruporesolutor_nombre_8e80652d_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX tickets_gruporesolutor_nombre_8e80652d_like ON public.tickets_gruporesolutor USING btree (nombre varchar_pattern_ops);


--
-- Name: tickets_notificacion_ticket_id_cc82fb37; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX tickets_notificacion_ticket_id_cc82fb37 ON public.tickets_notificacion USING btree (ticket_id);


--
-- Name: tickets_notificacion_usuario_id_3017c800; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX tickets_notificacion_usuario_id_3017c800 ON public.tickets_notificacion USING btree (usuario_id);


--
-- Name: tickets_ticket_activo_id_c0497af8; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX tickets_ticket_activo_id_c0497af8 ON public.tickets_ticket USING btree (activo_id);


--
-- Name: tickets_ticket_categoria_id_0a1509bc; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX tickets_ticket_categoria_id_0a1509bc ON public.tickets_ticket USING btree (categoria_id);


--
-- Name: tickets_ticket_correlativo_24ab8235_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX tickets_ticket_correlativo_24ab8235_like ON public.tickets_ticket USING btree (correlativo varchar_pattern_ops);


--
-- Name: tickets_ticket_creador_id_b29e7e91; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX tickets_ticket_creador_id_b29e7e91 ON public.tickets_ticket USING btree (creador_id);


--
-- Name: tickets_ticket_grupo_resolutor_id_1d35bb40; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX tickets_ticket_grupo_resolutor_id_1d35bb40 ON public.tickets_ticket USING btree (grupo_resolutor_id);


--
-- Name: tickets_ticket_prioridad_id_7052ab00; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX tickets_ticket_prioridad_id_7052ab00 ON public.tickets_ticket USING btree (prioridad_id);


--
-- Name: tickets_ticket_responsable_id_2e8d6597; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX tickets_ticket_responsable_id_2e8d6597 ON public.tickets_ticket USING btree (responsable_id);


--
-- Name: tickets_ticket_solicitante_id_f155a8aa; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX tickets_ticket_solicitante_id_f155a8aa ON public.tickets_ticket USING btree (solicitante_id);


--
-- Name: tickets_tickethistorial_ticket_id_f4c39ded; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX tickets_tickethistorial_ticket_id_f4c39ded ON public.tickets_tickethistorial USING btree (ticket_id);


--
-- Name: tickets_tickethistorial_usuario_id_f0162cb5; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX tickets_tickethistorial_usuario_id_f0162cb5 ON public.tickets_tickethistorial USING btree (usuario_id);


--
-- Name: utilidades_ayudarapida_activo_6efa7b5f; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX utilidades_ayudarapida_activo_6efa7b5f ON public.utilidades_ayudarapida USING btree (activo);


--
-- Name: utilidades_ayudarapida_orden_bd4f41db; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX utilidades_ayudarapida_orden_bd4f41db ON public.utilidades_ayudarapida USING btree (orden);


--
-- Name: utilidades_ayudarapida_titulo_6a589184_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX utilidades_ayudarapida_titulo_6a589184_like ON public.utilidades_ayudarapida USING btree (titulo varchar_pattern_ops);


--
-- Name: utilidades_checklistitem_activo_83f20ce1; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX utilidades_checklistitem_activo_83f20ce1 ON public.utilidades_checklistitem USING btree (activo);


--
-- Name: utilidades_checklistitem_orden_d93b2bc4; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX utilidades_checklistitem_orden_d93b2bc4 ON public.utilidades_checklistitem USING btree (orden);


--
-- Name: utilidades_pendiente_estado_0b3d1b98; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX utilidades_pendiente_estado_0b3d1b98 ON public.utilidades_pendiente USING btree (estado);


--
-- Name: utilidades_pendiente_estado_0b3d1b98_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX utilidades_pendiente_estado_0b3d1b98_like ON public.utilidades_pendiente USING btree (estado varchar_pattern_ops);


--
-- Name: utilidades_webapp_activo_031f3575; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX utilidades_webapp_activo_031f3575 ON public.utilidades_webapp USING btree (activo);


--
-- Name: utilidades_webapp_nombre_e54f006d_like; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX utilidades_webapp_nombre_e54f006d_like ON public.utilidades_webapp USING btree (nombre varchar_pattern_ops);


--
-- Name: utilidades_webapp_orden_7ff09a20; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX utilidades_webapp_orden_7ff09a20 ON public.utilidades_webapp USING btree (orden);


--
-- Name: visor_avisovisor_activo_b8721d10; Type: INDEX; Schema: public; Owner: ticsystem_admin
--

CREATE INDEX visor_avisovisor_activo_b8721d10 ON public.visor_avisovisor USING btree (activo);


--
-- Name: actas_acta actas_acta_encargado_id_285fabdc_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.actas_acta
    ADD CONSTRAINT actas_acta_encargado_id_285fabdc_fk_auth_user_id FOREIGN KEY (encargado_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: actas_actadetalle actas_actadetalle_acta_id_73ddccab_fk_actas_acta_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.actas_actadetalle
    ADD CONSTRAINT actas_actadetalle_acta_id_73ddccab_fk_actas_acta_id FOREIGN KEY (acta_id) REFERENCES public.actas_acta(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: actas_actadetalle actas_actadetalle_edificio_id_1cb35d69_fk_mantenedo; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.actas_actadetalle
    ADD CONSTRAINT actas_actadetalle_edificio_id_1cb35d69_fk_mantenedo FOREIGN KEY (edificio_id) REFERENCES public.mantenedores_edificio(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: actas_actadetalle actas_actadetalle_piso_id_89ab3dd4_fk_mantenedores_piso_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.actas_actadetalle
    ADD CONSTRAINT actas_actadetalle_piso_id_89ab3dd4_fk_mantenedores_piso_id FOREIGN KEY (piso_id) REFERENCES public.mantenedores_piso(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: actas_actadetalle actas_actadetalle_unidad_id_4650aec0_fk_mantenedores_unidad_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.actas_actadetalle
    ADD CONSTRAINT actas_actadetalle_unidad_id_4650aec0_fk_mantenedores_unidad_id FOREIGN KEY (unidad_id) REFERENCES public.mantenedores_unidad(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: anexos_anexo anexos_anexo_actualizado_por_id_f880f1ee_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.anexos_anexo
    ADD CONSTRAINT anexos_anexo_actualizado_por_id_f880f1ee_fk_auth_user_id FOREIGN KEY (actualizado_por_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: anexos_anexo anexos_anexo_creado_por_id_ea30cea2_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.anexos_anexo
    ADD CONSTRAINT anexos_anexo_creado_por_id_ea30cea2_fk_auth_user_id FOREIGN KEY (creado_por_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: anexos_anexo anexos_anexo_edificio_id_b9966609_fk_mantenedores_edificio_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.anexos_anexo
    ADD CONSTRAINT anexos_anexo_edificio_id_b9966609_fk_mantenedores_edificio_id FOREIGN KEY (edificio_id) REFERENCES public.mantenedores_edificio(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: anexos_anexo anexos_anexo_establecimiento_id_9d0fc07f_fk_mantenedo; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.anexos_anexo
    ADD CONSTRAINT anexos_anexo_establecimiento_id_9d0fc07f_fk_mantenedo FOREIGN KEY (establecimiento_id) REFERENCES public.mantenedores_institucion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: anexos_anexo anexos_anexo_modelo_anexo_id_1ce2338e_fk_mantenedo; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.anexos_anexo
    ADD CONSTRAINT anexos_anexo_modelo_anexo_id_1ce2338e_fk_mantenedo FOREIGN KEY (modelo_anexo_id) REFERENCES public.mantenedores_modeloanexo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: anexos_anexo anexos_anexo_piso_id_d0bd0bc3_fk_mantenedores_piso_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.anexos_anexo
    ADD CONSTRAINT anexos_anexo_piso_id_d0bd0bc3_fk_mantenedores_piso_id FOREIGN KEY (piso_id) REFERENCES public.mantenedores_piso(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: anexos_anexo anexos_anexo_pma_id_b62bc2ba_fk_mantenedores_pma_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.anexos_anexo
    ADD CONSTRAINT anexos_anexo_pma_id_b62bc2ba_fk_mantenedores_pma_id FOREIGN KEY (pma_id) REFERENCES public.mantenedores_pma(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: anexos_anexo anexos_anexo_proveedor_id_358de8b5_fk_mantenedores_proveedor_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.anexos_anexo
    ADD CONSTRAINT anexos_anexo_proveedor_id_358de8b5_fk_mantenedores_proveedor_id FOREIGN KEY (proveedor_id) REFERENCES public.mantenedores_proveedor(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: anexos_anexo anexos_anexo_unidad_id_cd2392a1_fk_mantenedores_unidad_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.anexos_anexo
    ADD CONSTRAINT anexos_anexo_unidad_id_cd2392a1_fk_mantenedores_unidad_id FOREIGN KEY (unidad_id) REFERENCES public.mantenedores_unidad(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: anexos_requerimientocambio anexos_requerimientocambio_anexo_id_0e4ade28_fk_anexos_anexo_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.anexos_requerimientocambio
    ADD CONSTRAINT anexos_requerimientocambio_anexo_id_0e4ade28_fk_anexos_anexo_id FOREIGN KEY (anexo_id) REFERENCES public.anexos_anexo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: axes_accessattemptexpiration axes_accessattemptex_access_attempt_id_6b73a47a_fk_axes_acce; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.axes_accessattemptexpiration
    ADD CONSTRAINT axes_accessattemptex_access_attempt_id_6b73a47a_fk_axes_acce FOREIGN KEY (access_attempt_id) REFERENCES public.axes_accessattempt(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: conocimiento_articuloconocimiento conocimiento_articul_categoria_id_2331dc21_fk_conocimie; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.conocimiento_articuloconocimiento
    ADD CONSTRAINT conocimiento_articul_categoria_id_2331dc21_fk_conocimie FOREIGN KEY (categoria_id) REFERENCES public.conocimiento_categoriaconocimiento(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_funcionario core_funcionario_cargo_id_43291cdf_fk_mantenedores_cargo_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.core_funcionario
    ADD CONSTRAINT core_funcionario_cargo_id_43291cdf_fk_mantenedores_cargo_id FOREIGN KEY (cargo_id) REFERENCES public.mantenedores_cargo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_funcionario core_funcionario_unidad_id_151a2b97_fk_mantenedores_unidad_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.core_funcionario
    ADD CONSTRAINT core_funcionario_unidad_id_151a2b97_fk_mantenedores_unidad_id FOREIGN KEY (unidad_id) REFERENCES public.mantenedores_unidad(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_perfilusuario core_perfilusuario_rol_id_dd0e25c8_fk_core_rol_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.core_perfilusuario
    ADD CONSTRAINT core_perfilusuario_rol_id_dd0e25c8_fk_core_rol_id FOREIGN KEY (rol_id) REFERENCES public.core_rol(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_perfilusuario core_perfilusuario_user_id_f33b9be3_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.core_perfilusuario
    ADD CONSTRAINT core_perfilusuario_user_id_f33b9be3_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: correos_correolog correos_correolog_ticket_id_1790aa94_fk_tickets_ticket_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.correos_correolog
    ADD CONSTRAINT correos_correolog_ticket_id_1790aa94_fk_tickets_ticket_id FOREIGN KEY (ticket_id) REFERENCES public.tickets_ticket(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: correos_miembrogrupocorreo correos_miembrogrupo_grupo_id_05325d71_fk_correos_g; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.correos_miembrogrupocorreo
    ADD CONSTRAINT correos_miembrogrupo_grupo_id_05325d71_fk_correos_g FOREIGN KEY (grupo_id) REFERENCES public.correos_grupocorreo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: equipos_bitacoraequipo equipos_bitacoraequi_solicitante_id_f5b2c848_fk_core_func; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.equipos_bitacoraequipo
    ADD CONSTRAINT equipos_bitacoraequi_solicitante_id_f5b2c848_fk_core_func FOREIGN KEY (solicitante_id) REFERENCES public.core_funcionario(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: equipos_bitacoraequipo equipos_bitacoraequipo_equipo_id_a0f57a1d_fk_equipos_equipo_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.equipos_bitacoraequipo
    ADD CONSTRAINT equipos_bitacoraequipo_equipo_id_a0f57a1d_fk_equipos_equipo_id FOREIGN KEY (equipo_id) REFERENCES public.equipos_equipo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: equipos_bitacoraequipo equipos_bitacoraequipo_tecnico_id_e0b7c38a_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.equipos_bitacoraequipo
    ADD CONSTRAINT equipos_bitacoraequipo_tecnico_id_e0b7c38a_fk_auth_user_id FOREIGN KEY (tecnico_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: equipos_bitacoraopcion equipos_bitacoraopcion_creado_por_id_6f47db54_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.equipos_bitacoraopcion
    ADD CONSTRAINT equipos_bitacoraopcion_creado_por_id_6f47db54_fk_auth_user_id FOREIGN KEY (creado_por_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: equipos_equipo equipos_equipo_articulo_id_8503937b_fk_mantenedores_articulo_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.equipos_equipo
    ADD CONSTRAINT equipos_equipo_articulo_id_8503937b_fk_mantenedores_articulo_id FOREIGN KEY (articulo_id) REFERENCES public.mantenedores_articulo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: equipos_equipo equipos_equipo_estado_id_56fb76ff_fk_mantenedo; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.equipos_equipo
    ADD CONSTRAINT equipos_equipo_estado_id_56fb76ff_fk_mantenedo FOREIGN KEY (estado_id) REFERENCES public.mantenedores_estadoequipo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: equipos_equipo equipos_equipo_marca_id_f40af6dd_fk_mantenedores_marca_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.equipos_equipo
    ADD CONSTRAINT equipos_equipo_marca_id_f40af6dd_fk_mantenedores_marca_id FOREIGN KEY (marca_id) REFERENCES public.mantenedores_marca(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: equipos_equipo equipos_equipo_modelo_id_1aeb07be_fk_mantenedores_modelo_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.equipos_equipo
    ADD CONSTRAINT equipos_equipo_modelo_id_1aeb07be_fk_mantenedores_modelo_id FOREIGN KEY (modelo_id) REFERENCES public.mantenedores_modelo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: equipos_equipo equipos_equipo_modificado_por_id_f3676570_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.equipos_equipo
    ADD CONSTRAINT equipos_equipo_modificado_por_id_f3676570_fk_auth_user_id FOREIGN KEY (modificado_por_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: equipos_equipo equipos_equipo_pma_id_cd63491b_fk_mantenedores_pma_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.equipos_equipo
    ADD CONSTRAINT equipos_equipo_pma_id_cd63491b_fk_mantenedores_pma_id FOREIGN KEY (pma_id) REFERENCES public.mantenedores_pma(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: equipos_equipo equipos_equipo_proveedor_id_2c9fca71_fk_mantenedo; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.equipos_equipo
    ADD CONSTRAINT equipos_equipo_proveedor_id_2c9fca71_fk_mantenedo FOREIGN KEY (proveedor_id) REFERENCES public.mantenedores_proveedor(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: equipos_equipo equipos_equipo_so_id_c3e85b7b_fk_mantenedo; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.equipos_equipo
    ADD CONSTRAINT equipos_equipo_so_id_c3e85b7b_fk_mantenedo FOREIGN KEY (so_id) REFERENCES public.mantenedores_sistemaoperativo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mantenedores_edificio mantenedores_edifici_institucion_id_18ca541d_fk_mantenedo; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_edificio
    ADD CONSTRAINT mantenedores_edifici_institucion_id_18ca541d_fk_mantenedo FOREIGN KEY (institucion_id) REFERENCES public.mantenedores_institucion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mantenedores_modelo mantenedores_modelo_marca_id_ab5df5a3_fk_mantenedores_marca_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_modelo
    ADD CONSTRAINT mantenedores_modelo_marca_id_ab5df5a3_fk_mantenedores_marca_id FOREIGN KEY (marca_id) REFERENCES public.mantenedores_marca(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mantenedores_modeloanexo mantenedores_modeloa_marca_id_8855e9b9_fk_mantenedo; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_modeloanexo
    ADD CONSTRAINT mantenedores_modeloa_marca_id_8855e9b9_fk_mantenedo FOREIGN KEY (marca_id) REFERENCES public.mantenedores_marca(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mantenedores_piso mantenedores_piso_edificio_id_621ed362_fk_mantenedo; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_piso
    ADD CONSTRAINT mantenedores_piso_edificio_id_621ed362_fk_mantenedo FOREIGN KEY (edificio_id) REFERENCES public.mantenedores_edificio(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mantenedores_pma mantenedores_pma_recinto_id_a42887d5_fk_mantenedores_recinto_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_pma
    ADD CONSTRAINT mantenedores_pma_recinto_id_a42887d5_fk_mantenedores_recinto_id FOREIGN KEY (recinto_id) REFERENCES public.mantenedores_recinto(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mantenedores_recinto mantenedores_recinto_piso_id_297e1edf_fk_mantenedores_piso_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_recinto
    ADD CONSTRAINT mantenedores_recinto_piso_id_297e1edf_fk_mantenedores_piso_id FOREIGN KEY (piso_id) REFERENCES public.mantenedores_piso(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mantenedores_recinto mantenedores_recinto_sector_id_b4acf0c4_fk_mantenedo; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_recinto
    ADD CONSTRAINT mantenedores_recinto_sector_id_b4acf0c4_fk_mantenedo FOREIGN KEY (sector_id) REFERENCES public.mantenedores_sector(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mantenedores_recinto mantenedores_recinto_unidad_id_875c2be4_fk_mantenedo; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_recinto
    ADD CONSTRAINT mantenedores_recinto_unidad_id_875c2be4_fk_mantenedo FOREIGN KEY (unidad_id) REFERENCES public.mantenedores_unidad(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mantenedores_sector mantenedores_sector_piso_id_5f130301_fk_mantenedores_piso_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_sector
    ADD CONSTRAINT mantenedores_sector_piso_id_5f130301_fk_mantenedores_piso_id FOREIGN KEY (piso_id) REFERENCES public.mantenedores_piso(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mantenedores_unidad mantenedores_unidad_area_hospitalaria_id_9d70b06d_fk_mantenedo; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.mantenedores_unidad
    ADD CONSTRAINT mantenedores_unidad_area_hospitalaria_id_9d70b06d_fk_mantenedo FOREIGN KEY (area_hospitalaria_id) REFERENCES public.mantenedores_areahospitalaria(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: redes_infraestructurared redes_infraestructur_edificio_id_6743fa40_fk_mantenedo; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.redes_infraestructurared
    ADD CONSTRAINT redes_infraestructur_edificio_id_6743fa40_fk_mantenedo FOREIGN KEY (edificio_id) REFERENCES public.mantenedores_edificio(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: redes_infraestructurared redes_infraestructur_institucion_id_9536b04f_fk_mantenedo; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.redes_infraestructurared
    ADD CONSTRAINT redes_infraestructur_institucion_id_9536b04f_fk_mantenedo FOREIGN KEY (institucion_id) REFERENCES public.mantenedores_institucion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: redes_infraestructurared redes_infraestructur_piso_id_96f56333_fk_mantenedo; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.redes_infraestructurared
    ADD CONSTRAINT redes_infraestructur_piso_id_96f56333_fk_mantenedo FOREIGN KEY (piso_id) REFERENCES public.mantenedores_piso(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: redes_infraestructurared redes_infraestructur_unidad_id_46ee0fc9_fk_mantenedo; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.redes_infraestructurared
    ADD CONSTRAINT redes_infraestructur_unidad_id_46ee0fc9_fk_mantenedo FOREIGN KEY (unidad_id) REFERENCES public.mantenedores_unidad(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: redes_infraestructurared redes_infraestructur_vlan_id_d8834ba1_fk_mantenedo; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.redes_infraestructurared
    ADD CONSTRAINT redes_infraestructur_vlan_id_d8834ba1_fk_mantenedo FOREIGN KEY (vlan_id) REFERENCES public.mantenedores_vlan(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: redes_infraestructurared redes_infraestructurared_pma_id_8c72b949_fk_redes_pma_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.redes_infraestructurared
    ADD CONSTRAINT redes_infraestructurared_pma_id_8c72b949_fk_redes_pma_id FOREIGN KEY (pma_id) REFERENCES public.redes_pma(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: redes_pma redes_pma_edificio_piso_id_129d60bc_fk_mantenedores_piso_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.redes_pma
    ADD CONSTRAINT redes_pma_edificio_piso_id_129d60bc_fk_mantenedores_piso_id FOREIGN KEY (edificio_piso_id) REFERENCES public.mantenedores_piso(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: redes_pma redes_pma_unidad_id_47dfdda1_fk_mantenedores_unidad_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.redes_pma
    ADD CONSTRAINT redes_pma_unidad_id_47dfdda1_fk_mantenedores_unidad_id FOREIGN KEY (unidad_id) REFERENCES public.mantenedores_unidad(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: redes_rangoip redes_rangoip_piso_id_b2e65b73_fk_mantenedores_piso_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.redes_rangoip
    ADD CONSTRAINT redes_rangoip_piso_id_b2e65b73_fk_mantenedores_piso_id FOREIGN KEY (piso_id) REFERENCES public.mantenedores_piso(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sla_slamatrix sla_slamatrix_prioridad_id_7f7e1282_fk_tickets_prioridad_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.sla_slamatrix
    ADD CONSTRAINT sla_slamatrix_prioridad_id_7f7e1282_fk_tickets_prioridad_id FOREIGN KEY (prioridad_id) REFERENCES public.tickets_prioridad(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_archivoadjunto tickets_archivoadjunto_subido_por_id_402143c0_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.tickets_archivoadjunto
    ADD CONSTRAINT tickets_archivoadjunto_subido_por_id_402143c0_fk_auth_user_id FOREIGN KEY (subido_por_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_archivoadjunto tickets_archivoadjunto_ticket_id_89a738fe_fk_tickets_ticket_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.tickets_archivoadjunto
    ADD CONSTRAINT tickets_archivoadjunto_ticket_id_89a738fe_fk_tickets_ticket_id FOREIGN KEY (ticket_id) REFERENCES public.tickets_ticket(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_categoria tickets_categoria_grupo_resolutor_id_55a94ded_fk_tickets_g; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.tickets_categoria
    ADD CONSTRAINT tickets_categoria_grupo_resolutor_id_55a94ded_fk_tickets_g FOREIGN KEY (grupo_resolutor_id) REFERENCES public.tickets_gruporesolutor(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_gruporesolutor_miembros tickets_gruporesolut_gruporesolutor_id_df61e9b2_fk_tickets_g; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.tickets_gruporesolutor_miembros
    ADD CONSTRAINT tickets_gruporesolut_gruporesolutor_id_df61e9b2_fk_tickets_g FOREIGN KEY (gruporesolutor_id) REFERENCES public.tickets_gruporesolutor(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_gruporesolutor_miembros tickets_gruporesolut_user_id_1de6fdb9_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.tickets_gruporesolutor_miembros
    ADD CONSTRAINT tickets_gruporesolut_user_id_1de6fdb9_fk_auth_user FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_notificacion tickets_notificacion_ticket_id_cc82fb37_fk_tickets_ticket_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.tickets_notificacion
    ADD CONSTRAINT tickets_notificacion_ticket_id_cc82fb37_fk_tickets_ticket_id FOREIGN KEY (ticket_id) REFERENCES public.tickets_ticket(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_notificacion tickets_notificacion_usuario_id_3017c800_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.tickets_notificacion
    ADD CONSTRAINT tickets_notificacion_usuario_id_3017c800_fk_auth_user_id FOREIGN KEY (usuario_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_ticket tickets_ticket_activo_id_c0497af8_fk_equipos_equipo_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.tickets_ticket
    ADD CONSTRAINT tickets_ticket_activo_id_c0497af8_fk_equipos_equipo_id FOREIGN KEY (activo_id) REFERENCES public.equipos_equipo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_ticket tickets_ticket_categoria_id_0a1509bc_fk_tickets_categoria_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.tickets_ticket
    ADD CONSTRAINT tickets_ticket_categoria_id_0a1509bc_fk_tickets_categoria_id FOREIGN KEY (categoria_id) REFERENCES public.tickets_categoria(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_ticket tickets_ticket_creador_id_b29e7e91_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.tickets_ticket
    ADD CONSTRAINT tickets_ticket_creador_id_b29e7e91_fk_auth_user_id FOREIGN KEY (creador_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_ticket tickets_ticket_grupo_resolutor_id_1d35bb40_fk_tickets_g; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.tickets_ticket
    ADD CONSTRAINT tickets_ticket_grupo_resolutor_id_1d35bb40_fk_tickets_g FOREIGN KEY (grupo_resolutor_id) REFERENCES public.tickets_gruporesolutor(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_ticket tickets_ticket_prioridad_id_7052ab00_fk_tickets_prioridad_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.tickets_ticket
    ADD CONSTRAINT tickets_ticket_prioridad_id_7052ab00_fk_tickets_prioridad_id FOREIGN KEY (prioridad_id) REFERENCES public.tickets_prioridad(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_ticket tickets_ticket_responsable_id_2e8d6597_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.tickets_ticket
    ADD CONSTRAINT tickets_ticket_responsable_id_2e8d6597_fk_auth_user_id FOREIGN KEY (responsable_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_ticket tickets_ticket_solicitante_id_f155a8aa_fk_core_funcionario_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.tickets_ticket
    ADD CONSTRAINT tickets_ticket_solicitante_id_f155a8aa_fk_core_funcionario_id FOREIGN KEY (solicitante_id) REFERENCES public.core_funcionario(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_tickethistorial tickets_tickethistorial_ticket_id_f4c39ded_fk_tickets_ticket_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.tickets_tickethistorial
    ADD CONSTRAINT tickets_tickethistorial_ticket_id_f4c39ded_fk_tickets_ticket_id FOREIGN KEY (ticket_id) REFERENCES public.tickets_ticket(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_tickethistorial tickets_tickethistorial_usuario_id_f0162cb5_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ticsystem_admin
--

ALTER TABLE ONLY public.tickets_tickethistorial
    ADD CONSTRAINT tickets_tickethistorial_usuario_id_f0162cb5_fk_auth_user_id FOREIGN KEY (usuario_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

\unrestrict kl6gpaCcvscOtvyCykTRz3q27oK5i6xmmenyIMvZblcYlCBixnUTDbxf24Up1eR

