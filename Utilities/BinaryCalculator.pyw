import tkinter as tk
from tkinter import ttk
import struct

class BinaryCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Binary Calculator")

        self.bit_length = tk.IntVar(value=8)
        self.signed = tk.BooleanVar(value=False)
        self.bit_vars = []

        self.value = 0

        self.create_widgets()
        self.update_bits_from_value()

    def create_widgets(self):
        # Row 1: Bit Length & Signed
        top_frame = tk.Frame(self)
        top_frame.pack(pady=5)

        for bits in [4, 8, 16, 32, 64]:
            tk.Radiobutton(top_frame, text=f"{bits}bit", variable=self.bit_length, value=bits,
                           command=self.on_bit_length_changed).pack(side=tk.LEFT, padx=2)

        tk.Checkbutton(top_frame, text="Signed", variable=self.signed, command=self.update_display).pack(side=tk.LEFT, padx=10)

        # Row 2: Bit Checkboxes
        self.bits_frame = tk.Frame(self)
        self.bits_frame.pack(pady=5)

        # Row 3: Binary & Hex Display
        val_frame = tk.Frame(self)
        val_frame.pack(pady=5)

        tk.Label(val_frame, text="Binary:").grid(row=0, column=0, sticky='e')
        self.binary_entry = tk.Entry(val_frame, width=70)
        self.binary_entry.grid(row=0, column=1, sticky='w')
        self.binary_entry.bind('<KeyRelease>', self.on_binary_changed)

        tk.Label(val_frame, text="Hex:").grid(row=1, column=0, sticky='e')
        self.hex_entry = tk.Entry(val_frame, width=20)
        self.hex_entry.grid(row=1, column=1, sticky='w')
        self.hex_entry.bind('<KeyRelease>', self.on_hex_changed)

        # Row 4: Int & Float Display
        num_frame = tk.Frame(self)
        num_frame.pack(pady=5)

        tk.Label(num_frame, text="Integer:").grid(row=0, column=0, sticky='e')
        self.int_entry = tk.Entry(num_frame, width=20)
        self.int_entry.grid(row=0, column=1, sticky='w')
        self.int_entry.bind('<KeyRelease>', self.on_int_changed)

        tk.Label(num_frame, text="Float:").grid(row=1, column=0, sticky='e')
        self.float_entry = tk.Entry(num_frame, width=20)
        self.float_entry.grid(row=1, column=1, sticky='w')
        self.float_entry.bind('<KeyRelease>', self.on_float_changed)

        self.build_bit_checkboxes()

    def on_bit_length_changed(self):
        self.build_bit_checkboxes()
        self.update_display()
		
    def set_all_ones(self):
        for var in self.bit_vars:
            var.set(1)
        self.on_bits_changed()

    def set_all_zeros(self):
        for var in self.bit_vars:
            var.set(0)
        self.on_bits_changed()

    def build_bit_checkboxes(self):
        for widget in self.bits_frame.winfo_children():
            widget.destroy()
        self.bit_vars.clear()

        bits = self.bit_length.get()
        for i in range(bits):
            var = tk.IntVar()
            cb = tk.Checkbutton(self.bits_frame, text=str(bits - 1 - i), variable=var,
                                command=self.on_bits_changed)
            cb.grid(row=i // 16, column=i % 16)
            self.bit_vars.append(var)

        # Add buttons below checkboxes
        button_frame = tk.Frame(self.bits_frame)
        button_frame.grid(row=(bits - 1) // 16 + 1, column=0, columnspan=16, pady=5)

        tk.Button(button_frame, text="Set All 1", command=self.set_all_ones).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Set All 0", command=self.set_all_zeros).pack(side=tk.LEFT, padx=10)


    def on_bits_changed(self):
        bits = self.bit_length.get()
        val = 0
        for i, var in enumerate(reversed(self.bit_vars)):
            if var.get():
                val |= (1 << i)

        if self.signed.get():
            sign_bit = 1 << (bits - 1)
            if val & sign_bit:
                val = val - (1 << bits)

        self.value = val
        self.update_display()

    def update_bits_from_value(self):
        bits = self.bit_length.get()
        val = self.value

        # Convert signed to unsigned if needed
        if self.signed.get():
            max_val = 1 << bits
            val &= (max_val - 1)

        for i in range(bits):
            bit = (val >> i) & 1
            self.bit_vars[bits - 1 - i].set(bit)

    def update_display(self):
        bits = self.bit_length.get()
        val = self.value

        max_val = 1 << bits
        if self.signed.get():
            unsigned_val = val & (max_val - 1)
        else:
            unsigned_val = val if val >= 0 else val + max_val

        # Update binary
        bin_str = f"{unsigned_val:0{bits}b}"
        self.binary_entry.delete(0, tk.END)
        self.binary_entry.insert(0, bin_str)

        # Update hex
        hex_str = f"{unsigned_val:0{bits // 4}X}"
        self.hex_entry.delete(0, tk.END)
        self.hex_entry.insert(0, hex_str)

        # Update integer
        self.int_entry.delete(0, tk.END)
        self.int_entry.insert(0, str(val))

        # Update float
        try:
            if bits == 32:
                float_val = struct.unpack('f', struct.pack('I', unsigned_val))[0]
            elif bits == 64:
                float_val = struct.unpack('d', struct.pack('Q', unsigned_val))[0]
            else:
                float_val = "N/A"
        except Exception:
            float_val = "Err"

        self.float_entry.delete(0, tk.END)
        self.float_entry.insert(0, str(float_val))

        self.update_bits_from_value()

    def on_binary_changed(self, event):
        try:
            bstr = self.binary_entry.get().strip().replace(" ", "")
            if len(bstr) != self.bit_length.get():
                return
            val = int(bstr, 2)
            if self.signed.get():
                sign_bit = 1 << (self.bit_length.get() - 1)
                if val & sign_bit:
                    val = val - (1 << self.bit_length.get())
            self.value = val
            self.update_display()
        except:
            pass

    def on_hex_changed(self, event):
        try:
            hstr = self.hex_entry.get().strip()
            val = int(hstr, 16)
            if self.signed.get():
                sign_bit = 1 << (self.bit_length.get() - 1)
                if val & sign_bit:
                    val = val - (1 << self.bit_length.get())
            self.value = val
            self.update_display()
        except:
            pass

    def on_int_changed(self, event):
        try:
            val = int(self.int_entry.get().strip())
            self.value = val
            self.update_display()
        except:
            pass

    def on_float_changed(self, event):
        try:
            fval = float(self.float_entry.get().strip())
            if self.bit_length.get() == 32:
                val = struct.unpack('I', struct.pack('f', fval))[0]
            elif self.bit_length.get() == 64:
                val = struct.unpack('Q', struct.pack('d', fval))[0]
            else:
                return
            if self.signed.get():
                sign_bit = 1 << (self.bit_length.get() - 1)
                if val & sign_bit:
                    val = val - (1 << self.bit_length.get())
            self.value = val
            self.update_display()
        except:
            pass

if __name__ == "__main__":
    app = BinaryCalculator()
    app.mainloop()
