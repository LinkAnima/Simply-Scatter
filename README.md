# Simply Scatter User Guide
## A Complete Guide to Creating Beautiful, Boundary-Safe Scatters

Welcome to Simply Scatter – your powerful tool for creating realistic, boundary-safe object distributions on meshes! Whether you're scattering grass, rocks, plants, or any other objects, this guide will help you master every feature.

---

## 🎯 What is Simply Scatter?

Simply Scatter is a Maya plugin that scatters objects across a mesh surface with advanced control over distribution patterns, proximity avoidance, and visual quality. It's designed to be both powerful and user-friendly for artists working on complex scenes.

---

## 🛠️ Getting Started

### Installation
1. **Save the script** as `simply_scatter.py`
2. **Open Maya**
3. **In the Script Editor**, select "Python" as language
4. **Run this code:**
```python
import sys
sys.path.append('/path/to/your/script')
import simply_scatter
simply_scatter.SimplyScatter()
```

### Opening the Tool
- Go to `Window > Scripts > Python` in Maya
- Run the script above, or use the shelf button if you've added it

---

## 📦 Basic Workflow

### Step 1: Select Your Objects
1. **Select objects** you want to scatter (multiple objects supported)
2. **Select your target mesh last** (the one to scatter on)
3. **Example**: Select 5 different tree models, then select the terrain mesh

### Step 2: Configure Settings
Adjust parameters using the intuitive UI:
- **Scene Settings**: Choose Y-Up or Z-Up for object orientation
- **Scatter Parameters**: Set count and base scale
- **Clustering Zones**: Group similar scatter locations together
- **Virtual Subdivision**: Control how objects spread from vertices
- **Rotation Variance**: Add natural randomness to rotations
- **Proximity Detection**: Prevent overlapping objects

### Step 3: Run Scatter
Click the "RUN SCATTER" button and watch your objects appear!

---

## 🎛️ Detailed Feature Guide

### Scene Settings
**Object Up Axis**
- Choose Y-Up or Z-Up based on your object orientation
- This affects how scattered objects are aligned to the mesh surface

### Scatter Parameters
**Object Count**
- Controls how many objects will be scattered
- Range: 1-5000 objects (default: 100)

**Base Scale**
- Sets the default size of all scattered objects
- Range: 0.01-20 units (default: 1.0)

**Use Uniform Scale**
- If checked, all objects get the same scale
- If unchecked, each gets a random scale between 0.5x and 1.5x

### Clustering Zones
**Enable Clustering**
- Creates groups of nearby objects for natural-looking distribution

**Number of Clusters**
- How many distinct grouping areas to create (default: 10)

**Cluster Strength**
- Controls how tightly clustered objects are:
  - 0.0 = evenly spread across mesh
  - 1.0 = all objects near cluster centers

### Virtual Subdivision (Boundary Safe)
**Enable Virtual Subdivision**
- Adds extra randomness to prevent objects from sitting exactly on vertices

**Subdivision Method**
- **Tangent Fit**: Objects move along surface tangent plane
- **Edge Sampling**: Objects sample from connected mesh edges for better locality

**Spread Intensity (0-10)**
- Controls how far objects can spread from original vertex:
  - 0 = no spread
  - 10 = maximum spread (up to 0.25 units)

### Rotation Variance
Add natural randomness to object rotations:

**X Tilt Randomness**: How much objects tilt side-to-side (0-360°)
**Y Twist Randomness**: How much objects twist around their axis (0-360°)  
**Z Tilt Randomness**: How much objects tilt forward/backward (0-360°)

### Proximity Detection
Prevent scattered objects from overlapping:

**Enable Collision Avoidance**
- If checked, objects won't overlap

**Min Distance**
- Minimum distance between objects (default: 1.0)
- Smaller values = more dense, more collisions

**Max Retries per Obj**
- How many attempts to place each object before giving up
- Higher = better placement quality, slower execution

### Advanced Features
**Align to Surface Normal**
- Objects align with mesh surface normals (default: ON)

**Use Instancing (Faster)**
- Creates faster duplicates for large counts (default: ON)

---

## 🎨 Best Practices for Professional Results

### For Realistic Natural Scattering:
1. **Start with 50-200 objects** for small areas
2. **Set Cluster Strength to 0.3-0.5** for natural grouping
3. **Use Spread Intensity of 3-5** for subtle variation
4. **Enable Proximity Detection** with Min Distance of 0.5-1.0

