extends MeshInstance3D

@export var speed: float = 3
@export var LIMIT_X: int = 2
@export var LIMIT_Y: int = 2

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	var inputs = Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
	
	position.x += inputs.x * speed * delta
	position.y += inputs.y * speed * delta
	
	position.x = clamp(position.x, -LIMIT_X, LIMIT_X)
	position.y = clamp(position.y, -LIMIT_Y, LIMIT_Y)
	pass
