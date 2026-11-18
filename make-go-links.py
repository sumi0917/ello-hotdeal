# -*- coding: utf-8 -*-
"""상품별 전용링크(go/*.html) + 미리보기 이미지(og/*) 생성기.

각 링크는 SNS 미리보기(og:image)에 그 상품의 표지 이미지가 뜨고,
사람이 누르면 바로 리틀리(https://litt.ly/ello)로 이동한다.

사용법 (리포 루트에서):
    python3 make-go-links.py
    # 이미지 원본 경로는 리포 기준 ../../(워크스페이스 루트)downloads/...
    python3 make-go-links.py --src-root ../../downloads
"""
import argparse
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://sumi0917.github.io/ello-hotdeal"
TARGET = "https://litt.ly/ello"
SIZE = 1080
MAX_BYTES = 800 * 1024

PRODUCTS = [
    dict(
        slug="ai-pack",
        title="[PDF] 하루 30분 AI 부업·블로그 스타터팩 (3,900원)",
        desc="왕초보도 따라 하는 하루 30분 수익화 로드맵 · 16쪽 실전 가이드 + 프롬프트",
        img="digital-product-starterpack/starterpack_cover.png",
    ),
    dict(
        slug="winter",
        title="[PDF] 겨울방학·크리스마스 엄마표 계획표 10종 (1,900원)",
        desc="하루 1장 프린트해서 바로 쓰는 겨울방학·크리스마스 활동지 14쪽 세트",
        img="digital-product-winter-kids/cover_sq.png",
    ),
    dict(
        slug="places",
        title="[PDF] 수도권 무료·가성비 아이체험 50곳 예약꿀팁집 (2,900원)",
        desc="무료 32곳·가성비 18곳 예약 오픈 시간, 주차 꿀팁 총정리 (39쪽)",
        img="digital-product-kids-places/cover_sq.png",
    ),
    dict(
        slug="math1-taste",
        title="[무료 PDF] 초1 2학기 수학 맛보기 문제집 (0원)",
        desc="핵심 개념부터 연습까지 부담 없이 시작하는 초1 수학 무료 학습지",
        img="digital-product-math-free/cover_sq.png",
    ),
    dict(
        slug="math1-rev",
        title="[무료 PDF] 초1 2학기 수학 복습 문제집 (21쪽 · 0원)",
        desc="1학년 2학기 전 단원 탄탄 복습 · 예비 2학년 겨울방학 무료 배포",
        img="digital-product-math-paid/g1_rev_cover_sq.png",
    ),
    dict(
        slug="math2-pre",
        title="[무료 PDF] 초2 1학기 수학 예습 문제집 (20쪽 · 0원)",
        desc="2학년 올라가기 전 미리 잡는 핵심 개념 · 무료 배포 학습지",
        img="digital-product-math-paid/g2_pre_cover_sq.png",
    ),
    dict(
        slug="math30",
        title="[PDF] 1학년 수학 총정리 30일 챌린지 68쪽 (41% 2,900원)",
        desc="예비 1학년부터 기초 다지는 2학년까지! 하루 2쪽 30일 완주 + 스티커 진도표",
        img="digital-product-math-30days/cover_sq.png",
    ),
]

PAGE = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{page_url}">

<!-- SNS 링크 미리보기 (스레드·카카오·X 등) -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="엘로 · 무료 학습지와 PDF">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{img_url}">
<meta property="og:image:secure_url" content="{img_url}">
<meta property="og:image:type" content="{img_type}">
<meta property="og:image:width" content="{img_w}">
<meta property="og:image:height" content="{img_h}">
<meta property="og:image:alt" content="{title}">
<meta property="og:url" content="{page_url}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{img_url}">

