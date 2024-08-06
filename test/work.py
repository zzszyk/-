import os
from langchain_community.chat_models import ChatZhipuAI
import qianfan
from PIL import Image
import io
import tempfile

# 千帆模型api
# 使用安全认证AK/SK鉴权，通过环境变量方式初始化；替换下列示例中参数，安全认证Access Key替换your_iam_ak，Secret Key替换your_iam_sk
os.environ["QIANFAN_ACCESS_KEY"] = "ALTAKDfgawJo6rQw31rlVxDwmt"
os.environ["QIANFAN_SECRET_KEY"] = "3e7f7aef330948d7a05842204b43acc5"
# 质谱ai模型api
os.environ["ZHIPUAI_API_KEY"] = "fc6a14b27eb88a57b8a8957e1bbc4900.jitgdtTdNBpBQOSZ"
# serpapi
os.environ["SERPAPI_API_KEY"] = "fd1f28bb97047faad4e494715cb463d280c4c771eae707900443f8251b29ce3a"
zhipuai_chat_model = ChatZhipuAI(model="glm-4")


# 建立检索文本向量库的工具
import build_vector
# 输入工具信息
descrip = "用此工具搜索有关诗歌的信息，一定要使用中文来搜索"  # 输入文档可检索信息
retriever_tool = build_vector.build_vector_retrivertool(descrip)  # 引入build_vector中的函数

# 建立工具组，含有Search工具（serpapi），含有documents_search工具
from langchain_community.agent_toolkits.load_tools import load_tools

tools = load_tools(tool_names=["serpapi"], llm=zhipuai_chat_model)
tools1 = tools
tools1.append(retriever_tool)

# 设置Agent提示词模版
from langchain_core.prompts import PromptTemplate
# ai写诗的提示词模版
template = '''你是一个拥有大量中国古代诗歌储备的，对中国古代诗歌十分了解的诗人。
        你擅长根据提供的诗歌主题自我创作中国古代诗歌，其中诗歌内容高度切合主题，诗句颇具韵味且独一无二，这世界上找不出第二句相同的诗句。
        你在创作诗歌时，可以参照某诗人的风格进行参考创作，也可以参考他的用词，但是绝对不会照搬他的诗句，这是不允许的事。

        当你需要创作一首诗歌时，使用 Search 。

        你可以使用以下工具：

        {tools}

        执行Action时，应为[{tool_names}]中的其中一个。注意！这里必须只放工具名称，不要有其他内容

        使用工具时，你必须需要使用以下格式：

        """
        Question: the input question you must answer
        Thought:我是否要选用工具？Yes
        Action: 你所选的工具名称要放在这里
        Action Input: 执行该行动所需要的输入
        Observation: 执行该行动所获得的结果或答案（这个思想/行动/行动输入/观察可以重复 N 次）
        """

        当你准备好向用户输出答案，再次检查答案是否与最初的问题相关，如果不相关，则返回重新回答。
        检查最初问题：如果是回答诗歌内容，则回答诗歌内容部分；如果是创作诗歌，则检查回答内容与搜索的重复性，不要有相似的句子
        ！！！输出答案只输出诗歌部分！！！
        当你准备好向用户输出答案，或者不需要使用任何工具时，你必须使用以下格式：


        Thought:我是否需要使用工具? No
        Final Answer: [你的最终答案要放在这里]


        # Begin!

        # 以前的聊天历史：
        # {chat_history}

        # -------
        # Question: {input}
        # {agent_scratchpad}
    '''
