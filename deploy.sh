#!/usr/bin/env bash
# 엘로 핫딜 페이지 배포: downloads/hotdeal-test 내용을 리포에 반영해 main과 gh-pages에 push
#
# 주의: go/ (상품별 전용링크)와 og/ (링크 미리보기 이미지)는 이 스크립트가 만들지도 지우지도 않는다.
#       실수로 지워진 채 배포되는 일이 없도록 배포 전후에 존재 여부와 내용을 확인한다.
#       (go/·og/ 를 다시 만들려면: python3 make-go-links.py)
set -euo pipefail
SRC="${1:-../../downloads/hotdeal-test}"
REPO="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO"

# --- 보호 대상 확인 (배포 전) ---
if [ ! -d go ] || [ ! -d og ]; then
  echo "❌ go/ 또는 og/ 폴더가 없습니다. 전용링크를 먼저 복구하세요: python3 make-go-links.py" >&2
  exit 1
fi
GO_OG_BEFORE="$(find go og -type f -print0 | sort -z | xargs -0 md5sum | md5sum)"

# --- 핫딜 목록(index.html)만 갱신 ---
rm -rf assets thumbs index.html
cp -r "$SRC/index.html" "$SRC/assets" "$SRC/thumbs" .
touch .nojekyll

# --- 보호 대상 확인 (배포 후) ---
if [ ! -d go ] || [ ! -d og ]; then
  echo "❌ 배포 준비 중 go/ 또는 og/ 가 사라졌습니다. 중단합니다." >&2
  exit 1
fi
GO_OG_AFTER="$(find go og -type f -print0 | sort -z | xargs -0 md5sum | md5sum)"
if [ "$GO_OG_BEFORE" != "$GO_OG_AFTER" ]; then
  echo "❌ go/ 또는 og/ 내용이 배포 중에 바뀌었습니다. 중단합니다." >&2
  exit 1
fi

git add -A
if git diff --cached --quiet; then
  echo "변경 없음"; exit 0
fi
git -c user.name=sumi0917 -c user.email="sm5915735@gmail.com" commit -m "엘로 핫딜 업데이트 $(TZ=Asia/Seoul date '+%Y-%m-%d %H:%M KST')"
git push origin main
git push origin main:gh-pages
