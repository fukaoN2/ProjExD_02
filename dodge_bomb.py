from random import randint
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900

lib = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

def check_bound(obj_rct: pg.rect):
    """
    引数　こうかとんRectか爆弾Rect
    戻り値：タプル（横方向判定効果、縦方向判定効果）
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right: #横方向判定
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom: #縦方向判定
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    """こうかとん"""
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = (900, 400) #こうかとんの初期座標を設定
    """爆弾"""
    bom = pg.Surface((20, 20)) #練習1 爆弾surfaceを作成
    pg.draw.circle(bom, (255, 0, 0), (10, 10), 10)
    bom.set_colorkey((0, 0, 0)) #黒い部分を透明に変更
    x, y = randint(0, WIDTH), randint(0, HEIGHT)
    bom_rct = bom.get_rect()
    bom_rct.center = x, y
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 0])

        """こうかとん"""
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in lib.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] #練習3 横方向の合計移動量
                sum_mv[1] += mv[1] #練習3 縦方向の合計移動量
        kk_rct.move_ip(sum_mv[0], sum_mv[1]) #練習3 移動させる
        if check_bound(kk_rct) != (True, True): #練習4 はみだし判定
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct) #練習3 表示させる

        """爆弾"""
        bom_rct.move_ip(vx, vy) #練習2 爆弾を動かす
        yoko, tate = check_bound(bom_rct)
        if not yoko: #練習4 横方向にはみ出たら
            vx *= -1
        if not tate: #練習4 縦方向にはみ出たら
            vy *= -1
        screen.blit(bom, bom_rct) #練習1 Rectを使用してblitする
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()