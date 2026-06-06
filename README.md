# Simply Scatter User Guide

## What is Simply Scatter?

Simply Scatter is a powerful Maya tool that helps you quickly scatter objects across any mesh surface with realistic placement, scaling, and positioning. Whether you're creating forests of trees, crowds of people, or intricate patterns on surfaces, this tool makes it easy and fast.

## Getting Started

### Installation
1. Copy the entire Python script into Maya's Script Editor
2. Click "Run" to execute the code
3. The Simply Scatter window will appear in Maya

### Basic Workflow
1. **Select your objects** - Choose what you want to scatter (multiple objects work!)
2. **Select your target mesh** - This should be the last item selected
3. **Adjust settings** - Customize how the scattering behaves
4. **Click "RUN SCATTER"** - Watch the magic happen!

## Understanding the Controls

### Scene Settings
- **Object Up Axis**: Choose whether your objects should point up in Y or Z direction
- *Tip: Usually Y-Up works best for most cases*

### Scaling Customization (NEW!)
- **Min Scale Factor**: Set the smallest size your scattered objects can be
- **Max Scale Factor**: Set the largest size your scattered objects can be
- *Example: Min=0.5, Max=2.0 = Objects range from 50% to 200% of original size*

### Scatter Parameters
- **Object Count**: How many objects to scatter (1-5000)
- **Base Scale**: The default scale for all objects
- **Use Uniform Scale**: When checked, all objects use the same scale; when unchecked, random variation

### Clustering Zones
- **Enable Clustering**: Group scattered objects into clusters instead of random distribution
- **Number of Clusters**: How many groups to create
- **Cluster Strength**: How tight the clustering is (0 = no clustering, 1 = very tight)

### Virtual Subdivision (Boundary Safe)
This is where the magic happens! It prevents objects from being placed too close to each other.

- **Enable Tangent Fit**: Adds variation within the tangent plane of the surface
- **Spread Intensity**: How much spread you want (0-10 scale)
- *Higher values create more spread, but never go beyond the mesh surface*

### Rotation Variance
Control how much random rotation your scattered objects get:

- **X Tilt Randomness**: Rotation around the X axis
- **Y Twist Randomness**: Rotation around the Y axis  
- **Z Tilt Randomness**: Rotation around the Z axis

### Proximity Detection
Prevents objects from overlapping or getting too close to each other:

- **Enable Collision Avoidance**: Turn on/off proximity checking
- **Min Distance**: How close objects can get to each other
- **Max Retries per Obj**: How many times to try placing an object before giving up

### Advanced Features
- **Align to Surface Normal**: Objects will point toward the surface they're placed on
- **Use Instancing (Faster)**: Creates faster results when using many objects

## Best Practices for Great Results

### 1. Start Simple
Begin with basic settings and gradually add complexity:
- Start with Count = 50, no clustering
- Try different spread intensities
- Enable proximity detection once you're happy with placement

### 2. Scaling Tips
- **For realistic forests**: Use Min=0.3, Max=1.2 to create natural size variation
- **For crowds**: Use Min=0.8, Max=1.5 for subtle differences
- **For decorative patterns**: Use Min=0.1, Max=3.0 for dramatic variation

### 3. Clustered Scattering
Great for:
- Creating realistic forests with trees grouped together
- Making crowds look more natural
- Building organic patterns

**Pro tip**: For clustered results, try Cluster Strength = 0.3-0.5 with many clusters (20-50)

### 4. Proximity Settings
- **Small objects**: Use Min Distance = 0.5-1.0
- **Large objects**: Use Min Distance = 2.0-5.0
- **Very tight spaces**: Increase Max Retries to 50-100

### 5. Surface Quality Matters
- **Smooth surfaces** work best for natural-looking results
- **High-resolution meshes** give better placement accuracy
- **Avoid very sharp edges** for cleaner scattering

## Common Use Cases

### Forest Creation
```
Object Count: 200-1000
Cluster Strength: 0.2-0.4
Spread Intensity: 3-6
Min Distance: 1.5-2.0
Use Uniform Scale: Unchecked
Scale Range: Min=0.3, Max=1.5
```

### Crowd Simulation
```
Object Count: 50-200  
Cluster Strength: 0.1-0.3
Spread Intensity: 2-4
Min Distance: 1.0-1.5
Use Uniform Scale: Unchecked
Scale Range: Min=0.8, Max=1.2
```

### Decorative Patterns
```
Object Count: 100-500
Cluster Strength: 0.0 (no clustering)
Spread Intensity: 8-10
Min Distance: 0.5-1.0
Use Uniform Scale: Unchecked
Scale Range: Min=0.1, Max=3.0
```

## Troubleshooting

### Objects Not Placing?
1. **Check selection**: Make sure you have at least 2 items selected (objects + target mesh)
2. **Target mesh**: Ensure your last item is a valid mesh with vertices
3. **Count too high**: Try reducing the object count to 100-500

### Too Many Objects Failed?
1. **Reduce Min Distance**: Increase this value if objects are fighting for space
2. **Increase Max Retries**: Allow more attempts per object (default is 20)
3. **Try clustering**: This helps distribute objects more evenly

### Performance Issues?
1. **Reduce Count**: Start with 50-100 objects and increase gradually
2. **Disable Instancing**: Uncheck "Use Instancing" for better performance
3. **Lower Resolution**: Use lower-polygon meshes for target surfaces

## Advanced Tips

### Combining Techniques
- **Small clusters + large spread**: Great for scattered but grouped patterns
- **High uniformity + tight proximity**: Perfect for precise, evenly spaced results
- **Low clustering + wide scale range**: Creates natural variation in both position and size

### Workflow Optimization
1. **Save your settings**: Adjust once, then copy-paste the UI values for consistency
2. **Use different target meshes**: Try multiple surfaces to see how they affect results
3. **Experiment with rotation**: Small tweaks can dramatically change the look

### Integration Tips
- **Combine with other tools**: Use Simply Scatter as a starting point, then manually adjust
- **Batch processing**: Create multiple versions with different settings for comparison
- **Animation**: Animate your target mesh to create dynamic scattering effects

## What's New in This Version?

### Major Updates:
- **Custom Scaling Range**: Set exactly what size range you want (not just 50%-150%)
- **Repositioned UI**: Scaling controls now appear second in the interface for better workflow
- **Improved Performance**: Faster calculations and better error handling

### Why Use Simply Scatter?
- **Easy to use** - No complex setup required
- **Powerful results** - Professional-quality scattering with minimal effort
- **Flexible settings** - Tons of options to customize exactly how you want your objects scattered
- **Fast execution** - Handles thousands of objects efficiently

## Getting Help

If you're having trouble:
1. Check the Maya Script Editor for error messages
2. Start with simple settings and add complexity gradually
3. Consult the help text in each control for specific guidance
4. Try the sample configurations above for your use case

Happy scattering! 🎯