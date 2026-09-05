# Simply Scatter: User Guide & Best Practices

**Simply Scatter** is a fast, robust tool for scattering objects across a mesh in Maya. It replaces older, slower scripts by using modern Maya APIs (OpenMaya) for speed and a "Virtual Subdivision" logic to get high-density scatter without exploding your scene with actual geometry.

This guide explains how to use the tool, what each setting does, and how to get the best results.

---

## 1. How to Use (The Workflow)

Using Simply Scatter is a three-step process: **Select**, **Configure**, **Run**.

### Step 1: Selection Order Matters
You must select the objects you want to scatter and the surface they will land on.
1.  Select the **Target Mesh** (the surface, e.g., a rock, a wall, the ground) **LAST**.
2.  Select the **Source Objects** (the items to scatter, e.g., grass, rocks, debris) **FIRST**.
3.  *Why this order?* The tool always assumes the **last selected object** is the surface. Everything else selected is treated as a "scatterer."

> **Tip:** You can select multiple source objects! The tool will randomly pick from your selection for each placed item.

### Step 2: Configure the Settings
Open the **Simply Scatter** window. Read through the sections below to choose your settings.

### Step 3: Run
Click the green **RUN SCATTER** button.
*   You will see a progress bar.
*   The tool will create a new group named `SimplyScatter_Result_GRP_XXXX`.
*   *Note:* If the mesh is large, the "Subdivision" phase may take a moment.

---

## 2. Understanding the Settings

### 🟢 Mesh Preparation
*This section prepares the surface. It creates a hidden, temporary copy of your target mesh to calculate placement.*

*   **Subdivision Levels (0-8):**
    *   **0:** Uses your mesh as-is. Good for simple, low-poly meshes.
    *   **1-2:** Adds smoothness/density. Recommended for most organic shapes.
    *   **3+:** Very high density. Use only if you need scatter on very detailed or smooth curved surfaces (like a sphere or brain).
*   **Keep Sharp Edges vs. Apply Smoothing:**
    *   **Keep Sharp Edges (Default):** Preserves the original silhouette of your mesh. The scatter will land exactly on the original hard edges.
    *   **Apply Smoothing:** Softens the mesh. Use this if you want scatter to land on a "smoothed" version of the surface (e.g., making a box look round for scatter).
*   **Keep Subdivided Target:**
    *   **Unchecked (Default):** Deletes the temporary hidden mesh after scattering. Keeps your scene clean.
    *   **Checked:** Keeps the hidden mesh in the result group. Useful for debugging or if you want to re-use the subdivided surface later.

### 🟢 Scatter Parameters
*   **Object Count:** How many objects you want to place.
*   **Base Scale:** The default size of your objects.
*   **Use Uniform Scale:**
    *   **Checked:** All objects are exactly the same size (Base Scale).
    *   **Unchecked:** Objects vary in size between **Min** and **Max Scale Factor**.
    *   *Watch the "Current Range" text!* It updates in real-time as you drag the Min/Max sliders, showing you the percentage range (e.g., "50% to 150%").

### 🟢 Clustering Zones
*This creates the "organic" look, making objects gather in groups rather than scattering evenly.*

*   **Enable Clustering:** Turn this **ON** for a natural look.
*   **Number of Clusters (1-25):**
    *   **Low (1-5):** Creates a few large "islands" of scatter.
    *   **High (10-25):** Creates many small, tight groups.
    *   *Note:* Increasing this number makes the scatter look more "broken up."
*   **Tightness (0.0 - 1.0):**
    *   **0.0 (Fully Spread):** Objects can land anywhere on the mesh, even far from the cluster centers.
    *   **1.0 (Tight):** Objects are locked to the cluster centers.
    *   *Sweet Spot:* **0.7 - 0.9** usually looks most natural.

### 🟢 Slope Filtering
*Prevents objects from landing on steep or vertical surfaces.*

*   **Enable Slope Filter:** **ON** by default. This is highly recommended.
*   **Angle (0-90°):**
    *   The tool measures the angle of the surface normal relative to the Up Axis.
    *   **60° (Default):** Only places objects on surfaces facing "upward." Prevents grass from growing sideways on cliffs or walls.
    *   **90°:** Allows objects on vertical walls.
    *   **0°:** Only places objects on perfectly flat, upward-facing surfaces.

### 🟢 Rotation Variance
*Adds randomness to how the objects are oriented.*

