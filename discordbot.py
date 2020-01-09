# coding: utf-8
import re
from datetime import datetime, timedelta, timezone
import asyncio
import discord
import jaconv

#######################################################################################################################
# プリコネクラバト凸管理用BOT Ver1.0.0 by Toki　Discord:Toki#1901 Twitter@Lunate_sheep
# Python3.6.x
# Discord.py 1.2.5 + jaconv
# BOTログイントークンさえ入れれば最低限起動します。
# 正常に動作していると、コンソールに1秒毎に現在時刻が表示されます。
# 初期設定項目 #########################################################################################################
TOKEN = 'NjY0NDUyNjE3MTk1MjI1MTI4.XhbRAQ.goFmxgIy5oJh4OXlOQNJd-nULhE'  # BOTログイントークン
ID_ROLE_ADMIN = 337610874615496704  # 飼い主ロールID（事前設定用）
ID_CHANNEL_MAIN = 664724026010107919  # 入力用チャンネルID（事前設定用）
ID_CHANNEL_LOG_MAIN = 664724174161575936  # 凸進捗出力用チャンネルID（事前設定用）
ID_CHANNEL_LOG_INCOMPLETE = 664724306034556930e  # 3凸未完了者リスト用チャンネルID（事前設定用）
ID_CHANNEL_LOG_REQUEST = 664724399135391784  # 持越中・通知登録者リスト用チャンネルID（事前設定用）
ID_CHANNEL_REACT = 664724441305055232  # 簡易入力用チャンネルID（事前設定用）
# 簡易入力用絵文字ID（物理凸, 物理〆, 魔法凸, 魔法〆）（事前設定用）
ID_EMOJI = [664727469252804619, 664727509593489409, 664727528338096138, 664727550588747776, 664727565357023242]
########################################################################################################################

# グローバル変数
client = discord.Client()
JST = timezone(timedelta(hours=+9), 'JST')  # 日本時間設定
DELAY_S = 3  # メッセージ削除までの時間（短）
DELAY_M = 30  # メッセージ削除までの時間（中）
DELAY_L = 60  # メッセージ削除までの時間（長）
Flg_Setup = False  # 初期設定フラグ
Flg_Sleep = False  # 休眠フラグ
Flg_No_Emoji = False  # 絵文字未設定フラグ
Flg_Demo = False  # デモモードフラグ
Message_Log_Main = None  # 凸進捗出力メッセージオブジェクト
Message_Log_Incomplete = None  # 凸未完了者リスト出力メッセージオブジェクト
Message_Log_Request = None  # 持越中・通知登録者リスト出力メッセージオブジェクト
Orig_Channel_ID = None  # メッセージ送信元チャンネルオブジェクト
Recent_Boss = ''  # 直近のボス情報
Is_Boss_Round_End = False  # 5ボス〆フラグ
Boss_Round_Count = 1  # 直近のボス情報（周回数）
playerData = []  # プレイヤーデータ配列
Message_Boss_Reaction = []  # ボス凸リアクション用メッセージオブジェクト配列
Emoji_Command = ["物理凸", "物理〆", "魔法凸", "魔法〆", "通知"]
Message_Sec1_Reaction = None  # 持越簡易入力用メッセージオブジェクトその1
Emoji_Sec1_Reaction_UTF = ['2️⃣', '3️⃣', '4️⃣', '5️⃣']
Emoji_Sec1_Command = [20, 30, 40, 50]
Message_Sec2_Reaction = None  # 持越簡易入力用メッセージオブジェクトその2
Emoji_Sec2_Reaction_UTF = ['6️⃣', '7️⃣', '8️⃣', '9️⃣']
Emoji_Sec2_Command = [60, 70, 80, 90]
Message_Etc_Reaction = None  # 特殊操作簡易入力用メッセージオブジェクト
Emoji_Etc_Reaction_UTF = ['🚫', '↩']
Emoji_Etc_Command = ["タスキル済", "元に戻す"]


