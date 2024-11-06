import os
from fastapi import APIRouter, HTTPException
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# 確認用のprint
print("テスト:", os.getenv("AZURE_CONNECTION_STRING"))

# Azureの接続情報を環境変数から取得
AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
BLOB_CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME")

# ルーターを定義
router = APIRouter()

# BlobServiceClientのインスタンスを作成
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)

@router.get("/watershedMaster", tags=["流域マスタを取得"])
async def get_watershedMaster_geojson():
  try:
    # 取得するファイル名を関数内で指定
    file_name = ""

    # BlobServiceClientのインスタンスを作成
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)

    # コンテナクライアントを取得
    container_client = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)

    # 指定したファイル名でBLOBクライアントを取得
    blob_client = container_client.get_blob_client(file_name)

    # BLOBデータをダウンロードして表示
    blob_data = blob_client.download_blob().readall()


    # JSONレスポンスとして返却
    return {"data": blob_data.decode("utf-8")}
  except Exception as e:
    # エラー処理
    raise HTTPException(status_code=500, detail=str(e))
