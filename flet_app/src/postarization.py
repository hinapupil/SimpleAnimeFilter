import cv2
import numpy as np
from PIL import Image

def postarization(image: Image.Image, saturation=2, level=8, smooth_strength=50, edge_strength=0.4) -> Image.Image:
    """
    画像をアニメ風に変換する関数
    :param image: 入力画像（PIL Image）
    :param saturation: 彩度の倍率
    :param level: ポスタリゼーションの色レベル
    :param smooth_strength: 平滑化の強さ（0-100）
    :param edge_strength: エッジ保持の強さ（0.0-1.0）
    :return: 変換後のアニメ調画像（PIL Image）
    """
    # PIL -> OpenCV (RGB->BGR)
    cv_image = np.array(image)
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)

    # 1) 彩度を上げる
    hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
    hsv[..., 1] = np.clip(hsv[..., 1] * saturation, 0, 255)
    saturated = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # 2) エッジを保ったまま平滑化（新しいパラメータ）
    sigma_s = smooth_strength  # 50以上でのっぺり感が増す
    sigma_r = max(0.01, edge_strength)  # 0.0にするとエラーになるので最小値を設定
    smooth = cv2.edgePreservingFilter(saturated, flags=1, sigma_s=sigma_s, sigma_r=sigma_r)

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