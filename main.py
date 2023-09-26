import discord
import random
import os
from discord.ext import commands
from keep_alive import keep_alive

# インテントの生成
intents = discord.Intents.default()
intents.message_content = True

# ボットを作成
bot = commands.Bot(command_prefix='/', intents=intents)

# Valorantエージェントのリスト
valorant_agents = [
    "ジェット", "レイズ", "フェニックス", "レイナ", "ヨル", "ネオン", "セージ", "サイファー", "キルジョイ",
    "チェンバー", "デッドロック", "ブリーチ", "ソーヴァ", "スカイ", "KAY/O", "フェイド", "ゲッコー", "オーメン",
    "ブリムストーン", "ヴァイパー", "アストラ", "ハーバー"
]

# ハンドガン武器リストとその出現確率（重み）
valorant_handgun = ["クラシック", "ショーティ", "フレンジー", "ゴースト", "シェリフ"]
handgun_weights = [1, 0.5, 1, 1, 1]  

#　普通の武器リストとその出現確率（重み）
valorant_eco = [
    "スティンガー", "バッキー", "アレス","マーシャル", "ジャッジ", "スペクター"
]
eco_weights = [1, 0.8, 1, 1, 0.8, 1]  

# 強い武器リストとその出現確率（重み）
valorant_buy = [
   "ブルドッグ", "ガーディアン", "ヴァンダル", "ファントム", "オーディン", "オペレーター"
]
buy_weights = [ 0.7, 0.7, 1, 1, 1, 0.7]  

# Discordコマンド
@bot.command(name='random_agent')
async def random_agent(ctx):
  # ランダムにValorantエージェントを選択
  random_agent = random.choice(valorant_agents)

  # コマンドを打ったチャンネルに結果を送信
  await ctx.send(f'{ctx.author.display_name} さんのランダムエージェントは {random_agent} です！')

@bot.command(name='random_agents')
async def random_agents(ctx):
  # ボイスチャンネルに参加しているユーザーを取得
  if ctx.author.voice and ctx.author.voice.channel:
    voice_channel = ctx.author.voice.channel
    members = voice_channel.members

    # ボイスチャンネルのユーザー数に合わせてランダムエージェントを選択
    if members:
      random_agent_list = random.sample(valorant_agents, len(members))
      response = "ランダムエージェント\n"

      # メンバーごとに名前とランダムエージェントを組み合わせて表示
      for member, agent in zip(members, random_agent_list):
        response += f"{member.display_name}: {agent}\n"

      # 1つのメッセージにまとめて送信
      await ctx.send(response)
    else:
      await ctx.send('ボイスチャンネルに誰もいません。')
  else:
    await ctx.send('ボイスチャンネルに接続していません。')


# ボイスチャンネルのユーザーにランダムな武器を割り当てるコマンド
@bot.command(name='random_weapons')
async def random_weapons(ctx):
    # ボイスチャンネルに参加しているユーザーを取得
    if ctx.author.voice and ctx.author.voice.channel:
        voice_channel = ctx.author.voice.channel
        members = voice_channel.members

        # ボイスチャンネルのユーザー数に合わせて武器結果を作成
        if members:
            response = f'ランダム武器\n'

            for member in members:
                handgun = random.choices(valorant_handgun, weights=handgun_weights, k=1)[0]
                eco = random.choices(valorant_eco, weights=eco_weights, k=1)[0]
                buy = random.choices(valorant_buy, weights=buy_weights, k=1)[0]

                response += f'{member.display_name} さん\n'
                response += f'1つ目の武器: {handgun}\n'
                response += f'2つ目の武器: {eco}\n'
                response += f'3つ目の武器: {buy}\n\n'

            await ctx.send(response)
        else:
            await ctx.send('ボイスチャンネルに誰もいません。')
    else:
        await ctx.send('ボイスチャンネルに接続していません。')


# ご利用の Discord ボットトークンを指定してクライアントを実行
keep_alive()
# シークレットキーの取得
my_secret = os.environ['KEY']

bot.run(my_secret)
