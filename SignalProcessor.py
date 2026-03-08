import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, savgol_filter

PASTA_DADOS = "dados"
os.makedirs("graficos/sinais_individuais", exist_ok=True)
os.makedirs("graficos/dispersao", exist_ok=True)

CORES  = ["blue", "orange", "green", "red", "purple", "brown"]
MARCAS = ["o", "s", "^", "D", "P", "X"]
LABELS = ["F1-Inicio subida", "F2-Pico interm.", "F3-Vale interm.",
          "F4-Pico maximo", "F5-Antes descida", "F6-Nivel basal"]


def extrair_pontos(t, y):
    wlen = max(11, len(y) // 60)
    if wlen % 2 == 0:
        wlen += 1
    ys = savgol_filter(y, wlen, 3)
    n = len(t)
    deriv = np.gradient(ys, t)

    i4 = int(np.argmax(ys))

    lim = 0.05 * deriv[:i4].max()
    cand = np.where(deriv[:i4] > lim)[0]
    i1 = int(cand[0]) if len(cand) else 0

    basal = np.percentile(ys, 10)
    cand6 = np.where((np.arange(n) > i4) & (ys < basal + 0.15 * (ys[i4] - basal)))[0]
    i6 = int(cand6[0]) if len(cand6) else n - 1

    segm = ys[i1:i4]
    picos, props = find_peaks(segm, distance=max(5, len(segm)//8), prominence=0.01)
    i2 = i1 + int(picos[np.argmax(props["prominences"])]) if len(picos) else i1 + int(np.argmax(np.gradient(segm)))

    segv = ys[i2:i4]
    vales, _ = find_peaks(-segv, distance=max(3, len(segv)//6))
    i3 = i2 + int(vales[0]) if len(vales) else i2 + int(np.argmin(segv))

    segd = ys[i4:i6]
    i5 = i4 + max(0, int(np.argmin(np.gradient(segd))) - 1) if len(segd) > 2 else i4 + 1

    idxs = [max(0, min(x, n-1)) for x in [i1, i2, i3, i4, i5, i6]]
    return [(idx, t[idx], y[idx]) for idx in idxs]


arquivos = sorted(glob.glob(os.path.join(PASTA_DADOS, "*.csv")))
print(f"{len(arquivos)} CSV(s) encontrados.\n")

todos = []

for k, arq in enumerate(arquivos, 1):
    df = pd.read_csv(arq)
    t = df.iloc[:, 0].values.astype(float)
    y = df.iloc[:, 1].values.astype(float)
    nome = os.path.basename(arq)

    pontos = extrair_pontos(t, y)
    todos.append(pontos)

    fig, ax = plt.subplots()
    ax.plot(t, y)
    for fi, (_, tx, yx) in enumerate(pontos):
        ax.plot(tx, yx, marker=MARCAS[fi], color=CORES[fi],
                markersize=8, label=f"F{fi+1}", linestyle="none")
        ax.annotate(f"F{fi+1}", (tx, yx), textcoords="offset points",
                    xytext=(5, 5), fontsize=8, color=CORES[fi])
    ax.set_title(nome)
    ax.set_xlabel("Tempo (ms)")
    ax.set_ylabel("Sinal")
    ax.legend(fontsize=7)
    fig.savefig(f"graficos/sinais_individuais/sinal_{k:02d}.png")
    plt.close(fig)
    print(f"[{k:02d}] {nome}")

# Dispersão geral
fig, ax = plt.subplots()
for fi in range(6):
    ax.plot(
        [todos[i][fi][1] for i in range(len(todos))],
        [todos[i][fi][2] for i in range(len(todos))],
        marker=MARCAS[fi], color=CORES[fi], linestyle="none", label=LABELS[fi]
    )
ax.set_title("Dispersao Geral")
ax.set_xlabel("Tempo (ms)")
ax.set_ylabel("Amplitude")
ax.legend(fontsize=7)
fig.savefig("graficos/dispersao/dispersao_geral.png")
plt.close(fig)
print("\n[dispersao] OK")

# Tabela estatística
print(f"\n{'Feature':<8}{'Media(t)':<12}{'DP(t)':<12}{'Media(y)':<12}{'DP(y)':<12}")
print("-" * 52)
linhas = []
for fi in range(6):
    ts = np.array([todos[i][fi][1] for i in range(len(todos))])
    ys = np.array([todos[i][fi][2] for i in range(len(todos))])
    linha = f"F{fi+1:<7}{ts.mean():<12.4f}{ts.std():<12.4f}{ys.mean():<12.4f}{ys.std():<12.4f}"
    linhas.append(linha)
    print(linha)

with open("tabela_estatistica.txt", "w") as f:
    f.write(f"{'Feature':<8}{'Media(t)':<12}{'DP(t)':<12}{'Media(y)':<12}{'DP(y)':<12}\n")
    f.write("-" * 52 + "\n")
    f.write("\n".join(linhas) + "\n")

print("\nConcluido!")
