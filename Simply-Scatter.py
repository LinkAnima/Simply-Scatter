import maya.cmds as cmds
import random
import math
import time
import uuid  # Added missing import

# Import OpenMaya for performance and proper rotation math
try:
    import maya.api.OpenMaya as om
    HAS_OPENMAYA = True
except ImportError:
    HAS_OPENMAYA = False

class SimplyScatter:
    def __init__(self):
        self.win_id = 'simplyScatterWin'
        self.created_materials = []  # Track materials to prevent accumulation
        
        # Clean up existing window
        if cmds.window(self.win_id, exists=True):
            cmds.deleteUI(self.win_id)
            
        # Create window with improved layout
        self.window = cmds.window(
            self.win_id, 
            title="Simply Scatter (Boundary Safe)", 
            widthHeight=(320, 1050)
        )
        
        # Use more organized layout
        self.layout = cmds.columnLayout(adj=True, rs=5, co=['both', 10])
        
        # Header section
        cmds.text(l="SIMPLY SCATTER", fn="boldLabelFont", h=40, backgroundColor=[0.2, 0.2, 0.2])
        
        # Scene Settings
        self._create_scene_settings()
        
        # Scaling Controls
        self._create_scaling_controls()
        
        # Scatter Parameters
        self._create_scatter_parameters()
        
        # Clustering Zones
        self._create_clustering_settings()
        
        # Virtual Subdivision Settings (Fixed)
        self._create_virtual_subdivision_settings()
        
        # Rotation Variance
        self._create_rotation_settings()
        
        # Proximity Detection
        self._create_proximity_settings()
        
        # Advanced Features
        self._create_advanced_features()
        
        # Material Assignment Section (NEW)
        self._create_material_assignment_section()
        
        # Execute Button
        cmds.button(
            l="RUN SCATTER", 
            c=self.execute_scatter, 
            h=50, 
            backgroundColor=[0.1, 0.4, 0.2]
        )
        
        cmds.showWindow(self.window)
    
    def _create_scene_settings(self):
        """Create scene settings section"""
        cmds.text(l="Scene Settings", al='left', fn="boldLabelFont")
        self.up_axis_ctrl = cmds.radioButtonGrp(
            l="Object Up Axis:", 
            numberOfRadioButtons=2, 
            labelArray2=["Y-Up", "Z-Up"], 
            select=1, 
            columnAlign2=["left", "left"]
        )
        cmds.separator(h=10)
    
    def _create_scaling_controls(self):
        """Create scaling customization section"""
        cmds.text(l="Scaling Customization", al='left', fn="boldLabelFont")
        self.scale_min_ctrl = cmds.floatSliderGrp(
            l="Min Scale Factor", 
            f=True, 
            min=0.01, 
            max=5.0, 
            v=0.5,  
            precision=2
        )
        
        self.scale_max_ctrl = cmds.floatSliderGrp(
            l="Max Scale Factor", 
            f=True, 
            min=0.01, 
            max=5.0, 
            v=1.5,  
            precision=2
        )
        
        # Show current range info
        self.scale_range_info = cmds.text(
            l="Current Range: 50% to 150%", 
            fn="smallPlainLabelFont", 
            al='center'
        )
        
        cmds.separator(h=5)
    
    def _create_scatter_parameters(self):
        """Create scatter parameters section"""
        cmds.text(l="Scatter Parameters", al='left', fn="boldLabelFont")
        self.cnt_ctrl = cmds.intSliderGrp(
            l="Object Count", 
            f=True, 
            min=1, 
            max=5000, 
            v=100
        )
        self.scl_ctrl = cmds.floatSliderGrp(
            l="Base Scale", 
            f=True, 
            min=0.01, 
            max=20, 
            v=1.0
        )
        self.uni_ctrl = cmds.checkBox(
            l="Use Uniform Scale (No Random)", 
            v=False
        )
        cmds.separator(h=5)
    
    def _create_clustering_settings(self):
        """Create clustering zones section"""
        cmds.text(l="Clustering Zones", al='left', fn="boldLabelFont")
        self.use_cluster_ctrl = cmds.checkBox(
            l="Enable Clustering", 
            v=True
        )
        self.cluster_count_ctrl = cmds.intSliderGrp(
            l="Number of Clusters", 
            f=True, 
            min=1, 
            max=100, 
            v=10
        )
        self.cluster_strength_ctrl = cmds.floatSliderGrp(
            l="Cluster Strength (Tightness)", 
            f=True, 
            min=0.0, 
            max=1.0, 
            v=0.2, 
            precision=2
        )
        cmds.separator(h=5)
    
    def _create_virtual_subdivision_settings(self):
        """Create virtual subdivision section with improved options"""
        cmds.text(l="Virtual Subdivision (Boundary Safe)", al='left', fn="boldLabelFont")
        
        # Add subdivision method selection - FIXED: Proper edge sampling
        self.subdiv_method_ctrl = cmds.radioButtonGrp(
            l="Subdivision Method:", 
            numberOfRadioButtons=2, 
            labelArray2=["Tangent Fit", "Edge Sampling"], 
            select=1, 
            columnAlign2=["left", "left"]
        )
        
        self.use_vsub_ctrl = cmds.checkBox(
            l="Enable Virtual Subdivision", 
            v=True
        )
        
        # UI Slider 0-10 mapped to 0-0.25 internally
        self.vsub_range_ctrl = cmds.intSliderGrp(
            l="Spread Intensity (0-10)", 
            f=True, 
            min=0, 
            max=10, 
            v=5,
            step=1
        )
        cmds.text(l="Higher values spread objects further from vertices.", fn="smallPlainLabelFont", al='center')
        cmds.text(l="Max physical offset is capped at 0.25 to prevent floating.", fn="smallPlainLabelFont", al='center')
        cmds.separator(h=5)
    
    def _create_rotation_settings(self):
        """Create rotation variance section"""
        cmds.text(l="Rotation Variance", al='left', fn="boldLabelFont")
        self.rx_ctrl = cmds.floatSliderGrp(
            l="X Tilt Randomness", 
            f=True, 
            min=0, 
            max=360, 
            v=15
        )
        self.ry_ctrl = cmds.floatSliderGrp(
            l="Y Twist Randomness", 
            f=True, 
            min=0, 
            max=360, 
            v=360
        )
        self.rz_ctrl = cmds.floatSliderGrp(
            l="Z Tilt Randomness", 
            f=True, 
            min=0, 
            max=360, 
            v=15
        )
        cmds.separator(h=5)
    
    def _create_proximity_settings(self):
        """Create proximity detection section"""
        cmds.text(l="Proximity Detection", al='left', fn="boldLabelFont")
        self.use_proximity_ctrl = cmds.checkBox(
            l="Enable Collision Avoidance", 
            v=True
        )
        self.proximity_dist_ctrl = cmds.floatSliderGrp(
            l="Min Distance", 
            f=True, 
            min=0.1, 
            max=10.0, 
            v=1.0
        )
        self.max_retries_ctrl = cmds.intSliderGrp(
            l="Max Retries per Obj", 
            f=True, 
            min=1, 
            max=100, 
            v=20
        )
        cmds.separator(h=5)
    
    def _create_advanced_features(self):
        """Create advanced features section"""
        cmds.text(l="Advanced Features", al='left', fn="boldLabelFont")
        self.align_ctrl = cmds.checkBox(
            l="Align to Surface Normal", 
            v=True
        )
        self.inst_ctrl = cmds.checkBox(
            l="Use Instancing (Faster)", 
            v=True
        )
        cmds.separator(h=20)
    
    def _create_material_assignment_section(self):
        """Create material assignment section"""
        cmds.text(l="Material Assignment", al='left', fn="boldLabelFont")
        self.use_materials_ctrl = cmds.checkBox(
            l="Assign Unique Materials to Object Types", 
            v=False
        )
        cmds.text(
            l="Creates one unique material per source object type.", 
            fn="smallPlainLabelFont", 
            al='center'
        )
        cmds.separator(h=20)
    
    def get_shape_node(self, node):
        """Helper to ensure we always get the shape node for geometry data."""
        if not cmds.objExists(node):
            return None
            
        if cmds.objectType(node, isType='mesh'):
            return node
            
        shapes = cmds.listRelatives(node, shapes=True, noIntermediate=True)
        if shapes:
            mesh_shapes = [s for s in shapes if cmds.objectType(s, isType='mesh')]
            if mesh_shapes:
                return mesh_shapes[0]
        
        return None
    
    def execute_scatter(self, *args):
        """Main execution method with improved error handling and performance"""
        # Validate selection
        selection = cmds.ls(selection=True)
        if not selection or len(selection) < 2:
            self._show_error("Select objects to scatter, then the Target Mesh LAST.")
            return
            
        target_node = selection[-1]
        source_objects = selection[:-1]
        
        # Validate target node
        target_shape = self.get_shape_node(target_node)
        if not target_shape:
            self._show_error("Target selection is not a valid mesh or transform with a mesh shape.")
            return
        
        # Get UI Values
        try:
            count_val = cmds.intSliderGrp(self.cnt_ctrl, q=True, v=True)
            scale_val = cmds.floatSliderGrp(self.scl_ctrl, q=True, v=True)
            use_uniform = cmds.checkBox(self.uni_ctrl, q=True, v=True)
            
            use_clustering = cmds.checkBox(self.use_cluster_ctrl, q=True, v=True)
            num_clusters = cmds.intSliderGrp(self.cluster_count_ctrl, q=True, v=True)
            cluster_strength = cmds.floatSliderGrp(self.cluster_strength_ctrl, q=True, v=True)
            
            subdiv_method = cmds.radioButtonGrp(self.subdiv_method_ctrl, q=True, select=True)
            use_vsub = cmds.checkBox(self.use_vsub_ctrl, q=True, v=True)
            use_proximity = cmds.checkBox(self.use_proximity_ctrl, q=True, v=True)
            vsub_ui_val = cmds.intSliderGrp(self.vsub_range_ctrl, q=True, v=True)
            
            # MAP UI 0-10 TO INTERNAL 0-0.25
            max_physical_offset = (vsub_ui_val / 10.0) * 0.25
            
            rx_range = cmds.floatSliderGrp(self.rx_ctrl, q=True, v=True)
            ry_range = cmds.floatSliderGrp(self.ry_ctrl, q=True, v=True)
            rz_range = cmds.floatSliderGrp(self.rz_ctrl, q=True, v=True)
            use_align = cmds.checkBox(self.align_ctrl, q=True, v=True)
            use_inst = cmds.checkBox(self.inst_ctrl, q=True, v=True)
            min_dist = cmds.floatSliderGrp(self.proximity_dist_ctrl, q=True, v=True)
            max_retries = cmds.intSliderGrp(self.max_retries_ctrl, q=True, v=True)
            
            # Get custom scaling values
            scale_min = cmds.floatSliderGrp(self.scale_min_ctrl, q=True, v=True)
            scale_max = cmds.floatSliderGrp(self.scale_max_ctrl, q=True, v=True)
            
            # Validate scale range
            if scale_min > scale_max:
                scale_min, scale_max = scale_max, scale_min
                cmds.floatSliderGrp(self.scale_min_ctrl, e=True, v=scale_min)
                cmds.floatSliderGrp(self.scale_max_ctrl, e=True, v=scale_max)
            
            # Update info text
            cmds.text(self.scale_range_info, e=True, l="Current Range: {:.0f}% to {:.0f}%".format(
                scale_min * 100, 
                scale_max * 100
            ))
            
            # Get up axis selection
            up_axis = cmds.radioButtonGrp(self.up_axis_ctrl, q=True, select=True)
            
            # Get material assignment setting
            use_materials = cmds.checkBox(self.use_materials_ctrl, q=True, v=True)
            
        except Exception as e:
            self._show_error("Error reading UI values: {}".format(str(e)))
            return
        
        # Setup Group with UUID to avoid conflicts
        group_name = "SimplyScatter_Result_GRP_{}".format(uuid.uuid4().hex[:8])
        result_grp = cmds.group(em=True, name=group_name)
        
        # Wrap in undo chunk for proper Maya behavior
        try:
            cmds.undoInfo(openChunk=True)
            
            # PRE-CALCULATION PHASE
            
            # Get Bounding Box
            bbox = cmds.exactWorldBoundingBox(target_shape)
            diag_x = bbox[3] - bbox[0]
            diag_y = bbox[4] - bbox[1]
            diag_z = bbox[5] - bbox[2]
            mesh_diagonal = math.sqrt(diag_x**2 + diag_y**2 + diag_z**2)
            
            # Get All Vertex Positions and Normals using OpenMaya for performance
            all_vtx_positions = []
            all_vtx_normals = []
            
            if HAS_OPENMAYA:
                try:
                    all_vtx_positions, all_vtx_normals = self._get_vertex_data_optimized(target_shape)
                except Exception as e:
                    print("OpenMaya error, falling back to standard Maya API: {}".format(str(e)))
                    all_vtx_positions, all_vtx_normals = self._get_vertex_data_standard(target_shape)
            else:
                all_vtx_positions, all_vtx_normals = self._get_vertex_data_standard(target_shape)
            
            # Determine Cluster Centers (Indices)
            cluster_centers_indices = []
            if use_clustering:
                actual_clusters = min(num_clusters, len(all_vtx_positions))
                cluster_centers_indices = random.sample(range(len(all_vtx_positions)), actual_clusters)
            else:
                cluster_centers_indices = list(range(len(all_vtx_positions)))
            
            # Create materials if enabled - CLEANUP PREVIOUS MATERIALS FIRST
            material_dict = {}
            if use_materials:
                # Clean up existing materials from previous runs
                self._cleanup_scatter_materials()
                material_dict = self._create_unique_materials(source_objects)
            
            # Storage for placed positions and spatial grid
            placed_positions = [] 
            success_count = 0
            failed_count = 0
            
            # Progress Bar Setup for Placement
            if cmds.progressWindow(query=True, exists=True):
                cmds.progressWindow(endProgress=True)
                
            cmds.progressWindow(
                title="Simply Scatter", 
                progress=0, 
                maxProgress=count_val, 
                status="Placing Objects...", 
                isInterruptable=True
            )
            
            try:
                # Create spatial hash grid for proximity checking (optimization)
                grid_size = min_dist
                grid = {}
                
                # Place objects with optimized logic
                for i in range(count_val):
                    if cmds.progressWindow(query=True, isCancelled=True):
                        break
                    
                    # Update progress every 25 objects to reduce UI overhead
                    if i % 25 == 0:
                        cmds.progressWindow(edit=True, progress=i)
                        
                    # Call the method with all necessary parameters including scale_min and scale_max
                    placed = self._place_object(
                        target_shape=target_shape,
                        source_objects=source_objects,
                        all_vtx_positions=all_vtx_positions,
                        all_vtx_normals=all_vtx_normals,
                        cluster_centers_indices=cluster_centers_indices,
                        mesh_diagonal=mesh_diagonal,
                        use_clustering=use_clustering,
                        num_clusters=num_clusters,
                        cluster_strength=cluster_strength,
                        max_physical_offset=max_physical_offset,
                        rx_range=rx_range,
                        ry_range=ry_range,
                        rz_range=rz_range,
                        use_align=use_align,
                        use_inst=use_inst,
                        use_proximity=use_proximity,
                        min_dist=min_dist,
                        max_retries=max_retries,
                        placed_positions=placed_positions,
                        result_grp=result_grp,
                        subdiv_method=subdiv_method,
                        scale_min=scale_min,
                        scale_max=scale_max,
                        material_dict=material_dict,
                        use_uniform=use_uniform,
                        use_materials=use_materials,
                        scale_val=scale_val,  # Added this parameter
                        use_vsub=use_vsub,    # FIXED: Add missing parameter
                        grid=grid,            # FIXED: Add spatial hash for proximity
                        grid_size=grid_size,   # FIXED: Add grid size
                        up_axis=up_axis       # FIXED: Pass up axis selection
                    )
                    
                    if placed:
                        success_count += 1
                    else:
                        failed_count += 1
                        
            except Exception as e:
                self._show_error("Error during object placement: {}".format(str(e)))
            finally:
                cmds.progressWindow(endProgress=True)
            
            print("Simply Scatter Complete: {} placed, {} failed.".format(success_count, failed_count))
            
        finally:
            cmds.undoInfo(closeChunk=True)
    
    def _get_vertex_data_standard(self, target_shape):
        """Standard Maya API vertex data retrieval"""
        all_vtx_positions = []
        all_vtx_normals = []
        
        try:
            vtx_count = cmds.polyEvaluate(target_shape, vertex=True)
        except Exception as e:
            self._show_error("Could not evaluate vertices on target shape: {}".format(str(e)))
            return [], []
            
        if vtx_count <= 0:
            self._show_error("No vertices found on target.")
            return [], []
        
        # Cache vertex data for better performance
        if cmds.progressWindow(query=True, exists=True):
            cmds.progressWindow(endProgress=True)
            
        cmds.progressWindow(
            title="Simply Scatter", 
            progress=0, 
            maxProgress=vtx_count, 
            status="Pre-calculating Mesh Data...", 
            isInterruptable=True
        )
        
        try:
            # Update every 100 vertices to reduce UI overhead
            for v_idx in range(vtx_count):
                if cmds.progressWindow(query=True, isCancelled=True):
                    break
                
                if v_idx % 100 == 0:
                    cmds.progressWindow(edit=True, progress=v_idx)
                
                vtx_path = "{}.vtx[{}]".format(target_shape, v_idx)
                pos = cmds.xform(vtx_path, q=True, ws=True, t=True)
                
                # Get normal more efficiently
                try:
                    norm_data = cmds.polyNormalPerVertex(target_shape, query=True, vector=True, index=v_idx)
                    if norm_data and len(norm_data) > 0:
                        n_x, n_y, n_z = norm_data[0][0], norm_data[0][1], norm_data[0][2]
                    else:
                        n_x, n_y, n_z = 0, 1, 0
                except Exception as e:
                    # Log error but continue with default normal
                    print("Warning: Failed to get vertex normal for index {}: {}".format(v_idx, str(e)))
                    n_x, n_y, n_z = 0, 1, 0
                    
                all_vtx_positions.append(pos)
                all_vtx_normals.append([n_x, n_y, n_z])
                
        finally:
            cmds.progressWindow(endProgress=True)
            
        return all_vtx_positions, all_vtx_normals
    
    def _get_vertex_data_optimized(self, target_shape):
        """Optimized OpenMaya vertex data retrieval - FIXED IMPLEMENTATION"""
        all_vtx_positions = []
        all_vtx_normals = []
        
        try:
            # FIXED: Proper OpenMaya implementation
            selection = om.MSelectionList()
            selection.add(target_shape)
            
            dag_path = selection.getDagPath(0)
            mesh_fn = om.MFnMesh(dag_path)
            
            # Get all vertex positions in bulk
            points = mesh_fn.getPoints(om.MSpace.kWorld)
            point_count = len(points)
            
            # Get normals in bulk  
            normals = mesh_fn.getVertexNormals(False, om.MSpace.kWorld)
            
            # Convert to standard list format
            for i in range(point_count):
                pos = [points[i].x, points[i].y, points[i].z]
                norm = [normals[i].x, normals[i].y, normals[i].z]
                all_vtx_positions.append(pos)
                all_vtx_normals.append(norm)
                
        except Exception as e:
            # Fall back to standard method if OpenMaya fails
            raise Exception("OpenMaya vertex data error: {}".format(str(e)))
            
        return all_vtx_positions, all_vtx_normals
    
    def _place_object(self, target_shape, source_objects, all_vtx_positions, all_vtx_normals,
                     cluster_centers_indices, mesh_diagonal, use_clustering, num_clusters,
                     cluster_strength, max_physical_offset, rx_range, ry_range, rz_range,
                     use_align, use_inst, use_proximity, min_dist, max_retries, placed_positions,
                     result_grp, subdiv_method, scale_min, scale_max, material_dict, use_uniform,
                     use_materials, scale_val, use_vsub, grid, grid_size, up_axis):
        """Place a single object with improved logic"""
        placed = False
        attempts = 0
        
        # Precompute squared distance for optimization
        min_dist_sq = min_dist * min_dist
        
        while not placed and attempts < max_retries:
            attempts += 1
            
            # Pick a Cluster Center Index
            current_center_idx = random.choice(cluster_centers_indices)
            center_pos = all_vtx_positions[current_center_idx]
            
            # Determine Placement Vertex based on Strength
            max_spread_dist = cluster_strength * mesh_diagonal
            
            if cluster_strength == 0.0:
                final_vtx_idx = current_center_idx
            else:
                found_valid = False
                for _ in range(20):
                    candidate_idx = random.randint(0, len(all_vtx_positions) - 1)
                    candidate_pos = all_vtx_positions[candidate_idx]
                    
                    dist_sq = self._calculate_distance_squared(
                        candidate_pos, 
                        center_pos
                    )
                    
                    if dist_sq <= max_spread_dist * max_spread_dist:
                        final_vtx_idx = candidate_idx
                        found_valid = True
                        break
                
                if not found_valid:
                    final_vtx_idx = current_center_idx
            
            # Get Base Position and Normal for Final Vertex
            base_pos = all_vtx_positions[final_vtx_idx]
            n_x, n_y, n_z = all_vtx_normals[final_vtx_idx]
            
            # Virtual Subdivision based on method - FIXED: use_vsub not use_proximity
            final_pos = list(base_pos)
            
            if use_vsub and max_physical_offset > 0:  # FIXED LOGIC
                # Apply subdivision method
                if subdiv_method == 1:  # Tangent Fit (original approach)
                    final_pos = self._apply_tangent_fit(
                        base_pos, 
                        n_x, n_y, n_z, 
                        max_physical_offset
                    )
                elif subdiv_method == 2:  # Edge Sampling (real implementation)
                    final_pos = self._apply_edge_sampling(
                        target_shape,
                        all_vtx_positions,  # FIXED: Now properly passed
                        base_pos,
                        n_x, n_y, n_z,
                        max_physical_offset,
                        final_vtx_idx  # NEW: Pass vertex index for better edge sampling
                    )
            
            # Check Proximity using spatial hash for better performance
            if use_proximity:
                # Use spatial hash to reduce proximity checks from O(N^2) to O(N)
                if self._check_proximity_optimized(final_pos, placed_positions, min_dist, grid, grid_size, min_dist_sq):
                    placed = True
                else:
                    # Spot taken. Retry with new cluster center
                    continue
            else:
                placed = True 
            
            if placed:
                # Create Object
                source_pick = random.choice(source_objects)
                if use_inst and not use_materials:  # FIXED: Only instance when no materials needed
                    new_item = cmds.instance(source_pick)[0]
                else:
                    # Force duplication when materials are required
                    new_item = cmds.duplicate(source_pick)[0]
                
                cmds.parent(new_item, result_grp)
                cmds.xform(new_item, translation=final_pos, worldSpace=True)
                
                # Rotation Logic - FIXED: Proper alignment with normal vectors using OpenMaya
                if use_align:
                    # Use actual rotation math with normal vector via OpenMaya
                    rot_x, rot_y, rot_z = self._compute_rotation_from_normal(
                        n_x, n_y, n_z, 
                        rx_range, ry_range, rz_range,
                        up_axis  # FIXED: Pass up axis selection
                    )
                    cmds.xform(new_item, rotation=(rot_x, rot_y, rot_z), worldSpace=True)
                else:
                    rx = random.uniform(-(rx_range/2), (rx_range/2))
                    ry = random.uniform(-(ry_range/2), (ry_range/2))
                    rz = random.uniform(-(rz_range/2), (rz_range/2))
                    cmds.xform(new_item, rotation=(rx, ry, rz), worldSpace=True)
                
                # Scale
                if use_uniform:
                    s = scale_val  # FIXED: Use passed parameter
                else:
                    s = random.uniform(scale_min, scale_max)  # FIXED: Use correct range
                cmds.scale(s, s, s, new_item)
                
                # Assign material if enabled
                if use_materials and source_pick in material_dict:
                    mat_info = material_dict[source_pick]
                    try:
                        # Assign the material to this instance/duplicate using existing SG
                        cmds.sets(new_item, e=True, forceElement=mat_info['shading_group'])
                    except Exception as e:
                        print("Material assignment error:", str(e))
                
                # Add to spatial hash for proximity checking
                self._add_to_spatial_grid(final_pos, grid, grid_size)
                placed_positions.append(final_pos)
                return True
        
        return False
    
    def _compute_rotation_from_normal(self, n_x, n_y, n_z, rx_range, ry_range, rz_range, up_axis):
        """Compute proper rotation from normal vector using OpenMaya for accurate math"""
        # Normalize the input normal
        length = math.sqrt(n_x*n_x + n_y*n_y + n_z*n_z)
        if length > 0:
            n_x /= length
            n_y /= length
            n_z /= length
        
        # Use OpenMaya for proper rotation calculation - FIXED: No special case needed
        if HAS_OPENMAYA:
            try:
                # Choose up vector based on UI selection
                if up_axis == 1:  # Y-Up (default)
                    up_vector = om.MVector(0, 1, 0)
                else:  # Z-Up
                    up_vector = om.MVector(0, 0, 1)
                
                normal_vector = om.MVector(n_x, n_y, n_z)
                
                # Calculate rotation quaternion to align up vector with normal
                quat = up_vector.rotateTo(normal_vector)
                
                # Convert to Euler rotation (XYZ order)
                euler_rotation = quat.asEulerRotation()
                
                # Convert from radians to degrees
                rot_x = math.degrees(euler_rotation.x)
                rot_y = math.degrees(euler_rotation.y) 
                rot_z = math.degrees(euler_rotation.z)
                
                # Add random variance
                rot_x += random.uniform(-(rx_range/2), (rx_range/2))
                rot_y += random.uniform(-(ry_range/2), (ry_range/2))
                rot_z += random.uniform(-(rz_range/2), (rz_range/2))
                
                return rot_x, rot_y, rot_z
                
            except Exception as e:
                # Fallback to simple approach if OpenMaya fails
                print("OpenMaya rotation error, falling back: {}".format(str(e)))
        
        # Fallback approach - still better than nothing
        rot_x = random.uniform(-(rx_range/2), (rx_range/2))
        rot_y = random.uniform(-(ry_range/2), (ry_range/2))
        rot_z = random.uniform(-(rz_range/2), (rz_range/2))
        
        return rot_x, rot_y, rot_z
    
    def _calculate_distance_squared(self, pos1, pos2):
        """Calculate squared distance between two points (faster)"""
        dx = pos1[0] - pos2[0]
        dy = pos1[1] - pos2[1]
        dz = pos1[2] - pos2[2]
        return dx*dx + dy*dy + dz*dz
    
    def _calculate_distance(self, pos1, pos2):
        """Calculate distance between two points"""
        return math.sqrt(
            (pos1[0] - pos2[0])**2 +
            (pos1[1] - pos2[1])**2 +
            (pos1[2] - pos2[2])**2
        )
    
    def _check_proximity_optimized(self, new_pos, existing_positions, min_dist, grid, grid_size, min_dist_sq):
        """Optimized proximity checking using spatial hashing"""
        # If we don't have a grid yet, do simple O(N) check (shouldn't happen in practice)
        if not grid or grid_size <= 0:
            for existing_pos in existing_positions:
                dist_sq = self._calculate_distance_squared(new_pos, existing_pos)
                if dist_sq < min_dist_sq:
                    return False
            return True
        
        # Use spatial hash to reduce comparisons
        cell_x = int(math.floor(new_pos[0] / grid_size))
        cell_y = int(math.floor(new_pos[1] / grid_size))
        cell_z = int(math.floor(new_pos[2] / grid_size))
        
        # Check nearby cells in the grid (3x3x3 neighborhood)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    cell_key = (cell_x + dx, cell_y + dy, cell_z + dz)
                    if cell_key in grid:
                        for existing_pos in grid[cell_key]:
                            dist_sq = self._calculate_distance_squared(new_pos, existing_pos)
                            if dist_sq < min_dist_sq:
                                return False
        
        return True
    
    def _add_to_spatial_grid(self, pos, grid, grid_size):
        """Add position to spatial hash grid"""
        if grid_size <= 0:
            return
            
        # Use math.floor for proper negative coordinate handling
        cell_x = int(math.floor(pos[0] / grid_size))
        cell_y = int(math.floor(pos[1] / grid_size))
        cell_z = int(math.floor(pos[2] / grid_size))
        
        cell_key = (cell_x, cell_y, cell_z)
        if cell_key not in grid:
            grid[cell_key] = []
        grid[cell_key].append(pos)
    
    def _compute_tangent_basis(self, n_x, n_y, n_z):
        """Compute tangent and bitangent vectors from normal - shared code"""
        # Find an arbitrary vector not parallel to normal
        if abs(n_y) < 0.9:
            arbitrary = [1, 0, 0]
        else:
            arbitrary = [0, 1, 0]
        
        # Calculate tangent and bitangent vectors
        t_x = arbitrary[1]*n_z - arbitrary[2]*n_y
        t_y = arbitrary[2]*n_x - arbitrary[0]*n_z
        t_z = arbitrary[0]*n_y - arbitrary[1]*n_x
        
        # Normalize tangent vector
        t_len = math.sqrt(t_x**2 + t_y**2 + t_z**2)
        if t_len > 0:
            t_x /= t_len
            t_y /= t_len
            t_z /= t_len
        else:
            t_x, t_y, t_z = 1, 0, 0
        
        # Calculate bitangent vector
        b_x = n_y*t_z - n_z*t_y
        b_y = n_z*t_x - n_x*t_z
        b_z = n_x*t_y - n_y*t_x
        
        # Normalize bitangent vector
        b_len = math.sqrt(b_x**2 + b_y**2 + b_z**2)
        if b_len > 0:
            b_x /= b_len
            b_y /= b_len
            b_z /= b_len
        else:
            b_x, b_y, b_z = 0, 1, 0
        
        return t_x, t_y, t_z, b_x, b_y, b_z
    
    def _apply_tangent_fit(self, base_pos, n_x, n_y, n_z, max_offset):
        """Apply tangent fit with optimized vector math"""
        # Use shared tangent basis computation
        t_x, t_y, t_z, b_x, b_y, b_z = self._compute_tangent_basis(n_x, n_y, n_z)
        
        # Generate random offset in tangent plane
        rand_t = random.uniform(-max_offset, max_offset)
        rand_b = random.uniform(-max_offset, max_offset)
        
        # Apply offset
        final_pos = [
            base_pos[0] + t_x * rand_t + b_x * rand_b,
            base_pos[1] + t_y * rand_t + b_y * rand_b,
            base_pos[2] + t_z * rand_t + b_z * rand_b
        ]
        
        return final_pos
    
    def _apply_edge_sampling(self, target_shape, all_vtx_positions, base_pos, n_x, n_y, n_z, max_offset, final_vtx_idx):
        """Apply edge sampling with better locality - IMPROVED VERSION"""
        try:
            # Get connected edges for better edge sampling locality
            if HAS_OPENMAYA:
                try:
                    selection = om.MSelectionList()
                    selection.add(target_shape)
                    dag_path = selection.getDagPath(0)
                    mesh_fn = om.MFnMesh(dag_path)
                    
                    # Get all edges connected to the final vertex for better locality
                    connected_edges = []
                    edge_it = om.MItMeshEdge(dag_path)
                    
                    # Find all edges connected to this vertex (FIXED: proper edge connection logic)
                    while not edge_it.isDone():
                        v1 = edge_it.vertexId(0)
                        v2 = edge_it.vertexId(1)
                        
                        if v1 == final_vtx_idx or v2 == final_vtx_idx:
                            connected_edges.append(edge_it.index())
                        edge_it.next()
                    
                    if connected_edges and len(connected_edges) > 0:
                        # Select one of the connected edges
                        random_edge_idx = random.choice(connected_edges)
                        
                        # Reset iterator to find this specific edge
                        edge_it.reset(dag_path)
                        while not edge_it.isDone():
                            if edge_it.index() == random_edge_idx:
                                break
                            edge_it.next()
                        
                        # Get vertices of the selected connected edge
                        v1_idx = edge_it.vertexId(0)
                        v2_idx = edge_it.vertexId(1)
                        
                        # Get positions of both vertices from passed array
                        v1_pos = all_vtx_positions[v1_idx]
                        v2_pos = all_vtx_positions[v2_idx]
                        
                        # Sample midpoint of edge with random offset in tangent plane
                        mid_x = (v1_pos[0] + v2_pos[0]) / 2.0
                        mid_y = (v1_pos[1] + v2_pos[1]) / 2.0
                        mid_z = (v1_pos[2] + v2_pos[2]) / 2.0
                        
                        # Use the normal at this point for better sampling
                        final_pos = [mid_x, mid_y, mid_z]
                        
                        # Apply tangent fit around this edge midpoint
                        t_x, t_y, t_z, b_x, b_y, b_z = self._compute_tangent_basis(n_x, n_y, n_z)
                        
                        rand_t = random.uniform(-max_offset, max_offset)
                        rand_b = random.uniform(-max_offset, max_offset)
                        
                        final_pos = [
                            final_pos[0] + t_x * rand_t + b_x * rand_b,
                            final_pos[1] + t_y * rand_t + b_y * rand_b,
                            final_pos[2] + t_z * rand_t + b_z * rand_b
                        ]
                        
                        return final_pos
                        
                except Exception as e:
                    print("Edge sampling error:", str(e))
            
            # Fallback to tangent fit if edge sampling fails
            return self._apply_tangent_fit(base_pos, n_x, n_y, n_z, max_offset)
            
        except Exception as e:
            # Fallback to simple offset if anything fails
            print(f"Edge sampling error: {str(e)}")
            final_pos = [
                base_pos[0] + random.uniform(-max_offset, max_offset),
                base_pos[1] + random.uniform(-max_offset, max_offset),
                base_pos[2] + random.uniform(-max_offset, max_offset)
            ]
        
        return final_pos
    
    def _safe_material_name(self, obj):
        """Generate safe material name avoiding namespace conflicts"""
        # Get short name without hierarchy
        short_name = cmds.ls(obj, shortNames=True)[0]
        # Sanitize for Maya naming conventions
        safe_name = "".join(c for c in short_name if c.isalnum() or c in "_")
        return "scatter_mat_{}".format(safe_name.replace(":", "_"))
    
    def _create_unique_materials(self, source_objects):
        """Create unique materials for each source object type"""
        material_dict = {}
        
        # Create a unique color for each source object
        colors = [
            [1, 0, 0],    # Red
            [0, 1, 0],    # Green  
            [0, 0, 1],    # Blue
            [1, 1, 0],    # Yellow
            [1, 0, 1],    # Magenta
            [0, 1, 1],    # Cyan
            [1, 0.5, 0],  # Orange
            [0.5, 0, 0.5], # Purple
            [0.5, 0.5, 0], # Olive
            [0, 0.5, 0.5]  # Teal
        ]
        
        for i, obj in enumerate(source_objects):
            # Get the object name without any path components
            obj_name = cmds.ls(obj, long=True)[0].split("|")[-1]
            
            # Create material name with unique identifier to prevent conflicts
            mat_name = "scatter_mat_{}_{}_{:.0f}".format(
                obj_name.replace(":", "_"), 
                i, 
                time.time()
            )
            
            # Use available color or cycle through if we have more objects than colors
            color_index = i % len(colors)
            color = colors[color_index]
            
            # Create blinn shader
            if not cmds.objExists(mat_name):
                material = cmds.shadingNode('blinn', asShader=True, name=mat_name)
                cmds.setAttr(material + ".color", color[0], color[1], color[2])
                cmds.setAttr(material + ".ambientColor", color[0], color[1], color[2])
                
                # Create shading group
                sg_name = mat_name + "SG"
                if not cmds.objExists(sg_name):
                    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=sg_name)
                    cmds.connectAttr(material + ".outColor", sg_name + ".surfaceShader")
                
                material_dict[obj] = {
                    'material': material,
                    'shading_group': sg_name
                }
                
                # Track created materials for cleanup
                self.created_materials.append(mat_name)
            else:
                # If material already exists, get it from the dict
                material_dict[obj] = {
                    'material': mat_name,
                    'shading_group': mat_name + "SG"
                }
        
        return material_dict
    
    def _cleanup_scatter_materials(self):
        """Clean up previously created scatter materials to prevent accumulation"""
        # Use pattern matching to find all scatter materials
        try:
            scatter_mats = cmds.ls("scatter_mat_*", materials=True)
            for mat_name in scatter_mats:
                if cmds.objExists(mat_name):
                    try:
                        # Get associated shading group
                        sg_name = mat_name + "SG"
                        if cmds.objExists(sg_name):
                            cmds.delete(sg_name)
                        # Delete material
                        cmds.delete(mat_name)
                    except Exception as e:
                        print("Cleanup error for {}: {}".format(mat_name, str(e)))
        except:
            pass  # Ignore errors in cleanup
        
        self.created_materials = []
    
    def _show_error(self, message):
        """Show error message in Maya"""
        print("Simply Scatter Error:", message)
        # Use warning instead of error for batch compatibility
        cmds.warning(message)

# Run the tool
SimplyScatter()
