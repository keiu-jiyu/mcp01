import psycopg2

try:
    conn = psycopg2.connect(
        "postgresql://postgres.uuscdkzdqqcorvhgfudo:zjy2611450000@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres"
    )
    print("✅ 连接成功！")
    conn.close()
except Exception as e:
    print(f"❌ 连接失败: {e}")