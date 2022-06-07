#import logging
import os
import signal
import ffmpeg  
from pyrogram import Client, filters
from pytgcalls import GroupCall




API_ID = int(os.environ.get("API_ID",18721675))
API_HASH = os.environ.get("API_HASH","168152fe87d971c45fba6f1b3f2f2802")
SESSION_NAME = os.environ.get("SESSION_NAME","BQCOUdmnEZ8O4CR-jaUyIEK2kURdZQBkKXpGF7CDhiNKmJSyk8s23oUGGukfbgp7mAV9BeaN5Yfx7YXE9M8FqvhTI9p3J4MRFf-nGDZC7Es20FUzq3x3MP36n8bQKFhHI1oci8oK1tSqhIAh0NnRD30fv3aCr7H2Ysi38_lULdBPtwFykEpTZUgg382r0Nr8TmTMgb1qxt8Eg5CnMT2H4JA5rr7qRVZ_439HUxfyoRea742TS2igWNfcbvmo270jyP6Q9Kf3LhQrA5sVoW8xdemRNDGagz6sCp80MdpRdk8u5PlxstToj0I3rk4h2X-nxhQX-2AXf4jnkFaOmZ1-WrFJdLsQ1wA")


app = Client(SESSION_NAME, API_ID, API_HASH)
#logging.basicConfig(level=logging.INFO)



RADIO ="""INDIAN  Radio stations:

1. https://radioindia.net/radio/hungamanow/icecast.audio

2. https://filmymirchihdliv-lh.akamaihd.net/i/FilmyMirchiHDLive_1_1@336266/master.m3u8

3. https://radioindia.net/radio/mirchi98/icecast.audio

4. https://radioindia.net/radio/hungamanow/icecast.audio

5. https://radioindia.in/air-vividh-bharati

6. https://node-31.zeno.fm/9msu0vbxezzuv

7. https://prclive1.listenon.in/Hindi

8. http://radio.garden/listen/radio-sugar-90-8-crs/JJjaMMrY

9. http://radio.garden/listen/hindi-christian-radio/zmE3xziv

If you Know any radio Station  Please Contact to   @i_Ajit we will add it.

ᴛᴏ ꜱᴛᴀʀᴛ ʀᴇᴘʟᴀʏ ᴛᴏ ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ ᴡɪᴛʜ ᴄᴏᴍᴍᴀɴᴅ /station <Station Number> ʟɪᴋᴇ /station 1
ᴛᴏ ᴇɴᴅ and ꜱᴛᴏᴘ ꜱᴛʀᴇᴀᴍ by /end ᴄᴏᴍᴍᴀɴᴅ  for any help join  @i_Ajit"""


GROUP_CALLS = {}
FFMPEG_PROCESSES = {}

@app.on_message(filters.command('radio',prefixes='/'))
async def help(client,message):
	get =await client.get_chat_member(message.chat.id,message.from_user.id)
	status = get. status
	cmd_user = ["administrator","creator"]
	if status in cmd_user:
		await message.reply_text(RADIO)


@app.on_message(filters.command('station', prefixes='/'))
async def start(client,message):
	get =await client.get_chat_member(message.chat.id,message.from_user.id)
	status = get. status
	cmd_user = ["administrator","creator"]
	if status in cmd_user:
		input_filename = f'radio-{message.chat.id}.raw'
		group_call = GROUP_CALLS.get(message.chat.id)
		if group_call is None:
		      group_call = GroupCall(client, input_filename, path_to_log_file='')
		      GROUP_CALLS[message.chat.id] = group_call
		if not message.reply_to_message or len(message.command) < 2:
		      await message.reply_text('You forgot to replay list of stations or pass a station ID')
		      return
	process = FFMPEG_PROCESSES.get(message.chat.id)
	if process:
		process.send_signal(signal.SIGTERM)
	station_stream_url = None
	station_id = message.command[1]
	msg_lines = message.reply_to_message.text.split('\n')
	for line in msg_lines:
	       line_prefix = f'{station_id}. '
	       if line.startswith(line_prefix):
	           station_stream_url = line.replace(line_prefix, '').replace('\n', '')
	           break
	if not station_stream_url:
	       await message.reply_text(f'Can\'t find a station with id {station_id}')
	       return
	await group_call.start(message.chat.id)
	process = ffmpeg.input(station_stream_url).output(        input_filename, format='s16le',       acodec='pcm_s16le', ac=2, ar='48k'  ).overwrite_output().run_async()
	FFMPEG_PROCESSES[message.chat.id] = process
	await message.reply_text(f'RADIO #{station_id} ꜱᴛᴀʀᴛᴇᴅ ᴘʟᴀʏɪɴɢ ᴜʀ ᴄʜᴏᴏꜱᴇɴ ꜱᴛᴀᴛɪᴏɴ JOIN @i_Ajit.')


@app.on_message( filters.command('end', prefixes='/'))
async def stop(client,message):
	get =await client.get_chat_member(message.chat.id,message.from_user.id)
	status = get. status
	cmd_user = ["administrator","creator"]
	if status in cmd_user:
	   group_call = GROUP_CALLS.get(message.chat.id)
	   if group_call:
	   	await group_call.stop()
	   process = FFMPEG_PROCESSES.get(message.chat.id)
	   if process:
	   	process.send_signal(signal.SIGTERM)
	   





app.run()

