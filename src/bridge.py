import json
import os

def build_anim_input(known, physics_result, visual_hooks, output_file="anim_input.json"):
    anim_data = {
        "motion_type": physics_result.get("motion_type"),
        "parameters": known,
        "hasil_fisika": physics_result.get("hasil"),
        "vectors_to_render": visual_hooks.get("vectors_template", [])
    }
    with open(output_file, "w") as f:
        json.dump(anim_data, f, indent=4)
    print(f"[+] anim_input.json ditulis.")
    return anim_data

if __name__ == "__main__":
    known = {"massa": 4, "sudut_permukaan": 30}
    physics = {"motion_type": "static_incline", "hasil": {"percepatan": 5.0}}
    visual = {"vectors_template": []}
    build_anim_input(known, physics, visual)
