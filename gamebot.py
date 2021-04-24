import discord
from discord.ext import commands


class GameBot(commands.Cog):
    def __init__(self, bot, cursor, connection):
        self.bot = bot
        self.connection = connection
        self.cursor = cursor

    @commands.command(aliases=['balance', 'cash'])
    async def __balance(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send(embed=discord.Embed(
                description=f"""Баланс пользователя **{ctx.author}** составляет **{self.cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} :leaves:**"""
            ))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"""Баланс пользователя **{member}** составляет **{self.cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]} :leaves:**"""
            ))

    @commands.command(aliases=['award'])
    @commands.has_permissions(administrator=True)
    async def __award(self, ctx, member: discord.Member = None, amount: int = None):
        if member is None:
            await ctx.send(f"**{ctx.author}**, укажите пользователя, которому желаете выдать определенную сумму")
        else:
            if amount is None:
                await ctx.send(f"**{ctx.author}**, укажите сумму, которую желаете начислить на счет пользователя")
            elif amount < 1:
                await ctx.send(f"**{ctx.author}**, укажите сумму больше 1 :leaves:")
            else:
                self.cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(amount, member.id))
                self.connection.commit()
                await ctx.message.add_reaction('✅')

    @commands.command(aliases=['take'])
    @commands.has_permissions(administrator=True)
    async def __take(self, ctx, member: discord.Member = None, amount=None):
        if member is None:
            await ctx.send(f"**{ctx.author}**, укажите пользователя, у которого желаете отнять сумму денег")
        else:
            if amount is None:
                await ctx.send(f"**{ctx.author}**, укажите сумму, которую желаете отнять у счета пользователя")
            elif amount == 'all':
                self.cursor.execute("UPDATE users SET cash = {} WHERE id = {}".format(0, member.id))
                self.connection.commit()
                await ctx.message.add_reaction('✅')
            elif int(amount) < 1:
                await ctx.send(f"**{ctx.author}**, укажите сумму больше 1 :leaves:")
            else:
                self.cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(int(amount), member.id))
                self.connection.commit()
                await ctx.message.add_reaction('✅')

    @commands.command(aliases=['add-shop'])
    @commands.has_permissions(administrator=True)
    async def __add_shop(self, ctx, role: discord.Role = None, cost: int = None):
        if role is None:
            await ctx.send(f"**{ctx.author}**, укажите роль, которую вы желаете внести в магазин")
        else:
            if cost is None:
                await ctx.send(f"**{ctx.author}**, укажите стоимость для даннойй роли")
            elif cost < 0:
                await ctx.send(f"**{ctx.author}**, стоимость роли не может быть такой маленькой")
            else:
                self.cursor.execute("INSERT INTO shop VALUES ({}, {}, {})".format(role.id, ctx.guild.id, cost))
                self.connection.commit()
                await ctx.message.add_reaction('✅')

    @commands.command(aliases=['remove-shop'])
    @commands.has_permissions(administrator=True)
    async def __remove_shop(self, ctx, role):
        try:
            if role is None:
                await ctx.send(f"**{ctx.author}**, укажите роль, которую вы желаете удалить из магазина")
            else:
                self.cursor.execute("DELETE FROM shop WHERE role_id = {}".format(role.id))
                self.connection.commit()
                await ctx.message.add_reaction('✅')
        except Exception:
            await ctx.send(f'Такой роли нет')

    @commands.command(aliases=['shop'])
    async def __shop(self, ctx):
        embed = discord.Embed(title='Магазин ролей')
        for row in self.cursor.execute("SELECT role_id, cost FROM shop WHERE id = {}".format(ctx.guild.id)):
            if ctx.guild.get_role(row[0]):
                embed.add_field(
                    name=f"Стоимость **{row[1]} :leaves:**",
                    value=f"Вы приобрете роль {ctx.guild.get_role(row[0]).mention}",
                    inline=False
                )
            else:
                pass
        await ctx.send(embed=embed)

    @commands.command(aliases=['buy', 'buy-role'])
    async def __buy(self, ctx, role):
        try:
            if role is None:
                await ctx.send(f"**{ctx.author}**, укажите роль, которую вы желаете приобрести")
            else:
                if role in ctx.author.roles:
                    await ctx.send(f"**{ctx.author}**, у вас уже имеется данная роль")
                elif self.cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0] > \
                        self.cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]:
                    await ctx.send(f"**{ctx.author}**, у вас недостаточно средств для покупки данной роли")
                else:
                    await ctx.author.add_roles(role)
                    self.cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(
                        self.cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0],
                        ctx.author.id))
                    self.connection.commit()
                    await ctx.message.add_reaction('✅')
        except Exception:
            await ctx.send('Такой роли нет')

    @commands.command(aliases=['rep', '+rep'])
    async def __rep(self, ctx, member):
        try:
            if member is None:
                await ctx.send(f"**{ctx.author}**, укажите участника сервера")
            else:
                if member.id == ctx.author.id:
                    await ctx.send(f"**{ctx.author}**, вы не можете указать смого себя")
                else:
                    self.cursor.execute("UPDATE users SET rep = rep + {} WHERE id = {}".format(1, member.id))
                    self.connection.commit()
                    await ctx.message.add_reaction('✅')
        except Exception:
            await ctx.send('Такого пользователья нет')

    @commands.command(aliases=['leaderboard', 'lb'])
    async def __leaderboard(self, ctx):
        embed = discord.Embed(title='Топ 10 сервера')
        counter = 0
        for row in self.cursor.execute(
                """SELECT name, cash, rep FROM users WHERE server_id = {} ORDER BY cash DESC LIMIT 10""".format(
                    ctx.guild.id)):
            counter += 1
            embed.add_field(
                name=f'# {counter} | `{row[0]}`',
                value=f'Баланс: {row[1]}\nПохвал: {row[2]}',
                inline=False
            )
        await ctx.send(embed=embed)
