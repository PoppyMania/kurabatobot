from discord.ext import commands
import asyncio
import random
import os
import math
import traceback
from datetime import datetime
from discord.ext import commands
from discord.ext import tasks

ID_role_1 = 767249291730747403
ID_role_2 = 767200011749949470
ID_role_3 = 767200106557865985
ID_role_tk = 767200196827676683
ID_clanmember = 666361330827132979
ID_role_test = 760094885364629524
prefix = '/'
token = os.environ['DISCORD_BOT_TOKEN']


        # プリコネキャラ
class SkillMotionGIF(commands.Cog, name = 'スキルモーション'):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        

    @commands.command()
    async def kurisu(self,ctx):
        """クリス"""
        await ctx.send('https://gyazo.com/39f3bddc360ed09f20431c79d809e3fb')
        await ctx.message.delete()
    @commands.command()
    async def mizumakoto(self,ctx):
        """マコト(サマー)"""
        await ctx.send('https://i.gyazo.com/6e1c942142ce952e7b15c8f1aa6e6d73 \n 水が弾けたら')
        await ctx.message.delete()
    @commands.command()
    async def makoto(self,ctx):
        """マコト"""
        await ctx.send('https://i.gyazo.com/016e0804ce330f11c6fcf75a60f89277 \n 黄色の鳴き声が消えたら')
        await ctx.message.delete()
    @commands.command()
    async def muimi(self,ctx):
        """ムイミ"""
        await ctx.send('https://i.gyazo.com/016e0804ce330f11c6fcf75a60f89277 \n 左斜め後ろに飛んだ時')
        await ctx.message.delete()
    @commands.command()
    async def tamaki(self,ctx):
        """タマキ"""
        await ctx.send('https://i.gyazo.com/ede0b883427fbbe2dbd944d03f0d3030')
        await ctx.message.delete()     
    @commands.command()
    async def onon(self,ctx):
        """ニノン(オーエド)"""
        await ctx.send('https://gyazo.com/9ef7490093e2ce4114fc33b49b68a9f9')
        await ctx.message.delete()
    @commands.command()
    async def mizuna(self,ctx):
        """スズナ(サマー)"""
        await ctx.send('https://i.gyazo.com/2b2c3b9dc2856a1d55d167bf920af87d')
        await ctx.message.delete()
    @commands.command()
    async def neneka(self,ctx):
        """ネネカ"""
        await ctx.send('https://i.gyazo.com/588cb732059044e1be0712694eadcffd')
        await ctx.message.delete()
    @commands.command()
    async def puripeko(self,ctx):
        """ペコリーヌ(プリンセス)"""
        await ctx.send('https://gyazo.com/0f0514e31d8b6136f87c33184b649b8d \n 切った後に剣を振り上げたタイミングでバフ付与')
        await ctx.message.delete()
    @commands.command()
    async def mizukyaru(self,ctx):
        """キャル(サマー)"""
        await ctx.send('https://i.gyazo.com/cf8625a0f3fbe7ce5a47f00e2305568a')
        await ctx.message.delete()
    @commands.command()
    async def purikoro(self,ctx):
        """コッコロ(プリンセス)"""
        await ctx.send('https://gyazo.com/04ffe3e6e434d79c816a837e435c1ff1')
        await ctx.message.delete()    
    @commands.command()
    async def harokyo(self,ctx):
        """キョウカ(ハロウィン)"""
        await ctx.send('https://i.gyazo.com/60d59c64eb5c8a9443bd4de074cc03de \n 箒を突き刺した時/箒を振り終わった後')
        await ctx.message.delete()
    @commands.command()
    async def mizusaren(self,ctx):
        """サレン(サマー)"""
        await ctx.send('https://gyazo.com/c22d7996cb2d8e91ae7308b53c66d6d4 \n 右を向いた時')
        await ctx.message.delete()
    @commands.command()
    async def nyukkoro(self,ctx):
        """コッコロ(ニューイヤー)"""
        await ctx.send('https://gyazo.com/c29e006bf82ce2fb0e3b44c06405a9ce \n 左を向いた時')
        await ctx.message.delete()    
    @commands.command()
    async def haromimi(self,ctx):
        """ミミ(ハロウィン)"""
        await ctx.send('https://i.gyazo.com/42f21611ee06890d48f4ffd4d38e6476 \n ぴょん ぴょん ぴょこ←ｺｺ')
        await ctx.message.delete()
    @commands.command()
    async def bazuru(self,ctx):
        """シズル(バレンタイン)"""
        await ctx.send('https://i.gyazo.com/87b47efe83e874247b66519ce2caa78b')
        await ctx.message.delete()
    @commands.command()
    async def kuritika(self,ctx):
        """チカ(クリスマス)"""
        await ctx.send('https://i.gyazo.com/d9b5fcdfca2cac56f82cfd1c9feefd9d \n 足元に魔法陣が出たら/tp配布の数字を見る')
        await ctx.message.delete()    
    @commands.command()
    async def yuni(self,ctx):
        """ユニ"""
        await ctx.send('https://gyazo.com/67a7c23623583779f069e697df22aa23 \n どちらもジャンプ着地時')
        await ctx.message.delete()
    @commands.command()
    async def rei(self,ctx):
        """レイ"""
        await ctx.send('https://i.gyazo.com/4dd4fbfc1687f4529e2f474a84c7a991')
        await ctx.message.delete()
    @commands.command()
    async def suzuna(self,ctx):
        """スズナ"""
        await ctx.send('https://gyazo.com/0f21de3dba9d6d69dee31ef7991b71fc')
        await ctx.message.delete()
    @commands.command()
    async def an(self,ctx):
        """アン"""
        await ctx.send('https://gyazo.com/4771ba5961617b5d66e8fe2aacdc3562')
        await ctx.message.delete()
    @commands.command()
    async def misato(self,ctx):
        """ミサト"""
        await ctx.send('https://gyazo.com/d759d75e36acd6942f1e20d5bf5654ba')
        await ctx.message.delete() 
    @commands.command()
    async def mizumaho(self,ctx):
        """マホ(サマー)"""
        await ctx.send('https://gyazo.com/2848612666b463901e2960c0282685b5')
        await ctx.message.delete()
    @commands.command()
    async def haromiso(self,ctx):
        """ミソギ(ハロウィン)"""
        await ctx.send('https://gyazo.com/667afa5b86200885f706cd8cf65e7651')
        await ctx.message.delete()
    @commands.command()
    async def hiyori(self,ctx):
        """ヒヨリ"""
        await ctx.send('https://gyazo.com/0fceb161f3ddeb1807f048271416525f')
        await ctx.message.delete()
    @commands.command()
    async def mizuhatsune(self,ctx):
        """ハツネ(サマー)"""
        await ctx.send('https://gyazo.com/84891d66caf2de0092a9041020d9145e')
        await ctx.message.delete()
    @commands.command()
    async def mizutama(self,ctx):
        """タマキ(サマー)"""
        await ctx.send('https://gyazo.com/b83b2ad4e9e769321a66749da3a59466')
        await ctx.message.delete() 
    @commands.command()
    async def haromiya(self,ctx):
        """ミヤコ(ハロウィン)"""
        await ctx.send('https://gyazo.com/f95a085630f753ee75f89bd666588484')
        await ctx.message.delete()  
    @commands.command()
    async def nyuyori(self,ctx):
        """ヒヨリ(ニューイヤー)"""
        await ctx.send('https://gyazo.com/fc9f5b592ccfabd7a138977e6d97e774')
        await ctx.message.delete() 
    @commands.command()
    async def tieru(self,ctx):
        """チエル"""
        await ctx.send('https://gyazo.com/828212c3cc6121942c37c8788425d5d2')
        await ctx.message.delete() 
        
    @commands.command()
    async def erogaki(self,ctx):
        """アカリ(エロガキ)"""
        await ctx.send('https://gyazo.com/0fa628c9a38b842fb48ab404cc57f6b5 \n S1:着地で押す')
        await ctx.message.delete() 
    @commands.command()
    async def rabirisuta(self,ctx):
        """ラビリスタ"""
        await ctx.send('https://i.gyazo.com/83468807130359544b8f7c987f5fabc3 \n https://i.gyazo.com/26bb2398837fb68c2fbd0bae128c88a7')
        await ctx.message.delete()
    @commands.command()
    async def akino(self,ctx):
        """アキノ"""
        await ctx.send('https://i.gyazo.com/095793437d33fce8cd982be40c0c39fa')
        await ctx.message.delete()
        

