import irc.bot
import openai
import textwrap

class GPT3Bot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, api_key):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, 6667)], nickname, nickname)
        self.channel = channel
        openai.api_key = api_key
        print("Init")

    def on_welcome(self, c, e):
        c.join(self.channel)
        print("Joined channel " + str(self.channel))

    def on_pubmsg(self, c, e):
        print("Public message")
        a = e.arguments[0]
        self.do_command(e, str(a))
        return

    def do_command(self, e, cmd):
        print("do")
        c = self.connection

        prompt = (f"{cmd}")
        completions = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        message = completions.choices[0].text
        print(message)
        messager = message.replace('\n', ' ')
        for line in textwrap.wrap(message.strip(), width=395):
            c.privmsg(self.channel, line)
            break
        print(messager)

bot = GPT3Bot("#channel", "Bot name", "IRC server address", "YOUR API KEY HERE")
print("Starting chatGPTree")
bot.start()
