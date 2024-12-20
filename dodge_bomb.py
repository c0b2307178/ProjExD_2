import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面の中か外かを判定する
    引数：こうかとんRect or 爆弾Rect
    戻り値：真理値タプル（横，縦）／画面内：True，画面外：False
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
    # 半透明の黒い画面を作成
    overlay = pg.Surface((WIDTH, HEIGHT))  # フルスクリーンサイズのSurface
    overlay.set_alpha(180)  # 透明度
    overlay.fill((0, 0, 0))  # 黒色で塗りつぶし

    # 泣いているこうかとん画像を読み込む
    crying_kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)
    crying_kk_rct = crying_kk_img.get_rect()
    crying_kk_rct.center = (WIDTH // 2, HEIGHT // 2 - 50)

    # フォントを設定し、「Game Over」の文字列を作成
    font = pg.font.Font(None, 100)
    game_over_text = font.render("GAME OVER", True, (255, 255, 255))
    text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

    # 画面を表示
    screen.blit(overlay, (0, 0))  # 半透明の黒い画面を描画
    screen.blit(crying_kk_img, crying_kk_rct)  # 泣いているこうかとんを描画
    screen.blit(game_over_text, text_rect)  # 「Game Over」の文字を描画
    pg.display.update()  # 画面を更新
    time.sleep(5)
    
def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  # 爆弾用の空Surface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 爆弾円を描く
    bb_img.set_colorkey((0, 0, 0))  # 四隅の黒を透過させる
    bb_rct = bb_img.get_rect()  # 爆弾Rectの抽出
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 爆弾速度ベクトル
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return  # ゲームを終了
        if kk_rct.colliderect(bb_rct):
            print("ゲームオーバー")
            return  # ゲームオーバー
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key] == True:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)  # 爆弾動く
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横にはみ出てる
            vx *= -1
        if not tate:  # 縦にはみ出てる
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
