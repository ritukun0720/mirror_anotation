import os
import shutil

def copy_json_and_png_pairs(source_dir, destination_dir):
    """
    指定されたソースディレクトリを再帰的に探索し、
    同名のJSONとPNGファイルのペアを宛先ディレクトリにコピーします。

    Args:
        source_dir (str): ファイルを探索する元のディレクトリ。
        destination_dir (str): 見つかったファイルをコピーする先のディレクトリ。
    """
    # コピー先ディレクトリが存在しない場合は作成する
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
        print(f"作成しました: '{destination_dir}'")

    copied_count = 0
    # os.walkでディレクトリツリーを再帰的に探索
    for dirpath, _, filenames in os.walk(source_dir):
        # 各ディレクトリ内のファイルをループ
        for filename in filenames:
            # ファイルが.jsonで終わるかチェック
            if filename.endswith('.json'):
                # 拡張子を除いたベース名を取得
                base_name = os.path.splitext(filename)[0]
                # 対応するPNGファイル名を作成
                png_filename = base_name + '.png'

                # 同じディレクトリ内に同名のPNGファイルが存在するかチェック
                if png_filename in filenames:
                    # --- ファイルパスの構築 ---
                    # 元のJSONファイルのフルパス
                    source_json_path = os.path.join(dirpath, filename)
                    # 元のPNGファイルのフルパス
                    source_png_path = os.path.join(dirpath, png_filename)

                    # --- ファイルのコピー ---
                    try:
                        # JSONファイルをコピー
                        shutil.copy2(source_json_path, destination_dir)
                        # PNGファイルをコピー
                        shutil.copy2(source_png_path, destination_dir)
                        
                        print(f"コピーしました: {filename} と {png_filename}")
                        copied_count += 1
                    except Exception as e:
                        print(f"エラー: {filename} または {png_filename} のコピー中にエラーが発生しました。 - {e}")

    if copied_count == 0:
        print("コピー対象のファイルペアは見つかりませんでした。")
    else:
        print(f"\n完了しました。合計 {copied_count} ペアのファイルをコピーしました。")

# --- ここから設定 ---

# 1. ファイルを探索するディレクトリを指定
SOURCE_DIRECTORY = './13. Kitchen'  # ← あなたの環境に合わせて変更してください

# 2. 見つかったファイルをコピーする先のディレクトリを指定
DESTINATION_DIRECTORY = './output' # ← あなたの環境に合わせて変更してください

# --- ここまで設定 ---

if __name__ == "__main__":
    # ディレクトリが存在するか確認
    if not os.path.isdir(SOURCE_DIRECTORY):
        print(f"エラー: 指定されたソースディレクトリ '{SOURCE_DIRECTORY}' が存在しません。")
    else:
        # 関数を実行
        copy_json_and_png_pairs(SOURCE_DIRECTORY, DESTINATION_DIRECTORY)