# 智能查诗的提示词模版
template1 = '''你是一个拥有大量中国古代诗歌储备的，对中国古代诗歌十分了解的诗词研究者。
    你能根据提供的中国古代诗歌的作者、诗句、诗名和主题轻松地搜索到对应的中国古代诗歌。
    
    关于使用 documents_search 的注意事项：
    - 对于搜索诗歌的问题，优先使用此工具
    - 优先使用知识库中的答案，知识库中没有再上网搜索
    - 如果答案过长，或者较为复杂，则截取部分作为答案。
    - 如果使用 documents_search 搜索不到答案时，使用 Search
    
    当你使用 documents_search 搜索不到答案时，使用 Search 。
    
    你可以使用以下工具：
    
    {tools}
    
    执行Action时，应为[{tool_names}]中的其中一个。注意！这里必须只放工具名称，不要有其他内容
    
    使用工具时，你必须需要使用以下格式：
    
    """
    Question: the input question you must answer
    Thought:我是否要选用工具？Yes
    Action: 你所选的工具名称要放在这里
    Action Input: 执行该行动所需要的输入
    Observation: 执行该行动所获得的结果或答案（这个思想/行动/行动输入/观察可以重复 N 次）
    """
    
    当你准备好向用户输出答案，再次检查答案是否与最初的问题相关，如果不相关，则返回重新回答。
    检查最初问题：如果是搜索作者，则回答该作者比较有名的一到三首诗歌名称和诗歌内容部分，注意请用中文进行回答；
    如果是搜索诗句，则回答该诗句对应的诗歌名称和完整的整首诗内容，回答完后检查诗句是否在诗歌内容中，如果不在则返回重新查找并返回正确的诗歌名称和完整的整首诗内容；
    如果是搜索诗名，则回答该诗名对应的完整诗歌内容；
    如果是搜索某个诗歌主题，则回答有关该主题的一到三首有名的诗歌名称和对应的诗歌内容。
    当你准备好向用户输出答案，或者不需要使用任何工具时，你必须使用以下格式：
    
    
    Thought:我是否需要使用工具? No
    Final Answer: [你的最终答案要放在这里]
    
    
    # Begin!
    
    # 以前的聊天历史：
    # {chat_history}
    
    # -------
    # Question: {input}
    # {agent_scratchpad}
    '''
# 在据诗作画中翻译诗句的提示词模版    # 改进整合？
template2 = '''你是一个拥有多年将中国古代诗歌翻译为英文经验的翻译官，你可以精确理解诗词的内容，然后准确地根据诗歌的内容将诗歌翻译为英文。
    你在翻译诗歌时，可以兼顾诗歌的内容和诗歌的意境，将诗歌内容尽可能详细地翻译出来，尽量翻译得更诗意一点、更有画面感一点。

    你可以使用 Search 给自己提供翻译上的帮助。

    你可以使用以下工具：

    {tools}

    执行Action时，应为[{tool_names}]中的其中一个。注意！这里必须只放工具名称，不要有其他内容

    使用工具时，你必须需要使用以下格式：

    """
    Question: the input question you must answer
    Thought:我是否要选用工具？Yes
    Action: 你所选的工具名称要放在这里
    Action Input: 执行该行动所需要的输入
    Observation: 执行该行动所获得的结果或答案（这个思想/行动/行动输入/观察可以重复 N 次）
    """

    当你准备好向用户输出答案，再次检查答案是否与最初的问题相关，如果不相关，则返回重新回答。
    当你准备好向用户输出答案，或者不需要使用任何工具时，你必须使用以下格式：
    """
    Thought:我是否需要使用工具? No
    Final Answer: [你的最终答案要放在这里]
    """


    Begin!

    以前的聊天历史：
    {chat_history}

    -------
    Question: {input}
    {agent_scratchpad}
    '''

prompt = PromptTemplate.from_template(template)
prompt1 = PromptTemplate.from_template(template1)
prompt2 = PromptTemplate.from_template(template2)

print("开始创建agent")
# 创建agent，根据不同功能创建agent
from langchain.agents import create_react_agent
from langchain.agents import AgentExecutor

agent = create_react_agent(zhipuai_chat_model, tools, prompt)
agent1 = create_react_agent(zhipuai_chat_model, tools1, prompt1)
agent2 = create_react_agent(zhipuai_chat_model, tools, prompt2)


