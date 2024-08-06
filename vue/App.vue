<template>
	<div class="back">
		<div id="app">
			<router-view v-if="isRouterAlive"></router-view>
		</div>
	</div>
</template>


<script>
import { ref, nextTick, provide } from "vue";

export default {
	name: "App",
	components: {},
	setup() {
		// 局部组件刷新,
		const isRouterAlive = ref(true);
		const reload = () => {
			isRouterAlive.value = false;
			nextTick(() => {
				isRouterAlive.value = true;
			});
		};
		provide("reload", reload);
		return {
			isRouterAlive,
		};
	},
};
</script>

<style>
.back {
	background-image: url(C:\Users\zzsz\Desktop\work1\vue-01\src\assets\background.jpg);
	background-size: cover;
	position: fixed;
	width: 100%;
	height: 100%;
	position: fixed;
	background-size: 100% 100%;
	animation: slideshow 30s infinite;
}
@keyframes slideshow {
	0% {
		background-image: url(C:\Users\zzsz\Desktop\work1\vue-01\src\assets\background1.jpg);
	}
	10% {
		background-image: url(C:\Users\zzsz\Desktop\work1\vue-01\src\assets\background2.jpg);
	}
	20% {
		background-image: url(C:\Users\zzsz\Desktop\work1\vue-01\src\assets\background3.jpg);
	}
	30% {
		background-image: url(C:\Users\zzsz\Desktop\work1\vue-01\src\assets\background4.jpg);
	}
	40% {
		background-image: url(C:\Users\zzsz\Desktop\work1\vue-01\src\assets\background5.jpg);
	}
	50% {
		background-image: url(C:\Users\zzsz\Desktop\work1\vue-01\src\assets\background4.jpg);
	}
	60% {
		background-image: url(C:\Users\zzsz\Desktop\work1\vue-01\src\assets\background3.jpg);
	}
	70% {
		background-image: url(C:\Users\zzsz\Desktop\work1\vue-01\src\assets\background2.jpg);
	}
	80% {
		background-image: url(C:\Users\zzsz\Desktop\work1\vue-01\src\assets\background1.jpg);
	}
	90% {
		background-image: url(C:\Users\zzsz\Desktop\work1\vue-01\src\assets\background2.jpg);
	}
	100% {
		background-image: url(C:\Users\zzsz\Desktop\work1\vue-01\src\assets\background1.jpg);
	}
}
</style>
