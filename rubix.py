from ursina import *

# Initialize the Ursina app
app = Ursina()
window.title = "3D Rubik's Cube"
window.borderless = False

# We will store all 27 little cubes (sub-cubes) in a list
cubes = []

# Generate the 3x3x3 grid of sub-cubes
for x in range(-1, 2):
    for y in range(-1, 2):
        for z in range(-1, 2):
            # Create a simple cube entity. 
            # We use 'white_cube' texture which has black borders so we can see the grid.
            sub_cube = Entity(
                model='cube',
                position=(x, y, z),
                texture='white_cube', 
                color=color.hsv(0, 0, random.uniform(0.9, 1)) # Slight color variation for depth
            )
            cubes.append(sub_cube)

# A pivot point located in the dead center of the cube (0,0,0).
# We will temporarily attach sub-cubes to this pivot to rotate them together.
pivot = Entity()

# State variable to prevent overlapping animations
is_animating = False

def input(key):
    global is_animating
    if is_animating:
        return

    # Map keys to face rotations (Left, Right, Up, Down, Front, Back)
    if key == 'l':
        rotate_face('x', -1, 1)
    elif key == 'r':
        rotate_face('x', 1, -1)
    elif key == 'u':
        rotate_face('y', 1, 1)
    elif key == 'd':
        rotate_face('y', -1, -1)
    elif key == 'f':
        rotate_face('z', -1, 1)
    elif key == 'b':
        rotate_face('z', 1, -1)

def rotate_face(axis, slice_val, direction):
    global is_animating
    is_animating = True

    # 1. Find all sub-cubes that belong to the face we want to rotate
    for b in cubes:
        # Check the position of the cube on the specified axis (x, y, or z)
        if getattr(b.position, axis) == slice_val:
            # Parent the cube to the central pivot
            b.parent = pivot

    # 2. Animate the rotation of the pivot by 90 degrees
    rotation_amount = 90 * direction
    if axis == 'x':
        pivot.animate_rotation_x(pivot.rotation_x + rotation_amount, duration=0.3)
    elif axis == 'y':
        pivot.animate_rotation_y(pivot.rotation_y + rotation_amount, duration=0.3)
    elif axis == 'z':
        pivot.animate_rotation_z(pivot.rotation_z + rotation_amount, duration=0.3)

    # 3. Wait for the animation to finish, then decouple the cubes
    invoke(reset_pivot, delay=0.35)

def reset_pivot():
    global is_animating
    for b in cubes:
        if b.parent == pivot:
            # Save the new world position and rotation
            world_pos, world_rot = b.world_position, b.world_rotation
            
            # Detach from the pivot and attach back to the main scene
            b.parent = scene
            
            # Round positions to avoid floating point inaccuracies over many rotations
            b.position = (round(world_pos.x), round(world_pos.y), round(world_pos.z))
            b.rotation = world_rot

    # Reset the pivot's rotation back to zero for the next move
    pivot.rotation = (0, 0, 0)
    is_animating = False

# Adds a free-look camera. Right-click and drag to look around.
EditorCamera()

# Start the engine
app.run()
