<template>
	<div>
		<button @click="gotoHome1" class="but">返回首页</button>
		<div v-if="this.value1" class="searchblog">
			<h3>搜索到的古诗：</h3>
			<p v-if="this.sign1">{{ poem1.message }}</p>
			<button v-if="this.value1" @click="pick" class="but1">返回提问</button>
		</div>

		<textarea v-if="!this.value1"  rows="4" cols="50" class="in" type="text" v-model="questionData1.input" placeholder="请输入作者、诗句或诗名、"></textarea>
		<d-button v-if="!this.value1" icon="icon-run-o" bsStyle="primary" bsSize="xs" title="开始输入" shape="circle" @click="start" class="yuyin"></d-button>
		<d-button v-if="!this.value1" icon="icon-suspend" bsStyle="primary" bsSize="xs" title="结束输入" shape="circle" @click="stop" class="yuyin1"></d-button>
		<d-button v-if="!this.value1" icon="icon-rerun" bsStyle="primary" bsSize="xs" title="本地试听" shape="circle" @click="test" class="yuyin2"></d-button>
		<button v-if="!this.value1" @click="sendpoem" type="submit" class="butt">上书</button>
	</div>
</template>

<script>
import axios from 'axios';
import Recorder from "js-audio-recorder";

export default {
	name:'SearchPage',
	data(){
		return{
			value1:false,
			sign1:false,
			sign2:false,
			questionData1:{
				input:'',
			},
			poem1:{},
			audioUrl:{url:"a",},
			recorder: new Recorder({
					sampleBits: 16, // 采样位数，支持 8 或 16，默认是16
					sampleRate: 16000, // 采样率，支持 11025、16000、22050、24000、44100、48000，根据浏览器默认值，我的chrome是48000
					numChannels: 1, // 声道，支持 1 或 2， 默认是1
			}),
		}
	},
	methods:{
		pick(){
			if(this.value1==false)this.value1=true;
			else this.value1=false;
		},
		gotoHome1(){
			this.$router.push('/');
		},
		sendpoem(){
			if(this.value1==false)this.value1=true;
			else this.value1=false;
			this.sign2 = true;
			axios.post('http://127.0.0.1:8000/poem',this.questionData1)
			.then(response=>{
				// 处理后端返回的响应
				console.log(response.data);
				setTimeout(()=>{
					this.fetchData1();
				},15000);
			})
			.catch(error => {
				// 处理请求错误
				console.error('请求错误：', error);
			});
		},
		fetchData1() {
			fetch('http://127.0.0.1:8000/poemresult')
				.then(response => response.json())
				.then(data => {
					this.poem1 = data;
					if(this.sign2 == true)
					this.sign1 = true;
				})
				.catch(error => {
					console.error('Fetch failed:', error);
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
			fetch('http://127.0.0.1:8000/audiowrite1')
			.then(response => response.json())
			.then(data => {
				this.poem1 = data;
				if(this.sign2 == true)
				this.sign1 = true;
				console.log(this.sign1);
				console.log(this.poem1);
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
			this.sign1 = false;
			this.sign2 = true;
			console.log("播放录音");
			this.recorder.play();
			if(this.value1==false)this.value1=true;
			else this.value1=false;

			this.audioUrl.url='C:/Users/zzsz/Desktop/work1/vue-01/src/assets/1.wav'
			axios.post('http://127.0.0.1:8000/audio', this.audioUrl)
			.then(response=>{
				// 处理后端返回的响应
				console.log(response.data);
				setTimeout(()=>{
					console.log(this.sign1)
					this.fetchData2();
				},15000);
			})
			.catch(error => {
				// 处理请求错误
				console.error('请求错误：', error);
			});
		},
	},
	created(){
		this.fetchData1();
	},
}
</script>

<style scoped>
.searchblog{
	background-image: url(C:\Users\zzsz\Desktop\work1\vue-01\src\assets\write.jpg);
	width: 500px;
	height: 750px;
	background-size:100% 100%;
	margin: auto;
	position:fixed;
	position: absolute;
	top: 0;
	left: 0;
	right: 0;
	bottom: 0;
}
.in{
	background-image: url(C:\Users\zzsz\Desktop\work1\vue-01\src\assets\w-ask.jpg);
	opacity: 0.7;
	width: 500px;
	height: 220px;
	background-size:100% 100%;
	margin: auto;
	position: absolute;
	top: 150px;
	left: 0;
	right: 0;
	bottom: 0;
}
textarea{
	font-family: 华文行楷;
	padding: 20px;
	background:transparent;
	border-style:none;
	font-size: 192%;
	line-height: 2;
}
.butt{
	font-family: 华文行楷;
	font-size: 20px;
	color:rgba(75, 61, 43, 0.849);
	background-image: url(C:\Users\zzsz\Desktop\work1\vue-01\src\assets\button.jpg);
	width: 200px;
	height:40px;
	margin: auto;
	position: absolute;
	top: 430px;
	left: 0;
	right: 0;
	bottom: 0;
}
.but1{
	font-family: 华文行楷;
	color:rgba(75, 61, 43, 0.849);
	font-size: 20px;
	margin: auto;
	position: absolute;
	top: 0;
	left: 0;
	right: 250px;
	bottom: 610px;
	width: 200px;
	height: 40px;
	background-image: url(C:\Users\zzsz\Desktop\work1\vue-01\src\assets\button.jpg);
}
.but{
	font-family: 华文行楷;
	color:rgba(75, 61, 43, 0.849);
	font-size: 20px;
	margin: 20px;
	width: 200px;
	height: 40px;
	background-image: url(C:\Users\zzsz\Desktop\work1\vue-01\src\assets\button.jpg) ;
}
.yuyin{
	margin: auto;
	position: absolute;
	top: 310px;
	left: 0;
	right: 350px;
	bottom: 0;
}
.yuyin1{
	margin: auto;
	position: absolute;
	top: 310px;
	left: 0;
	right: 280px;
	bottom: 0;
}
.yuyin2{
	margin: auto;
	position: absolute;
	top: 310px;
	left: 0;
	right: 210px;
	bottom: 0;
}
.po{
	font-family: "CustomFont", sans-serif;
	font-size: 35px;
	padding-top: 87px;
	writing-mode: tb-rl;
	height: 670px;
	padding-right: 27px;
	float: right;
}
</style>
