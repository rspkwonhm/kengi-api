import os
from fastapi import APIRouter, HTTPException
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# Azureの接続情報を環境変数から取得
AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
BLOB_CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME")

# ルーターを定義
router = APIRouter()

@router.get("/watershed")
async def get_watershed_geojson():
  try:
    # 取得するファイル名（パスを含む）
    file_name = "geojson/watershed.geojson"

    # BlobServiceClientのインスタンスを作成
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)

    # コンテナクライアントを取得
    container_client = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)

    # 指定したパスのBLOBクライアントを取得
    blob_client = container_client.get_blob_client(file_name)

    # BLOBデータをダウンロードして表示
    blob_data = blob_client.download_blob().readall()

    # JSONレスポンスとして返却
    return {"data": blob_data.decode("utf-8")}
  except Exception as e:
    # エラー処理
    raise HTTPException(status_code=500, detail=f"Failed to retrieve blob: {str(e)}")
