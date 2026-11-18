#!/usr/bin/env bash
# 엘로 핫딜 페이지 배포: downloads/hotdeal-test 내용을 리포에 반영해 main과 gh-pages에 push
set -euo pipefail
SRC="${1:-../../downloads/hotdeal-test}"
REPO="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO"
rm -rf assets thumbs index.html
cp -r "$SRC/index.html" "$SRC/assets" "$SRC/thumbs" .
touch .nojekyll
git add -A
if git diff --cached --quiet; then
  echo "변경 없음"; exit 0
fi
git -c user.name=sumi0917 -c user.email="sm5915735@gmail.com" commit -m "엘로 핫딜 업데이트 $(TZ=Asia/Seoul date '+%Y-%m-%d %H:%M KST')"
git push origin main
git push origin main:gh-pages
