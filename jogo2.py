import pygame
import random

pygame.init()

# Tamanho da janela
largura, altura = 800, 600
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Siga o Caminho em Movimento!")

# Fonte do placar
fonte = pygame.font.SysFont("Arial", 30)

# Jogador
x = largura // 2
y = altura - 100
raio = 20
velocidade = 6

# Caminho
faixa_largura = 130
velocidade_caminho = 5
segmentos = []

# Inicializar segmentos do caminho
for i in range(20):
    pos_x = largura // 2 + random.randint(-200, 200)
    segmentos.append([pos_x, i * -40])

# Placar de tempo
tempo_dentro = 0  # tempo total dentro do caminho (em milissegundos)
ultimo_tempo = pygame.time.get_ticks()

rodando = True
while rodando:
    pygame.time.delay(30)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Movimento do jogador
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        x -= velocidade
    if teclas[pygame.K_RIGHT]:
        x += velocidade
    if teclas[pygame.K_UP]:
        y -= velocidade
    if teclas[pygame.K_DOWN]:
        y += velocidade

    # Movimento do caminho
    for s in segmentos:
        s[1] += velocidade_caminho

    if segmentos and segmentos[-1][1] > 0:
        novo_x = segmentos[-1][0] + random.randint(-60, 60)
        novo_x = max(0, min(novo_x, largura - faixa_largura))
        segmentos.append([novo_x, -40])
    if segmentos[0][1] > altura:
        segmentos.pop(0)

    # Verifica se o jogador está dentro da faixa
    dentro = False
    for s in segmentos:
        seg_x, seg_y = s
        if seg_y <= y <= seg_y + 40:
            if seg_x <= x <= seg_x + faixa_largura:
                dentro = True
            break

    # Atualizar tempo se dentro do caminho
    tempo_atual = pygame.time.get_ticks()
    if dentro:
        tempo_dentro += tempo_atual - ultimo_tempo
    ultimo_tempo = tempo_atual

    # Fundo
    if dentro:
        janela.fill((0, 0, 0))
    else:
        janela.fill((100, 0, 0))

    # Desenhar caminho
    for s in segmentos:
        pygame.draw.rect(janela, (255, 255, 0), (s[0], s[1], faixa_largura, 50))

    # Desenhar jogador
    pygame.draw.circle(janela, (0, 255, 0), (x, y), raio)

    # Desenhar placar
    segundos = tempo_dentro // 1000
    texto = fonte.render(f"Tempo no caminho: {segundos} s", True, (255, 255, 255))
    janela.blit(texto, (10, 10))

    pygame.display.update()

pygame.quit()
