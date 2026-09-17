import pyxel
import os

SIZE = 41

btn_tugihe = (20, 80, 40, 20)
btn_uranau = (65, 95, 40, 15)
btn_modoru = (110, 95, 40, 15)

class Sankaku:
    def __init__(self, x, y, w, h, style):
        # self.　に =　を入れる
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.style = style

    def draw(self):
        if self.style == "UP":
            # 三角形(１つ目のx、y、２つ目のx、y、３つ目のx、y、色)
            pyxel.tri(self.x, self.y + self.h, self.x + self.w, self.y + self.h, self.x + self.w // 2, self.y, 5)
        if self.style == "DOWN":
            pyxel.tri(self.x, self.y, self.x + self.w, self.y, self.x + self.w // 2, self.y + self.h, 5)
        if self.style == "RIGHT":
            pyxel.tri(self.x, self.y, self.x, self.y + self.h, self.x + self.w, self.y + self.h // 2, 5)
        if self.style == "LEFT":
            pyxel.tri(self.x, self.y + self.h // 2, self.x + self.w, self.y + self.h, self.x + self.w, self.y, 5)

    def is_click(self):
        # 押される範囲 
        if self.x < pyxel.mouse_x < self.x + self.w and self.y < pyxel.mouse_y < self.y + self.h:
            return True
        else:
            return False

class Game:
    # 初期設定
    def __init__(self):
        pyxel.init(160, 120, title="今日の運勢知りたくない？？")
        pyxel.load("my_resource.pyxres")
        pyxel.mouse(True)
        # ↓これでフォントを定義
        # self.font=pyxel.Font("フォントの名前",サイズ)
        self.font_c = pyxel.Font("chika-Regular.ttf", 18)
        self.font_i = pyxel.Font("ipaexg.ttf", 15)
        # self.font_mt = pyxel.Font("misaki_gothic.ttf")
        self.font_mb = pyxel.Font("misaki_gothic.bdf")

        self.genzai_no_gamen = "itibanme"

        self.fusei_x = 100
        self.fusei_y = 60

        self.ten = "."

        # このボタンのときに指定した座標にそれぞれボタンを置く
        self.ue_btn_tuki = Sankaku(40, 30, 10, 10, "UP")
        self.shita_btn_tuki = Sankaku(40, 90, 10, 10, "DOWN")
        self.ue_btn_hiniti = Sankaku(110, 30, 10, 10, "UP")
        self.shita_btn_hiniti = Sankaku(110, 90, 10, 10, "DOWN")
        self.migi_btn = Sankaku(140, 60, 10, 10, "RIGHT")
        self.hidari_btn = Sankaku(10, 60, 10, 10, "LEFT")

        with open("tentai.txt", "r", encoding = "utf-8") as f:
            self.data_read1 = f.read().split()

        with open("item.txt", "r", encoding = "utf-8") as f:
            self.data_read2 = f.read().split()

        with open("spot.txt", "r", encoding = "utf-8") as f:
            self.data_read3 = f.read().split()

        with open("etati.txt", "r", encoding = "utf-8") as f:
            self.data_read4 = f.read().split()

        BASE = os.path.dirname(os.path.abspath(__file__))
        pyxel.load(os.path.join(BASE, "my_resource.pyxres"))

        self.CX, self.CY = 80, 60
        self.RX = 60
        self.RY = 40

        self.x = self.CX - self.RX
        self.dx = 1

        self.reset()

        pyxel.run(self.update, self.draw)
    def reset(self):
        self.number_t = 1
        self.number_h = 1
        self.count = 0
        self.kekka_page = "1"

    def up_itibanme(self):
        x, y, w, h = btn_tugihe
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.genzai_no_gamen == "itibanme":
                # 2番目の画面に飛ぶボタンの範囲
            if x < pyxel.mouse_x < x + w and y < pyxel.mouse_y < y + h:
                    self.genzai_no_gamen = "nibanme"

    def up_nibanme(self):
        x, y, w, h = btn_uranau
        # 日の上限を定義
        jyougen = 31

        if self.number_t == 2:
            jyougen = 29
        # 定義したものの中に[]をいれる。
        if self.number_t in [4, 6, 9, 11]:
            jyougen = 30

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT): 
            # 月のUPのボタンが押されたときの動作 
            if self.ue_btn_tuki.is_click():
                # self.nunber_tに += の数字分足す
                self.number_t += 1
                if 12 < self.number_t:
                # if 定義した数字 < self.nunber_t の方が大きくなったとき、self.nunber_t = を上限として表示する
                    self.number_t = 1

            # 月のDOWNのボタンが押されたときの動作
            if self.shita_btn_tuki.is_click():
                # self.nunber_tに -= の数字分引く
                self.number_t -= 1
                # if self.number_t < 定義した数字の方が大きくなったとき、self.number_t = を上限として表示する
                if self.number_t < 1:
                    self.number_t = 12

            # 日のUPのボタンが押された時の動作 月と同様の動作をする
            if self.ue_btn_hiniti.is_click():
                self.number_h += 1
                if jyougen < self.number_h:
                    self.number_h = 1

            if self.shita_btn_hiniti.is_click():
                self.number_h -= 1
                if self.number_h < 1:
                    self.number_h = jyougen

        #　上限を日付としてプリントする。 
        if jyougen < self.number_h:
            self.number_h = jyougen

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.genzai_no_gamen == "nibanme":
            # 3番目の画面に飛ぶボタンの範囲
            if x < pyxel.mouse_x < x + w and y < pyxel.mouse_y < y + h:
                self.genzai_no_gamen = "sanbanme"

    def up_sanbanme(self):

        # カウントを // で割る
        sec = self.count // 30
        # (割ったものを % で割り余りを出す)
        self.ten = "." * (sec % 4)
        self.count += 1
        # 本日の日付を呼びだす
        import datetime

        global x, dx
        self.x += self.dx

        if self.x >= self.CX + self.RX or self.x <= self.CX - self.RX:
            self.dx = -self.dx


        if 8 <= sec:            
            self.genzai_no_gamen = "kekka"
            tanjoubi = self.tukihi_no_keisan(self.number_t, self.number_h)
            honjitu = self.tukihi_no_keisan(datetime.datetime.now().month, datetime.datetime.now().day)
            self.goukei = self.tukihi_no_keisan(tanjoubi, honjitu)
            print(self.goukei)

    def tukihi_no_keisan(self, month, day):
        result = list(str(month) + str(day))
        hako = 0
        while hako == 0:
            for f in result:
                 hako += int(f)
            result = list(str(hako))
            if hako >= 10:
                hako = 0
        return hako

    def up_kekka(self):
        x, y, w, h = btn_modoru

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT): 
            if self.migi_btn.is_click():
                self.kekka_page = "2"

            elif self.hidari_btn.is_click():
                self.kekka_page = "1"

            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.genzai_no_gamen == "kekka":
            #     # 2番目の画面に飛ぶボタンの範囲
                if x < pyxel.mouse_x < x + w and y < pyxel.mouse_y < y + h and self.kekka_page == "2":
                    self.reset()
                    # self.up_itibanme()
                    self.genzai_no_gamen = "itibanme"
            

    def dr_itibanme(self):
        # 最初のページ
        pyxel.cls(0)
        x, y, w, h, = btn_tugihe
        # テキスト(x軸、y軸、表示するもの、色、フォント)
        pyxel.text(5, 15, "きょうのうんせい", 10, self.font_c)
        pyxel.text(5, 35, "しりたくない?", 10, self.font_c)
        # 上で定義した座標、色
        pyxel.rect(x, y, w, h, 1)              
        pyxel.text(32, 86, "つぎ", 10, self.font_mb)
        # F星の
        pyxel.blt(self.fusei_x, self.fusei_y,0, 0, 0, 60, 50, 0 )
        pyxel.text(116, 109, "Ｆ星", 10, self.font_mb) 

    def dr_nibanme(self):
        # 生年月日ページ
        pyxel.cls(0)
        x, y, w, h = btn_uranau
        pyxel.text(31, 5, "たんじょうびを入力してね", 7, self.font_mb)  
        pyxel.text(41, 20, "月", 7, self.font_mb)
        pyxel.text(112, 20, "日", 7, self.font_mb)
        # 月のところ
        self.ue_btn_tuki.draw()
        self.shita_btn_tuki.draw()
        self.ue_btn_hiniti.draw()
        self.shita_btn_hiniti.draw()

        # 月のところ
        # テキスト（ｘ座標、ｙ座標、self.numberを文字として置く、色）
        pyxel.text(40, 60, str(self.number_t), 7)
        pyxel.text(60, 35, "UP", 7)
        pyxel.text(60, 82, "DOWN", 7)
        # 日のところ
        pyxel.text(110, 60, str(self.number_h), 7)
        pyxel.text(130, 35, "UP", 7)
        pyxel.text(130, 82, "DOWN", 7)

        pyxel.rect(x, y, w, h, 1)
        pyxel.text(77, 99, "占う", 10, self.font_mb)

    def dr_sanbanme(self):
        pyxel.cls(0)
        pyxel.text(65, 55, f"占い中{self.ten}", 7, self.font_mb)
        if self.dx > 0:
            self.y = self.CY - self.RY * (1 - (self.x - self.CX)**2 / self.RX**2)**0.5
        else:
            self.y = self.CY + self.RY * (1 - (self.x - self.CX)**2 / self.RX**2)**0.5

        screen_x = self.x - SIZE / 2
        screen_y = self.y - SIZE / 2

        idx = (pyxel.frame_count // 10) % 6
        coords = [
            (0, 56),
            (0, 216),
            (0, 176),
            (0, 96),
            (0, 136),
            (49, 216),
        ]

        x_img, y_img = coords[idx]

        pyxel.blt(screen_x, screen_y, 0, x_img, y_img, SIZE+5, SIZE, 0)

    def dr_kekka(self):
        pyxel.cls(0)
        x, y, w, h = btn_modoru

        if self.kekka_page == "1":
            # 太陽
            if self.goukei == 1:
                pyxel.blt(25, 10, 2, 0, 0, 32, 32, 0)
            # 水星
            elif self.goukei == 2:
                pyxel.blt(25, 10, 2, 0, 40, 32, 32, 0)
            # 金星
            elif self.goukei == 3:
                pyxel.blt(25, 10, 2, 0, 120, 32, 32, 0)
            # 地球
            elif self.goukei == 4:
                pyxel.blt(25, 10, 2, 0, 160, 32, 32, 0)
            # 火星
            elif self.goukei == 5:
                pyxel.blt(25, 10, 2, 0, 80, 32, 32, 0)
            # 木星
            elif self.goukei == 6:
                pyxel.blt(25, 10, 2, 40, 40, 32, 32, 0)
            # 土星
            elif self.goukei == 7:
                pyxel.blt(25, 10, 2, 40, 80, 49, 32, 0)
            # 天王星
            elif self.goukei == 8:
                pyxel.blt(25, 10, 2, 40, 120, 32, 32, 0)
            # 海王星
            elif self.goukei == 9:
                pyxel.blt(25, 10, 2, 40, 160, 32, 32, 0)

            pyxel.text(93, 32, str(self.data_read1[self.goukei - 1]), 10, self.font_i)
            pyxel.text(75, 8, "今日のあなたの", 7, self.font_mb)
            pyxel.text(100, 18, "味方は...", 7, self.font_mb)
            self.migi_btn.draw()

            pyxel.text(20, 60, "洗濯運", 7, self.font_mb)
            pyxel.text(20, 75, "変顔運", 7, self.font_mb)
            pyxel.text(20, 90, "つまずかない運", 7, self.font_mb)
            pyxel.text(20, 105, "新しい出会い運", 7, self.font_mb)

            etati_kekka = self.data_read4[self.goukei]
            etati_kekka_list = list(etati_kekka)
            # print(aaaaa) => "5114"
            # aaaaaを各数字をリストにしてbbbbに入れる
            # bbbb ["5","1", "1", "4"] をつくる
            draw_y = 60
            editer_x = 0

                # hikaru_kosu = etati[0]
            # self.goukei
            for i in range(4): #項目ごとにループする
                hikaru_kosu = int(etati_kekka_list[i])
                # hikaru_kosu = int(bbbb[i])
                for j in range(5): # 光らせるものごとにループする
                    draw_x = 85 + j * 10

                    if j < hikaru_kosu:
                        u = 32
                        pyxel.blt(draw_x, draw_y, 1, editer_x, u, 8, 8, 0)
                    else:
                        u = 40
                        pyxel.blt(draw_x, draw_y, 1, editer_x, u, 8, 8, 0)
                editer_x += 8
                draw_y += 15


        elif self.kekka_page == "2":
            pyxel.text(33, 10, "ラッキーアイテム・スポット", 10, self.font_mb)
            self.hidari_btn.draw()
            pyxel.text(33, 40, "☆ ラッキーアイテム", 7, self.font_mb)
            pyxel.text(46, 50, str(self.data_read2[self.goukei - 1]), 7, self.font_mb)
            pyxel.text(33, 80, "☆ ラッキースポット", 7, self.font_mb)
            pyxel.text(46, 90, str(self.data_read3[self.goukei - 1]), 7, self.font_mb)
            pyxel.rect(x, y, w, h, 1)
            pyxel.text(118, 99, "トップ", 10, self.font_mb)
 
    def update(self):
        # pyxel. でタブを閉じる
        if pyxel.btnp(pyxel.KEY_0):
            pyxel.quit()

        if self.genzai_no_gamen == "itibanme":
            self.up_itibanme()

        elif self.genzai_no_gamen == "nibanme":
            self.up_nibanme()

        elif self.genzai_no_gamen == "sanbanme":
            self.up_sanbanme()

        elif self.genzai_no_gamen == "kekka":
            self.up_kekka()

    def draw(self):
        if self.genzai_no_gamen == "itibanme":
            self.dr_itibanme()

        elif self.genzai_no_gamen == "nibanme":
            self.dr_nibanme()

        elif self.genzai_no_gamen == "sanbanme":
            self.dr_sanbanme()

        elif self.genzai_no_gamen == "kekka":
            self.dr_kekka()

Game()