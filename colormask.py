import os
import json
from PIL import Image, ImageDraw
import numpy as np
import glob

# --- 設定項目 ---

# 1. 元の画像が入っているディレクトリのパス
IMAGE_DIR = "./rgb" 

# 2. labelmeのJSONファイルが入っているディレクトリのパス
JSON_DIR = "./json"

# 3. 色分けした画像を保存するディレクトリのパス
OUTPUT_DIR = "./color_mask"

# 4. ラベルと色の対応を定義 (R, G, B, A)
# A (アルファ値)は透明度です。0で完全に透明、255で完全に不透明になります。
# 128に設定すると半透明になり、下の元画像が見やすくなります。
LABEL_COLOR_MAP = {
    'mirror':        (255, 0, 0, 128),      # 赤
    'glass':         (0, 0, 255, 128),      # 青
    'mirror object': (0, 255, 0, 128),      # 緑
    'other':         (255, 255, 0, 128),    # 黄
    # もし上記以外のラベルがあった場合のデフォルト色
    '_default_':     (128, 128, 128, 128)   # 灰色
}

# --- スクリプト本体 ---

def create_visualized_image(json_path, image_dir, output_dir):
    """
    一つのJSONファイルと対応する画像から、色分けされたアノテーション画像を生成する
    """
    try:
        # JSONファイルを読み込む
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 対応する画像ファイルパスを取得
        # JSONファイル内の 'imagePath' を使うのが確実
        image_filename = data['imagePath']
        image_path = os.path.join(image_dir, image_filename)

        if not os.path.exists(image_path):
            print(f"警告: 画像ファイルが見つかりません: {image_path}")
            # もし 'imagePath' が相対パスの場合を考慮して、JSONファイルと同じ場所も探す
            base_json_dir = os.path.dirname(json_path)
            image_path = os.path.join(base_json_dir, image_filename)
            if not os.path.exists(image_path):
                print(f"再試行失敗: {image_path}")
                return

        # 元画像をRGBAモードで開く (アルファブレンディングのため)
        base_image = Image.open(image_path).convert('RGBA')

        # 元画像と同じサイズの透明なレイヤーを作成
        overlay = Image.new('RGBA', base_image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)

        # JSON内の各アノテーション（シェイプ）を処理
        for shape in data['shapes']:
            label = shape['label']
            points = shape['points']
            
            # shape_typeが 'polygon' のものだけを対象とする
            if shape['shape_type'] != 'polygon':
                continue

            # ラベルに対応する色を取得
            color = LABEL_COLOR_MAP.get(label, LABEL_COLOR_MAP['_default_'])
            
            # Pillowのpolygon描画用に点のリストをタプルのリストに変換
            points_tuples = [tuple(p) for p in points]
            
            # ポリゴンを描画
            draw.polygon(points_tuples, fill=color)

        # 元画像と描画したレイヤーを合成
        visualized_image = Image.alpha_composite(base_image, overlay)
        
        # 保存するファイルパスを生成
        # 出力ファイル名は元画像のファイル名に '_visualized.png' をつける
        base_filename = os.path.basename(image_path)
        name, ext = os.path.splitext(base_filename)
        output_filename = f"{name}_visualized.png"
        output_path = os.path.join(output_dir, output_filename)

        # 画像を保存 (PNG形式で保存すると透明度情報が維持される)
        visualized_image.save(output_path)
        print(f"生成完了: {output_path}")

    except Exception as e:
        print(f"エラーが発生しました ({json_path}): {e}")


def main():
    """
    メイン処理
    """
    # 出力ディレクトリがなければ作成
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # JSONディレクトリ内のすべてのJSONファイルを取得
    json_files = glob.glob(os.path.join(JSON_DIR, '*.json'))

    if not json_files:
        print(f"エラー: '{JSON_DIR}' ディレクトリにJSONファイルが見つかりません。")
        return

    # 各JSONファイルに対して処理を実行
    for json_path in json_files:
        create_visualized_image(json_path, IMAGE_DIR, OUTPUT_DIR)

if __name__ == '__main__':
    main()