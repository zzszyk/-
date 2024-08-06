from fastapi import FastAPI, WebSocket, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.websockets import WebSocketDisconnect
from fastapi.responses import JSONResponse
import io
import soundfile as sf
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess
# from transformers import AutoModel

import work
# import io
import asyncio
import os
import database

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


# 创建一个Pydantic模型来定义接收的数据结构

class FormData(BaseModel):
    name: str
    email: str


"""
class FormData(BaseModel):
    name: str
    age: int
"""


# 创建一个POST路由以接收来自Vue组件的请求
@app.post("/submit-form")
async def submit_form(data: FormData):
    # 在这里可以处理收到的表单数据，例如保存到数据库或进行其他操作
    # age = FormData.age+1
    return {"message": "表单数据已收到", "data": data}


class QuestionData(BaseModel):
    question: str


class PoemTitle(BaseModel):
    input: str


class PoemContent(BaseModel):
    content: str

class deletePath(BaseModel):
    deletepath: str

class audioUrl(BaseModel):
    url: str


class DataBase(BaseModel):
    Content: str
    Theme: str


result = {"response": "No question asked yet"}


result1 = {"response": "你好，很高兴为你服务"}


path = "0"


result2 = {"response": "1"}

t = "0"




# 接收前端提出的问题
@app.post("/question")
async def submit_question(data: QuestionData):
    global result
    result = work.chat(data.question)
    print(result)
    database.poemadd(result, data.question)
    return {"message": data}


@app.post("/poem")
async def submit_question(data: PoemTitle):
    global result1
    result1 = work.chat1(data.input)
    print(result1)
    return {"message": data}


@app.post("/poemcontent")
async def submit_question(data: PoemContent):
    global path
    path = work.chat3(data.content)
    print(path)
    return {"message": data}



@app.get("/monster")
async def root():
    return {"message": result}


@app.get("/poemresult")
async def root():
    return {"message": result1}


@app.get("/poemcontentresult")
async def root():
    return {"message": path}


@app.delete("/deleteResource")
def delete_resource(data: deletePath):
    try:
        os.remove(data.deletepath)
        print(data.deletepath)
        return {"message": "资源删除成功"}
    except Exception as e:
        return {"message": "删除资源失败"}


@app.post("/audio")
async def process_audio(data: audioUrl):

    # 读取上传的文件内容
    uploadfile = open('C:/Users/zzsz/Desktop/work1/test/web-video/1.wav','rb')
    content = uploadfile.read()

    # 使用 io.BytesIO 创建一个内存文件对象
    with io.BytesIO(content) as audio_file:
        # 从内存文件对象读取音频数据
        wav, sr = sf.read(audio_file, dtype='float32')

    # 保存处理后的音频
    sf.write('input.wav', data=wav, samplerate=sr)

    # 语音识别返回用户输入文本
    model_dir = "iic/SenseVoiceSmall"
    model = AutoModel(model=model_dir, trust_remote_code=True, remote_code="./model.py", device="cuda:0")
    res = model.generate(
        input='input.wav',
        cache={},
        language="auto",  # "zh", "en", "yue", "ja", "ko", "nospeech"
        use_itn=True,
        batch_size=64,
    )
    text = rich_transcription_postprocess(res[0]["text"])

    # 冒烟测试
    print(text)

    if not text:
        return JSONResponse(
            status_code=400,
            content={"message": "无法识别语音内容，请重试。"}
        )
    uploadfile.close()


    global t
    t = text

    try:
        os.remove('C:/Users/zzsz/Desktop/work1/test/web-video/1.wav')
        print("资源删除成功")
    except Exception as e:
        print("删除资源失败")
    return {"message": data}
    # return JSONResponse(content={"text": text})


@app.get("/audiowrite")
async def root():
    global result2
    result2 = work.chat(t)
    print(result2)
    return {"message": result2}

@app.get("/audiowrite1")
async def root():
    global result2
    result2 = work.chat1(t)
    print(result2)
    return {"message": result2}

@app.get("/audiowrite2")
async def root():
    global result2
    result2 = work.chat3(t)
    print(result2)
    return {"message": result2}

@app.post("/poemadd")
async def submit_question(data: DataBase):
    database.poemadd(data.Content, data.Theme)
    return {"message": "插入数据成功"}

@app.get("/poemshow")
async def root():
    return {"message": database.poemshow()}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
