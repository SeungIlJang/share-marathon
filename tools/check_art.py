"""모두의 마라톤 — 아트 납품 검수 도구.

ART-PROMPTS.md 규격대로 만들어졌는지 파일마다 확인하고, 합격한 파일만 게임용 폴더(art/)로 옮겨 목록(assets.json)을 만든다.

사용법 (share-marathon 폴더에서):
  python tools/check_art.py D:/AI/workspace/game/images/marathon            # 검수만
  python tools/check_art.py D:/AI/workspace/game/images/marathon --install  # 합격분을 art/ 로 복사 + assets.json 생성
  python tools/check_art.py <폴더> --preview <출력폴더>                      # 러너 시트의 '빨강→파랑' 미리보기 저장

배포는 art/ 폴더 내용을 games/marathon/ 에 올리면 된다(게임이 그 주소의 assets.json 을 읽음).
"""
import json
import os
import shutil
import sys
import time

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRAMES, CELL_W, CELL_H = 14, 247, 309
SIZE_BUDGET = {'runner': 400_000, 'bg': 350_000, 'item': 60_000, 'other': 250_000}   # 권장 최대 용량(바이트)


def is_red(r, g, b):
    """게임(uniformTint)이 '유니폼 빨강'으로 보는 픽셀과 같은 판정."""
    r, g, b = r / 255, g / 255, b / 255
    mx, mn = max(r, g, b), min(r, g, b)
    d = mx - mn
    if d < 0.25 or mx != r:
        return False
    h = ((g - b) / d) % 6 * 60
    if h < 0:
        h += 360
    return h <= 18 or h >= 340


def check_runner(im, name):
    err, warn, info = [], [], []
    if im.size != (FRAMES * CELL_W, CELL_H):
        err.append(f"크기 {im.size[0]}x{im.size[1]} — {FRAMES * CELL_W}x{CELL_H} 이어야 함")
        return err, warn, info
    im = im.convert('RGBA')
    a = im.getchannel('A')
    if a.getextrema()[0] > 0:
        err.append("투명 배경이 아님(알파 최소값 > 0)")
    bottoms, tops, widths, reds, opaque = [], [], [], 0, 0
    px = im.load()
    for f in range(FRAMES):
        cell = im.crop((f * CELL_W, 0, (f + 1) * CELL_W, CELL_H))
        bb = cell.getchannel('A').point(lambda v: 255 if v > 40 else 0).getbbox()
        if not bb:
            err.append(f"{f + 1}번 칸이 비어 있음")
            continue
        bottoms.append(bb[3]); tops.append(bb[1]); widths.append(bb[2] - bb[0])
        if bb[0] <= 0 or bb[2] >= CELL_W:
            warn.append(f"{f + 1}번 칸: 그림이 칸 좌우 끝에 닿음(잘렸을 수 있음)")
    for y in range(0, CELL_H, 2):
        for x in range(0, FRAMES * CELL_W, 2):
            r, g, b, al = px[x, y]
            if al > 60:
                opaque += 1
                if is_red(r, g, b):
                    reds += 1
    if bottoms:
        # 달리기는 공중에 뜨는 칸이 있으므로, 가장 낮은 발 위치(지면)가 칸마다 크게 다르지 않은지 본다
        ground = max(bottoms)
        info.append(f"지면선 y={ground} (칸 아래에서 {CELL_H - ground}px), 칸별 최저점 범위 {min(bottoms)}~{max(bottoms)}")
        if CELL_H - ground > 24 or CELL_H - ground < 2:
            warn.append(f"지면선이 칸 아래에서 {CELL_H - ground}px — 권장 약 8px")
        if max(bottoms) - min(bottoms) > 46:
            warn.append(f"칸별 발 높이 차이가 큼({max(bottoms) - min(bottoms)}px) — 캐릭터가 위아래로 튈 수 있음")
        if max(tops) - min(tops) > 40:
            warn.append(f"칸별 머리 높이 차이가 큼({max(tops) - min(tops)}px)")
    ratio = reds / max(1, opaque)
    info.append(f"빨강 픽셀 비율 {ratio * 100:.1f}% (기존 러너 시트는 약 29%)")
    if ratio < 0.04:
        err.append("빨강이 거의 없음 — 머리띠·소매·신발이 순수한 빨강인지 확인(게임이 색을 못 바꿈)")
    elif ratio > 0.40:
        warn.append("빨강이 너무 많음 — 피부·머리카락·볼터치에 빨강 계열이 섞였을 수 있음(--preview 로 확인)")
    return err, warn, info


def check_bg(im, name):
    err, warn, info = [], [], []
    if im.size != (2048, 512):
        err.append(f"크기 {im.size[0]}x{im.size[1]} — 2048x512 이어야 함")
        return err, warn, info
    im = im.convert('RGBA')
    px = im.load()
    # 좌우 이음매: 맨 왼쪽 열과 맨 오른쪽 열이 비슷해야 이어 붙였을 때 티가 안 남
    diff = 0
    for y in range(512):
        l, r = px[0, y], px[2047, y]
        diff += sum(abs(l[i] - r[i]) for i in range(4))
    seam = diff / (512 * 4)
    info.append(f"좌우 이음매 차이 {seam:.1f} (0에 가까울수록 좋음)")
    if seam > 28:
        warn.append("좌우 끝이 많이 다름 — 가로로 이어 깔면 경계가 보일 수 있음")
    top_alpha = sum(px[x, 4][3] for x in range(0, 2048, 16)) / 128
    if top_alpha > 30:
        warn.append("위쪽 하늘이 투명하지 않음 — 게임의 날씨·시간대 하늘이 가려짐")
    return err, warn, info


