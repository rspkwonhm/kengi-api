import os
from fastapi import HTTPException
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from datetime import datetime

# 環境変数の読み込み
load_dotenv()

# Azure接続情報を取得
AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
BLOB_CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME")

def rainfall_record_data_list_search(fromString: str, toString: str, three_digit_code: str, suffix1: str = None, suffix2: str = None):
  try:
    # 取得するディレクトリのパスを構成
    base_path = f"raindata/01_thiessen/1{three_digit_code}"
    if suffix1:
      base_path += f"_{suffix1}"
    if suffix2:
      base_path += f"_{suffix2}"

    # fromString と toString を日付形式に変換
    from_date = datetime.strptime(fromString, "%Y%m%d%H%M")
    to_date = datetime.strptime(toString, "%Y%m%d%H%M")

    # BlobServiceClientのインスタンスを作成
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    
    # コンテナクライアントを取得
    container_client = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)

    # 指定ディレクトリのBLOBリストを取得
    blob_list = container_client.list_blobs(name_starts_with=base_path)

    # ファイル名をフィルタリング
    files_in_range = []
    for blob in blob_list:
      date_str = blob.name.split("_")[-1].replace(".csv", "")
      file_date = datetime.strptime(date_str, "%Y%m%d%H%M")

      # 日付範囲に一致するファイルのみを追加
      if from_date <= file_date <= to_date:
        files_in_range.append(blob.name)

    # JSONレスポンスとして返却
    return {"files": files_in_range}
  except Exception as e:
    # エラー処理
    raise HTTPException(status_code=500, detail=f"Failed to retrieve files: {str(e)}")
