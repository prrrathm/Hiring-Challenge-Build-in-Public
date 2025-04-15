import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useGameStore = defineStore('notificationStore', () => {
	// state: () => ({
	// 	notifications: [],
	// }),
	// actions: {
	// 	addNotification(message) {
	// 		this.notifications.push(message)
	// 	},
	// },
	const leftWeights = ref<number[]>([])
	const rightWeights = ref<number[]>([])
	const userAnswer = ref<number | null>(null)

	const setWeights = (arr1: number[], arr2: number[]) => {
		leftWeights.value = arr1
		rightWeights.value = arr2
	}
	const setUserAnswer = (value: number | null) => {
		userAnswer.value = value
	}
	return { leftWeights, rightWeights, userAnswer, setWeights, setUserAnswer }
})
