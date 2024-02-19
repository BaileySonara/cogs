from .magenta_core import magenta_core


async def setup(bot):
    await bot.add_cog(magenta_core(bot))
