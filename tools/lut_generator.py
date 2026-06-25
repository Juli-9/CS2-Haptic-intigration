import numpy as np
import matplotlib.pyplot as plt

LUT_SIZE = 256


# ------------------------
# Kurvenbibliothek
# ------------------------

def exp_decay(x, k=8):
    return np.exp(-k * x)


def gamma_pulse(x, a=1.0, b=10.0):
    y = (x ** a) * np.exp(-b * x)
    return y / y.max()


def damped_sine(x, decay=5, cycles=2):
    y = np.exp(-decay * x) * np.abs(np.sin(2 * np.pi * cycles * x))
    return y / y.max()


def double_impact(x,
                  decay=15,
                  echo_pos=0.15,
                  echo_amp=0.4,
                  echo_width=200):
    y = np.exp(-decay * x)
    y += echo_amp * np.exp(-echo_width * (x - echo_pos) ** 2)
    return y / y.max()


def heavy_shot(x,
               plateau=0.12,
               decay=8):
    y = np.ones_like(x)

    idx = x > plateau
    y[idx] = np.exp(-decay * (x[idx] - plateau))

    return y / y.max()


# ------------------------
# Auswahl
# ------------------------

x = np.linspace(0, 1, LUT_SIZE)

y = gamma_pulse(x)

# y = double_impact(
#     x,
#     decay=12,
#     echo_pos=0.12,
#     echo_amp=0.25,
#     echo_width=800
# )

# ------------------------
# LUT erzeugen
# ------------------------

lut = np.round(
    np.clip(y, 0, 1) * 255
).astype(np.uint8)

# ------------------------
# C-Array ausgeben
# ------------------------

print("const uint8_t LUT[256] = {")

for i in range(0, 256, 16):
    row = ", ".join(f"{v:3d}" for v in lut[i:i+16])
    print(f"    {row},")

print("};")

# ------------------------
# Plot
# ------------------------

plt.figure(figsize=(10,4))
plt.plot(x, y)
plt.grid(True)
plt.ylim(0, 1.05)
plt.title("Envelope")
plt.xlabel("normalized time")
plt.ylabel("amplitude")
plt.show()