const arr = [1, 4, 5, 73, 13, 56, 34, 90, 5];

// two loops
// swap the arr[i] and arr[i+1] if arr[i+1] > arr[i]

for (i = 0; i < arr.length - 1; i++) {
	for (j = i+1; i < arr.length; i++) {
		console.log(`i:${i} j:${j} i:${arr[i]} j:${arr[j]}`);
		if (arr[i] > arr[j]) {
			const temp = arr[i];
			arr[i] = arr[j];
			arr[j] = temp;
		}
	}
}

console.log(arr);

// [1, 4, 5, 73, 13, 56, 34, 90, 5];
// 1 -> 4, 1->5, 