from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.llms import Tongyi
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("DASHSCOPE_API_KEY")

# 准备文档
docs = [
    "Python 是一种高级编程语言，用于数据科学、AI、Web 开发",
    "WebRTC 是实时通讯协议，用于音视频传输",
    "RAG 是检索增强生成，结合向量检索和大模型"
]

# 分割
splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
chunks = splitter.split_text("\n".join(docs))

print(f"✅ 分割后 {len(chunks)} 个chunk")

# 创建向量库
embeddings = DashScopeEmbeddings(model="text-embedding-v3")
vector_store = FAISS.from_texts(chunks, embeddings)

print("✅ 向量库创建成功")

# 查询
query = "Python 用来做什么？"
results = vector_store.similarity_search(query, k=2)

print(f"\n🔍 查询: {query}")
for i, doc in enumerate(results):
    print(f"  {i+1}. {doc.page_content[:50]}...")

# LLM 回答
print("\n⏳ LLM 生成中...")
llm = Tongyi()
prompt = f"""基于以下信息回答问题:

信息:
{results[0].page_content}

问题: {query}

请用简洁的中文回答。"""

answer = llm.invoke(prompt)
print(f"\n✅ 答案:\n{answer}")