# プレイヤーデータクラス
class PlayerData:
    def __init__(self, user, atk_list, atk_cnt_m, atk_cnt_b, done_cnt, task_killed, req_none, notice_req, req_list,
                 rolled_time, rolled_type, recent_boss):
        self.playLog = []  # PlayerDataオブジェク トバックアップスタック
        self.user = user  # Discord.user オブジェクト
        self.atk_cnt_m = atk_cnt_m  # 魔法凸カウンタ
        self.atk_cnt_b = atk_cnt_b  # 物理凸カウンタ
        self.done_cnt = done_cnt  # 当日凸カウンタ
        self.task_killed = task_killed  # タスキルフラグ
        self.req_none_rolled = req_none  # 持越先希望なしフラグ
        self.notice_req = notice_req  # 凸希望登録フラグ
        self.req_list = req_list  # 通知希望リスト
        self.atk_list = atk_list  # 凸済リスト
        self.rolled_time = rolled_time  # 持越時間
        self.rolled_type = rolled_type  # 持越種別
        self.recent_boss = recent_boss  # どのボス凸か

    # Discord.user Object
    def user(self):
        return self.user

    # 魔法凸カウンタ加算
    def add_atk_cnt_m(self):
        self.done_cnt += 1
        self.atk_cnt_m += 1
        return

    # 物理凸カウンタ加算
    def add_atk_cnt_b(self):
        self.done_cnt += 1
        self.atk_cnt_b += 1
        return

    # ボス凸処理
    def add_atk(self, boss):
        self.req_none_rolled = False
        self.req_list = 0
        self.notice_req = False
        self.atk_list += 10000 // 10 ** (boss - 1)
        return

    # 通知設定されているボスか否か
    def is_req_boss(self, boss):
        if self.req_list & 2 ** (boss - 1):
            return True

    # タスキル情報出力
    def get_task_killed(self):
        if self.task_killed:
            return '　タスキル済'
        else:
            return ''

    # 通知設定取得
    def get_req_boss(self):
        req_boss = ''
        for i in range(5):
            if self.req_list & 2 ** int(i):
                req_boss += str(i + 1)
        return req_boss

    # 通知設定情報出力
    def get_txt_req(self):
        req = ''
        # 凸通知
        if self.req_list or self.req_none_rolled:
            # 持越有か凸通知か
            req = '　持越先：'
            if self.notice_req:
                req = '　通知：'
            req += self.get_req_boss()
            if self.req_none_rolled:
                req = '　持越先：未定'
            if not self.notice_req and not self.rolled_time:
                req += ' @' + self.rolled_type
            if self.rolled_time:
                req += ' ' + self.rolled_type + '@' + str(self.rolled_time) + 's'
        return req

    # ボス凸情報出力
    def get_atk_boss(self):
        atk_boss = ''
        attacked_list = self.atk_list
        for i in range(5):
            boss_cnt = (attacked_list // (10000 // (10 ** int(i))))
            if boss_cnt == 0:
                boss_cnt = '-'
            atk_boss += " " + str(boss_cnt)
            attacked_list %= (10000 // (10 ** int(i)))
        return atk_boss

    # プレイヤーログ出力
    def get_player_log(self, mode):
        player_log = f''
        # 本日3凸済
        if mode == 0 and self.done_cnt == 3:
            player_log += f'+'
        elif mode == 0:
            player_log += f'-'
        player_log += f'{self.user.display_name}{self.get_task_killed()}{self.get_txt_req()}\n'
        player_log += f'　{self.done_cnt}/3(物{self.atk_cnt_b}魔{self.atk_cnt_m}) {self.get_atk_boss()}\n'
        return player_log

    # バックアップをプッシュ
    def backup_play_log(self):
        self.playLog.append(PlayerData(self.user, self.atk_list, self.atk_cnt_m, self.atk_cnt_b, self.done_cnt,
                                       self.task_killed, self.req_none_rolled, self.notice_req, self.req_list,
                                       self.rolled_time, self.rolled_type, self.recent_boss))
        return

    # ロールバック
    def revert_play_log(self):
        tmp_data = self.playLog.pop()
        self.user = tmp_data.user  # Discord.user Object
        self.atk_cnt_m = tmp_data.atk_cnt_m  # 魔法凸カウンタ
        self.atk_cnt_b = tmp_data.atk_cnt_b  # 物理凸カウンタ
        self.done_cnt = tmp_data.done_cnt  # 当日凸カウンタ
        self.task_killed = tmp_data.task_killed  # タスキルフラグ
        self.req_none_rolled = tmp_data.req_none_rolled  # 持越先希望なしフラグ
        self.notice_req = tmp_data.notice_req  # 凸希望登録フラグ
        self.req_list = tmp_data.req_list  # 通知希望リスト
        self.atk_list = tmp_data.atk_list  # 凸済リスト
        self.rolled_time = tmp_data.rolled_time  # 持越時間
        self.rolled_type = tmp_data.rolled_type  # 持越種別
        global Boss_Round_Count
        global Is_Boss_Round_End
        if Is_Boss_Round_End and self.recent_boss == "5ボス〆":
            Is_Boss_Round_End = False
        elif self.recent_boss == "5ボス〆":
            Boss_Round_Count -= 1
        self.recent_boss = tmp_data.recent_boss  # どのボス凸か
        return

    # バックアップ以外全てクリア
    def erase_all(self):
        self.atk_cnt_m = 0
        self.atk_cnt_b = 0
        self.done_cnt = 0
        self.task_killed = False
        self.req_none_rolled = False
        self.notice_req = False
        self.req_list = 0
        self.atk_list = 0
        self.rolled_time = 0
        self.rolled_type = ''
        self.recent_boss = ''
        return

    # バックアップクリア
    def erase_backup(self):
        self.playLog.clear()
        return


# 5am定時処理
async def rollover_by5am():
    global Message_Log_Main
    global Flg_Sleep
    global Flg_Demo
    is_day_rolled = True
    while True:
        # 現在時間を表示
        what_time = datetime.now(JST).strftime('%H:%M:%S')
        print(what_time)
        if Flg_Demo:
            await asyncio.sleep(1)
            continue
        # 5時ロールオーバー処理
        if datetime.now(JST).strftime('%H:%M:%S') < '04:59:59':
            is_day_rolled = False
        if datetime.now(JST).strftime('%H:%M:%S') >= '04:59:59' and not is_day_rolled and not Flg_Sleep:
            await update_channel_log()
            Message_Log_Main = None
            is_day_rolled = True
            for p in playerData:
                p.erase_all()
                p.erase_backup()
                await update_incomplete_channel_log()
                await update_request_channel_log()
        await asyncio.sleep(1)


# 持ち越しダメージ計算
async def rollover_simulate(message, msg_content):
    current_hp = 0
    expect_dmg = 0
    is_current_hp = False  # 現在のHP判定
    is_expected_dmg = False  # 想定ダメージ判定
    for i in msg_content:
        # ボス番号読み取って該当ボスのフラグを立てる
        if not is_expected_dmg and re.match('\d', i):
            is_current_hp = True
            current_hp = current_hp * 10 + int(i)
        if is_expected_dmg and re.match('\d', i):
            expect_dmg = expect_dmg * 10 + int(i)
        # 現HP読取後の区切り以降は想定ダメージとして読取
        if is_current_hp and not is_expected_dmg and (i == '-' or i == 'ー' or i == '－' or i == ' ' or i == '　'):
            is_expected_dmg = True

    if not expect_dmg:  # 想定ダメージが入力されていない場合、一定秒持越に必要なダメージを出す
        i = 70
        reply = '```持越秒数に対して必要なダメージ一覧\n\n'
        while True:
            suggested_dmg = current_hp / (1 - i / 90)
            reply += f"{i + 20}s：{int(suggested_dmg)} 万ダメージ\n"
            i -= 5
            if i < 0:
                break
        reply += "```"
        await reply_and_delete(message, reply, DELAY_L)
        return
    elif expect_dmg < current_hp:
        reply = "そのダメージだと倒しきれません"
        await reply_and_delete(message, reply, DELAY_S)
        return

    rolled_time = 90 * (1 - current_hp / expect_dmg) + 20
    if rolled_time >= 90:
        rolled_time = 90

    reply = "予想される持越時間は " + str(rolled_time) + "秒です"
    await reply_and_delete(message, reply, DELAY_M)
    return


# 凸情報を取得
async def get_attack_log(mode):
    done_total = 0
    today_total = 0
    reply = f''
    # リストアップ
    for p in playerData:
        done_total += p.done_cnt
        today_total += 3
        if mode == 1:  # 3凸未完了者抽出モード
            if p.done_cnt == 3:
                continue
        if mode == 2:  # 通知登録者抽出モード
            if not (p.req_list or p.req_none_rolled):
                continue
        reply += p.get_player_log(mode)
    # 全体の進捗
    reply += f'\n凸進捗度:{done_total}/{today_total} 現在:{Boss_Round_Count}周目{Recent_Boss}'
    return reply


# 凸情報を登録
async def submit_attack_log(message, orig_user):
    global Boss_Round_Count
    msg_content = jaconv.normalize(message.content)
    # 凸登録
    if re.match(r'^[1-5][物魔bm]', msg_content):
        # ボス凸先
        boss = int(msg_content[0])
        # 物魔判定
        atk_type_m = False
        if msg_content[1] == '魔' or msg_content[1] == 'm':
            atk_type_m = True
        # 通知設定判定
        is_req = False
        if re.match(r'^[1-5][物魔bm][1-5]', msg_content):
            is_req = True
        # 〆判定
        is_finished = False
        if re.match(r'^[1-5][物魔bm][ー〆-]', msg_content):
            is_finished = True
        # 通知設定判定
        req_boss = 0  # 通知対象記録
        is_timed = False  # 持越時間判定
        int_time = 0  # 持越時間
        if is_finished or is_req:
            is_this_boss = True
            for i in msg_content:
                # ボス番号読み取って該当ボスのフラグを立てる
                if not is_timed and not is_this_boss and '0' < i < '6':
                    req_boss |= 2 ** (int(i) - 1)
                if not is_timed and is_this_boss and '0' < i < '6':
                    is_this_boss = False  # 最初の数字は凸対象ボスだから無視

                # @以降は持越時間表記として読取
                if not is_timed and i == '@':
                    is_timed = True
                if is_timed and re.match('\d', i):
                    int_time *= 10
                    int_time += int(i)
                # メンションかs検知したらそこで通知判定終了
                if (is_timed and i == 's') or i == '<':
                    break

        for p in playerData:
            if p.user == orig_user:
                break
        else:
            reply = f'{orig_user.display_name}さんはリストに入っていません'
            await reply_and_delete(message, reply, DELAY_S)

        # リストから探して対象のログを更新
        for p in playerData:
            if p.user == orig_user:
                # 3凸済の場合は更新拒否
                if p.done_cnt == 3:
                    reply = f'{p.user.display_name}さんは本日既に3凸済です'
                    await reply_and_delete(message, reply, DELAY_S)
                    return
                # ログバックアップ
                p.backup_play_log()
                # カウント数バックアップ
                done_today = p.done_cnt
                # 持越消化凸か確認
                is_rolled = False
                txt_rolled = ''
                txt_finished = ''
                if p.req_none_rolled or (p.req_list and not p.notice_req):
                    is_rolled = True
                    txt_rolled = '持越分'
                # 持越で〆たら持越発生なし
                if is_finished and is_rolled:
                    txt_finished = '　持越で〆たため、持越発生なし'
                # 持越で〆なければ持越発生
                if is_finished and not is_rolled:
                    txt_finished = '　' + str(boss) + 'ボスで持越発生'
                    # 持越発生編成を記録
                    if atk_type_m:
                        p.rolled_type = '魔法'
                    else:
                        p.rolled_type = '物理'
                    # 時間入力がある場合は時間も記録
                    if int_time:
                        txt_finished += str(int_time) + '秒'
                        p.rolled_time = int_time
                # 凸登録処理
                p.add_atk(boss)
                # 翌周に来たか
                global Is_Boss_Round_End
                if Is_Boss_Round_End:
                    Boss_Round_Count += 1
                    Is_Boss_Round_End = False
                # 直近のボスを記録
                global Recent_Boss
                Recent_Boss = str(boss) + 'ボス'
                if is_finished:
                    Recent_Boss += '〆'
                    # 5〆で次周
                    if boss == 5:
                        Is_Boss_Round_End = True
                p.recent_boss = Recent_Boss
                # 通常凸と持越で〆た場合は凸カウント
                if not is_finished or (is_finished and is_rolled):
                    p.rolled_time = 0
                    p.rolled_type = ''
                    if atk_type_m:
                        p.add_atk_cnt_m()
                    else:
                        p.add_atk_cnt_b()
                # 3凸未完了で通知希望がある場合、通知設定
                if req_boss and p.done_cnt < 3:
                    p.req_list = req_boss
                    # 通常凸及び〆で持越使用時は凸希望扱い
                    if not is_finished or (is_finished and is_rolled):
                        p.notice_req = True
                # ボス希望〆なしの場合、持越先指定なしフラグを立てる
                if is_finished and not is_rolled and not req_boss:
                    p.req_none_rolled = True
                reply = f'{p.user.display_name}さんの{boss}ボス凸({done_today + 1}凸目{txt_rolled})確認{txt_finished}'
                await reply_and_delete(message, reply, DELAY_S)

        # 〆たら次ボス待機者チェック
        if is_finished:
            reply = ''
            rolled_target = ''  # 持越中通知
            notice_target = ''  # 通知対象
            next_boss = boss + 1
            # 5の次は1
            if 5 < next_boss:
                next_boss = 1
            # 通知希望者を探してリストアップ
            for p in playerData:
                if p.is_req_boss(next_boss) and not p.notice_req:
                    rolled_target += p.user.mention
                if p.is_req_boss(next_boss) and p.notice_req:
                    notice_target += p.user.mention
            # 待機者が居たら通知
            if rolled_target:
                reply += f'{rolled_target} {next_boss}ボスで持越使えるよー！起きてー！起きてー！\n'
            if notice_target:
                reply += f'{notice_target} {next_boss}ボスの時間だよー！\n'
            if reply:
                await message.channel.send(reply)


# 凸進捗リストチャンネルの更新
async def update_channel_log():
    global ID_CHANNEL_LOG_MAIN
    global Orig_Channel_ID

    channel = client.get_channel(ID_CHANNEL_LOG_MAIN)
    if ID_CHANNEL_LOG_MAIN is None:
        return

    reply = f'```diff\n' + datetime.now(JST).strftime('%d') + '日 ' \
            + datetime.now(JST).strftime('%H:%M:%S') + '時点の全体進捗状況\n\n'
    reply += await get_attack_log(0)
    reply += f'```'

    global Message_Log_Main
    if Message_Log_Main:
        try:
            await Message_Log_Main.edit(content=reply)
        except discord.NotFound:
            Message_Log_Main = await channel.send(reply)
    else:
        Message_Log_Main = await channel.send(reply)


# 3凸未完了リストチャンネルの更新
async def update_incomplete_channel_log():
    global ID_CHANNEL_LOG_INCOMPLETE
    global Orig_Channel_ID

    channel = client.get_channel(ID_CHANNEL_LOG_INCOMPLETE)
    if ID_CHANNEL_LOG_INCOMPLETE is None:
        return

    reply = f'```\n' + datetime.now(JST).strftime('%d') + '日 ' \
            + datetime.now(JST).strftime('%H:%M:%S') + '時点の3凸未完了状況\n\n'
    reply += await get_attack_log(1)
    reply += f'```'
    global Message_Log_Incomplete
    if Message_Log_Incomplete:
        try:
            await Message_Log_Incomplete.edit(content=reply)
        except discord.NotFound:
            Message_Log_Incomplete = await channel.send(reply)
    else:
        Message_Log_Incomplete = await channel.send(reply)


# 持越中・通知登録リストチャンネルの更新
async def update_request_channel_log():
    global ID_CHANNEL_LOG_REQUEST
    global Orig_Channel_ID

    channel = client.get_channel(ID_CHANNEL_LOG_REQUEST)
    if ID_CHANNEL_LOG_REQUEST is None:
        return

    reply = f'```\n' + datetime.now(JST).strftime('%d') + '日 ' \
            + datetime.now(JST).strftime('%H:%M:%S') + '時点の持越・通知登録状況\n\n'
    reply += await get_attack_log(2)
    reply += f'```'
    global Message_Log_Request
    if Message_Log_Request:
        try:
            await Message_Log_Request.edit(content=reply)
        except discord.NotFound:
            Message_Log_Request = await channel.send(reply)
    else:
        Message_Log_Request = await channel.send(reply)


# 全サブチャンネルを更新
async def update_all_log():
    await update_channel_log()
    await update_incomplete_channel_log()
    await update_request_channel_log()


# 一定時間でログクリア
async def reply_and_delete(message, txt, delay_sec):
    # 簡易入力利用時は、入力元にもリプライ
    if message.author.id == client.user.id and message.mentions:
        global ID_CHANNEL_REACT
        channel = client.get_channel(ID_CHANNEL_REACT)
        tmp_msg = await channel.send(txt)
        await tmp_msg.delete(delay=delay_sec)

    tmp_msg = await message.channel.send(txt)
    await tmp_msg.delete(delay=delay_sec)
    await update_all_log()


# 簡易入力用項目を展開
async def init_react_channel():
    global ID_CHANNEL_MAIN
    global ID_CHANNEL_REACT
    global Orig_Channel_ID
    global Message_Boss_Reaction
    global ID_EMOJI
    global Emoji_Command
    global Message_Etc_Reaction
    global Emoji_Etc_Reaction_UTF
    global Emoji_Etc_Command
    global Message_Sec1_Reaction
    global Emoji_Sec1_Reaction_UTF
    global Emoji_Sec1_Command
    global Message_Sec2_Reaction
    global Emoji_Sec2_Reaction_UTF
    global Emoji_Sec2_Command

    react_channel = client.get_channel(ID_CHANNEL_REACT)

    if ID_CHANNEL_REACT and ID_CHANNEL_MAIN:  # 初期設定済の場合、コマンドチャンネルに初期化メッセージ
        orig_channel = client.get_channel(ID_CHANNEL_MAIN)
    elif ID_CHANNEL_REACT:  # 簡易入力チャンネルのみ設定されている場合、そこに初期化メッセージ
        orig_channel = client.get_channel(ID_CHANNEL_REACT)
    elif Orig_Channel_ID:  # コマンドから初期設定される場合、その入力場所に初期化メッセージ
        orig_channel = client.get_channel(Orig_Channel_ID)
    else:  # 初期設定されておらず、コマンドからの設定でもない場合は終了
        return

    global ID_EMOJI
    for emoji_id in ID_EMOJI:
        if emoji_id is None:
            return

    # リアクション場所設置には時間かかるので、作業開始を伝える
    init_msg = await orig_channel.send("簡易入力用チャンネルの初期化中です、しばらくお待ち下さい")

    # 指定IDのチャンネルに簡易入力用項目を展開
    reply = "----------------------------------------\n"
    for i in range(5):
        reply += Emoji_Command[i] + "入力：" + str(client.get_emoji(ID_EMOJI[i])) + "\n"
    reply += "----------------------------------------"
    await react_channel.send(reply)
    # 5ボス分 メッセージを投稿（0から始まるので＋１してボス名投稿）
    for i in range(5):
        tmp_msg = await react_channel.send(str(i + 1) + "ボス物理　｜" + str(i + 1) + "ボス魔法｜通知")
        for emoji_ID in ID_EMOJI:
            await tmp_msg.add_reaction(client.get_emoji(emoji_ID))
        Message_Boss_Reaction.append(tmp_msg)

    # 秒1行目
    reply = "----------------------------------------\n持越時間入力\n"
    await react_channel.send(reply)
    reply = ''
    for i, emoji_UTF in enumerate(Emoji_Sec1_Reaction_UTF):
        reply += ' ' + str(Emoji_Sec1_Command[i]) + "秒"
        if i < 3:
            reply += "｜"
    Message_Sec1_Reaction = await react_channel.send(reply)
    # 投稿終わってからリアクションする
    for emoji_UTF in Emoji_Sec1_Reaction_UTF:
        await Message_Sec1_Reaction.add_reaction(emoji_UTF)
    # 秒2行目
    reply = ''
    for i, emoji_UTF in enumerate(Emoji_Sec2_Reaction_UTF):
        reply += ' ' + str(Emoji_Sec2_Command[i]) + "秒"
        if i < 3:
            reply += "｜"
    Message_Sec2_Reaction = await react_channel.send(reply)
    # 投稿終わってからリアクションする
    for emoji_UTF in Emoji_Sec2_Reaction_UTF:
        await Message_Sec2_Reaction.add_reaction(emoji_UTF)

    # 特殊操作
    reply = "----------------------------------------\n特殊操作\n"
    # 対応表も表示しておく
    for i, emoji_UTF in enumerate(Emoji_Etc_Reaction_UTF):
        reply += emoji_UTF + "：" + Emoji_Etc_Command[i] + "\n"
    Message_Etc_Reaction = await react_channel.send(reply)
    # 投稿終わってからリアクションする
    for emoji_UTF in Emoji_Etc_Reaction_UTF:
        await Message_Etc_Reaction.add_reaction(emoji_UTF)

    reply = "----------------------------------------"
    await react_channel.send(reply)
    # リアクション対象メッセージをつくりおわったので、告知メッセージは閉じる
    await init_msg.delete()


# 代理コマンド発行
async def send_command_by_reaction(reply, reaction, orig_user):
    # orig_userへのメンションをつけてコマンドを代理投稿する
    reply += ' ' + orig_user.mention

    # コマンド用チャンネルが設定されていなかったら代理コマンドはリアクションを受け付けたチャンネルに投稿する
    if ID_CHANNEL_MAIN is not None:
        channel = client.get_channel(ID_CHANNEL_MAIN)  # 代理コマンドをコマンド用チャンネルに行う
        # リアクション投稿を受け付けた元チャンネルをメンションする
        reply += ' ' + reaction.message.channel.mention
    else:
        channel = reaction.message.channel  # 未設定のためリアクションのあったメッセージのあるチャンネルにする

    # 代理投稿
    await channel.send(reply)


# リアクション処理
@client.event
async def on_reaction_add(reaction, user):
    # 自分自身のリアクションには無反応
    if user.id == client.user.id:
        return

    # 各簡易入力用リアクションへのリアクションかを確認する
    for boss_index, tmp_msg in enumerate(Message_Boss_Reaction):
        # 簡易入力用リアクションなら処理
        if tmp_msg.id == reaction.message.id:
            # ボス凸対応リアクションを確認して、対象であったら対応コマンドを発行
            for react_index, emoji_id in enumerate(ID_EMOJI):
                if reaction.emoji == client.get_emoji(emoji_id):
                    is_mage = react_index // 2
                    is_rolled = react_index % 2
                    reply = str(boss_index + 1)
                    if is_mage:
                        reply += "魔"
                    else:
                        reply += "物"
                    if is_rolled:
                        reply += "〆"
                    if react_index == 4:
                        reply = "通知追加 " + str(boss_index + 1)
                    await send_command_by_reaction(reply, reaction, user)  # 代理コマンド

            # 処理をしたらリアクションは消してやる（同コマンド代理を何度もできるように）
            await reaction.message.remove_reaction(reaction.emoji, user)

    # 持越時間簡易入力処理その1
    if Message_Sec1_Reaction:
        if reaction.message.id == Message_Sec1_Reaction.id:
            for react_index, emoji_id in enumerate(Emoji_Sec1_Reaction_UTF):
                if emoji_id == reaction.emoji:
                    reply = "持越 " + str(Emoji_Sec1_Command[react_index])
                    await send_command_by_reaction(reply, reaction, user)  # 代理コマンド

            # 処理をしたらリアクションは消してやる（同コマンド代理を何度もできるように）
            await reaction.message.remove_reaction(reaction.emoji, user)

    # 持越時間簡易入力処理その2
    if Message_Sec2_Reaction:
        if reaction.message.id == Message_Sec2_Reaction.id:
            for react_index, emoji_id in enumerate(Emoji_Sec2_Reaction_UTF):
                if emoji_id == reaction.emoji:
                    reply = "持越 " + str(Emoji_Sec2_Command[react_index])
                    await send_command_by_reaction(reply, reaction, user)  # 代理コマンド

            # 処理をしたらリアクションは消してやる（同コマンド代理を何度もできるように）
            await reaction.message.remove_reaction(reaction.emoji, user)

    # 特殊コマンド簡易入力処理
    if Message_Etc_Reaction:
        if reaction.message.id == Message_Etc_Reaction.id:
            for react_index, emoji_id in enumerate(Emoji_Etc_Reaction_UTF):
                if emoji_id == reaction.emoji:
                    await send_command_by_reaction(Emoji_Etc_Command[react_index], reaction, user)  # 代理コマンド

            # 処理をしたらリアクションは消してやる（同コマンド代理を何度もできるように）
            await reaction.message.remove_reaction(reaction.emoji, user)


# 初期設定
async def setup_wizard(message):
    global ID_CHANNEL_MAIN
    global ID_CHANNEL_LOG_MAIN
    global ID_CHANNEL_LOG_INCOMPLETE
    global ID_CHANNEL_LOG_REQUEST
    global ID_CHANNEL_REACT
    global ID_EMOJI
    global Flg_Setup
    global Flg_No_Emoji

    if not ID_CHANNEL_MAIN:
        reply = "コマンド入力用チャンネルが未設定です。コマンド入力用チャンネルを設定してください。\n\t"
        reply += '例:　入力チャンネル設定 #凸報告用\n\n'
        await reply_and_delete(message, reply, DELAY_L)
        return

    if not ID_CHANNEL_LOG_MAIN:
        reply = "凸進捗リスト出力チャンネルが未設定です。凸進捗リスト出力用チャンネルを設定してください。\n\t"
        reply += '例:　凸進捗リストチャンネル設定 #凸進捗リスト\n\n'
        await reply_and_delete(message, reply, DELAY_L)
        return

    if not ID_CHANNEL_LOG_INCOMPLETE:
        reply = "凸未完了リスト出力チャンネルが未設定です。凸未完了リスト出力用チャンネルを設定してください。\n\t"
        reply += '例:　凸未完了リストチャンネル設定 #3凸未完了リスト\n\n'
        await reply_and_delete(message, reply, DELAY_L)
        return

    if not ID_CHANNEL_LOG_REQUEST:
        reply = "通知リスト出力チャンネルが未設定です。通知リスト出力用チャンネルを設定してください。\n\t"
        reply += '例:　通知リストチャンネル設定 #持越中・通知登録リスト\n\n'
        await reply_and_delete(message, reply, DELAY_L)
        return

    if Flg_No_Emoji:
        reply = "簡易入力用絵文字が未設定です。簡易入力用絵文字を設定してください。\n\t"
        reply += '例:　絵文字設定 （絵文字）（絵文字）（絵文字）（絵文字）（絵文字）\n\t'
        reply += "※　前から順に物理凸、物理〆、魔法凸、魔法〆、通知登録用の合計5つの絵文字を入力してください\n"
        await reply_and_delete(message, reply, DELAY_L)
        return

    if not ID_CHANNEL_REACT:
        reply = "簡易入力チャンネルが未設定です。簡易入力用チャンネルを設定してください。\n\t"
        reply += '例:　簡易入力チャンネル設定 #簡易入力\n\n'
        await reply_and_delete(message, reply, DELAY_L)
        return


# 起動時処理
@client.event
async def on_ready():
    global ID_CHANNEL_MAIN
    global ID_CHANNEL_LOG_MAIN
    global ID_CHANNEL_LOG_INCOMPLETE
    global ID_CHANNEL_LOG_REQUEST
    global ID_CHANNEL_REACT
    global ID_EMOJI
    global Flg_Setup
    global Flg_No_Emoji

    for emoji_id in ID_EMOJI:
        if emoji_id is None:
            Flg_No_Emoji = True

    if ID_CHANNEL_MAIN and ID_CHANNEL_LOG_MAIN and ID_CHANNEL_LOG_INCOMPLETE \
            and ID_CHANNEL_LOG_REQUEST and ID_CHANNEL_REACT and not Flg_No_Emoji:
        Flg_Setup = False
    else:
        Flg_Setup = True
    if ID_CHANNEL_REACT is not None and not Flg_No_Emoji:
        await init_react_channel()
    asyncio.ensure_future(rollover_by5am())


# メッセージ処理
@client.event
async def on_message(message):
    global Message_Log_Main
    global Message_Log_Incomplete
    global Message_Log_Request
    global Flg_Sleep
    global Flg_Demo
    global Flg_No_Emoji
    global Flg_Setup
    global ID_ROLE_ADMIN
    global ID_CHANNEL_MAIN
    global ID_CHANNEL_LOG_MAIN
    global ID_CHANNEL_LOG_INCOMPLETE
    global ID_CHANNEL_LOG_REQUEST
    global ID_CHANNEL_REACT
    global ID_EMOJI
    global Orig_Channel_ID
    Orig_Channel_ID = message.channel.id

    msg_content = jaconv.normalize(message.content)

    # 代筆時以外の自分自身には無反応
    if message.author.id == client.user.id and not message.mentions:
        return

    # 持越時間予想
    if re.match(r'^持越時間|^持越し時間|^持ち越し時間|^rollover|^ro', msg_content):
        await rollover_simulate(message, msg_content)
        return

    # コマンド入力チャンネルが指定されている場合、指定チャンネル以外は無反応
    if ID_CHANNEL_MAIN is not None and message.channel != client.get_channel(ID_CHANNEL_MAIN):
        return

    # 飼い主か確認（飼い主未設定の場合、全員飼い主とみなす）
    is_admin = False
    if ID_ROLE_ADMIN is None:
        is_admin = True
    for r in message.author.roles:
        if r.id == ID_ROLE_ADMIN:
            is_admin = True

    # 休眠機能
    if is_admin and re.match(r'sleep$|/sleep$', msg_content):
        if Flg_Sleep:
            Flg_Sleep = False
            reply = f'休眠解除しました。'
            await reply_and_delete(message, reply, DELAY_S)
        else:
            Flg_Sleep = True
            reply = f'休眠に入ります。'
            await reply_and_delete(message, reply, DELAY_S)

    # 休眠判定
    if Flg_Sleep:
        return

    # デモモード機能
    if is_admin and re.match(r'demo$|/demo$', msg_content):
        if Flg_Demo:
            Flg_Demo = False
            reply = f'デモモード解除しました。'
            await reply_and_delete(message, reply, DELAY_S)
        else:
            Flg_Demo = True
            reply = f'デモモードに入ります。'
            await reply_and_delete(message, reply, DELAY_S)

    # 飼い主かBOT自身がメンションしてたら代筆機能
    orig_user = message.author
    if (is_admin and message.mentions) or (message.author.id == client.user.id and message.mentions):
        orig_user = message.mentions[0]

    # ヘルプ
    if re.match(r'help$|/help$|ジュウシマツの使い方$', msg_content):
        reply = f'```\n'
        reply += '(持越時間 or 持越し時間 or 持ち越し時間 or rollover or ro)(現在のボスHP)\n\t持越時間に対して必要なダメージを計算する\n\t例：持越時間　250\n\n'
        reply += '(持越時間 or 持越し時間 or 持ち越し時間 or rollover or ro)(現在のボスHP)-(ダメージ)\n\tダメージから予想される持越時間を計算する\n\t例：持越時間　250-600\n\n'
        reply += '(ボス番号)(物 or 魔 or b or m)\n\tボス凸履歴を登録\n\t例：1物　3b 5m\n\n'
        reply += '(ボス番号)(物 or 魔 or b or m)(通知希望のボス番号)\n\t' \
                 'ボス凸履歴を登録すると同時に、希望ボスまで来たら通知設定\n\t例：1物135　1m135（1ボス凸+1,3,5ボスが回ってきたら通知）\n\n'
        reply += '(ボス番号)(物 or 魔 or b or m)(〆 or -)\n\tボス撃破履歴を登録\n\t例：3魔〆 5m-\n\n'
        reply += '(ボス番号)(物 or 魔 or b or m)(〆 or -)(持越先として通知希望のボス番号)\n\t' \
                 'ボス撃破履歴を登録すると同時に、討伐時に通知設定\n\t例：1物〆135　1m-135（1ボス撃破+1,3,5ボスが回ってきたら通知）\n\n'
        reply += '(ボス番号)(物 or 魔 or b or m)(〆 or -)(持越先ボス番号)(@秒数s)\n\t' \
                 'ボス撃破履歴を登録すると同時に、討伐時に通知設定し、残り秒数を登録\n\t例：2物〆135@50s(135で通知、残り50s)　5m-5@90s(5で通知、残り90s)\n\n'
        reply += 'kd or killed or /killed or タスキル済\n\t今日のタスキル使用を登録\n\n'
        reply += 'nt(ボス番号) or notice(ボス番号) or /notice(ボス番号) or ボス通知(ボス番号)\n\t' \
                 'そのボスの番が来たら通知(持越希望先もこのコマンドで変更可)\n\t' \
                 '例：/notice 135　で1 3 5ボス到達で通知\n\t/notice （指定なし）で現在設定している通知設定を解除\n\n'
        reply += 'rt(持越時間) or rolled(持越時間) or /rolled(持越時間) or 持越(持越時間)\n\t' \
                 '持越時間の事後登録、もしくは変更\n\t' \
                 '例：/rolled 90 で90秒の持越時間を登録\n\t/rolled （指定なし）で現在登録している持越時間を削除\n\n'
        reply += 'rv or revert or /revert or 元に戻す \n\t凸リストをひとつ前の状態に戻す\n\n'
        reply += 'cl or clear or /clear or 凸リストをクリア \n\t凸リストをクリアする\n\n'
        reply += 'la or list-all or /list-all or 凸リストを表示 \n\tクラン全体の凸状況を表示する\n\n'
        reply += 'li or list or /list or 未凸リストを表示 \n\tクラン全体の未凸者一覧を表示する\n\n'
        reply += 'wl or waitlist or /waitlist or ウェイトリストを表示 \n\t持越中もしくは通知登録者一覧を表示する\n\n'
        reply += 'add or /add\n\tメンバーリストに自分を追加\n\n'
        reply += '```'
        await reply_and_delete(message, reply, DELAY_L)
        return

    # adminヘルプ
    if re.match(r'help-admin$|/help-admin$', msg_content):
        reply = f'```\n管理用コマンド一覧\n\n'
        reply += 'add @メンバー or /add @メンバー or メンバーを追加 @メンバー \n\t指定したメンバーをリストに追加（纏めてのメンションやロール指定可能）\n\n'
        reply += 'memberlist or /memberlist or メンバーリストを表示 \n\t登録されているメンバーの一覧表示\n\n'
        reply += 'ボス凸履歴登録記法 ＋ メンション\n\tボス凸登録代筆（飼い主のみ実行可能）\n\t' \
                 '例:　1物〆135@90s @ジュウシマツ住職（住職代筆で1ボス〆持越先135、物理編成90秒）\n\n'
        reply += 'correct or /correct\n\t周回数を訂正する（飼い主のみ実行可能）\n\t例:　/correct 50\n\n'
        reply += 'remove @メンバー or /remove @メンバー\n\t指定したメンバーをリストから削除（飼い主のみ実行可能）\n\n'
        reply += 'sleep or /sleep\n\t休眠状態を切り替える。（飼い主のみ実行可能）\n\n'
        reply += '凸リストを全てクリア\n\tメンバーの凸状況を全てクリアする（飼い主のみ実行可能）　\n\n'
        reply += 'メンバーリストをクリア\n\tメンバーリスト・凸状況をクリアする（飼い主のみ実行可能）\n\n'
        reply += '入力チャンネル設定\n\tコマンド入力を受け付けるチャンネルの指定（飼い主のみ実行可能）\n\t'
        reply += '例:　入力チャンネル設定 #凸報告用\n\n'
        reply += '凸進捗リストチャンネル設定\n\t凸進捗を出力するチャンネルの指定（飼い主のみ実行可能）\n\t'
        reply += '例:　凸進捗リストチャンネル設定 #凸進捗リスト\n\n'
        reply += '凸未完了リストチャンネル設定\n\t凸未完了者一覧を出力するチャンネルの指定（飼い主のみ実行可能）\n\t'
        reply += '例:　凸未完了リストチャンネル設定 #3凸未完了リスト\n\n'
        reply += '通知リストチャンネル設定\n\t持越・通知登録者一覧を出力するチャンネルの指定（飼い主のみ実行可能）\n\t'
        reply += '例:　通知リストチャンネル設定 #持越中・通知登録リスト\n\n'
        reply += '絵文字設定\n\t簡易入力用の絵文字の指定（飼い主のみ実行可能）\n\t'
        reply += '例:　絵文字設定 （絵文字）（絵文字）（絵文字）（絵文字）（絵文字）\n\t'
        reply += "※　前から順に物理凸、物理〆、魔法凸、魔法〆、通知登録用の合計5つの絵文字を入力してください\n"
        reply += '簡易入力チャンネル設定\n\t簡易入力を受け付けるチャンネルの指定（飼い主のみ実行可能）\n\t'
        reply += '例:　簡易入力チャンネル設定 #簡易入力\n\n'
        reply += '飼い主設定\n\t飼い主ロールの指定（飼い主のみ実行可能）\n\t'
        reply += '例:　飼い主設定 @飼い主\n\t'
        reply += '※ 飼い主未設定の場合、誰でも飼い主権限コマンドが実行可能です\n\t'
        reply += '※ ロールをメンション出来ない、メンションする方法が判らない場合：\n\t\t'
        reply += 'ロール->ロール設定->このロールに対して@mentionを許可するを設定してください \n\n'
        reply += '```'
        await reply_and_delete(message, reply, DELAY_L)
        return

    # 飼い主設定
    if is_admin and re.match(r'^飼い主設定', msg_content):
        if message.role_mentions:
            ID_ROLE_ADMIN = message.role_mentions[0].id
            reply = message.role_mentions[0].name
            reply += 'を飼い主として設定しました'
            await reply_and_delete(message, reply, DELAY_S)
        else:
            reply = 'ロールがメンションされていません\n\t'
            reply += '※ ロールをメンション出来ない、メンションする方法が判らない場合：\n\t\t'
            reply += 'ロール->ロール設定->このロールに対して@mentionを許可するを設定してください \n\n'
            await reply_and_delete(message, reply, DELAY_L)
        return

    # コマンド入力チャンネル設定
    if is_admin and message.content.startswith('入力チャンネル設定'):
        if message.channel_mentions:
            ID_CHANNEL_MAIN = message.channel_mentions[0].id
            reply = message.channel_mentions[0].name
            reply += 'チャンネルをコマンド入力用に設定しました'
            await reply_and_delete(message, reply, DELAY_S)
        else:
            reply = 'チャンネルがメンションされていません'
            await reply_and_delete(message, reply, DELAY_S)

    # 進捗リスト出力チャンネル設定
    if is_admin and message.content.startswith('凸進捗リストチャンネル設定'):
        if message.channel_mentions:
            ID_CHANNEL_LOG_MAIN = message.channel_mentions[0].id
            reply = message.channel_mentions[0].name
            reply += 'チャンネルを凸進捗リストの出力用に設定しました'
            Message_Log_Main = None  # 凸進捗出力メッセージオブジェクト
            await reply_and_delete(message, reply, DELAY_S)
        else:
            reply = 'チャンネルがメンションされていません'
            await reply_and_delete(message, reply, DELAY_S)

    # 凸未完了リスト出力チャンネル設定
    if is_admin and message.content.startswith('凸未完了リストチャンネル設定'):
        if message.channel_mentions:
            ID_CHANNEL_LOG_INCOMPLETE = message.channel_mentions[0].id
            reply = message.channel_mentions[0].name
            reply += 'チャンネルを凸未完了者リストの出力用に設定しました'
            Message_Log_Incomplete = None  # 凸未完了者リスト出力メッセージオブジェクト
            await reply_and_delete(message, reply, DELAY_S)
        else:
            reply = 'チャンネルがメンションされていません'
            await reply_and_delete(message, reply, DELAY_S)

    # 通知リスト出力チャンネル設定
    if is_admin and message.content.startswith('通知リストチャンネル設定'):
        if message.channel_mentions:
            ID_CHANNEL_LOG_REQUEST = message.channel_mentions[0].id
            reply = message.channel_mentions[0].name
            reply += 'チャンネルを持越・通知希望リストの出力用に設定しました'
            Message_Log_Request = None  # 持越中・通知登録者リスト出力メッセージオブジェクト
            await reply_and_delete(message, reply, DELAY_S)
        else:
            reply = 'チャンネルがメンションされていません'
            await reply_and_delete(message, reply, DELAY_S)

    # 簡易コマンドリアクション用絵文字設定
    if is_admin and message.content.startswith('絵文字設定'):
        tmp_emojis = re.findall(r'<:\w*:\d*>', message.content)
        tmp_emojis = [int(e.split(':')[2].replace('>', '')) for e in tmp_emojis]

        if len(tmp_emojis) < 5:
            reply = '設定する絵文字の数が足りません\n'
            reply += '例:　絵文字設定 （絵文字）（絵文字）（絵文字）（絵文字）（絵文字）\n\t'
            reply += "※　前から順に物理凸、物理〆、魔法凸、魔法〆、通知登録用の合計5つの絵文字を入力してください\n"
            await reply_and_delete(message, reply, DELAY_S)
        elif len(tmp_emojis) == 5:
            ID_EMOJI = tmp_emojis
            reply = '簡易入力用絵文字を設定しました'
            await reply_and_delete(message, reply, DELAY_S)
        else:
            for i in range(5):
                ID_EMOJI[i] = tmp_emojis[i]
            reply = '簡易入力用絵文字を設定しました'
            await reply_and_delete(message, reply, DELAY_S)

    # 簡易コマンドリアクション用チャンネル設定
    if is_admin and message.content.startswith('簡易入力チャンネル設定'):
        if message.channel_mentions:
            ID_CHANNEL_REACT = message.channel_mentions[0].id
            # リアクションメッセージ設定
            await init_react_channel()
            reply = message.channel_mentions[0].name
            reply += 'チャンネルを簡易リアクション用に設定しました'
            await reply_and_delete(message, reply, DELAY_S)
        else:
            reply = 'チャンネルがメンションされていません'
            await reply_and_delete(message, reply, DELAY_S)

    # 絵文字設定済か確認
    Flg_No_Emoji = False
    for emoji_id in ID_EMOJI:
        if emoji_id is None:
            Flg_No_Emoji = True

    # 初期設定
    if ID_CHANNEL_MAIN and ID_CHANNEL_LOG_MAIN and ID_CHANNEL_LOG_INCOMPLETE \
            and ID_CHANNEL_LOG_REQUEST and ID_CHANNEL_REACT and not Flg_No_Emoji:
        Flg_Setup = False
    else:
        Flg_Setup = True
        await setup_wizard(message)
        return

    # メンバーリストに追加
    if re.match(r'^add|^/add|^メンバーを追加', msg_content):
        if message.role_mentions:  # ロールがメンションされていれば、ロールのメンバーを追加
            member_list = message.role_mentions[0].members
        elif message.mentions:  # リプがあればリプ対象を追加
            member_list = message.mentions
        else:  # リプがなければ送信主を追加
            member_list = [message.author]
        reply = ''
        for i in member_list:
            # 登録済みか確認し、登録されてたらスキップ
            is_matched = False
            for p in playerData:
                if i == p.user:
                    is_matched = True
                    reply += f'{i.display_name}の事は既に知っているぜ\n'
            if not is_matched:
                playerData.append(PlayerData(i, 0, 0, 0, 0, False, False, False, 0, 0, '', ''))
                reply += f'{i.display_name}さんをメンバーリストに追加\n'
        await reply_and_delete(message, reply, DELAY_S)
        return

    # メンバーリスト表示
    if re.match(r'ml$|memberlist$|/memberlist$|メンバーリストを表示$', msg_content):
        reply = f'```\n'
        for p in playerData:
            reply += f' {p.user.display_name} \n'
        reply += f'```'
        await reply_and_delete(message, reply, DELAY_M)
        return

    # ボス通知登録
    if re.match(r'^nt|^notice|^/notice|^ボス通知', msg_content):
        # ボスフラグ生成
        req_boss = 0
        for i in msg_content:
            if '0' < i < '6':
                req_boss |= 2 ** (int(i) - 1)
            elif i == '@':
                break
        # 対象をリストから探す
        for p in playerData:
            if p.user == orig_user and p.done_cnt != 3:
                # ログバックアップ
                p.backup_play_log()
                # 有効なボス引数があれば上書き
                if req_boss:
                    # 持越先希望じゃなくて凸希望登録の場合は、凸希望登録フラグを立てる（初回のみでいい）
                    if not p.notice_req and not p.req_none_rolled and not p.req_list:
                        p.notice_req = True
                    # 書込み
                    p.req_none_rolled = False
                    p.req_list = req_boss
                    reply = f'{p.user.display_name}さんのボス通知希望を確認'
                    await reply_and_delete(message, reply, DELAY_S)
                # 指定なしで通知解除
                else:
                    if not p.notice_req and p.req_list:
                        p.req_none_rolled = True
                    p.req_list = 0
                    p.notice_req = False
                    reply = f'{p.user.display_name}さんのボス通知希望を解除しました'
                    await reply_and_delete(message, reply, DELAY_S)

            elif p.user == orig_user and p.done_cnt == 3:
                reply = f'{p.user.display_name}さんは本日既に3凸済です'
                await reply_and_delete(message, reply, DELAY_S)
        return

    # ボス通知追加
    if re.match(r'^通知追加', msg_content):
        # ボスフラグ生成
        req_boss = 0
        for i in msg_content:
            if '0' < i < '6':
                req_boss |= 2 ** (int(i) - 1)
            elif i == '@':
                break
        # 対象をリストから探す
        for p in playerData:
            if p.user == orig_user and p.done_cnt != 3:
                # ログバックアップ
                p.backup_play_log()
                # 有効なボス引数があれば追加
                and_tmp = req_boss & p.req_list
                if req_boss and not and_tmp:
                    # 持越先希望じゃなくて凸希望登録の場合は、凸希望登録フラグを立てる（初回のみでいい）
                    if not p.notice_req and not p.req_none_rolled and not p.req_list:
                        p.notice_req = True
                    # 書込み
                    p.req_none_rolled = False
                    p.req_list |= req_boss
                    reply = f'{p.user.display_name}さんのボス通知希望を確認'
                    await reply_and_delete(message, reply, DELAY_S)
                # 指定なしで通知解除
                elif req_boss and and_tmp:
                    if not p.notice_req and p.req_list and not p.req_list ^ req_boss:
                        p.req_none_rolled = True
                    p.req_list = p.req_list ^ req_boss
                    if p.req_list:
                        p.notice_req = False
                    reply = f'{p.user.display_name}さんのボス通知希望を解除しました'
                    await reply_and_delete(message, reply, DELAY_S)

            elif p.user == orig_user and p.done_cnt == 3:
                reply = f'{p.user.display_name}さんは本日既に3凸済です'
                await reply_and_delete(message, reply, DELAY_S)
        return

    # 持越時間設定
    if re.match(r'^rt|^rolled|^/rolled|^持越', msg_content):
        for p in playerData:
            if p.user == orig_user and p.rolled_type:
                # ログバックアップ
                p.backup_play_log()
                tmp_rolled_time = 0
                is_rolled_time = False
                for i in msg_content:
                    if re.match('\d', i):
                        is_rolled_time = True
                        tmp_rolled_time = tmp_rolled_time * 10 + int(i)
                    elif is_rolled_time and i == "<":
                        break

                if tmp_rolled_time == 0:
                    p.rolled_time = 0
                    reply = f'{orig_user.display_name}さんの持越時間登録を削除しました'
                elif tmp_rolled_time < 20:
                    reply = f'持越時間が短すぎます'
                elif 20 <= tmp_rolled_time <= 90:
                    p.rolled_time = tmp_rolled_time
                    reply = f'{orig_user.display_name}さんの持越時間を登録しました'
                elif 90 < tmp_rolled_time:
                    reply = f'持越時間が長すぎます'
                else:
                    reply = f'持越登録に失敗しました'
                await reply_and_delete(message, reply, DELAY_S)
            elif p.user == orig_user:
                reply = f'{orig_user.display_name}さんは持越していません'
                await reply_and_delete(message, reply, DELAY_S)
        return

    # タスキル済
    if re.match(r'^kd|^killed|^/killed|^タスキル済', msg_content):
        for p in playerData:
            if p.user == orig_user:
                # ログバックアップ
                p.backup_play_log()
                p.task_killed = True
                reply = f'{orig_user.display_name}さんのタスキルを確認'
                await reply_and_delete(message, reply, DELAY_S)
        return

    # 凸リスト表示
    if re.match(r'la$|list-all$|/list-all$|凸リストを表示$', msg_content):
        reply = f'```\n'
        reply += await get_attack_log(0)
        reply += f'```'
        await reply_and_delete(message, reply, DELAY_M)
        return

    # 未凸リスト表示
    if re.match(r'li$|list$|/list$|未凸リストを表示$', msg_content):
        reply = f'```\n未凸者リスト\n\n'
        reply += await get_attack_log(1)
        reply += f'```'
        await reply_and_delete(message, reply, DELAY_M)
        return

    # ウェイトリスト表示
    if re.match(r'wl$|waitlist$|/waitlist$|ウェイトリストを表示$', msg_content):
        reply = f'```\n持越・通知登録リスト\n\n'
        reply += await get_attack_log(2)
        reply += f'```'
        await reply_and_delete(message, reply, DELAY_M)
        return

    # 直近の変更を元に戻す
    if re.match(r'^rv|^revert|^/revert|^元に戻す', msg_content):
        for p in playerData:
            if p.user == orig_user:
                try:
                    p.revert_play_log()
                    reply = f'{orig_user.display_name}さんの凸リストを元に戻しました。'
                except IndexError:
                    reply = f'{orig_user.display_name}さんの凸履歴はありません。'
                await reply_and_delete(message, reply, DELAY_S)
        return

    # 凸リストクリア
    if re.match(r'^cl|^clear|^/clear|^凸リストをクリア', msg_content):
        for p in playerData:
            if p.user == orig_user:
                # ログバックアップ
                p.backup_play_log()
                p.erase_all()
                reply = f'{orig_user.display_name}さんの凸リストをクリアしました。'
                await reply_and_delete(message, reply, DELAY_S)
        return

    # 凸リストを全てクリア
    if is_admin and msg_content == '凸リストを全てクリア':
        for p in playerData:
            p.erase_all()
            p.erase_backup()
        Message_Log_Main = None
        reply = f'凸リストを全てクリアしました'
        await reply_and_delete(message, reply, DELAY_S)
        return

    # メンバーリストクリア
    if is_admin and msg_content == 'メンバーリストをクリア':
        playerData.clear()
        Message_Log_Main = None
        reply = f'メンバーリストをクリアしました'
        await reply_and_delete(message, reply, DELAY_S)
        return

    # 対象をメンバーリストからクリア
    if is_admin and re.match(r'^remove|^/remove', msg_content):
        # リプがあればリプ対象を追加、リプがなければ送信主を追加
        if message.mentions:
            remove_user = message.mentions[0]
        else:
            remove_user = message.author
        if remove_user:
            # 登録済みか確認し、登録されてたら終了
            for p in playerData:
                if remove_user == p.user:
                    playerData.remove(p)
                    reply = f'{remove_user.display_name}さんをリストから削除しました'
                    await reply_and_delete(message, reply, DELAY_S)
                    return
            reply = f'{remove_user.display_name}さんはリストに載っていません'
            await reply_and_delete(message, reply, DELAY_S)
        return

    # 周回数修正
    global Boss_Round_Count
    if is_admin and re.match(r'^correct|^/correct', msg_content):
        Boss_Round_Count = 0
        for i in msg_content:
            if re.match('\d', i):
                Boss_Round_Count *= 10
                Boss_Round_Count += int(i)
        reply = f'周回数を修正しました'
        await reply_and_delete(message, reply, DELAY_S)
        return

    # 凸登録
    await submit_attack_log(message, orig_user)

client.run(TOKEN)