<!-- 누르면 바로 리틀리로 이동 -->
<meta http-equiv="refresh" content="0; url={target}">
<style>
  :root {{ color-scheme: light; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; min-height: 100vh; display: flex; align-items: center; justify-content: center;
         background: #f7f7f8; color: #1f1f1f; line-height: 1.55; word-break: keep-all;
         font-family: Pretendard, "Noto Sans KR", "Apple SD Gothic Neo", -apple-system, BlinkMacSystemFont, sans-serif; }}
  main {{ width: 100%; max-width: 360px; margin: 24px 18px; padding: 22px 20px 24px; background: #fff;
         border-radius: 18px; box-shadow: 0 6px 24px rgba(20, 30, 60, .08); text-align: center; }}
  img {{ width: 100%; height: auto; border-radius: 12px; display: block; }}
  h1 {{ margin: 16px 0 6px; font-size: 17px; font-weight: 800; letter-spacing: -.5px; }}
  p.sub {{ margin: 0 0 18px; font-size: 13px; color: #6b6b6b; letter-spacing: -.2px; }}
  a.go {{ display: flex; align-items: center; justify-content: center; min-height: 48px; padding: 12px 14px;
         border-radius: 12px; background: #1f1f1f; color: #fff; font-size: 15px; font-weight: 800;
         letter-spacing: -.3px; text-decoration: none; }}
  a.go:active {{ background: #333; }}
  p.note {{ margin: 14px 0 0; font-size: 11.5px; color: #9a9a9a; letter-spacing: -.1px; }}
</style>
</head>
<body>
<main>
  <img src="../og/{og_file}" alt="{title}" width="{img_w}" height="{img_h}">
  <h1>{title}</h1>
  <p class="sub">{desc}</p>
  <a class="go" href="{target}">리틀리 페이지로 이동하기</a>
  <p class="note">자동으로 넘어가지 않으면 위 버튼을 눌러 주세요.</p>
</main>
<script>window.location.replace("{target}");</script>
</body>
</html>
"""


def prepare_image(src, dst_dir, slug):
    """1080 정사각 PNG로 맞추고, 너무 무거우면 JPEG로 낮춘다. (파일명, w, h, type) 반환"""
    from PIL import Image

    im = Image.open(src)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        im = bg
    else:
        im = im.convert("RGB")

    if im.size != (SIZE, SIZE):
        # 비율 유지한 채 1080 정사각으로 꽉 채우고 가운데 자르기
        w, h = im.size
        scale = max(SIZE / w, SIZE / h)
        im = im.resize((max(SIZE, round(w * scale)), max(SIZE, round(h * scale))), Image.LANCZOS)
        left = (im.width - SIZE) // 2
        top = (im.height - SIZE) // 2
        im = im.crop((left, top, left + SIZE, top + SIZE))

    png = os.path.join(dst_dir, slug + ".png")
    im.save(png, "PNG", optimize=True)
    if os.path.getsize(png) <= MAX_BYTES:
        return slug + ".png", im.width, im.height, "image/png"

    os.remove(png)
    jpg = os.path.join(dst_dir, slug + ".jpg")
    quality = 90
    while quality >= 60:
        im.save(jpg, "JPEG", quality=quality, optimize=True, progressive=True)
        if os.path.getsize(jpg) <= MAX_BYTES:
            break
        quality -= 5
    return slug + ".jpg", im.width, im.height, "image/jpeg"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src-root", default=os.path.normpath(os.path.join(HERE, "..", "..", "downloads")))
    ap.add_argument("--out", default=HERE)
    args = ap.parse_args()

    go_dir = os.path.join(args.out, "go")
    og_dir = os.path.join(args.out, "og")
    os.makedirs(go_dir, exist_ok=True)
    os.makedirs(og_dir, exist_ok=True)

    for p in PRODUCTS:
        src = os.path.join(args.src_root, p["img"])
        if not os.path.exists(src):
            sys.exit("이미지 원본이 없습니다: %s" % src)
        og_file, w, h, mime = prepare_image(src, og_dir, p["slug"])
        page = PAGE.format(
            title=html.escape(p["title"], quote=True),
            desc=html.escape(p["desc"], quote=True),
            page_url="%s/go/%s.html" % (SITE, p["slug"]),
            img_url="%s/og/%s" % (SITE, og_file),
            img_type=mime,
            og_file=og_file,
            img_w=w,
            img_h=h,
            target=TARGET,
        )
        path = os.path.join(go_dir, p["slug"] + ".html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(page)
        print("wrote %-16s og/%s (%dx%d, %.0fKB)" % (
            "go/%s.html" % p["slug"], og_file, w, h, os.path.getsize(os.path.join(og_dir, og_file)) / 1024))


if __name__ == "__main__":
    main()
