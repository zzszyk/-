<template lang="pug">
button.btn(@click="clickReturn") 返回首页
button.btn(@click="review") 获取更多内容
div#app
div.bullet-wrap
div.bullet-item(v-for="item in showingBullets" @animationend='removeBullet' :key="item.id" :data-line="item.line") {{item.name}}
div.input-wrap
input(v-model.trim="newBullet" type='text' maxlength='12' placeholder='来说点什么')
button.btn(@click="clickSend") 发送
</template>
<script>
import emitter from 'tiny-emitter/instance'
const getUUID = () => Math.random() + Math.random();
export default {
	data() {
		return {
			// 将要显示的弹幕队列
			waitBullets: [
				{ id: getUUID(), name: "江山如画展宏图，千里风光绮丽铺。\n山川纵横情无限，水波荡漾意何殊。\n铁马冰河入梦来，英雄豪迈共诗舞。\n岁月留痕铭刻骨，千里江山待明主。", isWished: false, line: 0 },
				{ id: getUUID(), name: "疾风知劲草，世有千里马。\n四蹄生风尘，一跃过山河。\n志存云霄外，胸怀凌云志。\n诗人笔落处，英姿照千里。", isWished: false, line: 0 },
				{ id: getUUID(), name: "常青藤蔓绕园墙，岁月悠悠映绿装。\n叶茂枝繁藏古意，风华绝代显风霜。\n坚韧执着攀高峰，生机盎然披翠光。\n诗心随藤攀援去，青春永驻梦常香。", isWished: false, line: 0 },
				{ id: getUUID(), name: "青山绿水伴藤生，常青之志永不更。\n攀缘直上九霄外，不畏风雨笑苍穹。\n繁华落尽依旧绿，岁月长河映劲踪。\n诗人笔下生光辉，常青藤蔓意重重。", isWished: false, line: 0 },
				{ id: getUUID(), name: "柳絮轻扬春风起，花开花落梦初醒。\n明月如盘挂天际，静观宇宙无穷境。\n思路若流水潺潺，诗意盎然在心头。\n此情此景难言尽，唯愿时光永停留。", isWished: false, line: 0 },
			],
			showingBullets: [],
			lines: 3,
			currentLine: 1,
			newBullet: "",
			isInfinite: true,
			show: {},
			};
		},
	mounted() {
		this.showNextBullet();
		const timer = setInterval(this.showNextBullet, 4500);
		// 组件销毁前，清除定时器
		emitter.once("hook:beforeDestroy", () => {
			clearInterval(timer);
		});
	},
	methods: {
		review(){
			fetch("http://127.0.0.1:8000/poemshow")
			.then((response) => response.json())
			.then((data) => {
				this.show = data;
				// 显示后端输出
				//if (this.sign1 == true) this.sign = true;
				console.log(this.show.message);
			})
			.catch((error) => {
				console.error("Fetch failed:", error);
			});
			for (let i=0;this.show.message!==undefined && this.show.message!=null && i<this.show.message.length;i++){
				const newBullet = {
					id: getUUID(),
					name: this.show.message[i][0],
					isWished: false,
					line: 0
				};
				this.waitBullets.push(newBullet);
			}
		},
		showNextBullet() {
			if (!this.waitBullets.length) {
				return;
			}
			// 先确定弹道，跟上一个弹道错开即可
			this.currentLine = (this.currentLine % this.lines) + 1;
			// 从等待集合里取出第一个
			const currentBullet = this.waitBullets.shift();
			// 想要无限循环的话
			this.isInfinite && this.waitBullets.push({
				id: getUUID(),
				name: currentBullet.name,
				isWished: false,
				line: 0
			});
			// 设置弹幕的弹道
			currentBullet.line = this.currentLine;
			// 弹幕放进显示集合里，弹幕开始滚动
			this.showingBullets.push(currentBullet);
		},
		// clickSend() {
		// 	if (!this.newBullet) {
		// 		return;
		// 	}
		// 	const newBullet = {
		// 		id: getUUID(),
		// 		name: this.newBullet,
		// 		isWished: false,
		// 		line: 0
		// 	};
		// 	this.waitBullets.push(newBullet);
		// },
		removeBullet() {
			this.showingBullets.shift();
			console.log(this.showingBullets);
		},
		clickReturn() {
			this.$router.push('/')
		},
	}
};
</script>

<style>
.bullet-wrap {
	height: 750px;
	position: relative;
}
.bullet-item {
	width: 700px;
	font-family: "CustomFont", sans-serif;
	font-size: 35px;
	position: absolute;
	animation: rightToleft 30s linear both;
}
/* .bullet-item[data-line="1"] {
	top: 0;
} */
.bullet-item[data-line="1"] {
	width: 1000px;
	top: 50px;
}
.bullet-item[data-line="2"] {
	top: 300px;
}
.bullet-item[data-line="3"] {
	width: 1200px;
	top: 600px;
}
@keyframes rightToleft {
	0% {
		transform: translate(100vw);
	}
	100% {
		transform: translate(-100%);
	}
}
.btn {
	font-family: 华文行楷;
	color:rgba(75, 61, 43, 0.849);
	font-size: 20px;
	margin: 20px;
	width: 200px;
	height: 40px;
	background-image: url(C:\Users\zzsz\Desktop\work1\vue-01\src\assets\button.jpg);
}
</style>