*   **Align to Surface Normal:**
    *   **Checked (Recommended):** Objects stand upright relative to the surface slope. A rock on a hill will tilt to match the hill.
    *   **Unchecked:** Objects use random global rotation (they might look "floating" or tilted strangely).
*   **X/Y/Z Randomness:**
    *   Adds a "wobble" on top of the normal alignment.
    *   **Y Twist:** Usually set higher (e.g., 360) for a 360-degree spin.
    *   **X/Z Tilt:** Usually set lower (e.g., 10-30) to keep objects mostly upright but slightly tilted for realism.

### 🟢 Proximity Detection
*Prevents objects from overlapping each other.*

*   **Enable Collision Avoidance:** **ON** by default.
*   **Min Distance:** The minimum space between object centers.
    *   *Best Practice:* Set this to roughly **1x the size of your largest object**.
*   **Retries per Object (1-10):**
    *   If the tool tries to place an object in a spot that is too close to another, it retries up to this number of times.
    *   If it fails all retries, it skips that object (resulting in "failed" count).
    *   *Tip:* If you have many "failed" objects, increase **Min Distance** or decrease **Object Count**.

### 🟢 Advanced Features
*   **Use Instancing:**
    *   **ON (Default):** Uses Maya's instancing. This is **much faster** and uses less memory.
    *   **OFF:** Duplicates the actual geometry. Use this ONLY if you need to delete or edit individual scattered objects later.
*   **Assign Unique Materials:**
    *   If you selected **multiple different objects** (e.g., 3 types of grass), check this to assign a unique color to each type so you can tell them apart.

---

## 3. Best Practices & Troubleshooting

### 💡 How to get the "Natural" Look
1.  **Turn ON Clustering:** Never use 100% even scatter unless it's a specific stylistic choice. Clustering mimics nature.
2.  **Use Slope Filtering:** Keep the Angle at **60°** or **45°**. This prevents objects from "dangling" on cliff faces.
3.  **Vary the Scale:** Turn OFF "Use Uniform Scale" and set a range like **80% - 120%**. This adds visual variety.
4.  **Add Rotation Wobble:** Keep "Align to Normal" ON, but add a small **Y Twist (e.g., 360)** and a small **X/Z Tilt (e.g., 15°)**.

### ⚠️ Troubleshooting Common Issues

| Problem | Solution |
| :--- | :--- |
| **"Selection Error"** | Make sure the **Target Mesh** is the **LAST** thing you selected. |
| **Objects are "Floating"** | 1. Increase **Min Distance** in Proximity. <br> 2. Check **Slope Angle** (lower it to 30-45°). <br> 3. Ensure **Align to Normal** is ON. |
| **Many "Failed" Objects** | The tool tried to place objects but ran out of space. <br> 1. Increase **Min Distance**. <br> 2. Decrease **Object Count**. <br> 3. Increase **Retries per Object** (max 10). |
| **Scatter looks "Blocky"** | Increase **Subdivision Levels** to 2 or 3. This allows the tool to place objects on smoother curves. |
| **Scene is Slow** | Ensure **Use Instancing** is ON. If it’s still slow, check your viewport shading mode (use "Shaded" not "Material"). |
| **Objects look "Smoothed" too much** | If you used **Apply Smoothing**, try switching to **Keep Sharp Edges** and re-run. |

### 🚀 Performance Tips
*   **High Density?** Use **Subdivision Level 1 or 2**. Avoid 4+ unless necessary.
*   **Many Clusters?** Keep **Number of Clusters** under 25. Higher numbers slow down the placement phase.
*   **Complex Meshes?** The tool automatically subdivides a *temporary* copy. If your original mesh has 100k polygons, subdivision will take time. Keep your target mesh reasonably optimized (2k-10k polys is ideal).

---

## 4. Quick Start Cheat Sheet

For a **quick, natural grass/rock scatter**:

1.  **Select** your ground mesh last, grass objects first.
2.  **Mesh Prep:** Subd Level **1**, Keep Sharp Edges **ON**.
3.  **Scatter:** Count **500**, Uniform Scale **OFF**, Range **80%-120%**.
4.  **Clustering:** Enable **ON**, Clusters **15**, Tightness **0.85**.
5.  **Slope:** Enable **ON**, Angle **60°**.
6.  **Rotation:** Align **ON**, Y Twist **360**, X/Z Tilt **15**.
7.  **Proximity:** Min Dist **1.0**, Retries **10**.
8.  **Click RUN.**

Enjoy your scatter! 🌿🪨
