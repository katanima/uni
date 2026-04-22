extends PathFollow3D

@export var rail_speed: float = 0.02
@export var max_speed: float = 0.1

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	if rail_speed < max_speed:
		rail_speed += delta
	
	progress_ratio += rail_speed * delta
	pass
