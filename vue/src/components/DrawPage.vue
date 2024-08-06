<template>
	<div>
		<div>
			<button @click="gotoHome2" class="but">返回首页</button>
			<div v-if="this.value" class="drawblog">
				<img v-if="this.sign" :src="address" alt="" class="pic" />
				<button v-if="this.value" @click="pick1" class="butto">返回提问</button>
			</div>
		</div>

		<textarea v-if="!this.value" rows="4" cols="50" class="in" type="text" v-model="questionData.content" placeholder="请输入一句诗或一首诗"></textarea>
		<d-button v-if="!this.value" icon="icon-run-o" bsStyle="primary" bsSize="xs" title="开始输入" shape="circle" @click="start" class="yuyin"></d-button>
		<d-button v-if="!this.value" icon="icon-suspend" bsStyle="primary" bsSize="xs" title="结束输入" shape="circle" @click="stop" class="yuyin1"></d-button>
		<d-button v-if="!this.value" icon="icon-rerun" bsStyle="primary" bsSize="xs" title="本地试听" shape="circle" @click="test" class="yuyin2"></d-button>
		<button v-if="!this.value" @click="submitQuestion1" type="submit" class="butt">上书</button>
		<button v-if="!this.value" @click="returnpic" type="submit" class="bu">返回生成图片</button>
	</div>
</template>

<script>
import axios from "axios";
import Recorder from "js-audio-recorder";
export default {
	name: "DrawPage",
	data() {
		return {
			value: false,
			valuey: false,
			sign: false,
			sign1: false,
			questionData: {
				content: "",
			},
			deletePath: {
				deletepath: "",
			},
			address: "example.jpg",
			poem2: {},
			audioUrl:{url:"a",},
			recorder: new Recorder({
				sampleBits: 16, // 采样位数，支持 8 或 16，默认是16
				sampleRate: 16000, // 采样率，支持 11025、16000、22050、24000、44100、48000，根据浏览器默认值，我的chrome是48000
				numChannels: 1, // 声道，支持 1 或 2， 默认是1
			}),
		};
	},
	methods: {
		pick() {
			if (this.value == false) this.value = true;
			else this.value = false;
		},
		pick1() {
			if (this.value == false) this.value = true;
			else this.value = false;
			this.sign = false;
			this.sign1 = false;
			this.deletePath.deletepath ="C:/Users/zzsz/Desktop/work1/vue-01/public/example.jpg"; // 待删除资源的路径
			axios({
				method: "DELETE",
				url: "http://127.0.0.1:8000/deleteResource",
				data: this.deletePath,
			})
			.then((response) => {
				// 处理后端返回的响应
				console.log(response.data);
			})
			.catch((error) => {
				// 处理请求错误
				console.error("请求错误：", error);
			});
		},
		gotoHome2() {
			this.$router.push("/");
		},
		submitQuestion1() {
			this.sign1 = true;
			if (this.value == false) this.value = true;
			else this.value = false;

			axios.post("http://127.0.0.1:8000/poemcontent", this.questionData)
			.then((response) => {
				// 处理后端返回的响应
				console.log(response.data);
				setTimeout(() => {
					this.fetchData();
				}, 8000);
			})
			.catch((error) => {
			// 处理请求错误
				console.error("请求错误：", error);
			});
		},
		fetchData() {
			console.log(this.address);

			fetch("http://127.0.0.1:8000/poemcontentresult")
			.then((response) => response.json()) //
			.then((data) => {
				if (this.sign1 == true) this.sign = true;

				console.log(data);
				//console.log(this.address);
			})
			.catch((error) => {
				console.error("Fetch failed:", error);
			});
		},
		start() {
			Recorder.getPermission().then(() => {
				console.log("开始录音");
				this.recorder.start(); // 开始录音
			},
			(error) => {
				this.$message({
					message: "请先允许该网页使用麦克风",
					type: "info",
				});
				console.log(`${error.name} : ${error.message}`);
			},);
		},
		fetchData2() {
			fetch('http://127.0.0.1:8000/audiowrite2')
			.then(response => response.json())
			.then(data => {
				this.poem2 = data;
				if(this.sign1 == true)
				this.sign = true;
				console.log(this.sign);
				console.log(this.poem);
			})
			.catch(error => {
				console.error('Fetch failed:', error);
			});
		},
		stop(){
			console.log("停止录音");
			this.recorder.stop();
			this.recorder.downloadWAV("1");
		},
		test(){
			this.sign = false;
			this.sign1 = true;
			console.log("播放录音");
			this.recorder.play();
			if(this.value==false)this.value=true;
			else this.value=false;

			this.audioUrl.url='C:/Users/zzsz/Desktop/work1/vue-01/src/assets/1.wav'
			axios.post('http://127.0.0.1:8000/audio', this.audioUrl)
			.then(response=>{
				// 处理后端返回的响应
				console.log(response.data);
				setTimeout(()=>{
					console.log(this.sign)
					this.fetchData2();
				},15000);
			})
			.catch(error => {
				// 处理请求错误
				console.error('请求错误：', error);
			});
		},
		returnpic(){
			this.sign1 = true;
			if (this.value == false) this.value = true;
			else this.value = false;
			this.sign = true;
		},
	},
	// created(){
	// 	this.fetchData();
	// }
};
</script>

