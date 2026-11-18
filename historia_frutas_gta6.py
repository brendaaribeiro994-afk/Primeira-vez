import numpy as np
from moviepy import ImageSequenceClip
from PIL import Image, ImageDraw, ImageFont

# Configurações do vídeo (Formato vertical 9:16)
LARGURA, ALTURA = 720, 1280
FPS = 24
DURACAO_TOTAL = 9  # 3 cenas de 3 segundos cada
TOTAL_FRAMES = FPS * DURACAO_TOTAL

frames = []

# Tenta carregar uma fonte padrão legível; se não encontrar, usa a básica
try:
    fonte = ImageFont.truetype("arial.ttf", 36)
    fonte_titulo = ImageFont.truetype("arial.ttf", 44)
except IOError:
    fonte = ImageFont.load_default()
    fonte_titulo = ImageFont.load_default()


def desenhar_banana(draw, x, y, triste=False, pulo=0):
    # Corpo da banana (arco amarelo)
    y_atual = y - pulo
    draw.pieslice(
        [x - 80, y_atual - 150, x + 120, y_atual + 150],
        start=110,
        end=250,
        fill=(255, 225, 53),
        outline=(180, 150, 0),
        width=4,
    )
    # Olhos
    draw.ellipse([x - 35, y_atual - 30, x - 20, y_atual - 15], fill="black")
    draw.ellipse([x - 10, y_atual - 30, x + 5, y_atual - 15], fill="black")
    # Boca
    if triste:
        draw.arc(
            [x - 35, y_atual + 10, x + 5, y_atual + 35],
            start=180,
            end=360,
            fill="black",
            width=4,
        )
        # Lágrima
        draw.ellipse(
            [x - 42, y_atual - 5, x - 32, y_atual + 10], fill=(100, 200, 255)
        )
    else:
        draw.arc(
            [x - 35, y_atual - 5, x + 5, y_atual + 20],
            start=0,
            end=180,
            fill="black",
            width=4,
        )


def desenhar_maca(draw, x, y, seria=False):
    # Corpo da maçã
    draw.ellipse(
        [x - 85, y - 80, x + 85, y + 80],
        fill=(220, 40, 40),
        outline=(140, 20, 20),
        width=4,
    )
    # Cabinho e folha
    draw.rectangle([x - 5, y - 105, x + 5, y - 75], fill=(101, 67, 33))
    draw.ellipse([x + 5, y - 105, x + 40, y - 85], fill=(50, 180, 50))
    # Olhos
    draw.ellipse([x - 30, y - 20, x - 15, y - 5], fill="black")
    draw.ellipse([x + 15, y - 20, x + 30, y - 5], fill="black")
    # Boca
    if seria:
        draw.line([x - 25, y + 25, x + 25, y + 25], fill="black", width=4)
    else:
        draw.arc(
            [x - 25, y + 10, x + 25, y + 35],
            start=0,
            end=180,
            fill="black",
            width=4,
        )


def desenhar_balao(draw, texto, x, y, largura=540, altura=180):
    draw.rounded_rectangle(
        [x, y, x + largura, y + altura],
        radius=25,
        fill="white",
        outline="black",
        width=4,
    )
    draw.multiline_text(
        (x + 25, y + 35), texto, fill="black", font=fonte, spacing=10
    )


# Geração quadro a quadro
for frame_idx in range(TOTAL_FRAMES):
    tempo = frame_idx / FPS

    # Cria imagem base (Fundo céu claro e chão de mesa)
    img = Image.new("RGB", (LARGURA, ALTURA), (135, 206, 235))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 880, LARGURA, ALTURA], fill=(210, 180, 140))  # Mesa

    # CENA 1 (0 a 3s): Banana animada
    if tempo < 3.0:
        pulo = abs(int(np.sin(tempo * 8) * 25))
        desenhar_banana(draw, 220, 780, triste=False, pulo=pulo)
        desenhar_maca(draw, 520, 800, seria=False)
        desenhar_balao(
            draw, "Maçã! Hoje eu vou\ncomprar o GTA 6!", 90, 320
        )

    # CENA 2 (3s a 6s): Maçã dá o choque de realidade
    elif tempo < 6.0:
        desenhar_banana(draw, 220, 780, triste=False, pulo=0)
        desenhar_maca(draw, 520, 800, seria=True)
        desenhar_balao(
            draw,
            "Banana, a gente custa\nR$ 5 o quilo e nem\ntem PS5 na fruteira!",
            90,
            300,
            altura=220,
        )

    # CENA 3 (6s a 9s): Banana chorando no drama
    else:
        tremor = int(np.sin(tempo * 30) * 4)
        desenhar_banana(draw, 220 + tremor, 780, triste=True, pulo=0)
        desenhar_maca(draw, 520, 800, seria=True)
        desenhar_balao(
            draw,
            "A vida de fruta CLT\né muito injusta...",
            90,
            320,
        )

    # Converte o desenho para formato compatível com o MoviePy
    frames.append(np.array(img))

# Compila os frames em vídeo MP4
clip = ImageSequenceClip(frames, fps=FPS)
clip.write_videofile("frutas_gta6.mp4", codec="libx264")
