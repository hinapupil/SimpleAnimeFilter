import cv2
import numpy as np
from PIL import Image

def convert_to_anime_style(image: Image.Image) -> Image.Image:
    # PIL -> OpenCV (RGB->BGR)
    cv_image = np.array(image)
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)

    # 1) 彩度を上げる
    hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
    # 彩度(S)をX倍（必要に応じてパラメータ調整）
    saturation = 2
    hsv[..., 1] = np.clip(hsv[..., 1] * saturation, 0, 255)
    saturated = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # 2) エッジを保ったまま平滑化
    # sigma_s=60, sigma_r=0.4 あたりは要調整
    smooth = cv2.edgePreservingFilter(saturated, flags=1, sigma_s=60, sigma_r=0.4)

    # 3) ポスタリゼーション（ビット落とし）
    # 例えば 8 段階 (0-255を32刻みに) TODO: ここを level = 8 みたいにしていできるようにしたい。
    # チャンネルごとに (x // 32) * 32
    poster = (smooth // 32) * 32
    poster = np.clip(poster, 0, 255).astype(np.uint8)

    # 4) 線画抽出 (Canny)
    gray = cv2.cvtColor(poster, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)

    # 線画を反転しておく
    edges_inv = cv2.bitwise_not(edges)
    edges_inv_colored = cv2.cvtColor(edges_inv, cv2.COLOR_GRAY2BGR)

    # 5) 線画を重ねる
    # アルファブレンドでもOK。ここでは bitwise_and の例
    # (線が白い部分だけ残し、背景をポスター画像にする)
    anime_image = cv2.bitwise_and(poster, edges_inv_colored)

    # OpenCV -> PIL (BGR->RGB)
    anime_image = cv2.cvtColor(anime_image, cv2.COLOR_BGR2RGB)
    anime_pil = Image.fromarray(anime_image)
    return anime_pil

if __name__ == "__main__":
    # 画像を読み込み
    input_path = "IMG_3680.JPEG"
    image = Image.open(input_path)

    # アニメ調に変換
    anime_image = convert_to_anime_style(image)

    # 保存
    output_path = "out.png"
    anime_image.save(output_path)
    print(f"アニメ調画像を保存しました: {output_path}")
