import math

LUT_SIZE = 256

ATTACK = 0.08      # 8 %
HOLD = 0.04        # 4 %
DECAY_RATE = 6.0   # größer = schnelleres Ausklingen

lut = []

for i in range(LUT_SIZE):

    t = i / (LUT_SIZE - 1)

    if t < ATTACK:
        # Linearer Attack
        y = 255.0 * (t / ATTACK)

    elif t < ATTACK + HOLD:
        # Peak halten
        y = 255.0

    else:
        # Exponentieller Decay
        d = (t - ATTACK - HOLD) / (1.0 - ATTACK - HOLD)
        y = 255.0 * math.exp(-DECAY_RATE * d)

    lut.append(round(max(0, min(255, y))))

print("const uint8_t deagle_lut[256] = {")
for i in range(0, LUT_SIZE, 16):
    line = ", ".join(f"{v:3d}" for v in lut[i:i+16])
    print(f"    {line},")
print("};") 