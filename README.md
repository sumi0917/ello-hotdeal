# 엘로 핫딜

구매 없이 참여하는 무료응모·혜택 모음 페이지입니다.

- 공개 주소: https://sumi0917.github.io/ello-hotdeal/
- 배포 방식: GitHub Pages (**`gh-pages` 브랜치 / 루트**를 배포 소스로 사용)
- `main` 브랜치는 작업용 사본입니다. **페이지에 반영하려면 `gh-pages` 브랜치에도 push해야 합니다.**

```bash
git push origin main
git push origin main:gh-pages
```

## 상품별 전용링크 (`go/`)

스레드·카카오 등에 붙이면 **그 상품의 표지 이미지가 링크 미리보기(og:image)로 뜨고, 누르면 바로 `https://litt.ly/ello`로 이동**하는 링크입니다.

| 상품 | 링크 | 미리보기 이미지 |
| --- | --- | --- |
| 1호 AI 부업·블로그 스타터팩 (3,900원) | https://sumi0917.github.io/ello-hotdeal/go/ai-pack.html | `og/ai-pack.png` |
| 2호 겨울방학·크리스마스 계획표 10종 (1,900원) | https://sumi0917.github.io/ello-hotdeal/go/winter.html | `og/winter.png` |
| 3호 수도권 아이체험 50곳 꿀팁집 (2,900원) | https://sumi0917.github.io/ello-hotdeal/go/places.html | `og/places.png` |
| 4호 초1 2학기 수학 맛보기 (무료) | https://sumi0917.github.io/ello-hotdeal/go/math1-taste.html | `og/math1-taste.png` |
| 5호 초1 2학기 수학 복습 (무료) | https://sumi0917.github.io/ello-hotdeal/go/math1-rev.html | `og/math1-rev.png` |
| 6호 초2 1학기 수학 예습 (무료) | https://sumi0917.github.io/ello-hotdeal/go/math2-pre.html | `og/math2-pre.png` |
| 7호 1학년 수학 총정리 30일 챌린지 (2,900원) | https://sumi0917.github.io/ello-hotdeal/go/math30.html | `og/math30.png` |
| 8호 초등 2학년 수학 1년 총정리 (80쪽·2,900원) | https://sumi0917.github.io/ello-hotdeal/go/math2-year.html | `og/math2-year.png` |

- 8호는 1~7호와 달리 이동 위치가 `https://litt.ly/ello`가 아니라 초2 블럭 판매 페이지 `https://litt.ly/ello/sale/esdKvdP` 입니다.
- `go/*.html`·`og/*` 를 다시 만들려면 리포 루트에서 `python3 make-go-links.py` (하나만: `python3 make-go-links.py --only math2-year`)
- `deploy.sh`는 `go/`·`og/` 를 지우지 않으며, 배포 전후에 내용이 같은지 확인하고 다르면 중단합니다.
