<template>
	<div class="choice">
		<ul>
			<li>
				<button @click="gotowrite" class="write" title="AI写诗">采词</button>
			</li>
			<li>
				<button @click="gotosearch" class="search" title="AI查诗">集韵</button>
			</li>
			<li>
				<button @click="gotodraw" class="draw" title="据诗作画">浮绘</button>
			</li>
		</ul>
	</div>
	<button @click="gototest" class="butt1">观阅</button>
</template>

<style>
.write{
	font-family: "CustomFont", sans-serif;
	font-size: 60px;
	background-image: url(C:\Users\zzsz\Desktop\work1\vue-01\src\assets\card1.bmp);
	width: 500px;
	height: 150px;
	background-size:100% 100%;
    position:fixed;
}
.search{
	font-family: "CustomFont", sans-serif;
	font-size: 60px;
	background-image: url(C:\Users\zzsz\Desktop\work1\vue-01\src\assets\card2.bmp);
	width: 500px;
	height: 150px;
	background-size:100% 100%;
    position:fixed;
}
.draw{
	font-family: "CustomFont", sans-serif;
	font-size: 60px;
	background-image: url(C:\Users\zzsz\Desktop\work1\vue-01\src\assets\card3.bmp);
	width: 500px;
	height: 150px;
	background-size:100% 100%;
    position:fixed;
}
.choice{
	width: 500px;
	padding-top: 80px;
	margin: auto;
	position: absolute;
	top: 0;
	left: 0;
	right: 90px;
	bottom: 0;
}
li{
    padding-bottom: 170px;
}
.butt1 {
	font-family: "CustomFont", sans-serif;
	font-size: 100px;
	writing-mode: tb-rl;
	margin: auto;
	position: absolute;
	top: 0;
	left: 0;
	right: 1200px;
	bottom: 300px;
}
</style>

<script>
export default {
	name:'QuestionChoice',
	methods:{
		gotowrite(){
			this.$router.push('/WritePage');
		},
		gotosearch(){
			this.$router.push('/SearchPage');
		},
		gotodraw(){
			this.$router.push('/DrawPage')
		},
		gototest(){
			this.$router.push('/ReviewPage')
		},
	}
}
</script>
