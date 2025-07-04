import secrets
import pyperclip

# Generate 32 random bytes for AES-256
key_bytes = [secrets.randbelow(256) for _ in range(32)]

# Format as C-style hex array
lines = []
lines.append("const uint8_t AES_KEY[32] = {")
for i in range(0, 32, 8):
    line = "    " + ",".join(f"0x{b:02X}" for b in key_bytes[i:i+8])
    lines.append(line + ("," if i + 8 < 32 else ""))
lines.append("};")

output = "\n".join(lines)

# Copy to clipboard
pyperclip.copy(output)

# Print to console as well
print(output)
print("\nAES key has been copied to clipboard.")