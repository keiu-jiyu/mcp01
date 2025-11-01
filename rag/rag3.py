from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.llms import Tongyi
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor
import json

load_dotenv()

api_key = os.getenv("DASHSCOPE_API_KEY")
database_url = os.getenv("DATABASE_URL")


# ============ 1️⃣ 从 CherryStudio 加载知识库文件 ============
def load_knowledge_base_from_files():
    """
    从本地 TXT 文件加载知识库
    你的结构：班级.txt 和 新闻.txt
    """
    docs = []

    # 文件列表（改成你的实际文件）
    file_paths = [
        "data/新闻.txt",  # 新闻内容
    ]

    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                docs.append(content)
                print(f"✅ 加载: {file_path}")
        except FileNotFoundError:
            print(f"⚠️ 文件不存在: {file_path}")

    return docs


# ============ 2️⃣ 从 CherryStudio 导出的 JSON 加载 ============
def load_from_cherrystudio_export(json_file):
    """
    如果你从 CherryStudio 导出为 JSON
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        docs = []
        for item in data:
            # 根据实际结构调整字段名
            content = item.get('content') or item.get('text') or item.get('文本')
            if content:
                docs.append(content)

        print(f"✅ 从 JSON 加载 {len(docs)} 个文档")
        return docs
    except Exception as e:
        print(f"❌ 加载 JSON 失败: {e}")
        return []


# ============ 3️⃣ 查询 Supabase 数据库 ============
def query_students(name=None):
    """查询学生信息"""
    try:
        conn = psycopg2.connect(database_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)

        if name:
            cur.execute("SELECT * FROM students WHERE name LIKE %s", (f"%{name}%",))
        else:
            cur.execute("SELECT * FROM students LIMIT 10")

        results = cur.fetchall()
        cur.close()
        conn.close()
        return results
    except Exception as e:
        print(f"❌ 数据库查询失败: {e}")
        return []


# ============ 4️⃣ 创建向量库 ============
def create_vector_store(docs):
    """创建 FAISS 向量库"""
    if not docs:
        print("❌ 没有文档数据")
        return None

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,  # 增大 chunk_size，适合较长文本
        chunk_overlap=100,
        separators=["\n\n", "\n", "。", "，", " ", ""]
    )

    chunks = splitter.split_text("\n".join(docs))

    embeddings = DashScopeEmbeddings(model="text-embedding-v3")
    vector_store = FAISS.from_texts(chunks, embeddings)

    print(f"✅ 向量库创建成功，{len(chunks)} 个 chunk")
    return vector_store


# ============ 5️⃣ 综合查询：文档 + 数据库 ============
def answer_question(query, vector_store):
    """
    综合查询：
    1. 从知识库检索相关文档
    2. 从数据库查询相关数据
    3. LLM 综合回答
    """

    print(f"\n🔍 查询: {query}")
    print("=" * 50)

    # 从知识库检索
    doc_results = vector_store.similarity_search(query, k=3)
    doc_context = "\n".join([f"- {doc.page_content[:200]}" for doc in doc_results])

    # 从数据库查询
    db_results = query_students()
    db_context = ""
    if db_results:
        db_context = "\n".join([f"- {student.get('name', '未知')}: {str(student)}"
                                for student in db_results[:3]])
    else:
        db_context = "数据库暂无学生数据"

    # LLM 综合回答
    llm = Tongyi()
    prompt = f"""你是一个学校助手。基于以下信息回答用户问题：

【知识库信息】
{doc_context}

【学生数据库信息】
{db_context}

【用户问题】
{query}

请用简洁的中文回答问题。如果信息不足，请说明。"""

    print("\n📝 正在生成答案...\n")
    answer = llm.invoke(prompt)
    print(f"✅ 答案:\n{answer}\n")
    return answer


# ============ 6️⃣ 主程序 ============
if __name__ == "__main__":

    print("🚀 加载知识库...")
    print("=" * 50)

    # 方法1：从 TXT 文件加载（推荐）
    docs = load_knowledge_base_from_files()

    # 方法2：从导出的 JSON 加载（可选）
    # docs = load_from_cherrystudio_export("data/knowledge_base.json")

    if not docs:
        print("❌ 没有加载到任何文档，请检查文件路径")
        exit(1)

    # 创建向量库
    vector_store = create_vector_store(docs)

    print("\n" + "=" * 50)
    print("✅ 系统就绪！开始提问...")
    print("=" * 50)

    # 测试查询
    questions = [
        "班级有哪些信息？",
        "最近有什么新闻？",
        "我们学校的学生有哪些？",
        "班级的具体情况是什么？"
    ]

    for question in questions:
        answer_question(question, vector_store)
        print("\n" + "=" * 50)

    # 交互式查询
    print("\n💬 进入交互模式 (输入 'exit' 退出)")
    print("=" * 50)
    while True:
        user_query = input("\n你的问题: ").strip()
        if user_query.lower() == 'exit':
            print("👋 再见！")
            break
        if user_query:
            answer_question(user_query, vector_store)