class DamageCalc(commands.Cog, name = '持ち越し計算機'):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.command()
    async def motikosi(self,ctx, boss: int, p1: int, p2: int):
        """持越し時間計算機 /motikosi (凸時のボスHP) (先に抜ける人の与ダメ) (後に抜ける人の与ダメ)"""
        total = p1 + p2
        if total > boss and p1 < boss and p2 < boss:
            cotime = 90 - (90*(boss-p1)/p2) + 20
            text = "持ち越し時間は" + str(math.ceil(cotime)) + "秒です"       
        else:
            text = "持ち越しは発生しません"
        #await ctx.send(text)
        sent = await ctx.send(text)        
        await asyncio.sleep(10)
        await ctx.message.delete()
        #sent = await ctx.send(text)
        await sent.delete()        
    async def gyakusan(self,ctx, boss: int, p1: int):
        """90秒計算機 /gyakusan (凸時のボスHP) (先に抜ける人の与ダメ)"""
        
        if p1 < boss:
            codamage = 9*(boss-p1)/2
            text = str(math.ceil(codamage)) + "ダメージ以上なら９０秒持ち越します"       
        else:
            text = "持ち越しは発生しません"
        #await ctx.send(text)
        sent = await ctx.send(text)  
        await asyncio.sleep(10) 
        await ctx.message.delete()        
        #ent = await ctx.send(text)
        await sent.delete()

