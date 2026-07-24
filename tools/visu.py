import numpy as np
import matplotlib.pyplot as plt

# 256 Stützstellen
x = np.arange(256)

# Sinus-LUT (0...255)
sin_lut = np.round(127.5 * (1 + np.sin(2 * np.pi * x / 256))).astype(int)

# Sägezahn aufsteigend
saw_up = x

# Sägezahn absteigend
saw_down = 255 - x

# HeavyShot LUT
heavy_shot = np.concatenate([
    np.full(32, 255),
    np.round(252 * np.exp(-np.linspace(0, 6, 224))).astype(int)
])

# GammaPulse (ähnliche Form)
gamma_pulse = np.round(
    255 * np.exp(-np.linspace(0, 7, 256))
).astype(int)
gamma_pulse[:25] = np.round(
    255 * np.sin(np.linspace(0, np.pi / 2, 25))
).astype(int)

# Konstante Kurve (optional)
constant = np.full(256, 180)

# -------------------------------------------------

plt.figure(figsize=(10, 6))

plt.plot(x, sin_lut,      label="Sinus")
plt.plot(x, saw_up,       label="Saw Up")
plt.plot(x, saw_down,     label="Saw Down")
plt.plot(x, heavy_shot,   label="Heavy Shot")
plt.plot(x, gamma_pulse,  label="Gamma Pulse")
plt.plot(x, constant, "--", label="Constant")

plt.xlim(0, 255)
plt.ylim(0, 255)

plt.xlabel("LUT-Index")
plt.ylabel("PWM-Wert")
plt.title("Verwendete Haptik-Wellenformen")

plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()