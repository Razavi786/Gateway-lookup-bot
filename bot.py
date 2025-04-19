from requests import Session as s
from telebot import types
import telebot
import time

token = "7109780945:AAHy11H0NkA2ztXwspbUW-ZZp9rGa8u78zM"
bot = telebot.TeleBot(token)

my = types.InlineKeyboardButton(text="Owner",url="t.me/ItzMeSahid")
xx = types.InlineKeyboardMarkup()
xx.add(my)

def req(url):
    if url.startswith("http") or url.startswith("https"):
         url = url
    else:
         url = "http://"+url
    try:
        res = s().get(url)
    except Exception as e:
        return
    return res
    
def check_gateway(res):
    gateways = ["stripe","stripe2d","braintree","square","paypal","payflow","authorize.net","checkout.com","adyen","shopify","sagepay","magneto","woocommerce","cyberforce"]
    found_gateways = []
    try:
        for gateway in gateways:
            if gateway in res.text.lower():
                found_gateways.append(gateway.title())
    except Exception as e:
        return e
    if found_gateways:
        return found_gateways
    else:
        return "No Gateway Found"
        
def captcha(res):
    try:
        if any(keyword in res.text.lower() for keyword in ["recaptcha","captcha","grecaptcha"]):
            msg = "True ⚠️"
        else:
            msg = "False ❌"
    except Exception as e:
        return e
    return msg

def cloudflare(res):
    try:
        if res.headers["server"] == "cloudflare" or any(keyword in res.text.lower() for keyword in["cloudflare","cdnjs.cloudflare.com","challanges.cloudflare.com"]):
            msg = "True ⚠️"
        else:
            msg = "False ❌"
    except Exception as e:
        return e
    return msg

def cms_scanner(res):
	try:
		if any(keyword in res.text.lower() for keyword in ["/wp-login","/wp-admin","/wp-config"]):
			msg = "WordPress"
		elif any(keyword in res.text.lower() for keyword in ["/.env","/env","/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php"]):
			msg = "Laravel"
		elif any(keyword in res.text.lower() for keyword in ["/administrator/manifests/files/joomla.xml","/joomla!","<version>(.*?)<\/version>"]):
			msg = "Joomla"
		elif "/drupal/" in res.text.lower():
			msg = "Drupal"
		else:
			msg = "No CMS Found"
	except:
		return
	return msg
		

def main(url):
    try:
        now = time.time()
        chk = req(url)
        if chk:
            print(text:= f"""<b><i>Site » </i></b><code>{url}</code><b><i>
Response » {chk.status_code}
Gateways » {check_gateway(chk)}
Captcha » {captcha(chk)}
Cloudflare » {cloudflare(chk)}
CMS » {cms_scanner(chk)}
Server » {chk.headers.get("server","Not Found")}
Time Taken » {(time.time() - now):.2f} Seconds
By » @ItzMeSahid
</i></b>""")
            return text
    except Exception as e:
       print(e)


@bot.message_handler(commands=["start"])
def welcome(message):
	bot.reply_to(message,"Welcome To Simple Gateway Checker BOT 🤡\n\n Just Send Website To Check Using /gate Command Or Send File Of Websites For Mass Checking 🤡",reply_markup=xx)

@bot.message_handler(commands=["gate","scan","url","gateway"])
def check(message):
	urls = message.text.split()[1:]
	if not urls:
		bot.reply_to(message,"Uses 😾 » /gate <urls>")
		return
	
	for url in urls:
	   try:
    		 ko = (bot.reply_to(message,"Processing ⌛").message_id)
    		 response = main(url)
    		 bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=response,parse_mode="HTML",reply_markup=xx)
	   except Exception as e:
            bot.reply_to(message, f"{url}\n❌ 𝗲𝗿𝗿𝗼𝗿: {e}")
            continue

@bot.message_handler(content_types=["document"])
def file(message):
	ee = bot.download_file(bot.get_file(message.document.file_id).file_path)
	with open("urls.txt","wb") as f:
		f.write(ee)
	with open("urls.txt","r") as f:
		urls = f.readlines()
	for url in urls:
		url = url.strip()
		if url:
			try:
			 	response = main(url)
			 	bot.reply_to(message,response,parse_mode="HTML",reply_markup=xx)
			except Exception as e:
			     bot.reply_to(message, f"{url}\n❌ 𝗲𝗿𝗿𝗼𝗿: {e}")
			     continue

if __name__ == "__main__":
    print("𝗕𝗼𝘁 𝗜𝘀 𝗥𝘂𝗻𝗻𝗶𝗻𝗴 𝗡𝗼𝗪 🎉")
    bot.infinity_polling()
