import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useNotificationStore = defineStore('notificationStore', () => {
	// state: () => ({
	// 	notifications: [],
	// }),
	// actions: {
	// 	addNotification(message) {
	// 		this.notifications.push(message)
	// 	},
	// },
	const notifications = ref<string[]>([])
	const addNotification = (val: string) => {
		if (notifications.value) {
			notifications.value = [...notifications.value, val]
		}
	}
	return { notifications, addNotification }
})
