import discord
from discord.ext import commands
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# IDs do servidor e dos canais
GUILD_ID = 1279229840238837874  # Substitua pelo ID do servidor
CHANNEL_ID = 1279796453832654914  # Substitua pelo ID do canal de registro
LOG_CHANNEL_ID = 1280118325678047262  # Canal para registrar informações de novos registros
SELECTION_CHANNEL_ID = 1279798462543827015  # Canal para seleção de cargos
CARGO_REQUEST_MESSAGE_ID = 1280859000153575537  # ID da mensagem para solicitar cargo

@bot.event
async def on_ready():
    print(f'Bot está online como {bot.user.name}')
    
    # Atualizando a mensagem de registro existente
    guild = bot.get_guild(GUILD_ID)
    if guild:
        channel = guild.get_channel(CHANNEL_ID)
        if channel:
            try:
                message = await channel.fetch_message(1280635360694767657)  # ID da mensagem existente de registro
                view = RegistroView()
                await message.edit(view=view)
            except discord.NotFound:
                print("Mensagem de registro não encontrada.")

        # Atualizando a mensagem de seleção de cargo existente
        selection_channel = guild.get_channel(SELECTION_CHANNEL_ID)
        if selection_channel:
            try:
                selection_message = await selection_channel.fetch_message(CARGO_REQUEST_MESSAGE_ID)  # ID da mensagem de seleção de cargo
                selection_view = CargoSelectionView()
                await selection_message.edit(view=selection_view)
            except discord.NotFound:
                print("Mensagem de solicitação de cargo não encontrada.")

@bot.command(name="horario")
async def horario(ctx):
    """Mostra a data e a hora atuais."""
    now = datetime.now()
    formatted_time = now.strftime("%d/%m/%Y %H:%M:%S")
    await ctx.send(f"A data e hora atuais são: {formatted_time}")

@bot.command(name="infos")
async def infos(ctx):
    """Mostra informações do bot e do servidor."""
    guild = ctx.guild
    bot_user = bot.user

    embed = discord.Embed(
        title="Informações do Servidor e do Bot",
        color=discord.Color.blue()
    )
    embed.add_field(name="Servidor", value=f"Nome: {guild.name}\nID: {guild.id}\nMembros: {guild.member_count}", inline=False)
    embed.add_field(name="Bot", value=f"Nome: {bot_user.name}\nID: {bot_user.id}\nCriado em: {bot_user.created_at.strftime('%d/%m/%Y')}", inline=False)
    embed.set_footer(text="Sistema de Informações • Groove RP")

    await ctx.send(embed=embed)

@bot.command(name="loc")
async def loc(ctx):
    """Informa como saber a localização da fac."""
    message = (
        "📍 **Como saber a localização da fac:**\n"
        "1. Esteja na cidade e tenha um celular.\n"
        "2. Clique no **F8**.\n"
        "3. Digite **'groove'**."
    )
    await ctx.send(message)

@bot.command(name="radio")
async def radio(ctx):
    """Mostra as informações sobre a rádio da fac."""
    embed = discord.Embed(
        title="Informações sobre a Rádio da Fac",
        color=discord.Color.green()
    )
    embed.add_field(name="📻 Frequência Principal", value="252", inline=False)
    embed.add_field(name="🔊 Anúncios da Fac", value="252.1", inline=False)
    embed.set_footer(text="Sistema de Rádio • Groove RP")

    await ctx.send(embed=embed)

@bot.command(name="userinfo")
async def userinfo(ctx, user: discord.User = None):
    """Mostra informações sobre um usuário específico."""
    if user is None:
        user = ctx.author
    
    embed = discord.Embed(
        title="Informações do Usuário",
        color=discord.Color.blue()
    )
    embed.add_field(name="Nome", value=user.name, inline=False)
    embed.add_field(name="ID", value=user.id, inline=False)
    embed.add_field(name="Criado em", value=user.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
    embed.add_field(name="Em servidor desde", value=user.joined_at.strftime("%d/%m/%Y %H:%M:%S") if hasattr(user, 'joined_at') else "N/A", inline=False)
    embed.set_thumbnail(url=user.avatar_url)
    embed.set_footer(text="Sistema de Informações • Groove RP")

    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    """Mostra o ping do bot."""
    await ctx.send(f"Pong! 🏓 Latência: {round(bot.latency * 1000)}ms")

@bot.command(name="avatar")
async def avatar(ctx, user: discord.User = None):
    """Mostra o avatar de um usuário específico."""
    if user is None:
        user = ctx.author
    embed = discord.Embed(title=f"Avatar de {user.name}", color=discord.Color.blue())
    embed.set_image(url=user.avatar_url)
    await ctx.send(embed=embed)

@bot.command(name="clear")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 10):
    """Limpa uma quantidade específica de mensagens no canal."""
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"{amount} mensagens foram limpas!", delete_after=5)

@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    """Expulsa um membro do servidor."""
    await member.kick(reason=reason)
    await ctx.send(f"{member} foi expulso do servidor. Razão: {reason}")

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    """Bane um membro do servidor."""
    await member.ban(reason=reason)
    await ctx.send(f"{member} foi banido do servidor. Razão: {reason}")

# Define as views e modais

class RegistroView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Fazer Registro", style=discord.ButtonStyle.success, emoji="✅")
    async def registro_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = RegistroModal()
        await interaction.response.send_modal(modal)

class RegistroModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Registro de RP")

        self.nome = discord.ui.TextInput(
            label="Seu Nome:",
            placeholder="Insira seu nome e sobrenome do RP",
            required=True
        )
        self.add_item(self.nome)

        self.passaporte = discord.ui.TextInput(
            label="Seu Passaporte:",
            placeholder="Insira seu passaporte do RP",
            required=True
        )
        self.add_item(self.passaporte)

        self.recrutador = discord.ui.TextInput(
            label="Nome do Recrutador:",
            placeholder="Insira o nome do recrutador",
            required=True
        )
        self.add_item(self.recrutador)

    async def on_submit(self, interaction: discord.Interaction):
        nome = self.nome.value
        passaporte = self.passaporte.value
        recrutador = self.recrutador.value

        novo_apelido = f"{nome}┃{passaporte}"

        guild = interaction.guild
        member = interaction.user

        try:
            await member.edit(nick=novo_apelido)
            
            log_channel = guild.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                embed = discord.Embed(
                    title="Novo Registro de RP",
                    description="Um novo usuário completou o registro!",
                    color=discord.Color.blue()
                )
                embed.add_field(name="Nome:", value=nome, inline=False)
                embed.add_field(name="Passaporte:", value=passaporte, inline=False)
                embed.add_field(name="Recrutador:", value=recrutador, inline=False)
                embed.add_field(name="Membro:", value=member.mention, inline=False)
                embed.set_footer(text="Sistema de Registro • Groove RP")
                
                await log_channel.send(embed=embed)
            else:
                print("Canal de log não encontrado. Verifique se o ID está correto.")
            
            await interaction.response.send_message(
                f"Registro completado! Seu novo nome no servidor é **{novo_apelido}**.",
                ephemeral=True
            )

            channel = guild.get_channel(CHANNEL_ID)
            await channel.set_permissions(member, view_channel=False)
            
            await interaction.followup.send(
                f"As permissões de visualização do canal foram removidas para {member.mention}.",
                ephemeral=True
            )
        
        except discord.Forbidden:
            await interaction.response.send_message(
                "Erro: Não consegui alterar seu nome ou modificar suas permissões no servidor. Verifique minhas permissões.",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"Ocorreu um erro: {str(e)}",
                ephemeral=True
            )

class CargoModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Solicitação de Cargo")

        self.cargo = discord.ui.TextInput(
            label="Cargo Pretendido:",
            placeholder="Insira o cargo que deseja",
            required=True
        )
        self.add_item(self.cargo)

        self.motivo = discord.ui.TextInput(
            label="Motivo:",
            placeholder="Por que você acha que deve receber esse cargo?",
            style=discord.TextStyle.paragraph,
            required=True
        )
        self.add_item(self.motivo)

    async def on_submit(self, interaction: discord.Interaction):
        cargo = self.cargo.value
        motivo = self.motivo.value

        embed = discord.Embed(
            title="Nova Solicitação de Cargo",
            description=f"{interaction.user.mention} solicitou o cargo de **{cargo}**.",
            color=discord.Color.green()
        )
        embed.add_field(name="Motivo:", value=motivo, inline=False)
        embed.add_field(name="Aprovações", value="✅ 0\n" + "Votantes: ", inline=True)
        embed.add_field(name="Rejeições", value="❌ 0\n" + "Votantes: ", inline=True)
        embed.set_footer(text="Sistema de Seleção de Cargo • Groove RP")

        log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
        message = await log_channel.send(embed=embed, view=ApprovalView())
        await interaction.response.send_message("Sua solicitação foi enviada para avaliação.", ephemeral=True)

        # Salvar o ID da mensagem para uso posterior
        self.message_id = message.id

class ApprovalView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.approvals = 0
        self.rejections = 0
        self.approvers = []
        self.rejectors = []

    @discord.ui.button(label="Aprovar", style=discord.ButtonStyle.success, emoji="✅")
    async def approve_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id not in self.approvers and interaction.user.id not in self.rejectors:
            self.approvals += 1
            self.approvers.append(interaction.user.mention)
            await self.update_message(interaction)
        else:
            await interaction.response.send_message("Você já votou nesta solicitação.", ephemeral=True)

    @discord.ui.button(label="Rejeitar", style=discord.ButtonStyle.danger, emoji="❌")
    async def reject_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id not in self.rejectors and interaction.user.id not in self.approvers:
            self.rejections += 1
            self.rejectors.append(interaction.user.mention)
            await self.update_message(interaction)
        else:
            await interaction.response.send_message("Você já votou nesta solicitação.", ephemeral=True)

    async def update_message(self, interaction: discord.Interaction):
        message = interaction.message
        embed = message.embeds[0]
        embed.set_field_at(1, name="Aprovações", value=f"✅ {self.approvals}\nVotantes: {', '.join(self.approvers)}", inline=True)
        embed.set_field_at(2, name="Rejeições", value=f"❌ {self.rejections}\nVotantes: {', '.join(self.rejectors)}", inline=True)
        await message.edit(embed=embed)
        await interaction.response.defer()

class CargoSelectionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Solicitar Cargo", style=discord.ButtonStyle.primary)
    async def request_cargo_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = CargoModal()
        await interaction.response.send_modal(modal)

bot.run('MTI4MDEwNzg4MzkyNDU1Nzg2NQ.G8NwJm.H_aJHvkUNkOtZZAv63sg8CX4TlvUrprZGHobhg')