### For Dense Scattering:
1. **Use Count of 1000+** for large areas
2. **Set Cluster Strength to 0.1-0.2** for even distribution
3. **Use Spread Intensity of 1-3** to prevent clumping
4. **Disable Proximity Detection** for performance (if acceptable)

### For Specific Effects:
**Grass Scattering:**
- Count: 500-2000
- Cluster Strength: 0.1-0.2
- Spread Intensity: 2-3
- Min Distance: 0.2-0.5

**Rock Scattering:**
- Count: 200-800
- Cluster Strength: 0.4-0.6
- Spread Intensity: 4-7
- Min Distance: 0.5-1.0

**Plant Scattering:**
- Count: 100-500
- Cluster Strength: 0.3-0.5
- Spread Intensity: 3-5
- Min Distance: 0.8-1.5

---

## ⚡ Performance Tips

### For Large Scenes:
1. **Use Instancing** - Much faster for high counts
2. **Reduce Proximity Detection** - Turn off for very large scenes (but may cause overlaps)
3. **Lower Spread Intensity** - Reduces computational overhead
4. **Use fewer Clusters** - More clusters = more processing time

### For Quick Previews:
1. **Set Count to 50-100** for testing
2. **Disable Proximity Detection**
3. **Use Lower Spread Intensity**
4. **Test with a small subset of your objects**

---

## 🔧 Troubleshooting Common Issues

### "Selection Error: Select objects to scatter, then the Target Mesh LAST"
Make sure:
- You have at least 2 selected objects
- The mesh is selected last in the list

### Objects are overlapping or too close together
Try:
- Increasing Min Distance value
- Enabling Proximity Detection
- Reducing Cluster Strength

### Tool is running very slowly
Try:
- Turning off Proximity Detection for large counts
- Using fewer objects
- Reducing Spread Intensity

### Materials not applying properly
Check:
- Make sure "Assign Unique Materials to Object Types" is enabled
- Verify that your source objects have materials
- Ensure you're using compatible object types

---

## 📈 Advanced Techniques

### Creating Natural Groupings:
1. **Use Cluster Strength of 0.4-0.6**
2. **Set Number of Clusters to 5-15** 
3. **Enable Virtual Subdivision** with Spread Intensity of 3-5
4. This creates natural-looking clusters like nature does

### Scattering on Complex Meshes:
1. **Start with low count** (50-100) for testing
2. **Use smaller Min Distance** (0.2-0.5)
3. **Enable Proximity Detection**
4. **Test with one object type first**

### Optimizing Large Scenes:
1. **Create multiple scatter passes** with different settings
2. **Use instance groups** for similar objects
3. **Apply different material types** to reduce memory usage

---

## 🎨 Tips for Professional Results

### For Maximum Realism:
- **Combine multiple scatter passes**: Use different settings to create depth and variety
- **Vary object scales**: Use uniform scale off for natural look
- **Use different object types**: Mix similar but distinct objects
- **Adjust rotation variance**: Add subtle randomness for organic feel

### For Efficient Workflow:
- **Save your favorite settings** in the UI
- **Use presets** for common scattering tasks (grass, rocks, plants)
- **Test with low counts first** before running full scene
- **Use undo/redo** to fine-tune results

---

## 🧠 Pro Tips from Industry Artists

### Real-World Usage:
- **Grass**: 1000+ objects, low cluster strength, small spread
- **Rocks**: 500-1000 objects, high cluster strength, moderate spread  
- **Trees**: 50-200 objects, high cluster strength, large spread
- **Foliage**: 2000+ objects, low cluster strength, small spread

### Quality vs Performance:
- **Quality Mode**: Enable proximity detection, use high counts
- **Speed Mode**: Disable proximity, reduce count, use fewer clusters
- **Balance**: Find your sweet spot based on scene complexity

### Workflow Optimization:
1. **Start with a simple test run** (50 objects)
2. **Adjust settings incrementally**
3. **Use the preview effect to check results**
4. **Iterate until you get desired look**

---

## 📝 Final Notes

Simply Scatter is designed to handle everything from small-scale detail work to large production environments. The key to success is understanding how each parameter affects your final result.

**Remember**: 
- Small changes in parameters can create dramatically different results
- Always test with a few objects first
- Use the undo feature to experiment safely
- Don't be afraid to combine multiple scatter passes for complex effects

Happy scattering! 🌿