class BestUrl(commands.Cog, name = 'みんなのおすすめ'):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        
        

    @commands.command()
    async def jantama(self,ctx):
        """じゃんたま公式HP"""
        await ctx.send(ctx.message.author.name + "さん、どうぞ！" + 'https://game.mahjongsoul.com/')
        await ctx.message.delete()
    @commands.command()
    async def dbd(self,ctx):
        """DbDストアページ"""
        await ctx.send(ctx.message.author.name + "さん、どうぞ！" + 'https://store.steampowered.com/app/381210/Dead_by_Daylight/')
        await ctx.message.delete()
    @commands.command()
    async def pubg(self,ctx):
        """pubuストアページ"""
        await ctx.send(ctx.message.author.name + "さん、どうぞ！" + 'https://store.steampowered.com/app/578080/PLAYERUNKNOWNS_BATTLEGROUNDS/')
        await ctx.message.delete()
    @commands.command()
    async def patora(self,ctx):
        """周防パトラ"""
        await ctx.send(ctx.message.author.name + "さん、どうぞ！" + 'https://www.youtube.com/channel/UCeLzT-7b2PBcunJplmWtoDg \n https://twitter.com/Patra_HNST') 
        await ctx.message.delete()
    @commands.command()
    async def suzuhara(self,ctx):
        """鈴原るる"""
        await ctx.send(ctx.message.author.name + "さん、どうぞ！" + 'https://www.youtube.com/channel/UC_a1ZYZ8ZTXpjg9xUY9sj8w')
        await ctx.message.delete()
    @commands.command()
    async def syaruru(self,ctx):
        """しゃるる"""
        await ctx.send(ctx.message.author.name + "さん、どうぞ！" + 'https://www.twitch.tv/syaruru3 \n https://www.youtube.com/channel/UC5SYDKMBeExdFs0ocWiK6xw')
        await ctx.message.delete()
    @commands.command()
    async def pekorakopipe(self,ctx):
        """ぺこらコピペ"""
        await ctx.send('ぺこーらいつもありがとう！ \n 最近ぺこーらへ感謝するのが日課になりつつあります！ \n 単刀直入に我慢してたこと書いちゃう！ \n ぺこーら愛してるぞおおおお \n (ps.厄介野うさぎだと思われてそうですがが長文赤スパ失礼！ \n ちなみに読まれてる頃にはあまりの恥ずかしさにユニバーサル大回転ぺこぺこの舞₍ ◝(‘ω’)◟ ⁾⁾₍₍ ◝(‘ω’)◜ ₎₎しながらベットの上で暴れてると思うので率直な一言貰ってもいいですか？w  \n 最後に一言！配信をはじめ本当にいつもありがとう！！！ \n 野うさぎ達を大切に思ってくれてる姿勢冗談抜きで本当に好きです。 \n 応援するしがいがあります！') 
        await ctx.message.delete()
    @commands.command()
    async def l4d2(self,ctx):
        """l4d2ストアページ"""
        await ctx.send(ctx.message.author.name + "さん、どうぞ！" + 'https://store.steampowered.com/app/550/Left_4_Dead_2/')
        await ctx.message.delete()
    @commands.command()
    async def kogatan(self,ctx):
        """月岡恋鐘フィギュア"""
        await ctx.send(ctx.message.author.name + "さん、どうぞ！" + '月岡恋鐘フィギュアが予約開始！予約はこちらから！↓↓↓ \n https://www.goodsmile.info/ja/product/9770/%E6%9C%88%E5%B2%A1%E6%81%8B%E9%90%98+%E3%83%95%E3%82%A7%E3%82%A4%E3%82%B9%E3%82%AA%E3%83%96%E3%83%88%E3%83%AC%E3%82%B8%E3%83%A3%E3%83%BCVer.html')
        await ctx.message.delete()
    @commands.command()
    async def ow(self,ctx):
        """クソゲ"""
        await ctx.send(ctx.message.author.name + "さん、どうぞ！" + 'https://playoverwatch.com/ja-jp/')
        await ctx.message.delete()
    @commands.command()
    async def apex(self,ctx):
        """apex公式"""
        await ctx.send(ctx.message.author.name + "さん、どうぞ！" + 'https://www.ea.com/ja-jp/games/apex-legends') 
        await ctx.message.delete()
    @commands.command()
    async def kaya(self,ctx):
        """ドラゴンズエンドフィ.gif"""
        await ctx.send('https://cdn.discordapp.com/attachments/620957812247363594/731102733188333600/nXasbmNiZdEOItOpeAYD1594378196-1594378480_1.gif')   
        await ctx.message.delete()     
    @commands.command()
    async def nyaru(self,ctx):
        """ニューイヤーバースト"""
        await ctx.send('https://cdn.discordapp.com/attachments/620957812247363594/731098724406919179/image0.gif')  
        await ctx.message.delete()
    @commands.command()
    async def bga(self,ctx):
        """ボードゲームアリーナ"""
        await ctx.send(ctx.message.author.name + "さん、どうぞ！" + 'https://ja.boardgamearena.com/')
        await ctx.message.delete()
    @commands.command()
    async def swb(self,ctx):
        """サマーウルフェンブリッツ.gif"""
        await ctx.send('http://cdn.gameinn.jp/wp-content/uploads/imgs/2020/03/Dz5PPIn.gif') 
        await ctx.message.delete()
    @commands.command()
    async def yabaiwayo(self,ctx):
        """ヤバいわよ.gif"""
        await ctx.send('https://img.animanch.com/2020/05/1588593715655.gif') 
        await ctx.message.delete()
    @commands.command()
    async def ron(self,ctx):
        """ケインコスギの物まね"""
        await ctx.send('https://www.youtube.com/watch?v=ZX5ctEzgbpw') 
        await ctx.message.delete()     
    @commands.command()
    async def tensura(self,ctx):
        """転スラwiki"""
        await ctx.send(ctx.message.author.name + "さん、どうぞ！" + 'https://ja.wikipedia.org/wiki/%E8%BB%A2%E7%94%9F%E3%81%97%E3%81%9F%E3%82%89%E3%82%B9%E3%83%A9%E3%82%A4%E3%83%A0%E3%81%A0%E3%81%A3%E3%81%9F%E4%BB%B6')
        await ctx.message.delete()   

        
    @commands.command()
    async def tinpokopon(self,ctx):
        """ちんぽこぽん"""
        await ctx.send('https://cdn.discordapp.com/attachments/638718958819606549/749276683302862891/pokopon.gif')   
        await ctx.message.delete()
    @commands.command()
    async def supusi(self,ctx):
        """プリコネスプシ"""
        await ctx.send(ctx.message.author.name + "さん、どうぞ！" + 'https://docs.google.com/spreadsheets/d/1nCdtFHS-60WcRZDx8hTXHFm3mPuEqefntQxeRfM2Lv0/edit#gid=632518118')
        await ctx.message.delete()
    
    @commands.command()
    async def saru(self,ctx):
        """さるさんを呼び出す"""
        saru = [
                'https://img.huffingtonpost.com/asset/5c63b0b72000008b026e784d.jpeg?ops=scalefit_960_noupscale',
                'https://tenor.com/view/monkey-laughing-lol-laughing-hysterically-gif-17632955',
                'https://cdn.discordapp.com/attachments/638718958819606549/749243434673635359/85635abe435992f4abf56c529f4b2be7.png',
                'https://tenor.com/view/boat-monkey-driving-monkey-monkey-driving-boat-funny-monkey-gif-5232687']
        await ctx.send(random.choice(saru) )
        await ctx.message.delete() 
    @commands.command()
    async def howa(self,ctx):
        """ほわさんを呼び出す"""
        howa = ['https://gyazo.com/2e64e20055545d61110c008050a8a016','https://gyazo.com/8d95c633faaf0a589631241d2274703f',
                'https://gyazo.com/3e655e7f91e586737bdd22e3d2964dcc','https://gyazo.com/572820a2a4a350187563528143aa1f28',
                'https://gyazo.com/b17a7733d777762ba75a3c9ed8bd9a47','https://media.discordapp.net/attachments/628175073504788491/748931562325803038/image0.png',
                'https://cdn.discordapp.com/attachments/628175073504788491/749234343838351462/howa_1.png',
                'https://gyazo.com/63c7a98e1657a7788a15c915604eb730',
                'https://cdn.discordapp.com/attachments/628175073504788491/749234943447793674/2020-08-29_5.png',
                'https://i.gyazo.com/thumb/1200/db0d354a6db0f23d5551bf2e4bfb1efb-png.jpg','https://gyazo.com/c2d098590fe775ee921fce983d72e2e4',
                'https://gyazo.com/dee2d094a1ad9a89fee2012c38248783','https://gyazo.com/4d5dd57a27255343f2310c999c0e1261',
                'https://gyazo.com/a01dd357ce772dae25305dd9700f5377']
        await ctx.send(ctx.message.author.name + 'が <@!260693854070505472> 様を呼んでいるよ！ \n ' + random.choice(howa) )
        await ctx.message.delete()
    @commands.command()
    async def sarunokuruma(self,ctx):
        """さるさんが以前乗っていたくるま"""
        await ctx.send('https://img.gifmagazine.net/gifmagazine/images/3083728/original.gif' )
        await ctx.message.delete()
    @commands.command()
    async def ritoriri(self,ctx):
        """リトルリリカルの星６UB"""
        await ctx.send('https://cdn.discordapp.com/attachments/668715128627396640/749213006784888842/image0.png' )
        await ctx.message.delete()
    @commands.command()
    async def madoka(self,ctx):
        """お前樋口円香わかってなさすぎるだろ"""
        await ctx.send('https://media.discordapp.net/attachments/668715128627396640/749213459954270208/image0.jpg' )
        await ctx.message.delete()
    @commands.command()
    async def waruine(self,ctx):
        """わるいね収容者リスト"""
        await ctx.send('https://twitter.com/i/lists/1227212620387643392' )
        await ctx.message.delete()
    @commands.command()
    async def sarurage(self,ctx):
        """さるさんがおこった"""
        await ctx.send('https://www.youtube.com/watch?v=GhxqIITtTtU' )
        await ctx.message.delete()
    @commands.command()
    async def sime(self,ctx):
        """〆"""
        await ctx.send('https://cdn.discordapp.com/attachments/668715128627396640/749583481121669120/EglWTaVVgAEIIBG.png' )
        await ctx.message.delete()
    @commands.command()
    async def gyouza(self,ctx):
        """ぎょうさ"""
        await ctx.send('https://cdn.discordapp.com/attachments/638718958819606549/749650658784837753/E9A483E5AD90E38391E383AAE38383E381A8E38195E3819BE3819FE3818FE381A601.png' )
        await ctx.message.delete()
    @commands.command()
    async def gacha(self,ctx):
        """ガチャシミュレータ"""
        gacha = ['10','20','30','40','50','60','70','80','90','100','110','120','130','140','150','160','170','180','190','200','210','220','230','240','250','260','270','280','290','300']
        await ctx.send(ctx.message.author.name + 'は' + random.choice(gacha) + '連で出ます' )
        await ctx.message.delete()
        
    @commands.command()
    async def gachapopimasa(self,ctx):
        """ガチャシミュレータ"""
        
        await ctx.send('ぽぴまさは単発で出ます' )
        await ctx.message.delete()


