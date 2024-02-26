from discord.ext import commands
import requests


class CryptoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="crypto",
        help="Gets the current price of a specified cryptocurrency by its symbol",
    )
    async def crypto(self, ctx, *, symbol: str):
        symbol = symbol.lower()  # Convert to lowercase to match keys in the dictionary
        if symbol in crypto_symbol_to_id:
            coin_id = crypto_symbol_to_id[symbol]
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
            try:
                response = requests.get(url).json()
                price = response[coin_id]["usd"]
                await ctx.send(
                    f"The current price of {symbol.upper()} ({coin_id.capitalize()}) is ${price} USD"
                )
            except Exception as e:
                await ctx.send(
                    f"There was an error retrieving the price for {symbol.upper()}. Please try again later."
                )
        else:
            await ctx.send(
                f"Symbol '{symbol.upper()}' not recognized. Please use a supported cryptocurrency symbol."
            )


async def setup(bot):
    await bot.add_cog(CryptoCog(bot))


crypto_symbol_to_id = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "ada": "cardano",
    # Add more mappings as needed
}
