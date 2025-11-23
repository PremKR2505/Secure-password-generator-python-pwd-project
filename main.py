#This is a secure password gen for your secret stuff 
import string, random
import secrets
import tkinter as tk
from tkinter import ttk,messagebox
import ttkbootstrap as ttk
#these are the libraries we will use in this project
rnd=secrets.SystemRandom()
#password generation logic
AMBI=set('Il1Lo0O')
def build_charset(include_lower, include_upper,include_digits,include_symbols,custom_symbols,exclude_AMBI,):
    parts=[]
    if include_lower:
        parts.append(string.ascii_lowercase)
    if include_upper:
        parts.append(string.ascii_uppercase)
    if include_digits:
        parts.append(string.digits)
    if include_symbols:
        parts.append(string.punctuation)
    if custom_symbols:
        parts.append(custom_symbols)
    pool = "".join(parts) or ""  # ensures that it returns string even if it may be empty
    if exclude_AMBI:
        pool = "".join(ch for ch in pool if ch not in AMBI)
    # remove duplicates while preserving order
    return ''.join(dict.fromkeys(pool))  # preserves original order
def ensure_required_chars(pool, include_lower, include_upper, include_digits, include_symbols, custom_symbols, exclude_AMBI):
    required = []
    if include_lower:
        s = string.ascii_lowercase
        if exclude_AMBI:
            s = "".join(ch for ch in s if ch not in AMBI)
        required.append(secrets.choice(s))
    if include_upper:
        s = string.ascii_uppercase
        if exclude_AMBI:
            s = "".join(ch for ch in s if ch not in AMBI)
        required.append(secrets.choice(s))
    if include_digits:
        s = string.digits
        if exclude_AMBI:
            s = "".join(ch for ch in s if ch not in AMBI)
        required.append(secrets.choice(s))
    if include_symbols:
        s = string.punctuation
        if exclude_AMBI:
            s = "".join(ch for ch in s if ch not in AMBI)
        required.append(secrets.choice(s))
    if custom_symbols:
        s = custom_symbols
        if exclude_AMBI:
            s = "".join(ch for ch in s if ch not in AMBI)
        if s:
            required.append(secrets.choice(s))
    return required

def insert_keyword_into_list(chars, keyword, position_mode):
    if not keyword:
        return chars
    kw_chars = list(keyword)
    if position_mode == "prefix":
        return kw_chars + chars
    if position_mode == "suffix":
        return chars + kw_chars
    if position_mode == "random":
        idx = secrets.randbelow(len(chars) + 1)
        return chars[:idx] + kw_chars + chars[idx:]
    # numeric position
    try:
        pos = int(position_mode)
        pos = max(0, min(pos, len(chars)))
        return chars[:pos] + kw_chars + chars[pos:]
    except Exception:
        # fallback to random
        idx = secrets.randbelow(len(chars) + 1)
        return chars[:idx] + kw_chars + chars[idx:]

# main password generation function

def generate_password(length, include_lower, include_upper, include_digits, include_symbols,
                      custom_symbols, exclude_AMBI, keyword, keyword_pos_mode, require_each_category):
    if length <= 0:
        raise ValueError("Length must be > 0")
    pool = build_charset(include_lower, include_upper, include_digits, include_symbols, custom_symbols, exclude_AMBI)
    # If pool empty but keyword provided, still generate(rest will be filled with safe charset)
    if not pool and not keyword:
        raise ValueError("No character sets selected and no keyword provided.")
    # Determine req chars(one from each selected category)if checked
    required = []
    if require_each_category:
        required = ensure_required_chars(pool, include_lower, include_upper, include_digits, include_symbols, custom_symbols, exclude_AMBI)
    # If pool empty but required is empty using fallback_pool
    fallback_pool = pool or ("abcdefghijklmnopqrstuvwxyz" if not exclude_AMBI else "".join(ch for ch in string.ascii_lowercase if ch not in AMBI))
    # Checkin' lengths
    kw_len = len(keyword) if keyword else 0
    min_needed = len(required) + kw_len
    if min_needed > length:
        raise ValueError(f"Length too small for required constraints. Need at least {min_needed} characters.")
    # Filling remaining positions
    remaining = length - min_needed
    rnd = secrets.choice
    generated = []
    for _ in range(remaining):
        generated.append(rnd(fallback_pool))
    # add required chars
    generated += required
    rnd.shuffle(generated)
    # insert keyword at specified position
    final_list = insert_keyword_into_list(generated, keyword or "", keyword_pos_mode)
    # final join
    return "".join(final_list)

# GUI logic

