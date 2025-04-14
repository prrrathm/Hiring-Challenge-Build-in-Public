<template class="flex flex-col max-w-[100vh]">
	<!-- <GameView /> -->
	<Scale />
	<div class="container mx-auto max-w-lg p-6">
		<h1 class="text-3xl font-bold text-gray-800 mb-6 text-center">Array Sum Game</h1>
		<button @click="startGame" :disabled="isConnecting"
			class="w-full py-2 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed mb-4">
			{{ isConnecting ? 'Connecting...' : 'Start Game' }}
		</button>
		<div v-if="gameActive" class="game-area bg-gray-800 p-4 rounded-md mb-4">
			<p class="mb-2">
				Array 1: <span class="font-mono">{{ array1.join(', ') }}</span>
			</p>
			<p class="mb-4">
				Array 2: <span class="font-mono">{{ array2.join(', ') }}</span>
			</p>
			<div class="flex gap-2">
				<input v-model.number="userAnswer" type="number" placeholder="Enter number to add" min="0"
					class="flex-1 p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
					@keyup.enter="submitAnswer" />
				<button @click="submitAnswer" :disabled="userAnswer === null"
					class="py-2 px-4 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed">
					Submit Answer
				</button>
			</div>
		</div>
		<div class="messages bg-gray-800 p-4 rounded-md shadow">
			<p v-for="(message, index) in messages" :key="index" class="text-gray-700" :class="{
				'text-green-600': message.includes('Correct'),
				'text-red-600': message.includes('Wrong'),
				'text-blue-600': message.includes('Connected'),
				'text-gray-500': message.includes('Disconnected'),
			}">
				{{ message }}
			</p>
		</div>
	</div>
</template>

<script setup lang="ts">
import { ref, onUnmounted } from 'vue';
import {
	type ClientMessage,
	type ServerMessage,
	type ArraysMessage,
	type ResultMessage,
	type ErrorMessage,
} from './types';
// import GameView from './views/GameView.vue';
import Scale from './views/Scale.vue';

const array1 = ref<number[]>([]);
const array2 = ref<number[]>([]);
const userAnswer = ref<number | null>(null);
const messages = ref<string[]>([]);
const gameActive = ref<boolean>(false);
const isConnecting = ref<boolean>(false);
let ws: WebSocket | null = null;

const startGame = () => {
	// Reset state
	array1.value = [];
	array2.value = [];
	userAnswer.value = null;
	messages.value = [];
	gameActive.value = false;
	isConnecting.value = true;

	if (ws && ws.readyState !== WebSocket.CLOSED) {
		ws.close();
	}

	ws = new WebSocket('ws://localhost:8000/ws');

	ws.onopen = () => {
		messages.value.push('Connected to server');
		isConnecting.value = false;
		const message: ClientMessage = { type: 'start' };
		ws?.send(JSON.stringify(message));
	};

	ws.onmessage = (event: MessageEvent) => {
		const data: ServerMessage = JSON.parse(event.data);

		if (data.type === 'arrays') {
			const arrays = data as ArraysMessage;
			array1.value = arrays.array1;
			array2.value = arrays.array2;
			gameActive.value = true;
		} else if (data.type === 'result') {
			const result = data as ResultMessage;
			messages.value.push(result.message);
			if (result.correct) {
				gameActive.value = false;
				userAnswer.value = null;
			}
		} else if (data.type === 'error') {
			const error = data as ErrorMessage;
			messages.value.push(error.message);
		}
	};

	ws.onclose = () => {
		messages.value.push('Disconnected from server');
		isConnecting.value = false;
		gameActive.value = false;
		ws = null;
	};

	ws.onerror = () => {
		messages.value.push('Error connecting to server');
		isConnecting.value = false;
		gameActive.value = false;
	};
};

const submitAnswer = () => {
	if (ws && ws.readyState === WebSocket.OPEN && userAnswer.value !== null) {
		if (userAnswer.value >= 0) {
			const message: ClientMessage = {
				type: 'answer',
				answer: userAnswer.value,
			};
			ws.send(JSON.stringify(message));
			userAnswer.value = null;
		} else {
			messages.value.push('Please enter a non-negative number');
		}
	} else {
		messages.value.push('Not connected to server or no answer provided');
	}
};

onUnmounted(() => {
	if (ws && ws.readyState !== WebSocket.CLOSED) {
		ws.close()
	}
});
</script>
