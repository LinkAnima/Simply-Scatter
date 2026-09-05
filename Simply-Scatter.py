import maya.cmds as cmds
import random
import math
import time
import uuid

# Import OpenMaya for performance and proper rotation math
try:
    import maya.api.OpenMaya as om
    HAS_OPENMAYA = True
except ImportError:
    HAS_OPENMAYA = False

class SimplyScatter:
    def __init__(self):
        self.win_id = 'simplyScatterWin'
        self.created_materials = []

        if cmds.window(self.win_id, exists=True):
            cmds.deleteUI(self.win_id)

        self.window = cmds.window(
            self.win_id,
            title="Simply Scatter",
            widthHeight=(350, 1100)
        )

        self.layout = cmds.columnLayout(adj=True, rs=5, co=['both', 10])

        cmds.text(l="SIMPLY SCATTER", fn="boldLabelFont", h=40, backgroundColor=[0.2, 0.2, 0.2])

        # --- Scene Settings ---
        cmds.text(l="Scene Settings", al='left', fn="boldLabelFont")
        self.up_axis_ctrl = cmds.radioButtonGrp(
            l="Object Up Axis:",
            numberOfRadioButtons=2,
            labelArray2=["Y-Up", "Z-Up"],
            select=1,
            columnAlign2=["left", "left"]
        )

        cmds.separator(h=10)

        # --- Mesh Preparation ---
        cmds.text(l="Mesh Preparation", al='left', fn="boldLabelFont")
        cmds.text(l="Duplicates target for higher density scatter.", fn="smallPlainLabelFont", al='center')

        self.subdiv_levels_ctrl = cmds.intSliderGrp(
            l="Subdivision Levels:",
            f=True,
            min=0,
            max=8,
            v=1,
            step=1
        )

        self.keep_sharp_ctrl = cmds.checkBox(
            l="Keep Sharp Edges",
            v=True,
            annotation="Subdivide topology only. Preserves original shape/silhouette.",
            cc=self._on_sharp_edges_changed
        )

        self.use_smoothing_ctrl = cmds.checkBox(
            l="Apply Smoothing",
            v=False,
            annotation="Subdivide with smoothing. Softens the mesh.",
            cc=self._on_smoothing_changed
        )

        self.keep_target_copy_ctrl = cmds.checkBox(
            l="Keep Subdivided Target",
            v=False
        )

        cmds.separator(h=5)

        # --- Scatter Parameters ---
        cmds.text(l="Scatter Parameters", al='left', fn="boldLabelFont")
        self.cnt_ctrl = cmds.intSliderGrp(l="Object Count", f=True, min=1, max=5000, v=100)
        self.scl_ctrl = cmds.floatSliderGrp(l="Base Scale", f=True, min=0.01, max=20, v=1.0)
        
        self.uni_ctrl = cmds.checkBox(
            l="Use Uniform Scale", 
            v=False,
            annotation="When enabled, all objects use the Base Scale exactly."
        )

        # Added changeCommand to trigger real-time UI update
        self.scale_min_ctrl = cmds.floatSliderGrp(
            l="Min Scale Factor", f=True, min=0.01, max=5.0, v=0.5, precision=2,
            changeCommand=self._update_scale_range_display
        )
        
        self.scale_max_ctrl = cmds.floatSliderGrp(
            l="Max Scale Factor", f=True, min=0.01, max=5.0, v=1.5, precision=2,
            changeCommand=self._update_scale_range_display
        )

        # The label that will be updated in real-time
        self.scale_range_info = cmds.text(
            l="Current Range: 50% to 150%", fn="smallPlainLabelFont", al='center'
        )
        
        # Call once on init to ensure correct initial display
        self._update_scale_range_display()

        cmds.separator(h=5)

        # --- Clustering Zones ---
        cmds.text(l="Clustering Zones", al='left', fn="boldLabelFont")
        self.use_cluster_ctrl = cmds.checkBox(l="Enable Clustering", v=True)
        
        # Reduced Max from 100 to 25
        self.cluster_count_ctrl = cmds.intSliderGrp(
            l="Number of Clusters", f=True, min=1, max=25, v=10
        )
        
        self.cluster_strength_ctrl = cmds.floatSliderGrp(
            l="Tightness",
            f=True, 
            min=0.0, 
            max=1.0, 
            v=0.8, 
            precision=2,
            annotation="0 is fully spread across mesh. 1 is clustered tightly at centers."
        )
        cmds.separator(h=5)

        # --- Slope Filtering ---
        # 1. Removed "/" from section header
        cmds.text(l="Slope Filtering", al='left', fn="boldLabelFont")
        cmds.text(l="Prevents scattering on steep surfaces.", fn="smallPlainLabelFont", al='center')
        self.use_slope_ctrl = cmds.checkBox(l="Enable Slope Filter", v=True)
        
        # 2. Removed "Max", "/", and "(Degrees)" from slider label
        self.max_slope_ctrl = cmds.floatSliderGrp(
            l="Angle", f=True, min=0, max=90, v=60, precision=1
        )
        cmds.separator(h=5)

        # --- Rotation Variance ---
        cmds.text(l="Rotation Variance", al='left', fn="boldLabelFont")
        self.rx_ctrl = cmds.floatSliderGrp(l="X Tilt Randomness", f=True, min=0, max=360, v=15)
        self.ry_ctrl = cmds.floatSliderGrp(l="Y Twist Randomness", f=True, min=0, max=360, v=360)
        self.rz_ctrl = cmds.floatSliderGrp(l="Z Tilt Randomness", f=True, min=0, max=360, v=15)
        cmds.separator(h=5)

        # --- Proximity Detection ---
        cmds.text(l="Proximity Detection", al='left', fn="boldLabelFont")
        self.use_proximity_ctrl = cmds.checkBox(l="Enable Collision Avoidance", v=True)
        self.proximity_dist_ctrl = cmds.floatSliderGrp(l="Min Distance", f=True, min=0.1, max=10.0, v=1.0)
        
        # 1. Reduced max to 10
        # 2. Changed label to "Retries per Object"
        self.max_retries_ctrl = cmds.intSliderGrp(
            l="Retries per Object", 
            f=True, 
            min=1, 
            max=10, 
            v=5
        )
        cmds.separator(h=5)

        # --- Advanced Features ---
        cmds.text(l="Advanced Features", al='left', fn="boldLabelFont")
        self.align_ctrl = cmds.checkBox(l="Align to Surface Normal", v=True)
        
        # 3. Removed "(Faster)"
        self.inst_ctrl = cmds.checkBox(
            l="Use Instancing", 
            v=True
        )

        self.use_materials_ctrl = cmds.checkBox(
            l="Assign Unique Materials to Object Types", v=False
        )

        cmds.separator(h=20)
        cmds.button(l="RUN SCATTER", c=self.execute_scatter, h=50, backgroundColor=[0.1, 0.4, 0.2])
        cmds.showWindow(self.window)

    # ------------------------------------------------------------------
    #  UI CALLBACKS
    # ------------------------------------------------------------------
    
    def _update_scale_range_display(self, *args):
        """
        Callback for the Scale Min/Max sliders.
        Updates the 'scale_range_info' text node in real-time.
        """
        try:
            min_val = cmds.floatSliderGrp(self.scale_min_ctrl, q=True, v=True)
            max_val = cmds.floatSliderGrp(self.scale_max_ctrl, q=True, v=True)
            
            # Ensure min <= max for display logic (though Maya usually handles slider limits)
            if min_val > max_val:
                # If user drags min above max, Maya might allow it depending on setup, 
                # but for display purposes we show the values as dragged.
                pass 

            cmds.text(self.scale_range_info, e=True,
                      l="Current Range: {:.0f}% to {:.0f}%".format(min_val * 100, max_val * 100))
        except Exception:
            # Fallback if UI controls don't exist yet (e.g. during init)
            pass

    def _on_sharp_edges_changed(self, *args):
        """
        Sharp mode selected.
        Always keep exactly one subdivision mode active.
        """
        if cmds.checkBox(self.keep_sharp_ctrl, q=True, v=True):
            # Sharp selected -> turn smoothing OFF
            cmds.checkBox(self.use_smoothing_ctrl, e=True, v=False)
        else:
            # User tried to turn Sharp OFF.
            # If smoothing isn't ON, restore Sharp.
            if not cmds.checkBox(self.use_smoothing_ctrl, q=True, v=True):
                cmds.checkBox(self.keep_sharp_ctrl, e=True, v=True)

    def _on_smoothing_changed(self, *args):
        """
        Smoothing mode selected.
        Always keep exactly one subdivision mode active.
        """
        if cmds.checkBox(self.use_smoothing_ctrl, q=True, v=True):
            # Smoothing selected -> turn Sharp OFF
            cmds.checkBox(self.keep_sharp_ctrl, e=True, v=False)
        else:
            # User tried to turn Smoothing OFF.
            # If Sharp isn't ON, restore Smoothing.
            if not cmds.checkBox(self.keep_sharp_ctrl, q=True, v=True):
                cmds.checkBox(self.use_smoothing_ctrl, e=True, v=True)

    # ------------------------------------------------------------------
    #  HELPER: resolve a shape node from a transform or shape name
    # ------------------------------------------------------------------
    def get_shape_node(self, node):
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

    # ------------------------------------------------------------------
    #  MAIN EXECUTION
    # ------------------------------------------------------------------
    def execute_scatter(self, *args):
        selection = cmds.ls(selection=True)
        valid_selection = [s for s in selection if cmds.objExists(s)]

        if not valid_selection or len(valid_selection) < 2:
            self._show_error("Selection Error: Select objects to scatter, then the Target Mesh LAST.")
            return

        target_node = valid_selection[-1]
        source_objects = valid_selection[:-1]

        if not cmds.objectType(target_node, isType='transform') and \
           not cmds.objectType(target_node, isType='mesh'):
            self._show_error("Target must be a Transform or Mesh.")
            return

        valid_sources = [s for s in source_objects
                         if cmds.objectType(s, isType='transform') or
                            cmds.objectType(s, isType='mesh')]
        if not valid_sources:
            self._show_error("No valid source objects.")
            return

        target_shape = self.get_shape_node(target_node)
        if not target_shape:
            self._show_error("Target is not a valid mesh.")
            return

        # ---- Read UI values ----
        try:
            count_val       = cmds.intSliderGrp(self.cnt_ctrl, q=True, v=True)
            scale_val       = cmds.floatSliderGrp(self.scl_ctrl, q=True, v=True)
            use_uniform     = cmds.checkBox(self.uni_ctrl, q=True, v=True)

            use_clustering  = cmds.checkBox(self.use_cluster_ctrl, q=True, v=True)
            num_clusters    = cmds.intSliderGrp(self.cluster_count_ctrl, q=True, v=True)
            cluster_strength= cmds.floatSliderGrp(self.cluster_strength_ctrl, q=True, v=True)

            use_slope_filter= cmds.checkBox(self.use_slope_ctrl, q=True, v=True)
            max_slope_angle = cmds.floatSliderGrp(self.max_slope_ctrl, q=True, v=True)

            subdiv_levels   = cmds.intSliderGrp(self.subdiv_levels_ctrl, q=True, v=True)
            
            use_sharp_edges = cmds.checkBox(self.keep_sharp_ctrl, q=True, v=True)
            use_smoothing   = cmds.checkBox(self.use_smoothing_ctrl, q=True, v=True)
            
            keep_target_copy= cmds.checkBox(self.keep_target_copy_ctrl, q=True, v=True)

            rx_range = cmds.floatSliderGrp(self.rx_ctrl, q=True, v=True)
            ry_range = cmds.floatSliderGrp(self.ry_ctrl, q=True, v=True)
            rz_range = cmds.floatSliderGrp(self.rz_ctrl, q=True, v=True)

            use_align     = cmds.checkBox(self.align_ctrl, q=True, v=True)
            use_inst      = cmds.checkBox(self.inst_ctrl, q=True, v=True)
            use_proximity = cmds.checkBox(self.use_proximity_ctrl, q=True, v=True)
            min_dist      = cmds.floatSliderGrp(self.proximity_dist_ctrl, q=True, v=True)
            max_retries   = cmds.intSliderGrp(self.max_retries_ctrl, q=True, v=True)

            scale_min = cmds.floatSliderGrp(self.scale_min_ctrl, q=True, v=True)
            scale_max = cmds.floatSliderGrp(self.scale_max_ctrl, q=True, v=True)
            
            # Ensure logical min/max for calculation
            if scale_min > scale_max:
                scale_min, scale_max = scale_max, scale_min

            up_axis       = cmds.radioButtonGrp(self.up_axis_ctrl, q=True, select=True)
            use_materials = cmds.checkBox(self.use_materials_ctrl, q=True, v=True)

        except Exception as e:
            self._show_error("Error reading UI: {}".format(str(e)))
            return

        # ---- Result group ----
        group_name = "SimplyScatter_Result_GRP_{}".format(uuid.uuid4().hex[:8])
        result_grp = cmds.group(em=True, name=group_name)

        temp_scatter_transform = None

        try:
            cmds.undoInfo(openChunk=True)

            # =========================================================
            #  PHASE 1: Create temporary subdivided mesh
            # =========================================================
            dup_name = "Temp_Scatter_Mesh_{}".format(uuid.uuid4().hex[:6])

            try:
                dup_result = cmds.duplicate(target_node, name=dup_name)
                if dup_result:
                    first_item = dup_result[0]
                    if cmds.objectType(first_item, isType='transform'):
                        temp_scatter_transform = first_item
                    else:
                        parents = cmds.listRelatives(first_item, parent=True, noIntermediate=True)
                        if parents:
                            temp_scatter_transform = parents[0]
                else:
                    raise Exception("Duplicate returned empty list.")
            except Exception as e:
                self._show_error("Failed to duplicate target: {}".format(str(e)))
                cmds.delete(result_grp)
                return

            if not temp_scatter_transform or not cmds.objExists(temp_scatter_transform):
                self._show_error("Duplicate creation failed.")
                cmds.delete(result_grp)
                return

            work_shape = self.get_shape_node(temp_scatter_transform)
            if not work_shape:
                self._show_error("Could not get shape from duplicate.")
                cmds.delete(result_grp)
                return

            # Bounding box for boundary checks (before subd)
            bbox = cmds.exactWorldBoundingBox(work_shape)
            if bbox:
                bbox_min = [bbox[0], bbox[1], bbox[2]]
                bbox_max = [bbox[3], bbox[4], bbox[5]]
                margin = 0.01 * (bbox[3] - bbox[0]) if (bbox[3] - bbox[0]) > 0 else 0.01
                bbox_min = [bbox_min[0] - margin, bbox_min[1] - margin, bbox_min[2] - margin]
                bbox_max = [bbox_max[0] + margin, bbox_max[1] + margin, bbox_max[2] + margin]
            else:
                bbox_min = [-1000, -1000, -1000]
                bbox_max = [1000, 1000, 1000]

            # =========================================================
            #  PHASE 1A: SUBDIVIDE THE TEMPORARY SCATTER MESH
            # =========================================================
            if subdiv_levels > 0:
                try:
                    # SHARP / NO SMOOTHING MODE
                    if use_sharp_edges:
                        cmds.polySmooth(
                            work_shape,
                            divisions=subdiv_levels,
                            continuity=0.0,
                            keepBorder=True,
                            keepHardEdge=True,
                            propagateEdgeHardness=True,
                            constructionHistory=False
                        )

                    # CATMULL-CLARK SMOOTHING MODE
                    elif use_smoothing:
                        cmds.polySmooth(
                            work_shape,
                            divisions=subdiv_levels,
                            continuity=1.0,
                            keepBorder=True,
                            keepHardEdge=False,
                            propagateEdgeHardness=True,
                            constructionHistory=False
                        )

                    # SAFETY FALLBACK
                    else:
                        cmds.polySmooth(
                            work_shape,
                            divisions=subdiv_levels,
                            continuity=0.0,
                            keepBorder=True,
                            keepHardEdge=True,
                            propagateEdgeHardness=True,
                            constructionHistory=False
                        )

                except Exception as e:
                    self._show_error("Subdivision failed: {}".format(str(e)))
                    if temp_scatter_transform and cmds.objExists(temp_scatter_transform):
                        cmds.delete(temp_scatter_transform)
                    if cmds.objExists(result_grp):
                        cmds.delete(result_grp)
                    return

            # Re-fetch shape (stays as 'mesh' type with polySmooth)
            temp_scatter_mesh = self.get_shape_node(temp_scatter_transform)
            if not temp_scatter_mesh:
                self._show_error("Invalid final mesh after subd.")
                if temp_scatter_transform and cmds.objExists(temp_scatter_transform):
                    cmds.delete(temp_scatter_transform)
                cmds.delete(result_grp)
                return

            cmds.setAttr(temp_scatter_transform + ".visibility", 0)

            if keep_target_copy:
                cmds.parent(temp_scatter_transform, result_grp)

            # =========================================================
            #  PHASE 2: Extract vertex data
            # =========================================================
            if HAS_OPENMAYA:
                try:
                    all_vtx_positions, all_vtx_normals = self._get_vertex_data_optimized(temp_scatter_mesh)
                except Exception as e:
                    print("OpenMaya failed, using fallback: {}".format(str(e)))
                    all_vtx_positions, all_vtx_normals = self._get_vertex_data_standard(temp_scatter_mesh)
            else:
                all_vtx_positions, all_vtx_normals = self._get_vertex_data_standard(temp_scatter_mesh)

            if not all_vtx_positions:
                self._show_error("No vertices found on subdivided mesh.")
                if temp_scatter_transform and cmds.objExists(temp_scatter_transform):
                    cmds.delete(temp_scatter_transform)
                cmds.delete(result_grp)
                return

            # Pre-calculate slopes if filtering is enabled
            if use_slope_filter and HAS_OPENMAYA:
                up_vector = om.MVector(0, 1, 0) if up_axis == 1 else om.MVector(0, 0, 1)
                all_vtx_slopes = []
                for i in range(len(all_vtx_positions)):
                    n = all_vtx_normals[i]
                    length = math.sqrt(n[0]**2 + n[1]**2 + n[2]**2)
                    if length > 0:
                        n_norm = om.MVector(n[0]/length, n[1]/length, n[2]/length)
                        angle_deg = math.degrees(up_vector.angle(n_norm))
                        all_vtx_slopes.append(angle_deg)
                    else:
                        all_vtx_slopes.append(0.0)
            elif use_slope_filter:
                all_vtx_slopes = [0.0] * len(all_vtx_positions)
            else:
                all_vtx_slopes = [0.0] * len(all_vtx_positions)

            mesh_diagonal = self._get_mesh_diagonal(temp_scatter_mesh)

            # ---- Determine cluster centers ----
            cluster_centers_indices = []
            if use_clustering:
                actual_clusters = min(num_clusters, len(all_vtx_positions))
                if use_slope_filter:
                    valid_indices = [i for i in range(len(all_vtx_positions))
                                     if all_vtx_slopes[i] <= max_slope_angle]
                    if valid_indices:
                        cluster_centers_indices = random.sample(valid_indices,
                                                               min(actual_clusters, len(valid_indices)))
                    else:
                        cluster_centers_indices = list(range(len(all_vtx_positions)))
                else:
                    cluster_centers_indices = random.sample(range(len(all_vtx_positions)), actual_clusters)
            else:
                cluster_centers_indices = list(range(len(all_vtx_positions)))

            # ---- Materials ----
            material_dict = {}
            if use_materials:
                self._cleanup_scatter_materials()
                material_dict = self._create_unique_materials(valid_sources)

            # ---- Placement ----
            placed_positions = []
            success_count = 0
            failed_count = 0

            grid_size = min_dist if use_proximity else 100
            grid = {}

            cmds.progressWindow(title="Simply Scatter", progress=0,
                                maxProgress=count_val,
                                status="Placing Objects...", isInterruptable=True)

            try:
                for i in range(count_val):
                    if cmds.progressWindow(query=True, isCancelled=True):
                        break
                    if i % 25 == 0:
                        cmds.progressWindow(edit=True, progress=i)

                    placed = self._place_object(
                        source_objects=valid_sources,
                        all_vtx_positions=all_vtx_positions,
                        all_vtx_normals=all_vtx_normals,
                        all_vtx_slopes=all_vtx_slopes,
                        cluster_centers_indices=cluster_centers_indices,
                        mesh_diagonal=mesh_diagonal,
                        use_clustering=use_clustering,
                        num_clusters=num_clusters,
                        cluster_strength=cluster_strength,
                        rx_range=rx_range, ry_range=ry_range, rz_range=rz_range,
                        use_align=use_align,
                        use_inst=use_inst,
                        use_proximity=use_proximity,
                        min_dist=min_dist, max_retries=max_retries,
                        placed_positions=placed_positions,
                        result_grp=result_grp,
                        scale_min=scale_min, scale_max=scale_max,
                        material_dict=material_dict,
                        use_uniform=use_uniform,
                        use_materials=use_materials,
                        scale_val=scale_val,
                        up_axis=up_axis,
                        grid=grid, grid_size=grid_size,
                        use_slope_filter=use_slope_filter,
                        max_slope_angle=max_slope_angle,
                        bbox_min=bbox_min, bbox_max=bbox_max
                    )

                    if placed:
                        success_count += 1
                    else:
                        failed_count += 1

            except Exception as e:
                self._show_error("Error during placement: {}".format(str(e)))
            finally:
                cmds.progressWindow(endProgress=True)

            # ---- Cleanup ----
            if not keep_target_copy:
                if temp_scatter_transform and cmds.objExists(temp_scatter_transform):
                    cmds.delete(temp_scatter_transform)

            print("Simply Scatter Complete: {} placed, {} failed.".format(success_count, failed_count))

        finally:
            cmds.undoInfo(closeChunk=True)

    # ------------------------------------------------------------------
    #  VERTEX DATA (standard Maya cmds)
    # ------------------------------------------------------------------
    def _get_vertex_data_standard(self, target_shape):
        all_vtx_positions = []
        all_vtx_normals = []

        if not target_shape or not cmds.objExists(target_shape):
            return [], []

        try:
            vtx_count = cmds.polyEvaluate(target_shape, vertex=True)
        except Exception as e:
            self._show_error("Could not evaluate vertices: {}".format(str(e)))
            return [], []

        if vtx_count <= 0:
            return [], []

        for v_idx in range(vtx_count):
            vtx_path = "{}.vtx[{}]".format(target_shape, v_idx)
            if not cmds.objExists(vtx_path):
                continue
            pos = cmds.xform(vtx_path, q=True, ws=True, t=True)
            try:
                norm_data = cmds.polyNormalPerVertex(vtx_path, query=True, xyz=True)
                if norm_data and len(norm_data) > 0:
                    n_x, n_y, n_z = norm_data[0], norm_data[1], norm_data[2]
                else:
                    n_x, n_y, n_z = 0, 1, 0
            except:
                n_x, n_y, n_z = 0, 1, 0
            all_vtx_positions.append(pos)
            all_vtx_normals.append([n_x, n_y, n_z])

        return all_vtx_positions, all_vtx_normals

    # ------------------------------------------------------------------
    #  VERTEX DATA (OpenMaya – faster)
    # ------------------------------------------------------------------
    def _get_vertex_data_optimized(self, target_shape):
        all_vtx_positions = []
        all_vtx_normals = []

        try:
            sel = om.MSelectionList()
            sel.add(target_shape)
            dag_path = sel.getDagPath(0)
            mesh_fn = om.MFnMesh(dag_path)

            points = mesh_fn.getPoints(om.MSpace.kWorld)
            point_count = len(points)
            normals = mesh_fn.getVertexNormals(False, om.MSpace.kWorld)

            for i in range(point_count):
                pos = [points[i].x, points[i].y, points[i].z]
                norm = [normals[i].x, normals[i].y, normals[i].z]
                all_vtx_positions.append(pos)
                all_vtx_normals.append(norm)
        except Exception as e:
            raise Exception("OpenMaya error: {}".format(str(e)))

        return all_vtx_positions, all_vtx_normals

    # ------------------------------------------------------------------
    #  MESH DIAGONAL
    # ------------------------------------------------------------------
    def _get_mesh_diagonal(self, mesh_shape):
        try:
            bbox = cmds.exactWorldBoundingBox(mesh_shape)
            if not bbox or len(bbox) < 6:
                return 1.0
            dx = bbox[3] - bbox[0]
            dy = bbox[4] - bbox[1]
            dz = bbox[5] - bbox[2]
            return math.sqrt(dx*dx + dy*dy + dz*dz)
        except:
            return 1.0

    # ------------------------------------------------------------------
    #  BOUNDARY CHECK
    # ------------------------------------------------------------------
    def _is_within_bounds(self, pos, bbox_min, bbox_max):
        return (
            bbox_min[0] <= pos[0] <= bbox_max[0] and
            bbox_min[1] <= pos[1] <= bbox_max[1] and
            bbox_min[2] <= pos[2] <= bbox_max[2]
        )

    # ------------------------------------------------------------------
    #  PLACE SINGLE OBJECT
    # ------------------------------------------------------------------
    def _place_object(self, source_objects, all_vtx_positions, all_vtx_normals,
                      all_vtx_slopes, cluster_centers_indices, mesh_diagonal,
                      use_clustering, num_clusters, cluster_strength,
                      rx_range, ry_range, rz_range,
                      use_align, use_inst, use_proximity, min_dist,
                      max_retries, placed_positions, result_grp,
                      scale_min, scale_max, material_dict, use_uniform,
                      use_materials, scale_val, up_axis, grid, grid_size,
                      use_slope_filter, max_slope_angle, bbox_min, bbox_max):

        placed = False
        attempts = 0
        min_dist_sq = min_dist * min_dist

        if not all_vtx_positions or not source_objects:
            return False

        final_vtx_idx = None

        while not placed and attempts < max_retries:
            attempts += 1

            # ---- 1. Determine candidate vertex ----
            if use_clustering:
                if not cluster_centers_indices:
                    continue
                current_center_idx = random.choice(cluster_centers_indices)
                center_pos = all_vtx_positions[current_center_idx]

                # 1.0 = tight, 0.0 = spread
                spread_factor = 1.0 - cluster_strength
                max_spread_dist = spread_factor * mesh_diagonal
                max_spread_sq = max_spread_dist * max_spread_dist

                if cluster_strength == 1.0:
                    final_vtx_idx = current_center_idx
                else:
                    found_valid = False
                    search_attempts = 10 + int((1.0 - cluster_strength) * 30)
                    for _ in range(search_attempts):
                        candidate_idx = random.randint(0, len(all_vtx_positions) - 1)
                        candidate_pos = all_vtx_positions[candidate_idx]
                        dist_sq = self._calculate_distance_squared(candidate_pos, center_pos)
                        if dist_sq <= max_spread_sq:
                            final_vtx_idx = candidate_idx
                            found_valid = True
                            break
                    if not found_valid:
                        final_vtx_idx = current_center_idx
            else:
                final_vtx_idx = random.randint(0, len(all_vtx_positions) - 1)

            if final_vtx_idx is None or final_vtx_idx >= len(all_vtx_positions):
                continue

            # ---- 2. Slope filter ----
            if use_slope_filter:
                if all_vtx_slopes[final_vtx_idx] > max_slope_angle:
                    continue

            base_pos = all_vtx_positions[final_vtx_idx]

            # ---- 3. Boundary safety ----
            if not self._is_within_bounds(base_pos, bbox_min, bbox_max):
                continue

            n_x, n_y, n_z = all_vtx_normals[final_vtx_idx]
            final_pos = list(base_pos)

            # ---- 4. Proximity check ----
            if use_proximity:
                if self._check_proximity_optimized(final_pos, placed_positions,
                                                   min_dist, grid, grid_size, min_dist_sq):
                    placed = True
                else:
                    continue
            else:
                placed = True

            if placed:
                source_pick = random.choice(source_objects)

                if use_inst and not use_materials:
                    new_item = cmds.instance(source_pick)[0]
                else:
                    new_item = cmds.duplicate(source_pick)[0]

                cmds.xform(new_item, translation=(0, 0, 0),
                           rotation=(0, 0, 0), scale=(1, 1, 1), worldSpace=False)

                cmds.parent(new_item, result_grp)
                cmds.xform(new_item, translation=final_pos, worldSpace=True)

                # Rotation
                if use_align:
                    rot_x, rot_y, rot_z = self._compute_rotation_from_normal(
                        n_x, n_y, n_z, rx_range, ry_range, rz_range, up_axis
                    )
                    cmds.xform(new_item, rotation=(rot_x, rot_y, rot_z), worldSpace=True)
                else:
                    rx = random.uniform(-(rx_range/2), rx_range/2)
                    ry = random.uniform(-(ry_range/2), ry_range/2)
                    rz = random.uniform(-(rz_range/2), rz_range/2)
                    cmds.xform(new_item, rotation=(rx, ry, rz), worldSpace=True)

                # Scale
                if use_uniform:
                    s = scale_val
                else:
                    s = random.uniform(scale_min, scale_max)
                cmds.scale(s, s, s, new_item)

                # Material
                if use_materials and source_pick in material_dict:
                    mat_info = material_dict[source_pick]
                    try:
                        cmds.sets(new_item, e=True, forceElement=mat_info['shading_group'])
                    except:
                        pass

                self._add_to_spatial_grid(final_pos, grid, grid_size)
                placed_positions.append(final_pos)
                return True

        return False

    # ------------------------------------------------------------------
    #  ROTATION FROM NORMAL (OpenMaya quaternion)
    # ------------------------------------------------------------------
    def _compute_rotation_from_normal(self, n_x, n_y, n_z, rx_range, ry_range, rz_range, up_axis):
        length = math.sqrt(n_x*n_x + n_y*n_y + n_z*n_z)
        if length > 0:
            n_x /= length
            n_y /= length
            n_z /= length

        if HAS_OPENMAYA:
            try:
                if up_axis == 1:
                    up_vector = om.MVector(0, 1, 0)
                else:
                    up_vector = om.MVector(0, 0, 1)

                normal_vector = om.MVector(n_x, n_y, n_z)

                if abs(normal_vector.x) + abs(normal_vector.y) + abs(normal_vector.z) < 1e-6:
                    return 0, 0, 0

                quat = up_vector.rotateTo(normal_vector)
                euler_rotation = quat.asEulerRotation()

                rot_x = math.degrees(euler_rotation.x)
                rot_y = math.degrees(euler_rotation.y)
                rot_z = math.degrees(euler_rotation.z)

                rot_x += random.uniform(-(rx_range/2), rx_range/2)
                rot_y += random.uniform(-(ry_range/2), ry_range/2)
                rot_z += random.uniform(-(rz_range/2), rz_range/2)

                return rot_x, rot_y, rot_z
            except:
                pass

        rot_x = random.uniform(-(rx_range/2), rx_range/2)
        rot_y = random.uniform(-(ry_range/2), ry_range/2)
        rot_z = random.uniform(-(rz_range/2), rz_range/2)
        return rot_x, rot_y, rot_z

    # ------------------------------------------------------------------
    #  SPATIAL GRID PROXIMITY
    # ------------------------------------------------------------------
    def _calculate_distance_squared(self, pos1, pos2):
        dx = pos1[0] - pos2[0]
        dy = pos1[1] - pos2[1]
        dz = pos1[2] - pos2[2]
        return dx*dx + dy*dy + dz*dz

    def _check_proximity_optimized(self, new_pos, existing_positions, min_dist,
                                   grid, grid_size, min_dist_sq):
        if not grid or grid_size <= 0:
            for existing_pos in existing_positions:
                dist_sq = self._calculate_distance_squared(new_pos, existing_pos)
                if dist_sq < min_dist_sq:
                    return False
            return True

        cell_x = int(math.floor(new_pos[0] / grid_size))
        cell_y = int(math.floor(new_pos[1] / grid_size))
        cell_z = int(math.floor(new_pos[2] / grid_size))

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
        if grid_size <= 0:
            return
        cell_x = int(math.floor(pos[0] / grid_size))
        cell_y = int(math.floor(pos[1] / grid_size))
        cell_z = int(math.floor(pos[2] / grid_size))
        cell_key = (cell_x, cell_y, cell_z)
        if cell_key not in grid:
            grid[cell_key] = []
        grid[cell_key].append(pos)

    # ------------------------------------------------------------------
    #  MATERIALS
    # ------------------------------------------------------------------
    def _create_unique_materials(self, source_objects):
        material_dict = {}
        colors = [
            [1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 0, 1],
            [0, 1, 1], [1, 0.5, 0], [0.5, 0, 0.5], [0.5, 0.5, 0], [0, 0.5, 0.5]
        ]

        for i, obj in enumerate(source_objects):
            if not cmds.objExists(obj):
                continue
            obj_name = cmds.ls(obj, long=True)[0].split("|")[-1]
            mat_name = "scatter_mat_{}_{}_{:.0f}".format(
                obj_name.replace(":", "_"), i, time.time()
            )
            color = colors[i % len(colors)]

            if not cmds.objExists(mat_name):
                material = cmds.shadingNode('blinn', asShader=True, name=mat_name)
                cmds.setAttr(material + ".color", color[0], color[1], color[2])
                cmds.setAttr(material + ".ambientColor", color[0], color[1], color[2])

                sg_name = mat_name + "SG"
                if not cmds.objExists(sg_name):
                    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=sg_name)
                    cmds.connectAttr(material + ".outColor", sg_name + ".surfaceShader")

                material_dict[obj] = {'material': material, 'shading_group': sg_name}
                self.created_materials.append(mat_name)
            else:
                material_dict[obj] = {'material': mat_name, 'shading_group': mat_name + "SG"}

        return material_dict

    def _cleanup_scatter_materials(self):
        try:
            for mat_name in self.created_materials:
                if cmds.objExists(mat_name):
                    sg_name = mat_name + "SG"
                    if cmds.objExists(sg_name):
                        cmds.delete(sg_name)
                    cmds.delete(mat_name)
        except:
            pass
        self.created_materials = []

    # ------------------------------------------------------------------
    #  ERROR
    # ------------------------------------------------------------------
    def _show_error(self, message):
        print("Simply Scatter Error:", message)
        cmds.warning(message)


# Run the tool
SimplyScatter()