class PasswordGeneratorGUI:
    def __init__(self, root):
        self.root = root
        root.title("Secure Password Generator")
        root.resizable(False, False)
        padx = 8
        pady = 6

        main = ttk.Frame(root, padding=12)
        main.grid(row=0, column=0, sticky="nsew")

        # Length
        ttk.Label(main, text="Length:").grid(row=0, column=0, sticky="w")
        self.length_var = tk.IntVar(value=16)
        self.length_spin = ttk.Spinbox(main, from_=4, to=256, textvariable=self.length_var, width=6)
        self.length_spin.grid(row=0, column=1, sticky="w", padx=(4, 10))

        # Character set checkboxes
        self.lower_var = tk.BooleanVar(value=True)
        self.upper_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=False)

        ttk.Checkbutton(main, text="lowercase", variable=self.lower_var).grid(row=1, column=0, sticky="w")
        ttk.Checkbutton(main, text="UPPERCASE", variable=self.upper_var).grid(row=1, column=1, sticky="w")
        ttk.Checkbutton(main, text="digits", variable=self.digits_var).grid(row=2, column=0, sticky="w")
        ttk.Checkbutton(main, text="symbols", variable=self.symbols_var).grid(row=2, column=1, sticky="w")

        # Custom symbols
        ttk.Label(main, text="Custom symbols (optional):").grid(row=3, column=0, sticky="w", pady=(8,0))
        self.custom_entry = ttk.Entry(main, width=30)
        self.custom_entry.grid(row=3, column=1, columnspan=2, sticky="w")

        # Exclude AMBI
        self.ambig_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main, text="Exclude AMBI (Il1O0)", variable=self.ambig_var).grid(row=4, column=0, sticky="w", pady=(6,0))

        # Require each selected category
        self.require_each_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main, text="Require at least one from each selected category", variable=self.require_each_var).grid(row=5, column=0, columnspan=2, sticky="w", pady=(6,0))

        # Keyword and position
        ttk.Label(main, text="Keyword (optional):").grid(row=6, column=0, sticky="w", pady=(8,0))
        self.keyword_entry = ttk.Entry(main, width=30)
        self.keyword_entry.grid(row=6, column=1, columnspan=2, sticky="w", pady=(8,0))

        ttk.Label(main, text="Keyword position:").grid(row=7, column=0, sticky="w")
        self.kw_pos_var = tk.StringVar(value="random")
        pos_frame = ttk.Frame(main)
        pos_frame.grid(row=7, column=1, columnspan=2, sticky="w")
        ttk.Radiobutton(pos_frame, text="prefix", variable=self.kw_pos_var, value="prefix").grid(row=0, column=0)
        ttk.Radiobutton(pos_frame, text="suffix", variable=self.kw_pos_var, value="suffix").grid(row=0, column=1)
        ttk.Radiobutton(pos_frame, text="random", variable=self.kw_pos_var, value="random").grid(row=0, column=2)
        ttk.Radiobutton(pos_frame, text="at index", variable=self.kw_pos_var, value="0").grid(row=0, column=3)
        self.kw_index_spin = ttk.Spinbox(pos_frame, from_=0, to=255, width=4)
        self.kw_index_spin.grid(row=0, column=4, padx=(4,0))
        # Update radio when index changed
        def set_index_mode(*_):
            self.kw_pos_var.set(self.kw_index_spin.get())
        self.kw_index_spin.bind("<<Increment>>", set_index_mode)
        self.kw_index_spin.bind("<<Decrement>>", set_index_mode)
        self.kw_index_spin.bind("<FocusOut>", set_index_mode)
        self.kw_index_spin.bind("<KeyRelease>", set_index_mode)

        # Output and buttons
        self.output_var = tk.StringVar()
        output_entry = ttk.Entry(main, textvariable=self.output_var, width=50, font=("Consolas", 10))
        output_entry.grid(row=8, column=0, columnspan=3, pady=(10,0))

        btn_frame = ttk.Frame(main)
        btn_frame.grid(row=9, column=0, columnspan=3, pady=(8,0))
        gen_btn = ttk.Button(btn_frame, text="Generate", command=self.on_generate)
        gen_btn.grid(row=0, column=0, padx=(0,6))
        copy_btn = ttk.Button(btn_frame, text="Copy", command=self.on_copy)
        copy_btn.grid(row=0, column=1, padx=(0,6))
        save_btn = ttk.Button(btn_frame, text="Save to file", command=self.on_save)
        save_btn.grid(row=0, column=2)

        # Status
        self.status_var = tk.StringVar(value="")
        ttk.Label(main, textvariable=self.status_var, foreground="green").grid(row=10, column=0, columnspan=3, sticky="w", pady=(8,0))

    def on_generate(self):
        try:
            length = int(self.length_var.get())
        except Exception:
            messagebox.showerror("Invalid", "Length must be an integer.")
            return
        include_lower = self.lower_var.get()
        include_upper = self.upper_var.get()
        include_digits = self.digits_var.get()
        include_symbols = self.symbols_var.get()
        custom_symbols = self.custom_entry.get().strip()
        exclude_AMBI = self.ambig_var.get()
        keyword = self.keyword_entry.get()
        kw_pos = self.kw_pos_var.get()
        # If kw_pos is numeric string from spinbox, keep it; else 'prefix','suffix','random'
        try:
            password = generate_password(length, include_lower, include_upper, include_digits, include_symbols,
                                         custom_symbols, exclude_AMBI, keyword, kw_pos, self.require_each_var.get())
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        self.output_var.set(password)
        self.status_var.set(f"Generated ({len(password)} chars)")

    def on_copy(self):
        pwd = self.output_var.get()
        if not pwd:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(pwd)
        self.status_var.set("Copied to clipboard")

    def on_save(self):
        pwd = self.output_var.get()
        if not pwd:
            messagebox.showinfo("Nothing", "No password to save.")
            return
        try:
            with open("generated_password.txt", "a", encoding="utf-8") as f:
                f.write(pwd + "\n")
            self.status_var.set("Saved to generated_password.txt")
        except Exception as e:
            messagebox.showerror("Save error", str(e))

def main():
    app = ttk.Window(themename="cyborg") 
    app.title("Secure Password Generator")
    app.resizable(False, False)
    
    PasswordGeneratorGUI(app)  
    app.mainloop()
if __name__ == "__main__":
    main()