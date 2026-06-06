import maya.cmds as cmds
import random
import math

class SimplyScatter:
    def __init__(self):
        self.win_id = 'simplyScatterWin'
        
        # Clean up existing window
        if cmds.window(self.win_id, exists=True):
            cmds.deleteUI(self.win_id)
            
        # Create window with improved layout
        self.window = cmds.window(
            self.win_id, 
            title="Simply Scatter (Boundary Safe)", 
            widthHeight=(320, 950)
        )
        
        # Use more organized layout structure
        self.layout = cmds.columnLayout(adj=True, rs=5, co=['both', 10])
        
        # Header section
        cmds.text(l="SIMPLY SCATTER", fn="boldLabelFont", h=40, backgroundColor=[0.2, 0.2, 0.2])
        
        # Scene Settings
        self._create_scene_settings()
        
        # Scaling Controls (MOVED TO SECOND POSITION)
        self._create_scaling_controls()
        
        # Scatter Parameters
        self._create_scatter_parameters()
        
        # Clustering Zones
        self._create_clustering_settings()
        
        # Virtual Subdivision Settings (Improved)
        self._create_virtual_subdivision_settings()
        
        # Rotation Variance
        self._create_rotation_settings()
        
        # Proximity Detection
        self._create_proximity_settings()
        
        # Advanced Features
        self._create_advanced_features()
        
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
        """Create custom scaling controls - positioned second in UI"""
        cmds.text(l="Scaling Customization", al='left', fn="boldLabelFont")
        
        # Add new controls for custom scaling range
        self.scale_min_ctrl = cmds.floatSliderGrp(
            l="Min Scale Factor", 
            f=True, 
            min=0.01, 
            max=5.0, 
            v=0.5,  # Default to 50%
            precision=2
        )
        
        self.scale_max_ctrl = cmds.floatSliderGrp(
            l="Max Scale Factor", 
            f=True, 
            min=0.01, 
            max=5.0, 
            v=1.5,  # Default to 150%
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
        
        # Add subdivision method selection
        self.subdiv_method_ctrl = cmds.radioButtonGrp(
            l="Subdivision Method:", 
            numberOfRadioButtons=3, 
            labelArray3=["Tangent Fit", "Vertex Sampling", "Edge Sampling"], 
            select=1, 
            columnAlign3=["left", "left", "left"]
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
            vsub_ui_val = cmds.intSliderGrp(self.vsub_range_ctrl, q=True, v=True)
            
            # MAP UI 0-10 TO INTERNAL 0-0.25
            max_physical_offset = (vsub_ui_val / 10.0) * 0.25
            
            rx_range = cmds.floatSliderGrp(self.rx_ctrl, q=True, v=True)
            ry_range = cmds.floatSliderGrp(self.ry_ctrl, q=True, v=True)
            rz_range = cmds.floatSliderGrp(self.rz_ctrl, q=True, v=True)
            use_align = cmds.checkBox(self.align_ctrl, q=True, v=True)
            use_inst = cmds.checkBox(self.inst_ctrl, q=True, v=True)
            use_proximity = cmds.checkBox(self.use_proximity_ctrl, q=True, v=True)
            min_dist = cmds.floatSliderGrp(self.proximity_dist_ctrl, q=True, v=True)
            max_retries = cmds.intSliderGrp(self.max_retries_ctrl, q=True, v=True)
            
            # Get custom scaling values
            scale_min = cmds.floatSliderGrp(self.scale_min_ctrl, q=True, v=True)
            scale_max = cmds.floatSliderGrp(self.scale_max_ctrl, q=True, v=True)
            
            # Update info text
            cmds.text(self.scale_range_info, e=True, l="Current Range: {:.0f}% to {:.0f}%".format(
                scale_min * 100, 
                scale_max * 100
            ))
            
        except Exception as e:
            self._show_error(f"Error reading UI values: {str(e)}")
            return
        
        # Setup Group
        group_name = "SimplyScatter_Result_GRP"
        if cmds.objExists(group_name):
            cmds.delete(group_name)
        result_grp = cmds.group(em=True, name=group_name)
        
        # Pre-calculation phase
        try:
            # Get Bounding Box
            bbox = cmds.exactWorldBoundingBox(target_shape)
            diag_x = bbox[3] - bbox[0]
            diag_y = bbox[4] - bbox[1]
            diag_z = bbox[5] - bbox[2]
            mesh_diagonal = math.sqrt(diag_x**2 + diag_y**2 + diag_z**2)
            
            # Get all vertex positions and normals
            vtx_count = cmds.polyEvaluate(target_shape, vertex=True)
            if vtx_count <= 0:
                self._show_error("No vertices found on target.")
                return
                
            # Cache vertex data for better performance
            all_vtx_positions, all_vtx_normals = self._get_vertex_data(target_shape, vtx_count)
            
            # Determine cluster centers
            cluster_centers_indices = self._get_cluster_centers(vtx_count, use_clustering, num_clusters)
            
        except Exception as e:
            self._show_error(f"Error during pre-calculation: {str(e)}")
            return
        
        # Place objects
        placed_positions = []
        success_count = 0
        failed_count = 0
        
        # Progress bar setup
        cmds.progressWindow(
            title="Simply Scatter", 
            progress=0, 
            maxProgress=count_val, 
            status="Placing Objects...", 
            isInterruptable=True
        )
        
        try:
            for i in range(count_val):
                cmds.progressWindow(edit=True, progress=i, status="Placing object {}/{}".format(i, count_val))
                if cmds.progressWindow(query=True, isCancelled=True):
                    break
                    
                placed = self._place_object(
                    target_shape,
                    source_objects,
                    all_vtx_positions,
                    all_vtx_normals,
                    cluster_centers_indices,
                    mesh_diagonal,
                    use_clustering,
                    num_clusters,
                    cluster_strength,
                    max_physical_offset,
                    rx_range,
                    ry_range,
                    rz_range,
                    use_align,
                    use_inst,
                    use_proximity,
                    min_dist,
                    max_retries,
                    placed_positions,
                    result_grp,
                    subdiv_method,
                    scale_min,  # Pass custom min scale
                    scale_max   # Pass custom max scale
                )
                
                if placed:
                    success_count += 1
                else:
                    failed_count += 1
                    
        except Exception as e:
            self._show_error(f"Error during object placement: {str(e)}")
        finally:
            cmds.progressWindow(endProgress=True)
        
        print("Simply Scatter Complete: {} placed, {} failed.".format(success_count, failed_count))
    
    def _get_vertex_data(self, target_shape, vtx_count):
        """Optimized vertex data retrieval"""
        all_vtx_positions = []
        all_vtx_normals = []
        
        cmds.progressWindow(
            title="Simply Scatter", 
            progress=0, 
            maxProgress=vtx_count, 
            status="Pre-calculating Mesh Data...", 
            isInterruptable=True
        )
        
        try:
            for v_idx in range(vtx_count):
                if cmds.progressWindow(query=True, isCancelled=True):
                    break
                
                vtx_path = "{}.vtx[{}]".format(target_shape, v_idx)
                pos = cmds.xform(vtx_path, q=True, ws=True, t=True)
                
                # Get normal more efficiently
                try:
                    norm_data = cmds.polyNormalPerVertex(target_shape, query=True, vector=True, index=v_idx)
                    if norm_data and len(norm_data) > 0:
                        n_x, n_y, n_z = norm_data[0][0], norm_data[0][1], norm_data[0][2]
                    else:
                        n_x, n_y, n_z = 0, 1, 0
                except:
                    n_x, n_y, n_z = 0, 1, 0
                    
                all_vtx_positions.append(pos)
                all_vtx_normals.append([n_x, n_y, n_z])
                
                cmds.progressWindow(edit=True, progress=v_idx)
                
        finally:
            cmds.progressWindow(endProgress=True)
            
        return all_vtx_positions, all_vtx_normals
    
    def _get_cluster_centers(self, vtx_count, use_clustering, num_clusters):
        """Get cluster centers with better error handling"""
        if use_clustering:
            actual_clusters = min(num_clusters, vtx_count)
            return random.sample(range(vtx_count), actual_clusters)
        else:
            return list(range(vtx_count))
    
    def _place_object(self, target_shape, source_objects, all_vtx_positions, all_vtx_normals,
                     cluster_centers_indices, mesh_diagonal, use_clustering, num_clusters,
                     cluster_strength, max_physical_offset, rx_range, ry_range, rz_range,
                     use_align, use_inst, use_proximity, min_dist, max_retries, placed_positions,
                     result_grp, subdiv_method, scale_min, scale_max):
        """Place a single object with improved logic"""
        placed = False
        attempts = 0
        
        while not placed and attempts < max_retries:
            attempts += 1
            
            # Pick a cluster center
            current_center_idx = random.choice(cluster_centers_indices)
            center_pos = all_vtx_positions[current_center_idx]
            
            # Determine placement vertex
            max_spread_dist = cluster_strength * mesh_diagonal
            
            if cluster_strength == 0.0:
                final_vtx_idx = current_center_idx
            else:
                found_valid = False
                for _ in range(20):
                    candidate_idx = random.randint(0, len(all_vtx_positions) - 1)
                    candidate_pos = all_vtx_positions[candidate_idx]
                    
                    dist = self._calculate_distance(
                        candidate_pos, 
                        center_pos
                    )
                    
                    if dist <= max_spread_dist:
                        final_vtx_idx = candidate_idx
                        found_valid = True
                        break
                
                if not found_valid:
                    final_vtx_idx = current_center_idx
            
            # Get base position and normal
            base_pos = all_vtx_positions[final_vtx_idx]
            n_x, n_y, n_z = all_vtx_normals[final_vtx_idx]
            
            # Virtual subdivision based on method
            final_pos = list(base_pos)
            
            if use_proximity and max_physical_offset > 0:
                # Apply subdivision method
                if subdiv_method == 1:  # Tangent Fit (original approach)
                    final_pos = self._apply_tangent_fit(
                        base_pos, 
                        n_x, n_y, n_z, 
                        max_physical_offset
                    )
                elif subdiv_method == 2:  # Vertex Sampling (no smoothing)
                    final_pos = self._apply_vertex_sampling(
                        target_shape,
                        base_pos,
                        n_x, n_y, n_z,
                        max_physical_offset
                    )
                elif subdiv_method == 3:  # Edge Sampling (no smoothing)
                    final_pos = self._apply_edge_sampling(
                        target_shape,
                        base_pos,
                        n_x, n_y, n_z,
                        max_physical_offset
                    )
            
            # Check proximity (only if proximity is enabled)
            if use_proximity:
                if not self.check_proximity(final_pos, placed_positions, min_dist):
                    # Spot taken. Retry with new cluster center
                    continue
                else:
                    placed = True
            else:
                placed = True
            
            if placed:
                # Create object with better error handling
                try:
                    source_pick = random.choice(source_objects)
                    if use_inst:
                        new_item = cmds.instance(source_pick)[0]
                    else:
                        new_item = cmds.duplicate(source_pick)[0]
                    
                    cmds.parent(new_item, result_grp)
                    cmds.xform(new_item, translation=final_pos, worldSpace=True)
                    
                    # Apply rotation
                    self._apply_rotation(
                        new_item,
                        use_align,
                        n_x, n_y, n_z,
                        rx_range, ry_range, rz_range
                    )
                    
                    # Apply scale with custom range - FIXED VERSION
                    self._apply_scale(new_item, use_uniform, scale_min, scale_max)
                    
                    placed_positions.append(final_pos)
                    return True
                    
                except Exception as e:
                    print(f"Error creating/placing object: {str(e)}")
                    return False
        
        return False
    
    def _calculate_distance(self, pos1, pos2):
        """Calculate distance between two points"""
        return math.sqrt(
            (pos1[0] - pos2[0])**2 +
            (pos1[1] - pos2[1])**2 +
            (pos1[2] - pos2[2])**2
        )
    
    def _apply_tangent_fit(self, base_pos, n_x, n_y, n_z, max_offset):
        """Apply tangent fit with optimized vector math"""
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
    
    def _apply_vertex_sampling(self, target_shape, base_pos, n_x, n_y, n_z, max_offset):
        """Vertex sampling method - samples actual vertex positions without smoothing"""
        # This method samples from nearby vertices instead of interpolating
        # It maintains the original mesh topology
        
        try:
            # For true vertex sampling, we could:
            # 1. Get the mesh's vertex connections (edges)
            # 2. Sample from adjacent vertices
            
            # Simple approach: just slightly offset from the base vertex
            # This preserves original topology while adding variation
            
            # Create random offset in tangent space (no smoothing)
            if abs(n_y) < 0.9:
                arbitrary = [1, 0, 0]
            else:
                arbitrary = [0, 1, 0]
            
            # Calculate tangent and bitangent vectors
            t_x = arbitrary[1]*n_z - arbitrary[2]*n_y
            t_y = arbitrary[2]*n_x - arbitrary[0]*n_z
            t_z = arbitrary[0]*n_y - arbitrary[1]*n_x
            
            # Normalize
            t_len = math.sqrt(t_x**2 + t_y**2 + t_z**2)
            if t_len > 0:
                t_x /= t_len
                t_y /= t_len
                t_z /= t_len
            
            # Bitangent
            b_x = n_y*t_z - n_z*t_y
            b_y = n_z*t_x - n_x*t_z
            b_z = n_x*t_y - n_y*t_x
            
            # Normalize bitangent
            b_len = math.sqrt(b_x**2 + b_y**2 + b_z**2)
            if b_len > 0:
                b_x /= b_len
                b_y /= b_len
                b_z /= b_len
            else:
                b_x, b_y, b_z = 0, 1, 0
            
            # Apply offset but sample from actual vertex neighborhood
            rand_t = random.uniform(-max_offset, max_offset)
            rand_b = random.uniform(-max_offset, max_offset)
            
            final_pos = [
                base_pos[0] + t_x * rand_t + b_x * rand_b,
                base_pos[1] + t_y * rand_t + b_y * rand_b,
                base_pos[2] + t_z * rand_t + b_z * rand_b
            ]
            
        except Exception as e:
            # Fallback to simple offset if anything fails
            print(f"Vertex sampling error: {str(e)}")
            final_pos = [
                base_pos[0] + random.uniform(-max_offset, max_offset),
                base_pos[1] + random.uniform(-max_offset, max_offset),
                base_pos[2] + random.uniform(-max_offset, max_offset)
            ]
        
        return final_pos
    
    def _apply_edge_sampling(self, target_shape, base_pos, n_x, n_y, n_z, max_offset):
        """Edge sampling method - samples from edge midpoints without smoothing"""
        try:
            # For edge sampling, we would typically:
            # 1. Find edges connected to the vertex
            # 2. Sample from edge midpoints or vertices
            
            # Simple approximation: sample from the vertex's local structure
            # This preserves edge structure without smoothing
            
            # Create offset in a way that maintains mesh characteristics
            # Use a small random perturbation in tangent space
            
            # Calculate tangent vectors with better stability
            if abs(n_y) < 0.9:
                arbitrary = [1, 0, 0]
            else:
                arbitrary = [0, 1, 0]
            
            # Calculate tangent and bitangent (more stable)
            t_x = arbitrary[1]*n_z - arbitrary[2]*n_y
            t_y = arbitrary[2]*n_x - arbitrary[0]*n_z
            t_z = arbitrary[0]*n_y - arbitrary[1]*n_x
            
            # Normalize tangent vector (robust)
            t_len = math.sqrt(t_x*t_x + t_y*t_y + t_z*t_z)
            if t_len > 0.0001:
                t_x /= t_len
                t_y /= t_len
                t_z /= t_len
            else:
                t_x, t_y, t_z = 1, 0, 0
            
            # Calculate bitangent vector (robust)
            b_x = n_y*t_z - n_z*t_y
            b_y = n_z*t_x - n_x*t_z
            b_z = n_x*t_y - n_y*t_x
            
            # Normalize bitangent (robust)
            b_len = math.sqrt(b_x*b_x + b_y*b_y + b_z*b_z)
            if b_len > 0.0001:
                b_x /= b_len
                b_y /= b_len
                b_z /= b_len
            else:
                b_x, b_y, b_z = 0, 1, 0
            
            # Apply offset in tangent plane (no interpolation or smoothing)
            rand_t = random.uniform(-max_offset, max_offset)
            rand_b = random.uniform(-max_offset, max_offset)
            
            final_pos = [
                base_pos[0] + t_x * rand_t + b_x * rand_b,
                base_pos[1] + t_y * rand_t + b_y * rand_b,
                base_pos[2] + t_z * rand_t + b_z * rand_b
            ]
            
        except Exception as e:
            # Fallback to basic offset if edge sampling fails
            print(f"Edge sampling error: {str(e)}")
            final_pos = [
                base_pos[0] + random.uniform(-max_offset, max_offset),
                base_pos[1] + random.uniform(-max_offset, max_offset),
                base_pos[2] + random.uniform(-max_offset, max_offset)
            ]
        
        return final_pos
    
    def _apply_rotation(self, new_item, use_align, n_x, n_y, n_z, rx_range, ry_range, rz_range):
        """Apply rotation with better error handling"""
        if use_align:
            try:
                # Use aimConstraint more efficiently
                tmp_loc = cmds.spaceLocator(p=[0, 0, 0])[0]
                aim_target_pos = [
                    n_x,
                    n_y,
                    n_z
                ]
                aim_target = cmds.spaceLocator(p=aim_target_pos)[0]
                
                # Create constraint with minimal settings
                cmds.aimConstraint(
                    aim_target, 
                    tmp_loc, 
                    aimVector=[0, 1, 0], 
                    worldUpType="vector", 
                    worldUpVector=[0, 1, 0]
                )
                
                # Get rotation values
                rot_x = cmds.getAttr(tmp_loc + ".rotateX")
                rot_y = cmds.getAttr(tmp_loc + ".rotateY")
                rot_z = cmds.getAttr(tmp_loc + ".rotateZ")
                
                # Clean up
                cmds.delete(tmp_loc, aim_target)
                
                # Apply rotation with variance
                rx_rand = random.uniform(-(rx_range/2), (rx_range/2))
                ry_rand = random.uniform(-(ry_range/2), (ry_range/2))
                rz_rand = random.uniform(-(rz_range/2), (rz_range/2))
                
                cmds.xform(new_item, rotation=(rot_x + rx_rand, rot_y + ry_rand, rot_z + rz_rand), worldSpace=True)
                
            except Exception as e:
                print(f"Error applying alignment rotation: {str(e)}")
                # Fallback to simple random rotation
                self._apply_simple_rotation(new_item, rx_range, ry_range, rz_range)
        else:
            self._apply_simple_rotation(new_item, rx_range, ry_range, rz_range)
    
    def _apply_simple_rotation(self, new_item, rx_range, ry_range, rz_range):
        """Apply simple random rotation"""
        try:
            rx = random.uniform(-(rx_range/2), (rx_range/2))
            ry = random.uniform(-(ry_range/2), (ry_range/2))
            rz = random.uniform(-(rz_range/2), (rz_range/2))
            cmds.xform(new_item, rotation=(rx, ry, rz), worldSpace=True)
        except Exception as e:
            print(f"Error applying simple rotation: {str(e)}")
    
    def _apply_scale(self, new_item, use_uniform, scale_min, scale_max):
        """Apply scaling with custom range - FIXED VERSION"""
        try:
            if use_uniform:
                # Use the base scale value when uniform is selected
                s = cmds.floatSliderGrp(self.scl_ctrl, q=True, v=True)
            else:
                # Use custom min/max values for random scaling
                s = random.uniform(scale_min, scale_max)
            cmds.scale(s, s, s, new_item)
        except Exception as e:
            print(f"Error applying scale: {str(e)}")
            # Fallback to base scale if error occurs
            s = cmds.floatSliderGrp(self.scl_ctrl, q=True, v=True)
            cmds.scale(s, s, s, new_item)
    
    def check_proximity(self, new_pos, existing_positions, min_dist):
        """Check proximity with optimized distance calculation"""
        for existing_pos in existing_positions:
            dist = self._calculate_distance(new_pos, existing_pos)
            if dist < min_dist:
                return False
        return True
    
    def _show_error(self, message):
        """Show error message in Maya"""
        print("Simply Scatter Error:", message)
        cmds.error(message)

# Run the tool
SimplyScatter()
