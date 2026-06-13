import bpy
import random

CZESTOTLIWOSC_MIGOTANIA = 6
MIN_EMISSION = 1.0
MAX_EMISSION = 25.0
SZANSA_BLYSKU = 0.2

obj = bpy.context.active_object

bsdf = mat.node_tree.nodes.get("Principled BSDF")

scene = bpy.context.scene

for frame in range(
        scene.frame_start,
        scene.frame_end,
        CZESTOTLIWOSC_MIGOTANIA):

    scene.frame_set(frame)

    if random.random() < SZANSA_BLYSKU:
        strength = random.uniform(
            MAX_EMISSION * 0.7,
            MAX_EMISSION
        )
    else:
        strength = random.uniform(
            MIN_EMISSION,
            MAX_EMISSION * 0.4
        )

    bsdf.inputs["Emission Strength"].default_value = strength

    bsdf.inputs["Emission Strength"].keyframe_insert(
        data_path="default_value",
        frame=frame
    )