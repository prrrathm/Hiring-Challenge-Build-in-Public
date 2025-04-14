<template>
	<div class="container">
		<canvas ref="canvas" width="800" height="600"></canvas>
	</div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import * as Matter from 'matter-js';

const { Engine, Render, Runner, Bodies, Composite, Body, Events, Constraint } = Matter;

const canvas = ref(null);
const engine = ref(null);
const render = ref(null);
const runner = ref(null);

// Scale components
const pivot = ref(null);
const beam = ref(null);
const leftPan = ref(null);
const rightPan = ref(null);
const leftChain = ref(null);
const rightChain = ref(null);

// Trackers
const objectsOnLeft = ref([]);
const objectsOnRight = ref([]);
const leftWeight = ref(0);
const rightWeight = ref(0);

// Scale properties
const beamLength = 400;
const beamHeight = 20;
const pivotY = 200;
const panRadius = 100;
const panHeight = 20;
const chainLength = 150;


function initPhysics() {
	engine.value = Engine.create({
		gravity: {
			x: 0,
			y: 0.5
		}
	});
	render.value = Render.create({
		canvas: canvas.value,
		engine: engine.value,
		options: {
			width: 800,
			height: 600,
			wireframes: false,
			background: '#f4f4f8'
		}
	});

	runner.value = Runner.create();

	pivot.value = Bodies.circle(400, pivotY, 10, {
		isStatic: true,
		render: {
			fillStyle: '#333333'
		}
	});

	beam.value = Bodies.rectangle(400, pivotY + 20, beamLength, beamHeight, {
		render: {
			fillStyle: '#8B4513' // Brown wooden beam
		},
		frictionAir: 0.1
	});

	const pivotJoint = Constraint.create({
		bodyA: pivot.value,
		bodyB: beam.value,
		pointA: { x: 0, y: 0 },
		pointB: { x: 0, y: -20 },
		length: 0,
		stiffness: 0.9,
		render: {
			visible: true,
			lineWidth: 2,
			strokeStyle: '#666'
		}
	});

	// leftPan.value = Bodies.circle(400 - beamLength / 3, pivotY + chainLength, panRadius, {
	// 	render: {
	// 		fillStyle: '#C0C0C0' // Silver pan
	// 	},
	// 	chamfer: { radius: 10 },
	// 	frictionAir: 0.02
	// });
	leftPan.value = Bodies.rectangle(400 - beamLength / 3, pivotY + chainLength, panRadius * 2, panHeight, {
		render: {
			fillStyle: '#C0C0C0' // Silver pan
		},
		chamfer: { radius: 4 },
		frictionAir: 0.02
	});
	rightPan.value = Bodies.rectangle(400 - beamLength / 3, pivotY + chainLength, panRadius * 2, panHeight, {
		render: {
			fillStyle: '#C0C0C0' // Silver pan
		},
		chamfer: { radius: 4 },
		frictionAir: 0.02
	});

	// Prevent pans from rotating
	Body.setInertia(leftPan.value, Infinity);
	Body.setInertia(rightPan.value, Infinity);

	leftChain.value = Constraint.create({
		bodyA: beam.value,
		bodyB: leftPan.value,
		pointA: { x: -beamLength / 3, y: 0 },
		pointB: { x: 0, y: -panHeight / 2 },
		length: chainLength - 20,
		stiffness: 0.9,
		render: {
			visible: true,
			lineWidth: 2,
			strokeStyle: '#999'
		}
	});
	rightChain.value = Constraint.create({
		bodyA: beam.value,
		bodyB: rightPan.value,
		pointA: { x: beamLength / 3, y: 0 },
		pointB: { x: 0, y: -panHeight },
		length: chainLength - 20,
		render: {
			visible: true,
			lineWidth: 2,
			strokeStyle: '#999'
		}
	});

	const wallOptions = {
		isStatic: true,
		render: {
			fillStyle: 'transparent'
		}
	};

	const walls = [
		// Floor
		Bodies.rectangle(400, 610, 810, 60, wallOptions),
		// Left wall
		Bodies.rectangle(-10, 300, 60, 600, wallOptions),
		// Right wall
		Bodies.rectangle(810, 300, 60, 600, wallOptions),
		// Ceiling
		Bodies.rectangle(400, -10, 810, 60, wallOptions)
	];

	// Add all objects to the world
	Composite.add(engine.value.world, [
		pivot.value,
		beam.value,
		pivotJoint,
		leftPan.value,
		rightPan.value,
		leftChain.value,
		rightChain.value,
		...walls
	]);

	// Run the engine and renderer
	Render.run(render.value);
	Runner.run(runner.value, engine.value);

	// Track weights and update
	Events.on(engine.value, 'afterUpdate', () => {
		// Calculate total weights on each pan
		updateWeights();
	});
}