# 设置历史对话
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(memory_key="chat_history")
agent_executor = AgentExecutor.from_agent_and_tools(agent=agent,
                                                    tools=tools,
                                                    memory=memory,
                                                    verbose=True,  #
                                                    handle_parsing_errors=True)

memory1 = ConversationBufferMemory(memory_key="chat_history")
agent_executor1 = AgentExecutor.from_agent_and_tools(agent=agent1,
                                                     tools=tools1,
                                                     memory=memory1,
                                                     verbose=True,  #
                                                     handle_parsing_errors=True)

memory2 = ConversationBufferMemory(memory_key="chat_history")
agent_executor2 = AgentExecutor.from_agent_and_tools(agent=agent2,
                                                     tools=tools,
                                                     memory=memory2,
                                                     verbose=True,  #
                                                     handle_parsing_errors=True)
print("开始对话")


# 对话
def chat(question):
    # 初始对话历史设置
    from langchain_core.messages import HumanMessage, AIMessage

    chat_history = [
        HumanMessage(content="请介绍一下你自己"),
        AIMessage(content="我是一个诗人，可以为你创作诗歌。")
    ]

    # 进行对话
    while True:
        # 问题输入，human_message 用户问题
        human_message = question
        if human_message == "end":
            break
        # agent运行
        response = agent_executor.invoke({
            "chat_history": chat_history,
            "input": "请帮我根据以下主题创作诗歌：" + human_message
        })
        # 输出答案
        ai_message = response['output']
        # 历史追加
        chat_history.append(HumanMessage(content=human_message))
        chat_history.append(AIMessage(content=ai_message))
        return ai_message

# 下同
def chat1(question):
    from langchain_core.messages import HumanMessage, AIMessage
    chat_history1 = [
        HumanMessage(content="请介绍一下你自己"),
        AIMessage(content="我是一个诗歌研究者，可以为你搜索查询诗歌。")
    ]
    while True:
        human_message = question
        if human_message == "end":
            break
        response = agent_executor1.invoke({
            "chat_history": chat_history1,
            "input": "请帮我查找以下作者、主题、诗句或诗名对应的一首或几首诗歌" + human_message
        })
        ai_message = response['output']
        chat_history1.append(HumanMessage(content=human_message))
        chat_history1.append(AIMessage(content=ai_message))
        return ai_message

def chat2(question):
    from langchain_core.messages import HumanMessage, AIMessage
    chat_history2 = [
        HumanMessage(content="请介绍一下你自己"),
        AIMessage(content="我是一个翻译官，可以为你翻译诗歌。")
    ]
    while True:
        human_message = question
        if human_message == "end":
            break
        # human_message 是那个问题
        response = agent_executor1.invoke({
            "chat_history": chat_history2,
            "input": "请帮我将以下诗词翻译为英文" + human_message
        })
        ai_message = response['output']
        chat_history2.append(HumanMessage(content=human_message))
        chat_history2.append(AIMessage(content=ai_message))
        return ai_message

# AI画图生成图片
def chat3(question):

    # 设置模型及输入
    content = chat2(question)
    prompt = content
    t2i = qianfan.Text2Image()

    # 调用模型生成图片
    resp = t2i.do(prompt=prompt, with_decode="base64", style="Texture")
    img_data = resp["body"]["data"][0]["image"]

    # 展示图片
    img = Image.open(io.BytesIO(img_data))

    # 将图片保存到指定文件夹中
    folder_path = 'C:/Users/zzsz/Desktop/work1/vue-01/public'  # 替换为实际的文件夹路径
    file_name = 'example.jpg'  # 替换为你想要保存的文件名
    # 创建文件夹如果不存在
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 完整文件路径
    file_path = os.path.join(folder_path, file_name)

    # 保存图片到指定文件夹
    img.save(file_path)

    return file_name
