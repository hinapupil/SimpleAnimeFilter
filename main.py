import os
import cv2
import numpy as np
from PIL import Image

def convert_to_anime_style(image: Image.Image, saturation=2, level=8) -> Image.Image:
    """
    画像をアニメ風に変換する関数
    :param image: 入力画像（PIL Image）
    :param saturation: 彩度の倍率（デフォルト 2）
    :param level: ポスタリゼーションの色レベル（デフォルト 8）
    :return: 変換後のアニメ調画像（PIL Image）
    """
    # PIL -> OpenCV (RGB->BGR)
    cv_image = np.array(image)
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)

    # 1) 彩度を上げる
    hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
    hsv[..., 1] = np.clip(hsv[..., 1] * saturation, 0, 255)
    saturated = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # 2) エッジを保ったまま平滑化
    smooth = cv2.edgePreservingFilter(saturated, flags=1, sigma_s=60, sigma_r=0.4)

    # 3) ポスタリゼーション（ビット落とし）
    step = 256 // level  # 色レベルに応じた量子化ステップ
    poster = (smooth // step) * step
    poster = np.clip(poster, 0, 255).astype(np.uint8)

    # 4) 線画抽出 (Canny)
    gray = cv2.cvtColor(poster, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)

    # 線画を反転しておく
    edges_inv = cv2.bitwise_not(edges)
    edges_inv_colored = cv2.cvtColor(edges_inv, cv2.COLOR_GRAY2BGR)

    # 5) 線画を重ねる
    anime_image = cv2.bitwise_and(poster, edges_inv_colored)

    # OpenCV -> PIL (BGR->RGB)
    return Image.fromarray(cv2.cvtColor(anime_image, cv2.COLOR_BGR2RGB))

if __name__ == "__main__":
    input_dir = "./input"
    output_dir = "./output"

    # 出力フォルダを作成（既にあればスキップ）
    os.makedirs(output_dir, exist_ok=True)

    # 画像ファイルの拡張子リスト
    valid_extensions = (".jpg", ".jpeg", ".png", ".bmp")

    # `./input/` 内のすべての画像を処理
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(valid_extensions):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            print(f"Processing: {input_path} -> {output_path}")

            # 画像を読み込み
            image = Image.open(input_path)

            # アニメ調に変換（彩度2倍、ポスタリゼーション8レベル）
            anime_image = convert_to_anime_style(image, saturation=2, level=8)

            # 保存
            anime_image.save(output_path)

    print(f"✅ すべての画像を {output_dir} に保存しました！")