function updateWeights() {
	// Sum up masses on left pan
	leftWeight.value = objectsOnLeft.value.reduce((sum, obj) => sum + obj.mass, 0);

	// Sum up masses on right pan
	rightWeight.value = objectsOnRight.value.reduce((sum, obj) => sum + obj.mass, 0);
}

function addObject(side, weight) {
	const size = 20 + (weight * 5); // Size varies with weight
	const options = {
		mass: weight,
		restitution: 0.3,
		friction: 0.8,
		frictionAir: 0.02,
		render: {
			fillStyle: getColorForWeight(weight)
		}
	};

	let x, y;
	// Position based on which pan
	if (side === 'left') {
		x = leftPan.value.position.x + (Math.random() * 50 - 25);
		y = leftPan.value.position.y - 100;
	} else {
		x = rightPan.value.position.x + (Math.random() * 50 - 25);
		y = rightPan.value.position.y - 100;
	}

	// Create different shapes based on weight
	let object;
	if (weight === 1) {
		// Small cube for 1kg
		object = Bodies.rectangle(x, y, size, size, options);
	} else if (weight === 2) {
		// Hexagon for 2kg
		object = Bodies.polygon(x, y, 6, size / 1.5, options);
	} else {
		// Octagon for 5kg
		object = Bodies.polygon(x, y, 8, size / 1.8, options);
	}

	// Add to world and tracking arrays
	Composite.add(engine.value.world, object);
	if (side === 'left') {
		objectsOnLeft.value.push(object);
	} else {
		objectsOnRight.value.push(object);
	}
}

function getColorForWeight(weight) {
	switch (weight) {
		case 1: return '#3498db'; // Blue for 1kg
		case 2: return '#2ecc71'; // Green for 2kg
		case 5: return '#e74c3c'; // Red for 5kg
		default: return '#95a5a6';
	}
}

onMounted(() => {
	initPhysics();
	addObject('right', 1)
	addObject('left', 1)
	addObject('right', 1)
});

onUnmounted(() => {
	// Clean up Matter.js resources
	if (runner.value) Runner.stop(runner.value);
	if (render.value) Render.stop(render.value);
	engine.value = null;
});
</script>

<style scoped>
.container {
	display: flex;
	flex-direction: column;
	align-items: center;
	font-family: Arial, sans-serif;
}

.controls {
	width: 800px;
	padding: 20px;
	background: #fff;
	border-radius: 8px;
	margin-bottom: 20px;
	box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h1 {
	text-align: center;
	color: #2c3e50;
	margin-top: 0;
}

h3 {
	margin-top: 0;
	color: #34495e;
}

.weight-display {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin: 20px 0;
	padding: 10px;
	background: #f8f9fa;
	border-radius: 8px;
	border: 1px solid #ddd;
}

.left-weight,
.right-weight {
	font-size: 18px;
	font-weight: bold;
	padding: 10px;
	width: 100px;
	text-align: center;
}

.balance-indicator {
	flex-grow: 1;
	text-align: center;
	font-size: 20px;
	font-weight: bold;
}

.actions {
	display: flex;
	justify-content: space-between;
	margin-bottom: 20px;
}

.left-controls,
.right-controls {
	flex: 1;
	display: flex;
	flex-direction: column;
	gap: 10px;
	padding: 15px;
	background: #f8f9fa;
	border-radius: 8px;
	margin: 0 10px;
	align-items: center;
}

button {
	background-color: #4a90e2;
	color: white;
	border: none;
	padding: 8px 12px;
	border-radius: 4px;
	cursor: pointer;
	font-size: 14px;
	transition: background-color 0.3s;
	width: 80px;
}

button:hover {
	background-color: #3a7bc8;
}

button:active {
	transform: translateY(1px);
}

.reset-button {
	width: auto;
	padding: 10px 20px;
	background-color: #e74c3c;
	margin: 0 auto;
	display: block;
}

.reset-button:hover {
	background-color: #c0392b;
}

canvas {
	border: 1px solid #ddd;
	border-radius: 4px;
	background: #f4f4f8;
}
</style>