class Game(commands.Cog, name = 'おもちゃ'):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.command()
    async def uranai(self,ctx):
        """占い"""
        #レスポンスされる運勢のリストを作成
        unsei = ["大吉", "中吉", "吉", "末吉", "小吉", "凶", "大凶"]
        choice = random.choice(unsei) #randomモジュールでunseiリストからランダムに一つを選出
        await ctx.send(choice)

    @commands.command()
    async def janken(self,ctx):
        """じゃんけん"""
        #レスポンスされる運勢のリストを作成
        janken = ["<:31lolgoo:666949640955887628>", "✌️ ", "🖐️"]
        choice = random.choice(janken) #randomモジュールでunseiリストからランダムに一つを選出
        await ctx.send(choice)
        
    @commands.command()  
    async def rolereset(self, ctx):
        # role1 = discord.utils.find(lambda r: r.name == '1凸', ctx.guild.roles)  
        # role2 = discord.utils.find(lambda r: r.name == '2凸', ctx.guild.roles) 
        # role3 = discord.utils.find(lambda r: r.name == '3凸', ctx.guild.roles) 
        # roletk = discord.utils.find(lambda r: r.name == 'タスクキル済', ctx.guild.roles)  
        role1 = ctx.guild.get_role(ID_role_1)
        role2 = ctx.guild.get_role(ID_role_2)
        role3 = ctx.guild.get_role(ID_role_3)
        roletk = ctx.guild.get_role(ID_role_tk) 

        
        for member in ctx.guild.members:  
            if not member.bot:  
                await ctx.send(member.name)              
                await member.remove_roles(role1)
                await member.remove_roles(role2)  
                await member.remove_roles(role3)
                await member.remove_roles(roletk)
        await ctx.send('本日の凸状況をすべてリセットしました')
                
    @commands.command()
    async def roleremovetest(self, ctx):
        roletest = ctx.guild.get_role(ID_role_test)
        for member in ctx.guild.members:
            if not member.bot:

                await member.remove_roles(roletest)
        await ctx.send('本日の凸状況をすべてリセットしました')
        await asyncio.sleep(5) 
        await ctx.message.delete()


bot = commands.Bot(command_prefix=prefix)
bot.add_cog(SkillMotionGIF(bot=bot))
bot.add_cog(DamageCalc(bot=bot))
bot.add_cog(BestUrl(bot=bot))
bot.add_cog(Game(bot=bot))

bot.run(token)   
