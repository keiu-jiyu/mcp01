from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.llms import Tongyi
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()

api_key = os.getenv("DASHSCOPE_API_KEY")
database_url = os.getenv("DATABASE_URL")


# ============ 1️⃣ 查询 Supabase 数据库 ============
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


# ============ 2️⃣ 从 CherryStudio 加载知识库 ============
def load_knowledge_base():
    """从文件加载知识库（模拟 CherryStudio 导出）"""
    # 实际应该从 CherryStudio 导出的 JSON/CSV 文件读取
    docs = [
        "学生规定：学生必须遵守校规校纪",
        "成绩评分：90-100优秀，80-89良好，70-79中等",
        "奖学金政策：GPA大于3.5可申请奖学金",
        "请假规则：事假需提前申请，病假需医证",
    ]
    return docs


# ============ 3️⃣ 创建向量库 ============
docs = load_knowledge_base()
splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
chunks = splitter.split_text("\n".join(docs))

embeddings = DashScopeEmbeddings(model="text-embedding-v3")
vector_store = FAISS.from_texts(chunks, embeddings)

print(f"✅ 知识库加载成功，{len(chunks)} 个chunk")


# ============ 4️⃣ 综合查询：文档 + 数据库 ============
def answer_question(query):
    """
    综合查询：
    1. 从知识库检索相关文档
    2. 从数据库查询相关数据
    3. LLM 综合回答
    """

    print(f"\n🔍 查询: {query}")

    # 从知识库检索
    doc_results = vector_store.similarity_search(query, k=2)
    doc_context = "\n".join([doc.page_content for doc in doc_results])

    # 从数据库查询
    db_results = query_students()
    db_context = "\n".join([f"- {student['name']}: 班级={student['class']}, 成绩={student['grade']}"
                            for student in db_results[:3]])

    # LLM 综合回答
    llm = Tongyi()
    prompt = f"""你是一个学生管理助手。基于以下信息回答问题：

【知识库信息】
{doc_context}

【学生数据】
{db_context}

【问题】
{query}

请用简洁的中文回答。"""

    answer = llm.invoke(prompt)
    print(f"\n✅ 答案:\n{answer}")
    return answer


# ============ 5️⃣ 测试 ============
if __name__ == "__main__":

    # 测试1：只查知识库
    print("=" * 50)
    print("【测试1】查询成绩评分标准")
    print("=" * 50)
    answer_question("成绩怎样评分？")

    # 测试2：只查数据库
    print("\n" + "=" * 50)
    print("【测试2】查询学生信息")
    print("=" * 50)
    students = query_students()
    print(f"✅ 查询到 {len(students)} 个学生")
    for s in students[:3]:
        print(f"  - {s['name']}: {s['email']}")

    # 测试3：综合查询
    print("\n" + "=" * 50)
    print("【测试3】综合查询（知识库 + 数据库）")
    print("=" * 50)
    answer_question("我们学校有哪些学生？奖学金政策是什么？")