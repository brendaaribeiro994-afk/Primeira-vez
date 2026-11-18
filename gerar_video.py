import asyncio
import os
import edge_tts
from moviepy.editor import ImageClip, AudioFileClip

TEXTO = (
    "Gente, para tudo! Vocês viram as novidades absurdas do GTA 6?! "
    "O mapa de Vice City tá gigante, muito maior que o do GTA 5, e os gráficos parecem filme da vida real! "
    "Sem contar a dinâmica incrível entre a Lucia e o Jason, e a inteligência artificial dos NPCs que tá surreal. "
    "O hype tá nas alturas! Comenta aí: qual é a primeira coisa que você vai fazer quando entrar no jogo?"
)

VOZ = "pt-BR-FranciscaNeural"
ARQUIVO_AUDIO = "voz_streamer.mp3"
IMAGEM_AVATAR = "streamer.png"
VIDEO_FINAL = "video_gta6.mp4"

async def criar_audio():
    comunicacao = edge_tts.Communicate(TEXTO, VOZ, rate="+10%")
    await comunicacao.save(ARQUIVO_AUDIO)

def montar_video():
    if not os.path.exists(IMAGEM_AVATAR):
        raise FileNotFoundError(f"A imagem '{IMAGEM_AVATAR}' não foi encontrada no repositório!")

    audio = AudioFileClip(ARQUIVO_AUDIO)
    imagem = ImageClip(IMAGEM_AVATAR).set_duration(audio.duration)
    video = imagem.set_audio(audio)
    
    video.write_videofile(
        VIDEO_FINAL, 
        fps=24, 
        codec="libx264", 
        audio_codec="aac",
        preset="ultrafast"
    )

if __name__ == "__main__":
    asyncio.run(criar_audio())
    montar_video()