<style scoped>
.drawblog {
	background-image: url(C:\Users\zzsz\Desktop\work1\vue-01\src\assets\draw.jpg);
	width: 600px;
	height: 600px;
	background-size: 100% 100%;
	margin: auto;
	position: fixed;
	position: absolute;
	top: 0;
	left: 0;
	right: 0;
	bottom: 0;
}
.in {
	background-image: url(C:\Users\zzsz\Desktop\work1\vue-01\src\assets\w-ask.jpg);
	opacity: 0.7;
	width: 500px;
	height: 220px;
	background-size: 100% 100%;
	margin: auto;
	position: absolute;
	top: 150px;
	left: 0;
	right: 0;
	bottom: 0;
}
textarea {
	font-family: 华文行楷;
	padding: 20px;
	background: transparent;
	border-style: none;
	font-size: 192%;
	line-height: 2;
}
.butto {
	font-family: 华文行楷;
	font-size: 20px;
	color:rgba(75, 61, 43, 0.849);
	width: 200px;
	height: 40px;
	margin: auto;
	position: absolute;
	left: 0;
	right: 0;
	bottom: 0;
	background-image: url(C:\Users\zzsz\Desktop\work1\vue-01\src\assets\button.jpg);
}
.but {
	font-family: 华文行楷;
	font-size: 20px;
	color:rgba(75, 61, 43, 0.849);
	width: 200px;
	height: 40px;
	background-image: url(C:\Users\zzsz\Desktop\work1\vue-01\src\assets\button.jpg);
}
.butt {
	font-family: 华文行楷;
	font-size: 20px;
	color:rgba(75, 61, 43, 0.849);
	width: 200px;
	height: 40px;
	background-image: url(C:\Users\zzsz\Desktop\work1\vue-01\src\assets\button.jpg);
	margin: auto;
	position: absolute;
	top: 520px;
	left: 0;
	right: 245px;
	bottom: 0;
}
.pic {
	width: 530px;
	height: 530px;
	margin: auto;
	position: absolute;
	left: 0;
	right: 0;
	bottom: 0;
	top: 0px;
}
.yuyin {
	margin: auto;
	position: absolute;
	top: 310px;
	left: 0;
	right: 350px;
	bottom: 0;
}
.yuyin1 {
	margin: auto;
	position: absolute;
	top: 310px;
	left: 0;
	right: 280px;
	bottom: 0;
}
.yuyin2 {
	margin: auto;
	position: absolute;
	top: 310px;
	left: 0;
	right: 210px;
	bottom: 0;
}

.bu {
	font-family: 华文行楷;
	font-size: 20px;
	color:rgba(75, 61, 43, 0.849);
	width: 200px;
	height: 40px;
	background-image: url(C:\Users\zzsz\Desktop\work1\vue-01\src\assets\button.jpg);
	margin: auto;
	position: absolute;
	top: 520px;
	left: 245px;
	right: 0;
	bottom: 0;
}
</style>
