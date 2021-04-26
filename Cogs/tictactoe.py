import discord
from discord.ext import commands
import random


class TicTacToe(commands.Cog):
    def __init__(self, bot, connection, cursor):
        self.bot = bot
        self.player1 = ""
        self.player2 = ""
        self.turn = ""
        self.gameOver = True
        self.connection = connection
        self.cursor = cursor
        self.board = []
        self.check_winer = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]

    @commands.command()
    async def tictactoe(self, ctx, p1: discord.User = None, p2: discord.User = None): # начало игры

        if self.gameOver:
            self.board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                          ":white_large_square:", ":white_large_square:", ":white_large_square:",
                          ":white_large_square:", ":white_large_square:", ":white_large_square:"]
            self.turn = ""
            self.gameOver = False
            self.count = 0
            self.player1 = p1
            self.player2 = p2
            self.line = ""
            for x in range(len(self.board)):
                if x == 2 or x == 5 or x == 8:
                    self.line += " " + self.board[x]
                    await ctx.send(self.line)
                    self.line = ""
                else:
                    self.line += " " + self.board[x]
            num = random.randint(1, 2)
            if num == 1:
                self.turn = self.player1
                await ctx.send("Начинет <@" + str(self.player1.id) + ">.")
            elif num == 2:
                self.turn = self.player2
                await ctx.send("Начинае <@" + str(self.player2.id) + ">.")
        else:
            await ctx.send("Игра уже идет! Закончите, прежде чем начинать новую.")

    @commands.command()
    async def place(self, ctx, pos: int): # сама игра
        if not self.gameOver:
            mark = ""
            if self.turn == ctx.author:
                if self.turn == self.player1:
                    mark = ":regional_indicator_x:"
                    self.player1_mark = mark
                elif self.turn == self.player2:
                    mark = ":o2:"
                    self.player2_mark = mark
                if 0 < pos < 10 and self.board[pos - 1] == ":white_large_square:":
                    self.board[pos - 1] = mark
                    self.count += 1

                    # print the board
                    self.line = ""
                    for x in range(len(self.board)):
                        if x == 2 or x == 5 or x == 8:
                            self.line += " " + self.board[x]
                            await ctx.send(self.line)
                            self.line = ""
                        else:
                            self.line += " " + self.board[x]

                    self.checkWinner(self.check_winer, mark)
                    if self.gameOver:
                        await ctx.send(mark + " победил!")
                        if self.player1_mark == mark:
                            self.cursor.execute(
                                "UPDATE users SET cash = cash + {} WHERE id = {}".format(1000, self.player1.id))
                            self.connection.commit()
                        else:
                            self.cursor.execute(
                                "UPDATE users SET cash = cash + {} WHERE id = {}".format(1000, self.player2.id))
                            self.connection.commit()
                    elif self.count == 9:
                        self.gameOver = True
                        await ctx.send("Ничья")
                    if self.turn == self.player1:
                        self.turn = self.player2
                    elif self.turn == self.player2:
                        self.turn = self.player1
                else:
                    await ctx.send("Обязательно выберите целое число от 1 до 9 (включительно).")
            else:
                if ctx != self.player1 or ctx != self.player2:
                    await ctx.send("Вы не играете.")
                else:
                    await ctx.send("Сейчас не Ваш ход.")
        else:
            if 0 < pos < 10:
                await ctx.send('Эта клатка уже занята')
            else:
                await ctx.send("Начните новую игру с помощью команды !tictactoe.")

    def checkWinner(self, check_winer, mark): # проверка победителя
        for check in check_winer:
            if self.board[check[0]] == mark and self.board[check[1]] == mark and self.board[check[2]] == mark:
                self.gameOver = True

    @tictactoe.error
    async def tictactoe_error(self, ctx, error): # ошибка ,когда не ввели одного / двух игроков
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Пожалуйста, укажите 2 игроков для этой команды.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Не забудьте упомянуть игроков (ie. <@688534433879556134>).")

    @place.error
    async def place_error(self, ctx, error): # проверка на нормальный ввод числа
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Пожалуйста, введите позицию, которую вы хотите отметить.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Убедитесь, что вы ввели целое число.")

    @commands.command()
    async def restart(self, ctx): # отмена игры
        self.gameOver = True
        await ctx.send("Игра отменена.")
