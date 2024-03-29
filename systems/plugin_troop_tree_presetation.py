from compiler import *
register_plugin(__name__)

presentations = [
    ("faction_troop_trees", 0, 0, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
        
        (create_mesh_overlay, reg1, "mesh_load_window"),
        (position_set_x, pos1, 0),
        (position_set_y, pos1, 0),
        (overlay_set_position, reg1, pos1),
        
        ## combo_button
        (create_combo_button_overlay, "$g_presentation_obj_1"),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 690),
        (overlay_set_position, "$g_presentation_obj_1", pos1),
        # factions
        (store_sub, ":num_factions", npc_kingdoms_end, npc_kingdoms_begin),
        (store_add, ":num_pages", ":num_factions", 3),
        
        ## page names, from bottom to top
        (overlay_add_item, "$g_presentation_obj_1", "@Others"),
        (overlay_add_item, "$g_presentation_obj_1", "@Outlaws"),
        (overlay_add_item, "$g_presentation_obj_1", "@Mercenary"),
        (try_for_range_backwards, ":page_no", 0, ":num_factions"),
          (store_add, ":faction_no", ":page_no", npc_kingdoms_begin),
          (str_store_faction_name, s0, ":faction_no"),
          (overlay_add_item, "$g_presentation_obj_1", s0),
        (try_end),
        (store_sub, ":presentation_obj_val", ":num_pages", "$g_selected_page"),
        (val_sub, ":presentation_obj_val", 1),
        (overlay_set_val, "$g_presentation_obj_1", ":presentation_obj_val"),
        
        ## back
        (create_game_button_overlay, "$g_presentation_obj_2", "@Close"),
        (position_set_x, pos1, 750),
        (position_set_y, pos1, 685),
        (overlay_set_position, "$g_presentation_obj_2", pos1),
        
        ## tips
        (create_text_overlay, reg1, "@Click the center button to toggle faction^Click the avatars to view details of them", tf_left_align),
        (position_set_x, pos1, 800),
        (position_set_y, pos1, 800),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, 30),
        (position_set_y, pos1, 690),
        (overlay_set_position, reg1, pos1),
        
        ## pic_arms
        (try_begin),
          (is_between, "$g_selected_page", 0, ":num_factions"), 
          (store_add, ":pic_arms", "mesh_pic_arms_swadian", "$g_selected_page"),
          (create_mesh_overlay, reg1, ":pic_arms"),
          (position_set_x, pos1, 120),
          (position_set_y, pos1, 100),
          (overlay_set_position, reg1, pos1),
          (position_set_x, pos1, 300),
          (position_set_y, pos1, 300),
          (overlay_set_size, reg1, pos1),
        (try_end),

        # detect_total_max_tier, calculate offset_x
        (assign, ":total_max_tier", 1),
        (try_for_range, ":cur_troop", soldiers_begin, soldiers_end),
          (neg|troop_is_hero, ":cur_troop"),
          # can upgrade
          (troop_get_upgrade_troop, ":upgrade_troop", ":cur_troop", 0),
          (gt, ":upgrade_troop", 0), 
          # page_no_for_cur_troop
          (call_script, "script_get_page_no_of_troop_tree_for_troop_on", ":cur_troop"),
          (assign, ":page_no_for_cur_troop", reg0),
          # on current page_no
          (eq, ":page_no_for_cur_troop", "$g_selected_page"),
          (assign, reg0, 1), # reg0: init max_tier to 1
          (call_script, "script_troop_tree_recursive_detect_max_tier", ":cur_troop", 1),
          (assign, ":cur_max_tier", reg0),
          (try_begin),
            (gt, ":cur_max_tier", ":total_max_tier"),
            (assign, ":total_max_tier", ":cur_max_tier"),
          (try_end),
        (try_end),
        (val_sub, ":total_max_tier", 1),
        (val_max, ":total_max_tier", 1),
        (store_div, ":offset_x", 700, ":total_max_tier"),
        (val_min, ":offset_x", 120),
        
        (str_clear, s0),
        (create_text_overlay, reg1, s0, tf_scrollable),
        (position_set_x, pos1, 15),
        (position_set_y, pos1, 15),
        (overlay_set_position, reg1, pos1),
        (position_set_x, pos1, 800),
        (position_set_y, pos1, 660),
        (overlay_set_area_size, reg1, pos1),
        (set_container_overlay, reg1),
        
        (assign, "$g_cur_slot_no", 0),
        (assign, reg2, 75),
        # find all root troops of selected faction
        (try_for_range, ":cur_troop", soldiers_begin, soldiers_end),
          (neg|troop_is_hero, ":cur_troop"),
          # can upgrade
          (troop_get_upgrade_troop, ":upgrade_troop", ":cur_troop", 0),
          (gt, ":upgrade_troop", 0), 
          # page_no_for_cur_troop
          (call_script, "script_get_page_no_of_troop_tree_for_troop_on", ":cur_troop"),
          (assign, ":page_no_for_cur_troop", reg0),
          # on current page_no
          (eq, ":page_no_for_cur_troop", "$g_selected_page"),
          # can't be upgraded from other troops of the same page
          (assign, ":is_root_troop", 1),
          (assign, ":end_cond", soldiers_end),
          (try_for_range, ":loop_troop", soldiers_begin, ":end_cond"),
            (neg|troop_is_hero, ":loop_troop"),
            # page_no_for_loop_troop
            (call_script, "script_get_page_no_of_troop_tree_for_troop_on", ":loop_troop"),
            (assign, ":page_no_for_loop_troop", reg0),
            # on current page_no
            (eq,  ":page_no_for_loop_troop", "$g_selected_page"),
            (troop_get_upgrade_troop, ":upgrade_troop_1", ":loop_troop", 0),
            (troop_get_upgrade_troop, ":upgrade_troop_2", ":loop_troop", 1),
            (this_or_next|eq, ":upgrade_troop_1", ":cur_troop"),
            (eq, ":upgrade_troop_2", ":cur_troop"),
            (assign, ":is_root_troop", 0),
            (assign, ":end_cond", 0), #break
          (try_end),
          (eq, ":is_root_troop", 1), # draw troop tree of cur root_troop
          (call_script, "script_troop_tree_recursive_backtracking", ":cur_troop", 50, reg2, ":offset_x"),
          (val_add, reg2, 160),
        (try_end),
        
        (set_container_overlay, -1),
        
        ## draw selected_troop: Attributes, Skills, Equipments,
        (try_begin),
          (gt, "$g_selected_troop", 0), 
          (store_mul, ":cur_troop", "$g_selected_troop", 2), #with weapons
          (create_image_button_overlay_with_tableau_material, reg1, -1, "tableau_game_party_window", ":cur_troop"),
          (position_set_x, pos1, 450),
          (position_set_y, pos1, 600),
          (overlay_set_size, reg1, pos1),
          (position_set_x, pos1, 810),
          (position_set_y, pos1, 550),
          (overlay_set_position, reg1, pos1),
          
          # pos2: text size
          (position_set_x, pos2, 750),
          (position_set_y, pos2, 750),
          # pos2: title text size
          (position_set_x, pos3, 900),
          (position_set_y, pos3, 900),
          # Name
          (str_store_troop_name, s1, "$g_selected_troop"),
          (create_text_overlay, reg1, s1, tf_center_justify),
          (position_set_x, pos1, 900),
          (position_set_y, pos1, 710),
          (overlay_set_position, reg1, pos1),
          (overlay_set_size, reg1, pos2),
          
          # level and HP
          (store_character_level, reg3, "$g_selected_troop"),
          (assign, ":troop_hp", 35),
          (store_skill_level, ":skill", skl_ironflesh, "$g_selected_troop"),
          (store_attribute_level, ":strength", "$g_selected_troop", ca_strength),
          (val_mul, ":skill", 2),
          (val_add, ":troop_hp", ":skill"),
          (val_add, ":troop_hp", ":strength"),
          (assign, reg4, ":troop_hp"),
          (create_text_overlay, reg1, "@Level: {reg3}^Health: {reg4}", tf_left_align),
          (position_set_x, pos1, 900),
          (position_set_y, pos1, 665),
          (overlay_set_position, reg1, pos1),
          (overlay_set_size, reg1, pos2),
          
          # Attributes
          (create_text_overlay, reg1, "@Attributes", tf_left_align),
          (position_set_x, pos1, 900),
          (position_set_y, pos1, 630),
          (overlay_set_position, reg1, pos1),
          (overlay_set_size, reg1, pos3),
          (create_text_overlay, reg1, "@STR^AGI^INT^CHA", tf_left_align),
          (position_set_x, pos1, 900),
          (position_set_y, pos1, 570),
          (overlay_set_position, reg1, pos1),
          (overlay_set_size, reg1, pos2),
          
          (try_for_range, ":attrib_id", 0, 4),
            (try_begin),
              (eq, ":attrib_id", 0),
              (store_attribute_level, reg2, "$g_selected_troop", ":attrib_id"),
              (str_store_string, s1, "@{reg2}"),
            (else_try),
              (store_attribute_level, reg2, "$g_selected_troop", ":attrib_id"),
              (str_store_string, s1, "@{s1}^{reg2}"),
            (try_end),
          (try_end),
          (create_text_overlay, reg1, s1, tf_right_align),
          (position_set_x, pos1, 980),
          (position_set_y, pos1, 570),
          (overlay_set_position, reg1, pos1),
          (overlay_set_size, reg1, pos2),
          
          # Skills
          (create_text_overlay, reg1, "@Skills", tf_left_align),
          (position_set_x, pos1, 840),
          (position_set_y, pos1, 527),
          (overlay_set_position, reg1, pos1),
          (overlay_set_size, reg1, pos3),
          (create_text_overlay, reg1, "@Ironflesh^Power Strike^Power Throw^Power Draw^Shield^Athletics^Riding^Horse Archery", tf_left_align),
          (position_set_x, pos1, 840),
          (position_set_y, pos1, 415),
          (overlay_set_position, reg1, pos1),
          (overlay_set_size, reg1, pos2),
          
          (try_for_range_backwards, ":skill_id", 0, 42),
            (try_begin),
              (eq, ":skill_id", "skl_ironflesh"),
              (store_skill_level, reg2, ":skill_id", "$g_selected_troop"),
              (str_store_string, s1, "@{reg2}"),
            (else_try),
              (this_or_next|eq, ":skill_id", "skl_power_strike"),
              (this_or_next|eq, ":skill_id", "skl_power_throw"),
              (this_or_next|eq, ":skill_id", "skl_power_draw"),
              (this_or_next|eq, ":skill_id", "skl_shield"),
              (this_or_next|eq, ":skill_id", "skl_athletics"),
              (this_or_next|eq, ":skill_id", "skl_riding"),
              (eq, ":skill_id", "skl_horse_archery"),
              (store_skill_level, reg2, ":skill_id", "$g_selected_troop"),
              (str_store_string, s1, "@{s1}^{reg2}"),
            (try_end),
          (try_end),
          (create_text_overlay, reg1, s1, tf_right_align),
          (position_set_x, pos1, 980),
          (position_set_y, pos1, 415),
          (overlay_set_position, reg1, pos1),
          (overlay_set_size, reg1, pos2),
          
          # Weapon Proficiencies
          (create_text_overlay, reg1, "@Proficiencies", tf_left_align),
          (position_set_x, pos1, 840),
          (position_set_y, pos1, 370),
          (overlay_set_position, reg1, pos1),
          (overlay_set_size, reg1, pos3),
          (create_text_overlay, reg1, "@1H Weapons^2H Weapons^Polearms^Archery^Crossbows^Throwing", tf_left_align),
          (position_set_x, pos1, 840),
          (position_set_y, pos1, 285),
          (overlay_set_position, reg1, pos1),
          (overlay_set_size, reg1, pos2),
          
          (try_for_range, ":wp_id", 0, 6),
            (try_begin),
              (eq, ":wp_id", wpt_one_handed_weapon),
              (store_proficiency_level, reg2, "$g_selected_troop", ":wp_id"),
              (str_store_string, s1, "@{reg2}"),
            (else_try),
              (is_between, ":wp_id", wpt_two_handed_weapon, wpt_firearm),
              (store_proficiency_level, reg2, "$g_selected_troop", ":wp_id"),
              (str_store_string, s1, "@{s1}^{reg2}"),
            (try_end),
          (try_end),
          (create_text_overlay, reg1, s1, tf_right_align),
          (position_set_x, pos1, 980),
          (position_set_y, pos1, 285),
          (overlay_set_position, reg1, pos1),
          (overlay_set_size, reg1, pos2),
          
          # Equipments
          (create_text_overlay, reg1, "@Equipments", tf_left_align),
          (position_set_x, pos1, 840),
          (position_set_y, pos1, 235),
          (overlay_set_position, reg1, pos1),
          (overlay_set_size, reg1, pos3),
          (str_clear, s0),
          (create_text_overlay, "$g_presentation_obj_3", s0, tf_scrollable),
          (position_set_x, pos1, 840),
          (position_set_y, pos1, 30),
          (overlay_set_position, "$g_presentation_obj_3", pos1),
          (position_set_x, pos1, 138),
          (position_set_y, pos1, 202),
          (overlay_set_area_size, "$g_presentation_obj_3", pos1),
          (set_container_overlay, "$g_presentation_obj_3"),
          
          (troop_clear_inventory, "trp_temp_array_a"),
          (troop_get_inventory_capacity, ":inv_cap", "$g_selected_troop"),
          (try_for_range, ":i_slot", 0, ":inv_cap"),
            (troop_get_inventory_slot, ":item", "$g_selected_troop", ":i_slot"),
            (gt, ":item", -1),
            (troop_get_inventory_slot_modifier, ":imod", "$g_selected_troop", ":i_slot"),
            (troop_add_item,"trp_temp_array_a",":item", ":imod"),
          (try_end),
          
          (assign, ":pos_x", 0),
          (assign, ":pos_y", 280),
          (assign, ":slot_no", 10),
          (try_for_range, ":unused_height", 0, 8),
            (try_for_range, ":unused_width", 0, 3),
              (create_mesh_overlay, reg1, "mesh_mp_inventory_choose"),
              (position_set_x, pos1, 320),
              (position_set_y, pos1, 320),
              (overlay_set_size, reg1, pos1),
              (position_set_x, pos1, ":pos_x"),
              (position_set_y, pos1, ":pos_y"),
              (overlay_set_position, reg1, pos1),
              (troop_set_slot, "trp_temp_array_a", ":slot_no", reg1),
              (create_mesh_overlay, reg1, "mesh_inv_slot"),
              (position_set_x, pos1, 400),
              (position_set_y, pos1, 400),
              (overlay_set_size, reg1, pos1),
              (position_set_x, pos1, ":pos_x"),
              (position_set_y, pos1, ":pos_y"),
              (overlay_set_position, reg1, pos1),
              (troop_get_inventory_slot, ":item_no", "trp_temp_array_a", ":slot_no"),
              (val_max, ":item_no", 0),
              (create_mesh_overlay_with_item_id, reg1, ":item_no"),
              (position_set_x, pos1, 400),
              (position_set_y, pos1, 400),
              (overlay_set_size, reg1, pos1),
              (store_add, ":item_x", ":pos_x", 20),
              (store_add, ":item_y", ":pos_y", 20),
              (position_set_x, pos1, ":item_x"),
              (position_set_y, pos1, ":item_y"),
              (overlay_set_position, reg1, pos1),
              (troop_set_slot, "trp_temp_array_b", ":slot_no", reg1),
              (val_add, ":pos_x", 40),
              (val_add, ":slot_no", 1),
            (try_end),
            (assign, ":pos_x", 0),
            (val_sub, ":pos_y", 40),
          (try_end),
          (set_container_overlay, -1),
        (try_end),
      ]),
      
    (ti_on_presentation_mouse_enter_leave,
      [
      (store_trigger_param_1, ":object"),
      (store_trigger_param_2, ":enter_leave"),
      
      (try_begin),
        (gt, "$g_selected_troop", 0), 
        (try_begin),
          (eq, ":enter_leave", 0),
          (try_for_range, ":slot_no", 10, 106),
            (troop_slot_eq, "trp_temp_array_a", ":slot_no", ":object"),
            (troop_get_inventory_slot, ":item_no", "trp_temp_array_a", ":slot_no"),
            (troop_get_inventory_slot_modifier, ":cur_imod", "trp_temp_array_a", ":slot_no"),
            (try_begin),
              (gt, ":item_no", -1),
              (troop_get_slot, ":target_obj", "trp_temp_array_b", ":slot_no"),
              (overlay_get_position, pos0, ":target_obj"),
              (show_item_details_with_modifier, ":item_no", ":cur_imod", pos0, 100),
              (assign, "$g_current_opened_item_details", ":slot_no"),
            (try_end),
          (try_end),
        (else_try),
          (try_for_range, ":slot_no", 10, 106),
            (troop_slot_eq, "trp_temp_array_a", ":slot_no", ":object"),
            (try_begin),
              (eq, "$g_current_opened_item_details", ":slot_no"),
              (close_item_details),
            (try_end),
          (try_end),
        (try_end),
      (try_end),
    ]),
      
    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
        
        (try_for_range, ":slot_no", 0, "$g_cur_slot_no"),
          (troop_slot_eq, "trp_stack_selection_amounts", ":slot_no", ":object"),
          (troop_get_slot, "$g_selected_troop", "trp_stack_selection_ids", ":slot_no"),
          (start_presentation, "prsnt_faction_troop_trees"),
        (try_end),
        
        (try_begin),
          (eq, ":object", "$g_presentation_obj_1"),
          (store_sub, ":num_pages", npc_kingdoms_end, npc_kingdoms_begin),
          (val_add, ":num_pages", 3),
          (store_sub, "$g_selected_page", ":num_pages", ":value"),
          (val_sub, "$g_selected_page", 1),
          (assign, "$g_selected_troop", 0), 
          (start_presentation, "prsnt_faction_troop_trees"),
        (else_try),
          (eq, ":object", "$g_presentation_obj_2"),
          (assign, "$g_selected_troop", 0), 
          (assign, "$g_selected_page", 0),
          (presentation_set_duration, 0),
        (try_end),
      ]),
    ]),
]
scripts = [
    ("troop_tree_recursive_backtracking", 
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":cur_x", 2),
      (store_script_param, ":cur_y", 3),
      (store_script_param, ":offset_x", 4),
      
      (store_add, ":next_x", ":cur_x", ":offset_x"),
      # upgrade_troop
      (troop_get_upgrade_troop, ":upgrade_troop_1", ":troop_no", 0),
      (troop_get_upgrade_troop, ":upgrade_troop_2", ":troop_no", 1),
      (try_begin),
        (gt,  ":upgrade_troop_2", 0),
        (call_script, "script_troop_tree_recursive_backtracking", ":upgrade_troop_2", ":next_x", reg2, ":offset_x"),
        (assign, ":upgrade_troop_2_y", reg0),
        (val_add, reg2, 160), # current global y
        (call_script, "script_troop_tree_recursive_backtracking", ":upgrade_troop_1", ":next_x", reg2, ":offset_x"),
        (assign, ":upgrade_troop_1_y", reg0),
      (else_try),
        (gt,  ":upgrade_troop_1", 0),
        (call_script, "script_troop_tree_recursive_backtracking", ":upgrade_troop_1", ":next_x", reg2, ":offset_x"),
        (assign, ":upgrade_troop_1_y", reg0),
      (try_end),
      
      # troop_tree_line
      (try_begin),
        (gt,  ":upgrade_troop_2", 0),
        (store_add, reg0, ":upgrade_troop_1_y", ":upgrade_troop_2_y"),
        (val_div, reg0, 2),
        #               ---- upgrade_troop_1
        #              |
        # troop_no ----
        #              |
        #               ---- upgrade_troop_2
        (store_div, ":half_offset_x", ":offset_x", 2),
        (store_add, ":middle_x", ":cur_x", ":half_offset_x"),
        (call_script, "script_prsnt_line", ":half_offset_x", 4, ":cur_x", reg0, 0),
        (call_script, "script_prsnt_line", ":half_offset_x", 4, ":middle_x", ":upgrade_troop_1_y", 0),
        (call_script, "script_prsnt_line", ":half_offset_x", 4, ":middle_x", ":upgrade_troop_2_y", 0),
        (store_sub, ":size_y", ":upgrade_troop_1_y", ":upgrade_troop_2_y"),
        (val_add, ":size_y", 4),
        (call_script, "script_prsnt_line", 4, ":size_y", ":middle_x", ":upgrade_troop_2_y", 0),
      (else_try),
        (gt,  ":upgrade_troop_1", 0),
        (assign, reg0, ":upgrade_troop_1_y"),
        #
        # troop_no -------- upgrade_troop_1
        #
        (call_script, "script_prsnt_line", ":offset_x", 4, ":cur_x", ":upgrade_troop_1_y", 0),
      (else_try),
        (assign, reg0, ":cur_y"),
      (try_end),
      
      # troop name
      (str_store_troop_name, s1, ":troop_no"),
      (create_text_overlay, reg1, "@{s1}", tf_center_justify|tf_vertical_align_center|tf_double_space|tf_scrollable),
      (store_sub, ":name_x", ":cur_x", 57),
      (store_sub, ":name_y", reg0, 120),
      (position_set_x, pos1, ":name_x"),
      (position_set_y, pos1, ":name_y"),
      (overlay_set_position, reg1, pos1),
      (position_set_x, pos1, 100),
      (position_set_y, pos1, 60),
      (overlay_set_area_size, reg1, pos1),
      (position_set_x, pos1, 640),
      (position_set_y, pos1, 640),
      (overlay_set_size, reg1, pos1),
      
      # troop avatar
      (store_sub, ":avatar_x", ":cur_x", 60),
      (store_sub, ":avatar_y", reg0, 60),
      (store_mul, ":cur_troop", ":troop_no", 2), #with weapons
      (create_image_button_overlay_with_tableau_material, reg1, -1, "tableau_game_party_window", ":cur_troop"),
      (position_set_x, pos1, 360),
      (position_set_y, pos1, 480),
      (overlay_set_size, reg1, pos1),
      (position_set_x, pos1, ":avatar_x"),
      (position_set_y, pos1, ":avatar_y"),
      (overlay_set_position, reg1, pos1),
      
      # troop info
      (troop_set_slot, "trp_stack_selection_amounts", "$g_cur_slot_no", reg1),
      (troop_set_slot, "trp_stack_selection_ids", "$g_cur_slot_no", ":troop_no"),
      (val_add, "$g_cur_slot_no", 1),
    ]),

   # reg0: cur max_tier
   ("troop_tree_recursive_detect_max_tier", 
    [
      (store_script_param, ":troop_no", 1),
      (store_script_param, ":cur_tier", 2),
      
      (store_add, ":next_tier", ":cur_tier", 1),
      # upgrade_troop
      (troop_get_upgrade_troop, ":upgrade_troop_1", ":troop_no", 0),
      (troop_get_upgrade_troop, ":upgrade_troop_2", ":troop_no", 1),
      (try_begin),
        (gt,  ":upgrade_troop_2", 0),
        (call_script, "script_troop_tree_recursive_detect_max_tier", ":upgrade_troop_2", ":next_tier"),
        (call_script, "script_troop_tree_recursive_detect_max_tier", ":upgrade_troop_1", ":next_tier"),
      (else_try),
        (gt,  ":upgrade_troop_1", 0),
        (call_script, "script_troop_tree_recursive_detect_max_tier", ":upgrade_troop_1", ":next_tier"),
      (try_end),
      
      (try_begin),
        (gt, ":cur_tier", reg0),
        (assign, reg0, ":cur_tier"),
      (try_end),
    ]),
    
  ("prsnt_line",
    [
      (store_script_param, ":size_x", 1),
      (store_script_param, ":size_y", 2),
      (store_script_param, ":pos_x", 3),
      (store_script_param, ":pos_y", 4),
      (store_script_param, ":color", 5),

      (create_mesh_overlay, reg1, "mesh_white_plane"),
      (val_mul, ":size_x", 50),
      (val_mul, ":size_y", 50),
      (position_set_x, pos0, ":size_x"),
      (position_set_y, pos0, ":size_y"),
      (overlay_set_size, reg1, pos0),
      (position_set_x, pos0, ":pos_x"),
      (position_set_y, pos0, ":pos_y"),
      (overlay_set_position, reg1, pos0),
      (overlay_set_color, reg1, ":color"),
  ]),
    
  # script_get_page_no_of_troop_tree_for_troop_on
  # Input: troop_no
  # Output: page_no
  ("get_page_no_of_troop_tree_for_troop_on",
  [
      (store_script_param, ":troop_no", 1),
      
      (store_sub, ":num_factions", npc_kingdoms_end, npc_kingdoms_begin),
      (store_troop_faction, ":troop_faction", ":troop_no"),
      (try_begin),
        (is_between, ":troop_faction", npc_kingdoms_begin, npc_kingdoms_end), 
        (store_sub, ":page_no", ":troop_faction", npc_kingdoms_begin),
      (else_try),
        (is_between, ":troop_no", soldiers_begin, mercenary_troops_end),
        (store_add, ":page_no", ":num_factions", 0), # mercenary
      (else_try),
        (eq, ":troop_faction", "fac_outlaws"),
        (store_add, ":page_no", ":num_factions", 1), # Outlaws
      (else_try),
        (store_add, ":page_no", ":num_factions", 2), # Others
      (try_end),
      (assign, reg0, ":page_no"),
  ]),
]

injection = {
  'view_troop_tree': [
    ("action_view_troop_trees",[],"View troop trees.",
      [
        (start_presentation, "prsnt_faction_troop_trees"),
      ]
    ),
  ],
}