import os
import bs4

# 根据指定web地址爬取网页文本，建立文本向量库，并建立检索工具
def build_vector_retrivertool(description):
	# 设置web路径
	from langchain_community.document_loaders import WebBaseLoader
	# 分别为李白，李清照，纳兰性德，苏轼，杜甫诗歌网页首页
	web_path=(
		"https://www.gushicimingju.com/shiren/libai/",
		"https://www.gushicimingju.com/shiren/liqingzhao/",
		"https://www.gushicimingju.com/shiren/nalanxingde/",
		"https://www.gushicimingju.com/shiren/sushi/",
		"https://www.gushicimingju.com/shiren/dufu/"
	)
	documents = []
	# 爬取网页指定标签内容，存储在documents里
	for i in range(len(web_path)):
		loader = WebBaseLoader(
			web_path=web_path[i],
			bs_kwargs=dict(
        		parse_only=bs4.SoupStrainer(
            		class_=("simple-shiciqu has-author main-data")
        		)
    		)
		)
		documents.extend(loader.load())


	print("开始分割文本")
	# 进行文本分割
	from langchain_text_splitters import RecursiveCharacterTextSplitter
	text_splitter = RecursiveCharacterTextSplitter(chunk_size=250,
                                                   chunk_overlap=50)
	documents_ = text_splitter.split_documents(documents=documents)
	#
	'''
	def extract(content: str, schema: dict):
		return create_extraction_chain(schema=schema, llm=chat_model).run(documents_)

	documents1 = extract(schema=schema, content=documents_)
	'''


	print("开始构建向量库")
	# 构建文本向量库
	from langchain_huggingface import HuggingFaceEmbeddings
	EMBEDDING_DEVICE = "cpu"
	# 使用m3e模型
	embeddings = HuggingFaceEmbeddings(model_name="C:\\Users\\zzsz\\Desktop\\work1\\test\\model\\m3e-base",
                                   model_kwargs={'device': EMBEDDING_DEVICE})

	#使用FAISS向量库
	from langchain_community.vectorstores import FAISS
	vector = FAISS.from_documents(documents=documents_, embedding=embeddings)


	print("开始构建工具")
	# 构建检索工具
	from langchain.tools.retriever import create_retriever_tool
	retriever = vector.as_retriever()
	retriever_tool = create_retriever_tool(
    	retriever,
    	"documents_search",
    	description
	)
	return retriever_tool
