"""Nice selfbot goodies."""
import asyncio
import io
from datetime import datetime
import util.commands as commands
from util.perms import echeck_perms
import util.dynaimport as di
ImageGrab = di.load('pyscreenshot')
from .cog import Cog

class SelfbotGoodies(Cog):
    """Some nice things for selfbot goodies."""

    def __init__(self, bot):
        self.start_time = datetime.now()
        super().__init__(bot)

    @commands.command(pass_context=True)
    async def screenshot(self, ctx):
        """Take a screenshot.
        Usage: screenshot"""
        await echeck_perms(ctx, ['bot_owner'])
        image = ImageGrab.grab()
        img_bytes = io.BytesIO()
        image.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        await self.bot.upload(img_bytes, filename='screenshot.png', content='This is *probably* what my screen looks like right now.')

    @commands.command(pass_context=True)
    async def msg_rate(self, ctx):
        """Get the message rate.
        Usage: msg_rate"""
        await echeck_perms(ctx, ['bot_owner'])
        msg = await self.bot.say('Please wait...')
        start_time = datetime.now()
        m = {'messages': 0}
        async def msg_task(m):
            while True:
                await self.bot.wait_for_message()
                m['messages'] += 1
        task = self.loop.create_task(msg_task(m))
        await asyncio.sleep(8)
        task.cancel()
        time_elapsed = datetime.now() - start_time
        time_elapsed = time_elapsed.total_seconds()
        await self.bot.edit_message(msg, 'I seem to be getting ' + str(round(m['messages'] / time_elapsed, 2)) + ' messages per second.')

def setup(bot):
    bot.add_cog(SelfbotGoodies(bot))