def check_square(size):
    def f(im, name):
        err, warn, info = [], [], []
        if im.size != size:
            err.append(f"크기 {im.size[0]}x{im.size[1]} — {size[0]}x{size[1]} 이어야 함")
            return err, warn, info
        a = im.convert('RGBA').getchannel('A')
        if a.getextrema()[0] > 0:
            err.append("투명 배경이 아님")
        bb = a.point(lambda v: 255 if v > 40 else 0).getbbox()
        if bb and (bb[0] <= 1 or bb[1] <= 1 or bb[2] >= size[0] - 1 or bb[3] >= size[1] - 1):
            warn.append("그림이 가장자리에 닿음(여백 없음)")
        return err, warn, info
    return f


def check_opaque(size):
    def f(im, name):
        err = [] if im.size == size else [f"크기 {im.size[0]}x{im.size[1]} — {size[0]}x{size[1]} 이어야 함"]
        return err, [], []
    return f


def rule_for(name):
    """(종류, 검사 함수, 게임에 올리는 파일인지)"""
    if name.startswith('runner-'):
        return 'runner', check_runner, True
    if name.startswith('bg-'):
        return 'bg', check_bg, True
    if name.startswith('item-'):
        return 'item', check_square((256, 256)), True
    if name == 'aid-station.png':
        return 'other', check_square((600, 200)), False      # 게임 슬롯 아직 없음
    if name.startswith('crowd-'):
        return 'other', check_square((1024, 160)), False
    if name == 'finish-arch.png':
        return 'other', check_square((400, 420)), False
    if name == 'feature-1024x500.png':
        return 'other', check_opaque((1024, 500)), False     # 스토어용
    if name == 'icon-512.png':
        return 'other', check_opaque((512, 512)), False
    return None, None, False


def save_preview(im, out_path):
    """빨강 판정 픽셀을 파랑으로 바꾼 미리보기 — 피부·머리가 파랗게 변하면 색 규칙 위반."""
    im = im.convert('RGBA')
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a > 20 and is_red(r, g, b):
                px[x, y] = (40, 110, 255, a)
    im.save(out_path)


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')   # Windows 콘솔(cp949)에서도 기호·한글이 깨지지 않게
    except Exception:
        pass
    args = sys.argv[1:]
    if not args or args[0].startswith('-'):
        print(__doc__)
        return 2
    src = args[0]
    install = '--install' in args
    preview_dir = args[args.index('--preview') + 1] if '--preview' in args else None
    files = sorted(f for f in os.listdir(src) if f.lower().endswith('.png'))
    if not files:
        print("PNG 파일이 없습니다:", src)
        return 2
    passed, failed = [], 0
    for name in files:
        kind, fn, in_game = rule_for(name)
        path = os.path.join(src, name)
        if not fn:
            print(f"[??] {name} — ART-PROMPTS.md 에 없는 파일명(건너뜀)")
            continue
        im = Image.open(path)
        err, warn, info = fn(im, name)
        size = os.path.getsize(path)
        if size > SIZE_BUDGET[kind]:
            warn.append(f"용량 {size // 1024}KB — 권장 {SIZE_BUDGET[kind] // 1024}KB 이하(색 수를 줄여 압축 권장)")
        mark = '불합격' if err else ('주의' if warn else '합격')
        print(f"[{mark}] {name} ({im.size[0]}x{im.size[1]}, {size // 1024}KB)")
        for e in err:
            print("    ✖", e)
        for w in warn:
            print("    ⚠", w)
        for i in info:
            print("    ·", i)
        if err:
            failed += 1
        elif in_game:
            passed.append(name)
        if preview_dir and kind == 'runner' and not err:
            os.makedirs(preview_dir, exist_ok=True)
            save_preview(im, os.path.join(preview_dir, name.replace('.png', '-recolor-preview.png')))
    print(f"\n합계: 게임 반영 가능 {len(passed)}개, 불합격 {failed}개")
    if install:
        dst = os.path.join(ROOT, 'art')
        os.makedirs(dst, exist_ok=True)
        for name in passed:
            shutil.copyfile(os.path.join(src, name), os.path.join(dst, name))
        listed = sorted(f for f in os.listdir(dst) if f.lower().endswith('.png'))
        with open(os.path.join(dst, 'assets.json'), 'w', encoding='utf-8') as fh:
            json.dump({'v': int(time.time()), 'files': listed}, fh, ensure_ascii=False, indent=1)
        print(f"art/ 로 {len(passed)}개 복사, assets.json 에 {len(listed)}개 기록 — 배포하려면 art/ 내용을 games/marathon/ 에 올리세요")
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
