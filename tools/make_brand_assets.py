"""모두의 마라톤 — 앱 아이콘·스플래시·스토어 이미지 생성기.

runner-sprite.png(14프레임 러닝 스프라이트)에서 러너를 잘라 하늘·트랙 배경과 합성한다.
사용법:  python tools/make_brand_assets.py   (share-marathon 폴더에서 실행)
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, 'android', 'app', 'src', 'main', 'res')
STORE = os.path.join(ROOT, 'store-assets')
SPRITE = os.path.join(ROOT, 'runner-sprite.png')
FONT_B = 'C:/Windows/Fonts/malgunbd.ttf'
SKY_TOP, SKY_BOT = (110, 196, 255), (214, 239, 255)
GRASS, TRACK, LINE = (127, 206, 137), (91, 100, 114), (233, 239, 246)
CELL_W, CELL_H, FRAMES = 247, 309, 14


def runner(frame=4, tint=None):
    """스프라이트 한 프레임을 잘라 투명 여백을 걷어낸 RGBA 이미지."""
    sheet = Image.open(SPRITE).convert('RGBA')
    fw = sheet.width // FRAMES
    im = sheet.crop((frame * fw, 0, (frame + 1) * fw, sheet.height))
    im = im.crop(im.getbbox())
    if tint:
        layer = Image.new('RGBA', im.size, tint + (0,))
        a = im.getchannel('A').point(lambda v: int(v * 0.55))
        layer.putalpha(a)
        im = Image.alpha_composite(im, layer)
    return im


def fit(im, h):
    return im.resize((max(1, round(im.width * h / im.height)), h), Image.LANCZOS)


def sky(w, h, ground_y=None):
    """하늘 그라데이션 + 해 + (선택) 잔디·트랙."""
    bg = Image.new('RGBA', (w, h))
    d = ImageDraw.Draw(bg)
    gy = ground_y if ground_y is not None else h
    for y in range(h):
        t = min(1, y / max(1, gy))
        d.line([(0, y), (w, y)], fill=tuple(round(SKY_TOP[i] + (SKY_BOT[i] - SKY_TOP[i]) * t) for i in range(3)) + (255,))
    r = round(min(w, h) * 0.11)
    d.ellipse([round(w * 0.16) - r, round(h * 0.2) - r, round(w * 0.16) + r, round(h * 0.2) + r], fill=(255, 224, 138, 255))
    if ground_y is not None:
        d.rectangle([0, gy, w, gy + round(h * 0.035)], fill=GRASS + (255,))
        d.rectangle([0, gy + round(h * 0.035), w, h], fill=TRACK + (255,))
        lw = max(2, round(h * 0.012))
        ly = gy + round((h - gy) * 0.55)
        seg = round(w * 0.12)
        for x in range(-seg // 2, w, seg * 2):
            d.rectangle([x, ly, x + seg, ly + lw], fill=LINE + (255,))
    return bg


def speed_lines(img, x, y, h, n=3):
    d = ImageDraw.Draw(img)
    lw = max(2, round(h * 0.035))
    for i in range(n):
        yy = y + round(h * (0.3 + i * 0.16))
        ln = round(h * (0.42 - i * 0.08))
        d.rounded_rectangle([x - ln, yy, x, yy + lw], radius=lw // 2, fill=(255, 255, 255, 210))


def place(base, im, cx, foot_y):
    """발이 foot_y에 닿도록 중앙 정렬 + 그림자."""
    sh = Image.new('RGBA', base.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse([cx - im.width * 0.38, foot_y - im.height * 0.035, cx + im.width * 0.38, foot_y + im.height * 0.035], fill=(0, 0, 0, 60))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(max(1, im.height // 60))))
    base.alpha_composite(im, (round(cx - im.width / 2), round(foot_y - im.height)))


def full_icon(size, frame=4, run_h=0.72):
    """정사각 풀블리드 아이콘(스토어 512 / 레거시 런처 원본)."""
    img = sky(size, size, ground_y=round(size * 0.80))
    r = fit(runner(frame), round(size * run_h))
    speed_lines(img, round(size * 0.5 - r.width * 0.36), round(size * 0.80 - r.height), r.height)
    place(img, r, size * 0.53, size * 0.86)
    return img


def rounded(img, radius_ratio=0.22, circle=False):
    m = Image.new('L', img.size, 0)
    d = ImageDraw.Draw(m)
    if circle:
        d.ellipse([0, 0, img.width - 1, img.height - 1], fill=255)
    else:
        d.rounded_rectangle([0, 0, img.width - 1, img.height - 1], radius=round(img.width * radius_ratio), fill=255)
    out = img.copy()
    out.putalpha(m)
    return out


def text(d, xy, s, size, fill, stroke=0, anchor='mm'):
    f = ImageFont.truetype(FONT_B, size)
    d.text(xy, s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(255, 255, 255, 255), anchor=anchor)


def splash(w, h):
    port = h >= w
    gy = round(h * (0.70 if port else 0.74))
    img = sky(w, h, ground_y=gy)
    rh = round((h if port else h) * (0.26 if port else 0.40))
    r = fit(runner(4), rh)
    cx = w * 0.5 if port else w * 0.30
    speed_lines(img, round(cx - r.width * 0.36), gy - r.height + round(rh * 0.04), r.height)
    place(img, r, cx, gy + round(h * 0.05))
    d = ImageDraw.Draw(img)
    s = min(w, h)
    if port:
        text(d, (w / 2, h * 0.30), '모두의 마라톤', round(s * 0.11), (43, 58, 74, 255), stroke=max(2, round(s * 0.012)))
        text(d, (w / 2, h * 0.37), '리듬 런 · 레이스', round(s * 0.05), (95, 113, 134, 255))
    else:
        text(d, (w * 0.66, h * 0.38), '모두의 마라톤', round(s * 0.13), (43, 58, 74, 255), stroke=max(2, round(s * 0.014)))
        text(d, (w * 0.66, h * 0.52), '리듬 런 · 레이스', round(s * 0.06), (95, 113, 134, 255))
    return img.convert('RGB')


def feature():
    w, h = 1024, 500
    img = sky(w, h, ground_y=360)
    for col, x, fr in [((255, 176, 32), 70, 2), ((63, 160, 255), 165, 9)]:
        place(img, fit(runner(fr, tint=col), 170), x, 425)
    me = fit(runner(4), 240)
    place(img, me, 330, 440)
    d = ImageDraw.Draw(img)
    text(d, (705, 165), '모두의 마라톤', 70, (43, 58, 74, 255), stroke=6)
    text(d, (705, 240), '음악에 맞춰 달리고, 10명과 겨뤄라!', 28, (43, 58, 74, 255), stroke=3)
    for i, (lbl, col) in enumerate([('리듬 런', (154, 92, 255)), ('레이스', (255, 111, 156))]):
        x0 = 545 + i * 175
        d.rounded_rectangle([x0, 285, x0 + 150, 335], radius=25, fill=col + (255,))
        text(d, (x0 + 75, 310), lbl, 26, (255, 255, 255, 255))
    return img.convert('RGB')


def main():
    os.makedirs(STORE, exist_ok=True)
    full_icon(512).convert('RGB').save(os.path.join(STORE, 'icon-512.png'))
    feature().save(os.path.join(STORE, 'feature-1024x500.png'))
    master = full_icon(1024)
    dens = {'mdpi': 1, 'hdpi': 1.5, 'xhdpi': 2, 'xxhdpi': 3, 'xxxhdpi': 4}
    for name, k in dens.items():
        d = os.path.join(RES, 'mipmap-' + name)
        leg = round(48 * k)
        rounded(master.resize((leg, leg), Image.LANCZOS)).save(os.path.join(d, 'ic_launcher.png'))
        rounded(master.resize((leg, leg), Image.LANCZOS), circle=True).save(os.path.join(d, 'ic_launcher_round.png'))
        ad = round(108 * k)                                # 적응형 아이콘: 108dp 캔버스, 중앙 66dp 안전영역
        bg = sky(ad, ad, ground_y=round(ad * 0.70))
        bg.save(os.path.join(d, 'ic_launcher_bg.png'))
        fg = Image.new('RGBA', (ad, ad), (0, 0, 0, 0))
        r = fit(runner(4), round(ad * 0.50))
        speed_lines(fg, round(ad * 0.5 - r.width * 0.36), round(ad * 0.73 - r.height), r.height)
        place(fg, r, ad * 0.53, ad * 0.75)
        fg.save(os.path.join(d, 'ic_launcher_foreground.png'))
    for sub in os.listdir(RES):
        p = os.path.join(RES, sub, 'splash.png')
        if os.path.exists(p):
            w, h = Image.open(p).size
            splash(w, h).save(p)
    print('done:', STORE)


if __name__ == '__main__':
    main()
