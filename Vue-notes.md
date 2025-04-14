useState

const count = ref(0); // Primitive values
const state = reactive({ count: 0 }); // Objects
// Update values
count.value++; // For ref
state.count++; // For reactive


useEffect
<script setup>
import { watch, watchEffect, onMounted, onUnmounted } from 'vue';

// 1. Watchers (equivalent to useEffect with dependencies)
watch(dependencies, (newVal, oldVal) => {
  // Side effect
});

// 2. Immediate watcher (runs immediately + tracks dependencies)
watchEffect(() => {
  // Side effect
});

// 3. Lifecycle hooks
onMounted(() => { /* componentDidMount */ });
onUnmounted(() => { /* componentWillUnmount */ });
</script>

Memoization
<script setup>
import { computed } from 'vue';

const memoizedValue = computed(() => computeValue(dep));

// For functions, just return a function
const memoizedFn = computed(() => () => doSomething(dep));
</script>

