import logging  # これを追加！
def run_query(query: str):
    logging.info("--- 検索と生成を開始します ---")
    try:
        # 1. 検索（リトリーバー）
        # ※ model_nameなどは上で定義したものと同じであることを確認してください
        model_name = "all-MiniLM-L6-v2"
        embeddings = HuggingFaceEmbeddings(model_name=model_name)
        vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
        
        # 検索の実行
        docs = vectorstore.similarity_search(query, k=3)
        context_text = "\n\n".join([d.page_content for d in docs])

        # 2. Google AI Studio のコードで回答生成
        from google import genai
        # APIキーが環境変数 GEMINI_API_KEY に入っている必要があります
        client = genai.Client()
        
        # 資料(context_text)を組み込んだプロンプト
        prompt_text = f"""以下の資料に基づいて日本語で回答してください。
資料にないことは「分かりません」と答えてください。

資料:
{context_text}

質問: {query}"""

        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt_text
        )
        
        answer = response.text
        
        # 3. 結果の保存とログ
        # 保存先をカレントディレクトリではなく、マウント先の /app に固定する
        # これにより、ホスト側のフォルダに確実に同期されます
        output_file = pathlib.Path("/app/answer.txt") 
        output_file.write_text(answer, encoding="utf-8")
        logging.info(f"[成功] 回答を'{output_file}'に保存しました。")
        print(f"\n--- 生成された回答 ---\n{answer}")
        
        print("\n" + "="*50)
        print("【Gemini からの回答】")
        print(answer)
        print("="*50 + "\n")
        logging.info(f"[成功] AI StudioのSDKで回答を生成しました。")
        return answer

    except Exception as e:
        # 既存のエラー処理
        error_file = pathlib.Path("error_log.txt")
        error_msg = traceback.format_exc()
        error_file.write_text(error_msg, encoding="utf-8")
        logging.error(f"実行中にエラーが発生しました。詳細は {error_file} を参照してください。")
        raise