from random import randint
import sys
import pygame as pg
import math


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

    #こうかとん画像向き別辞書　修正なし
    lib2 = {
        (+5, 0): (pg.transform.flip(kk_img, True, False), 0),
        (+5, -5): (pg.transform.flip(kk_img, True, False), +45),
        (0, -5): (pg.transform.flip(kk_img, True, False), +90),
        (-5, -5): (kk_img, -45),
        (-5, 0): (kk_img, 0),
        (-5, +5): (kk_img, +45),
        (0, +5): (pg.transform.flip(kk_img, True, False), -90),
        (+5, +5): (pg.transform.flip(kk_img, True, False), -45),
    }

    """爆弾"""
    bom = pg.Surface((20, 20)) #練習1 爆弾surfaceを作成
    pg.draw.circle(bom, (255, 0, 0), (10, 10), 10)
    bom.set_colorkey((0, 0, 0)) #黒い部分を透明に変更
    x, y = randint(0, WIDTH), randint(0, HEIGHT)
    bom_rct = bom.get_rect()
    bom_rct.center = x, y
    vx, vy = +5, +5

    clock = pg.time.Clock()
    font = pg.font.Font(None, 80) #追加機能 時間表示
    tmr = 0

    accs = [a for a in range(1, 11)] #追加機能2 加速
    bom_imgs = []
    for r in range(1, 11):
        bom_img = pg.Surface((20*r, 20*r), pg.SRCALPHA)
        pg.draw.circle(bom_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bom_imgs.append(bom_img)


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        txt = font.render(str(tmr), True, (0, 100, 100)) #追加機能 時間表示

        screen.blit(bg_img, [0, 0])

        """こうかとん"""
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        kk_mv = kk_img

        for key, mv in lib.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] #練習3 横方向の合計移動量
                sum_mv[1] += mv[1] #練習3 縦方向の合計移動量
        kk_rct.move_ip(sum_mv[0], sum_mv[1]) #練習3 移動させる

        for kk, mm in lib2.items():
            if sum_mv[0] == kk[0] and sum_mv[1] == kk[1]:
                kk_mv = pg.transform.rotozoom(mm[0], mm[1], 1.0) #追加1 画像指定
        screen.blit(kk_mv, [kk_rct.x, kk_rct.y]) #追加1 表示

        if check_bound(kk_rct) != (True, True): #練習4 はみだし判定
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        # screen.blit(kk_img, kk_rct) #練習3 表示させる

        """爆弾"""
        yoko, tate = check_bound(bom_rct)
        if not yoko: #練習4 横方向にはみ出たら
            vx *= -1
        if not tate: #練習4 縦方向にはみ出たら
            vy *= -1
        """追いかけ機能"""
        dis = (kk_rct.centerx-bom_rct.centerx, kk_rct.centery-bom_rct.centery) #追加機能4 距離
        dis2 = math.sqrt(dis[0]**2 + dis[1]**2)
        if dis2 < 500:
            avx, avy = vx, vy
        else:
            vctr = (dis[0] / dis2* math.sqrt(50), dis[1] / dis2 * math.sqrt(50))
            avx, avy = vx*accs[min(tmr//500, 9)], vy*accs[min(tmr//500, 9)]
            vx, vy = vctr[0], vctr[1]

        bom_img = bom_imgs[min(tmr//500, 9)]
        # bom_rct.move_ip(vx, vy) #練習2 爆弾を動かす
        bom_rct.move_ip(avx, avy)
        # screen.blit(bom, bom_rct) #練習1 Rectを使用してblitする
        screen.blit(bom_img, [bom_rct.x, bom_rct.y])

        if kk_rct.colliderect(bom_rct):
            print("ゲームオーバー")
            return

        screen.blit(txt, [200, 200]) #追加機能 時間表示
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()