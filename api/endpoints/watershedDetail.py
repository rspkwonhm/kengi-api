import os
from fastapi import APIRouter, HTTPException
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# Azure Blob Storage接続情報を取得
AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
BLOB_CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME")

# ルーターを定義
router = APIRouter()

def get_blob_file_name(three_digit_code: str, suffix1: str = None, suffix2: str = None) -> str:
    """指定された引数に基づいてファイル名を構成する"""
    # 基本ファイル名を作成
    file_name = f"geojson/1{three_digit_code}_geojson/1{three_digit_code}"
    
    # suffix1, suffix2 が指定されている場合、それぞれに `_suffix` を追加
    if suffix1:
        file_name += f"_{suffix1}"
    if suffix2:
        file_name += f"_{suffix2}"
    
    # ファイル名に拡張子を追加
    file_name += ".geojson"
    
    return file_name

def download_blob(three_digit_code: str, suffix1: str = None, suffix2: str = None):
  try:
    # BlobServiceClientのインスタンスを作成
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    
    # コンテナクライアントを取得
    container_client = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)
    
    # ファイル名を構成
    blob_name = get_blob_file_name(three_digit_code, suffix1, suffix2)
    
    # 指定したファイル名でBLOBを取得
    blob_client = container_client.get_blob_client(blob_name)
    
    # BLOBデータをダウンロード
    blob_data = blob_client.download_blob().readall()
    return blob_data.decode("utf-8")
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Failed to download blob: {str(e)}")

@router.get("/raindata/{three_digit_code}", tags=["集水域等の流域取得"])
async def get_files_in_directory(three_digit_code: str):
  # 入力が3桁の数値であることを確認
  if not (three_digit_code.isdigit() and len(three_digit_code) == 3):
    raise HTTPException(status_code=400, detail="The code must be a 3-digit number.")
  
  files = get_files_in_directory(three_digit_code)
  return {"files": files}
