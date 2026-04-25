"""
CIOSP v19.0 — customtkinter
pip install customtkinter gspread oauth2client pynput

Funcionalidades:
  - Meta diária com barra de progresso
  - Contador por turno (Manhã / Tarde / Noite)
  - Reset com confirmação
  - Histórico 30 dias com gráfico (canvas)
  - Estatísticas: média, melhor dia, total do mês
  - Exportar CSV
  - Dashboard admin em tempo real
  - Deletar usuário
  - Configurações persistidas em JSON
  - Som ao incrementar
  - Indicador online/offline
  - Notificação ao bater meta
  - Iniciar com o Windows
  - Teclas configuráveis
  - Auto-sync 5 min em thread
  - Login offline + cache local
  - Sair sem fechar o app
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
from pynput import keyboard as kb
import sqlite3, os, csv, json, winreg, threading, queue
from datetime import datetime, date, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ── CAMINHOS ──────────────────────────────────────────────────────────────────
PASTA        = r"C:\Contador_CIOSP"
os.makedirs(PASTA, exist_ok=True)
DB_LOCAL     = os.path.join(PASTA, "usuarios_backup.db")
DB_CACHE     = os.path.join(PASTA, "cache_contagem.db")
DB_HIST      = os.path.join(PASTA, "historico.db")
ARQUIVO_JSON = os.path.join(PASTA, "identidade.json")
CFG_FILE     = os.path.join(PASTA, "config.json")

ID_PLANILHA_USUARIOS = "1p77_VDE0US-xC53iqdz5fK0NWQ0wMN4662ojJp4Qb20"
ID_PLANILHA_DADOS    = "1OKjJYE6zVYb_zzAkR21F3ZDSpqYPpK2UFOCBRAR_0jw"
ABA_USUARIOS         = "DB_USUARIOS"
ABA_DADOS            = "LOG DADOS"

# ── CORES ─────────────────────────────────────────────────────────────────────
C_BG    = "#0A0A0A"
C_BG2   = "#111111"
C_BG3   = "#1A1A1A"
C_BORD  = "#2A2A2A"
C_WHITE = "#FFFFFF"
C_MUTED = "#555555"
C_MUT2  = "#333333"
C_GREEN = "#2A7A4A"
C_RED   = "#CC3333"
MONO    = "Courier New"

# ── CONFIG ────────────────────────────────────────────────────────────────────
CFG_DEF = {
    "meta_diaria":     80,
    "som_ativo":       True,
    "tecla_mais":      107,
    "tecla_menos":     109,
    "notif_meta":      True,
    "iniciar_windows": False,
}

def cfg_load():
    try:
        with open(CFG_FILE) as f:
            return {**CFG_DEF, **json.load(f)}
    except Exception:
        return dict(CFG_DEF)

def cfg_save(c):
    with open(CFG_FILE, "w") as f:
        json.dump(c, f, indent=2)

# ── DB ────────────────────────────────────────────────────────────────────────
def iniciar_bancos():
    with sqlite3.connect(DB_LOCAL) as c:
        c.execute("CREATE TABLE IF NOT EXISTS usuarios "
                  "(nome TEXT PRIMARY KEY, senha TEXT, tipo INTEGER, "
                  "turno TEXT DEFAULT 'MANHA')")
        try:
            c.execute("ALTER TABLE usuarios ADD COLUMN turno TEXT DEFAULT 'MANHA'")
        except sqlite3.OperationalError:
            pass
    with sqlite3.connect(DB_CACHE) as c:
        c.execute("CREATE TABLE IF NOT EXISTS saldo_diario "
                  "(usuario TEXT, data TEXT, total INTEGER, "
                  "PRIMARY KEY(usuario, data))")
    with sqlite3.connect(DB_HIST) as c:
        c.execute("CREATE TABLE IF NOT EXISTS historico "
                  "(usuario TEXT, data TEXT, total INTEGER, "
                  "PRIMARY KEY(usuario, data))")

def carregar_hoje(usuario):
    hoje = date.today().isoformat()
    with sqlite3.connect(DB_CACHE) as conn:
        res = conn.execute(
            "SELECT total FROM saldo_diario WHERE usuario=? AND data=?",
            (usuario, hoje)).fetchone()
    return {"total": res[0] if res else 0}

def salvar_hoje(usuario, d):
    hoje = date.today().isoformat()
    with sqlite3.connect(DB_CACHE) as conn:
        conn.execute("INSERT OR REPLACE INTO saldo_diario VALUES (?,?,?)",
                     (usuario, hoje, d["total"]))
    with sqlite3.connect(DB_HIST) as conn:
        conn.execute("INSERT OR REPLACE INTO historico VALUES (?,?,?)",
                     (usuario, hoje, d["total"]))

def turno_do_usuario(usuario):
    """Retorna o turno fixo do usuário salvo no cache local."""
    with sqlite3.connect(DB_LOCAL) as conn:
        res = conn.execute(
            "SELECT turno FROM usuarios WHERE nome=?", (usuario,)).fetchone()
    return res[0] if res and res[0] else "MANHA"

# Mapeamento turno → label e horário exibido
TURNOS_INFO = {
    "MADRUGADA": ("MADRUGADA", "00:00 – 06:00"),
    "MANHA":     ("MANHÃ",     "06:00 – 12:00"),
    "TARDE":     ("TARDE",     "12:00 – 18:00"),
    "NOITE":     ("NOITE",     "18:00 – 00:00"),
}

def historico_usuario(usuario, dias=30):
    ini = (date.today() - timedelta(days=dias - 1)).isoformat()
    with sqlite3.connect(DB_HIST) as conn:
        rows = conn.execute(
            "SELECT data, total FROM historico "
            "WHERE usuario=? AND data>=? ORDER BY data",
            (usuario, ini)).fetchall()
    return {r[0]: r[1] for r in rows}

# ── GOOGLE ────────────────────────────────────────────────────────────────────
def conectar_google(id_planilha):
    try:
        scope = ["https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(ARQUIVO_JSON, scope)
        return gspread.authorize(creds).open_by_key(id_planilha)
    except Exception:
        return None

# ── HELPERS ───────────────────────────────────────────────────────────────────
def em_thread(fn, *args):
    threading.Thread(target=fn, args=args, daemon=True).start()

def beep():
    try:
        import winsound
        threading.Thread(target=lambda: winsound.Beep(1000, 40), daemon=True).start()
    except Exception:
        pass

APP_NAME = "CIOSP"
APP_PATH = os.path.abspath(__file__)

def set_startup(ativo):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Run",
                             0, winreg.KEY_SET_VALUE)
        if ativo:
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, f'"{APP_PATH}"')
        else:
            try: winreg.DeleteValue(key, APP_NAME)
            except FileNotFoundError: pass
        winreg.CloseKey(key)
    except Exception:
        pass

# ── ÍCONE ─────────────────────────────────────────────────────────────────────
def gerar_icone():
    ico_path = os.path.join(PASTA, "ciosp.ico")
    if os.path.exists(ico_path):
        return ico_path
    try:
        from PIL import Image, ImageDraw, ImageFont
        img  = Image.new("RGBA", (64, 64), (10, 10, 10, 255))
        draw = ImageDraw.Draw(img)
        draw.rectangle([1, 1, 62, 62], outline=(255, 255, 255), width=2)
        try:
            font = ImageFont.truetype("courbd.ttf", 20)
        except Exception:
            font = ImageFont.load_default()
        draw.text((8, 18), "CI", fill=(255, 255, 255), font=font)
        draw.text((8, 36), "OS", fill=(255, 255, 255), font=font)
        img.save(ico_path, format="ICO", sizes=[(64, 64), (32, 32), (16, 16)])
        return ico_path
    except Exception:
        return None

# ── WIDGET GRÁFICO ────────────────────────────────────────────────────────────
class Grafico(tk.Canvas):
    def __init__(self, master, dados, hoje_key, **kw):
        super().__init__(master, bg=C_BG, highlightthickness=0, **kw)
        self._dados    = dados
        self._hoje_key = hoje_key
        self.bind("<Configure>", self._draw)

    def _draw(self, _=None):
        self.delete("all")
        if not self._dados: return
        w, h  = self.winfo_width(), self.winfo_height()
        vals  = list(self._dados.values())
        keys  = list(self._dados.keys())
        maxi  = max(vals) if max(vals) > 0 else 1
        n     = len(vals)
        gap   = 3
        bw    = max(3, (w - gap * (n + 1)) // n)
        for i, (k, v) in enumerate(zip(keys, vals)):
            x  = gap + i * (bw + gap)
            bh = int((v / maxi) * (h - 18))
            y  = h - 18 - bh
            cor = C_WHITE if k == self._hoje_key else C_BG3
            self.create_rectangle(x, y, x + bw, h - 18, fill=cor, outline="")
            if i % max(1, n // 7) == 0:
                self.create_text(x + bw // 2, h - 8,
                                 text=k[8:], fill=C_MUTED,
                                 font=(MONO, 7))

# ── APP ───────────────────────────────────────────────────────────────────────
class AppCIOSP(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CIOSP v19.0")
        self.geometry("400x580")
        self.resizable(False, False)
        self.configure(fg_color=C_BG)
        try:
            ico = gerar_icone()
            if ico:
                self.iconbitmap(ico)
        except Exception:
            pass

        self.cfg         = cfg_load()
        self.user_logado = None
        self.is_admin    = False
        self.turno_user  = "MANHA"
        self.dados       = {}
        self._kb_lst     = None
        self._kb_q       = queue.Queue()
        self._meta_notif = False
        self._online     = False

        iniciar_bancos()
        self._tela_login()
        self._verificar_online()

    # ── ONLINE ────────────────────────────────────────────────────────────────
    def _verificar_online(self):
        def check():
            ok = conectar_google(ID_PLANILHA_DADOS) is not None
            self.after(0, lambda: self._set_online(ok))
        em_thread(check)
        self.after(30_000, self._verificar_online)

    def _set_online(self, ok):
        self._online = ok
        if hasattr(self, "lbl_conn"):
            self.lbl_conn.configure(
                text="● ONLINE" if ok else "○ OFFLINE",
                text_color=C_GREEN if ok else C_MUTED)

    # ── LIMPAR ────────────────────────────────────────────────────────────────
    def _limpar(self):
        for w in self.winfo_children():
            w.destroy()

    # ── LOGIN ─────────────────────────────────────────────────────────────────
    def _tela_login(self):
        self._limpar()
        self.geometry("400x520")

        outer = ctk.CTkFrame(self, fg_color="transparent")
        outer.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(outer, text="CIOSP",
                     font=(MONO, 58, "bold"),
                     text_color=C_WHITE).pack()
        ctk.CTkLabel(outer, text="S I S T E M A   D E   C O N T A G E M",
                     font=(MONO, 8), text_color=C_MUT2).pack(pady=(0, 28))

        ecfg = dict(width=280, height=42, corner_radius=0,
                    border_width=1, border_color=C_BORD,
                    fg_color=C_BG2, text_color=C_WHITE,
                    font=(MONO, 12), justify="center",
                    placeholder_text_color=C_MUTED)

        ctk.CTkLabel(outer, text="USUÁRIO", font=(MONO, 8),
                     text_color=C_MUTED).pack(anchor="w", padx=2)
        self.e_u = ctk.CTkEntry(outer, placeholder_text="SEU LOGIN", **ecfg)
        self.e_u.pack(pady=(2, 10))

        ctk.CTkLabel(outer, text="SENHA", font=(MONO, 8),
                     text_color=C_MUTED).pack(anchor="w", padx=2)
        self.e_s = ctk.CTkEntry(outer, placeholder_text="••••••••",
                                show="*", **ecfg)
        self.e_s.pack(pady=(2, 0))
        self.e_s.bind("<Return>", lambda _: self._logar())

        self.btn_login = ctk.CTkButton(
            outer, text="[ ENTRAR ]", command=self._logar,
            width=280, height=50, corner_radius=0,
            fg_color=C_WHITE, text_color=C_BG,
            hover_color="#DDDDDD", font=(MONO, 13, "bold"))
        self.btn_login.pack(pady=24)

        ctk.CTkLabel(outer, text="v19.0  ·  OFFLINE READY",
                     font=(MONO, 7), text_color=C_MUT2).pack()

    def _logar(self):
        u = self.e_u.get().upper().strip()
        s = self.e_s.get().strip()
        if not u or not s:
            messagebox.showwarning("Aviso", "Preencha usuário e senha.")
            return
        self.btn_login.configure(state="disabled", text="AUTENTICANDO...")
        self.update_idletasks()

        with sqlite3.connect(DB_LOCAL) as conn:
            res = conn.execute(
                "SELECT tipo FROM usuarios WHERE nome=? AND senha=?",
                (u, s)).fetchone()

        if res:
            self._finalizar_login(u, res[0] == 1)
        else:
            em_thread(self._logar_online, u, s)

    def _logar_online(self, u, s):
        planilha = conectar_google(ID_PLANILHA_USUARIOS)
        if planilha is None:
            self.after(0, lambda: self._erro_login("Sem conexão e sem cache local."))
            return
        try:
            lista = planilha.worksheet(ABA_USUARIOS).get_all_values()
            auth  = next((r for r in lista if len(r) >= 2
                          and r[0].upper().strip() == u
                          and r[1].strip() == s), None)
            if auth is None:
                self.after(0, lambda: self._erro_login("Usuário ou senha incorretos."))
                return
            is_admin = len(auth) > 2 and str(auth[2]) == "1"
            turno    = auth[3].upper().strip() if len(auth) > 3 and auth[3].strip() else "MANHA"
            with sqlite3.connect(DB_LOCAL) as conn:
                conn.execute("INSERT OR REPLACE INTO usuarios VALUES (?,?,?,?)",
                             (u, s, 1 if is_admin else 0, turno))
            self.after(0, lambda: self._finalizar_login(u, is_admin))
        except Exception as e:
            self.after(0, lambda: self._erro_login(str(e)))

    def _erro_login(self, msg):
        self.btn_login.configure(state="normal", text="[ ENTRAR ]")
        messagebox.showerror("Erro", msg)

    def _finalizar_login(self, usuario, is_admin):
        self.user_logado = usuario
        self.is_admin    = is_admin
        self.turno_user  = turno_do_usuario(usuario)
        self.dados       = carregar_hoje(usuario)
        self._meta_notif = False
        self._montar_principal()
        self._iniciar_teclado()
        self.after(300_000, self._auto_sync)

    # ── HELPER TABS ───────────────────────────────────────────────────────────
    def _make_tabs(self, parent):
        """Cria CTkTabview com cores legíveis em todos os estados."""
        tabs = ctk.CTkTabview(
            parent,
            segmented_button_selected_color=C_BG,
            segmented_button_unselected_color=C_BG2,
            fg_color="transparent",
            corner_radius=0)
        try:
            tabs._segmented_button.configure(
                selected_color=C_BG,
                unselected_color=C_BG2,
                selected_hover_color=C_BG3,
                unselected_hover_color=C_BG3,
                text_color=C_WHITE,
                text_color_disabled=C_MUTED,
                font=(MONO, 10, "bold"),
            )
        except Exception:
            pass
        return tabs

    # ── PRINCIPAL ─────────────────────────────────────────────────────────────
    def _montar_principal(self):
        self._limpar()
        self.geometry("330x330")
        self.resizable(False, False)

        # Top bar compacta
        bar = ctk.CTkFrame(self, height=28, fg_color=C_WHITE, corner_radius=0)
        bar.pack(fill="x"); bar.pack_propagate(False)

        ctk.CTkLabel(bar, text=f"● {self.user_logado}",
                     font=(MONO, 9, "bold"),
                     text_color=C_BG).pack(side="left", padx=10)

        ctk.CTkButton(bar, text="SAIR", command=self._sair,
                      width=36, height=18, corner_radius=0,
                      fg_color="transparent", text_color=C_MUTED,
                      hover_color="#EEEEEE",
                      font=(MONO, 7)).pack(side="right", padx=6)

        self.lbl_sync_badge = ctk.CTkLabel(
            bar, text="--:--", font=(MONO, 7), text_color=C_MUTED)
        self.lbl_sync_badge.pack(side="right", padx=3)

        self.lbl_conn = ctk.CTkLabel(
            bar, text="○", font=(MONO, 9), text_color=C_MUTED)
        self.lbl_conn.pack(side="right", padx=6)

        # Botão ferramentas no rodapé
        rodape = ctk.CTkFrame(self, height=24, fg_color=C_BG2, corner_radius=0)
        rodape.pack(fill="x", side="bottom"); rodape.pack_propagate(False)

        self.btn_sync = ctk.CTkButton(
            rodape, text="↑", command=self._sync_now,
            width=28, height=18, corner_radius=0,
            fg_color="transparent", text_color=C_MUTED,
            hover_color=C_BG3, font=(MONO, 10))
        self.btn_sync.pack(side="right", padx=6, pady=3)

        ctk.CTkButton(rodape, text="⋯", command=self._abrir_ferramentas,
                      width=28, height=18, corner_radius=0,
                      fg_color="transparent", text_color=C_MUTED,
                      hover_color=C_BG3, font=(MONO, 10)).pack(
            side="right", padx=2, pady=3)

        ctk.CTkLabel(rodape, text="Numpad +/−",
                     font=(MONO, 7), text_color=C_MUT2).pack(
            side="left", padx=8)

        # Contador ocupa o resto
        self._build_contar(self)

    def _abrir_ferramentas(self):
        if hasattr(self, "_win_tools") and self._win_tools.winfo_exists():
            self._win_tools.focus(); return

        win = ctk.CTkToplevel(self)
        win.title("CIOSP — Ferramentas")
        win.geometry("420x560")
        win.resizable(False, False)
        win.configure(fg_color=C_BG)
        try:
            ico = gerar_icone()
            if ico: win.iconbitmap(ico)
        except Exception:
            pass
        self._win_tools = win

        tabs = self._make_tabs(win)
        tabs.pack(fill="both", expand=True)

        t_hist  = tabs.add("HISTÓRICO")
        if self.is_admin:
            t_admin = tabs.add("ADMIN")
        t_cfg   = tabs.add("CONFIG")
        t_ajuda = tabs.add("AJUDA")

        self._build_historico(t_hist)
        if self.is_admin:
            self._build_admin(t_admin)
        self._build_config(t_cfg)
        self._build_ajuda(t_ajuda)

    # ── ABA CONTAR ────────────────────────────────────────────────────────────
    def _build_contar(self, f):
        meta = max(1, self.cfg["meta_diaria"])

        # Progresso fino no topo
        self.prog = ctk.CTkProgressBar(f, width=290, height=3, corner_radius=0,
                                       fg_color=C_BG3, progress_color=C_WHITE)
        self.prog.set(min(self.dados["total"] / meta, 1.0))
        self.prog.pack(pady=(8, 0))

        # Número grande
        self.lbl_num = ctk.CTkLabel(f, text=str(self.dados["total"]),
                                    font=(MONO, 90, "bold"),
                                    text_color=C_WHITE)
        self.lbl_num.pack(pady=(0, 0))

        # Meta + turno na mesma linha
        info_f = ctk.CTkFrame(f, fg_color="transparent")
        info_f.pack(pady=(0, 6))

        self.lbl_meta = ctk.CTkLabel(info_f, text=self._meta_txt(),
                                     font=(MONO, 8), text_color=C_MUTED)
        self.lbl_meta.pack(side="left", padx=(0, 10))

        nome_turno = TURNOS_INFO.get(self.turno_user, ("?", ""))[0]
        ctk.CTkLabel(info_f, text=f"[{nome_turno}]",
                     font=(MONO, 8, "bold"), text_color=C_MUT2).pack(side="left")

        # Data/hora pequena
        self.lbl_sub = ctk.CTkLabel(f, text=self._sub_txt(),
                                    font=(MONO, 7), text_color=C_MUT2)
        self.lbl_sub.pack()
        self._tick()

        # Botões − + ↺
        bf = ctk.CTkFrame(f, fg_color="transparent")
        bf.pack(pady=8)

        ctk.CTkButton(bf, text="−", command=lambda: self._update_val(-1),
                      width=60, height=44, corner_radius=0,
                      fg_color=C_BG3, text_color=C_WHITE,
                      hover_color=C_BORD,
                      font=(MONO, 22, "bold")).pack(side="left", padx=4)

        ctk.CTkButton(bf, text="+", command=lambda: self._update_val(1),
                      width=60, height=44, corner_radius=0,
                      fg_color=C_WHITE, text_color=C_BG,
                      hover_color="#DDDDDD",
                      font=(MONO, 22, "bold")).pack(side="left", padx=4)

        ctk.CTkButton(bf, text="↺", command=self._reset,
                      width=38, height=44, corner_radius=0,
                      fg_color=C_BG2, text_color=C_MUTED,
                      hover_color=C_BG3,
                      font=(MONO, 13)).pack(side="left", padx=4)

    def _meta_txt(self):
        m = self.cfg["meta_diaria"]
        t = self.dados.get("total", 0)
        return "✓ META ATINGIDA" if t >= m else f"META: {m}  ·  FALTAM: {m-t}"

    def _sub_txt(self):
        return f"{datetime.now().strftime('%d/%m/%Y')}  ·  {datetime.now().strftime('%H:%M')}"

    def _tick(self):
        if hasattr(self, "lbl_sub"):
            self.lbl_sub.configure(text=self._sub_txt())
        self.after(30_000, self._tick)

    def _update_val(self, d):
        self.dados["total"] = max(0, self.dados["total"] + d)
        salvar_hoje(self.user_logado, self.dados)
        self._refresh_contar()
        if d > 0 and self.cfg.get("som_ativo"):
            beep()

    def _refresh_contar(self):
        t = self.dados["total"]
        m = self.cfg["meta_diaria"]
        self.lbl_num.configure(text=str(t),
                               text_color=C_GREEN if t >= m else C_WHITE)
        self.lbl_meta.configure(text=self._meta_txt(),
                                text_color=C_GREEN if t >= m else C_MUTED)
        self.prog.set(min(t / max(1, m), 1.0))
        if t >= m and not self._meta_notif and self.cfg.get("notif_meta"):
            self._meta_notif = True
            messagebox.showinfo("CIOSP", f"Meta de {m} atingida!")

    def _reset(self):
        if messagebox.askyesno("Reset", "Zerar o contador de hoje?"):
            self.dados = {"total": 0, "manha": 0, "tarde": 0, "noite": 0}
            self._meta_notif = False
            salvar_hoje(self.user_logado, self.dados)
            self._refresh_contar()

    # ── SYNC ──────────────────────────────────────────────────────────────────
    def _sync_now(self):
        self.btn_sync.configure(state="disabled", text="SINCRONIZANDO...")
        self.update_idletasks()
        em_thread(self._sync_worker)

    def _sync_worker(self):
        planilha = conectar_google(ID_PLANILHA_DADOS)
        if planilha is None:
            self.after(0, lambda: self._sync_res(False)); return
        try:
            aba   = planilha.worksheet(ABA_DADOS)
            hoje  = datetime.now().strftime("%d/%m/%Y")
            agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            rows  = aba.get_all_values()
            linha = next((i+1 for i,r in enumerate(rows)
                          if len(r)>=2 and r[0].split()[0]==hoje
                          and r[1]==self.user_logado), -1)
            if linha != -1:
                aba.update_cell(linha, 4, self.dados["total"])
                aba.update_cell(linha, 1, agora)
            else:
                aba.append_row([agora, self.user_logado,
                                datetime.now().strftime("%m/%Y"),
                                self.dados["total"]])
            self.after(0, lambda: self._sync_res(True))
        except Exception:
            self.after(0, lambda: self._sync_res(False))

    def _sync_res(self, ok):
        hora = datetime.now().strftime("%H:%M")
        if ok:
            self.btn_sync.configure(text=f"✓ SYNC {hora}",
                                    text_color=C_WHITE)
            self.lbl_sync_badge.configure(text=hora)
        else:
            self.btn_sync.configure(text="✗ FALHA", text_color=C_RED)
        self.after(2500, lambda: self.btn_sync.configure(
            state="normal", text="↑ SYNC NUVEM", text_color=C_MUTED))

    def _auto_sync(self):
        if self.user_logado: self._sync_now()
        self.after(300_000, self._auto_sync)

    # ── ABA HISTÓRICO ─────────────────────────────────────────────────────────
    def _build_historico(self, f):
        dados = historico_usuario(self.user_logado, 30)
        hoje  = date.today().isoformat()

        ctk.CTkLabel(f, text="ÚLTIMOS 30 DIAS",
                     font=(MONO, 8), text_color=C_MUT2).pack(
            anchor="w", padx=20, pady=(12, 6))

        chart = Grafico(f, dados, hoje, width=340, height=100)
        chart.pack(padx=20, pady=(0, 8))

        # Stats
        vals   = list(dados.values())
        media  = int(sum(vals)/len(vals)) if vals else 0
        melhor = max(vals) if vals else 0
        total_m = sum(v for k,v in dados.items() if k[:7]==hoje[:7])

        sf = ctk.CTkFrame(f, fg_color="transparent")
        sf.pack(fill="x", padx=20, pady=4)
        for col, (lbl_t, val) in enumerate([
            ("MÉDIA/DIA", media), ("MELHOR DIA", melhor), ("TOTAL MÊS", total_m)]):
            card = ctk.CTkFrame(sf, fg_color=C_BG2, corner_radius=0,
                                border_width=1, border_color=C_BORD)
            card.grid(row=0, column=col, padx=3, sticky="nsew")
            sf.columnconfigure(col, weight=1)
            ctk.CTkLabel(card, text=lbl_t, font=(MONO, 7),
                         text_color=C_MUT2).pack(pady=(6,0))
            ctk.CTkLabel(card, text=str(val), font=(MONO, 17, "bold"),
                         text_color=C_WHITE).pack(pady=(0,6))

        ctk.CTkLabel(f, text="ÚLTIMOS 7 DIAS",
                     font=(MONO, 8), text_color=C_MUT2).pack(
            anchor="w", padx=20, pady=(10, 4))

        for d_str, total in reversed(sorted(dados.items())[-7:]):
            try:
                d_obj = date.fromisoformat(d_str)
                nome_dia = ["Seg","Ter","Qua","Qui","Sex","Sáb","Dom"][d_obj.weekday()]
                fmt = f"{nome_dia} {d_obj.strftime('%d/%m')}"
            except Exception:
                fmt = d_str
            row = ctk.CTkFrame(f, fg_color=C_BG2, corner_radius=0,
                               border_width=1, border_color=C_BG3)
            row.pack(fill="x", padx=20, pady=2)
            ctk.CTkLabel(row, text=fmt, font=(MONO, 10),
                         text_color=C_MUTED).pack(side="left", padx=10, pady=5)
            ctk.CTkLabel(row, text=str(total), font=(MONO, 11, "bold"),
                         text_color=C_WHITE).pack(side="right", padx=10)

        ctk.CTkButton(f, text="↓ EXPORTAR CSV",
                      command=lambda: self._exportar(dados),
                      width=160, height=32, corner_radius=0,
                      fg_color="transparent", text_color=C_MUTED,
                      hover_color=C_BG3, border_width=1, border_color=C_BORD,
                      font=(MONO, 9)).pack(pady=10)

    def _exportar(self, dados):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV","*.csv")],
            initialfile=f"historico_{self.user_logado}.csv")
        if not path: return
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["Data","Total"])
                for d, v in sorted(dados.items()):
                    w.writerow([d, v])
            messagebox.showinfo("Exportado", f"Salvo em:\n{path}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # ── ABA ADMIN ─────────────────────────────────────────────────────────────
    def _build_admin(self, f):
        tabs2 = self._make_tabs(f)
        tabs2.pack(fill="both", expand=True)
        dash_f  = tabs2.add("DASHBOARD")
        users_f = tabs2.add("USUÁRIOS")
        self._build_dash(dash_f)
        self._build_users(users_f)

    def _build_dash(self, f):
        ctk.CTkLabel(f, text="HOJE EM TEMPO REAL",
                     font=(MONO, 8), text_color=C_MUT2).pack(
            anchor="w", padx=16, pady=(10,6))

        self._dash_f = ctk.CTkFrame(f, fg_color="transparent")
        self._dash_f.pack(fill="x", padx=16)

        self._lbl_total = ctk.CTkLabel(f, text="TOTAL: —",
                                       font=(MONO, 13, "bold"),
                                       fg_color=C_WHITE, text_color=C_BG,
                                       corner_radius=0)
        self._lbl_total.pack(fill="x", padx=16, pady=8, ipady=8)

        ctk.CTkButton(f, text="↻ ATUALIZAR", command=self._carregar_dash,
                      width=140, height=30, corner_radius=0,
                      fg_color="transparent", text_color=C_MUTED,
                      hover_color=C_BG3, border_width=1, border_color=C_BORD,
                      font=(MONO, 9)).pack()
        self._carregar_dash()

    def _carregar_dash(self):
        em_thread(self._dash_worker)

    def _dash_worker(self):
        planilha = conectar_google(ID_PLANILHA_DADOS)
        if planilha is None:
            self.after(0, lambda: self._on_dash([])); return
        try:
            hoje  = datetime.now().strftime("%d/%m/%Y")
            rows  = planilha.worksheet(ABA_DADOS).get_all_values()
            # Busca turno de cada usuário no cache local
            with sqlite3.connect(DB_LOCAL) as conn:
                turnos_db = {r[0]: r[1] for r in conn.execute(
                    "SELECT nome, turno FROM usuarios").fetchall()}
            res = {}
            for r in rows:
                if len(r) >= 4 and r[0].split()[0] == hoje and r[1] not in res:
                    try:
                        turno = turnos_db.get(r[1], "MANHA")
                        res[r[1]] = (int(r[3]), turno)
                    except Exception:
                        pass
            resultado = [(u, v, t) for u, (v, t) in res.items()]
            resultado.sort(key=lambda x: -x[1])
            self.after(0, lambda: self._on_dash(resultado))
        except Exception:
            self.after(0, lambda: self._on_dash([]))

    def _on_dash(self, dados):
        # dados = [(usuario, valor, turno), ...]
        for w in self._dash_f.winfo_children():
            w.destroy()

        # Agrupa por turno
        grupos = {"MADRUGADA": [], "MANHA": [], "TARDE": [], "NOITE": []}
        for usuario, valor, turno in dados:
            t = turno.upper() if turno else "MANHA"
            grupos.setdefault(t, []).append((usuario, valor))

        total_geral = sum(v for _, v, _ in dados)
        maxi = max((v for _, v, _ in dados), default=1)

        for turno_key, membros in grupos.items():
            if not membros: continue
            nome_t, horario_t = TURNOS_INFO.get(turno_key, (turno_key, ""))
            # Header do turno
            hdr = ctk.CTkFrame(self._dash_f, fg_color=C_BG3,
                               corner_radius=0, border_width=1,
                               border_color="#444")
            hdr.pack(fill="x", pady=(6,2))
            ctk.CTkLabel(hdr, text=nome_t, font=(MONO, 9, "bold"),
                         text_color=C_WHITE).pack(side="left", padx=10, pady=4)
            subtotal = sum(v for _, v in membros)
            ctk.CTkLabel(hdr, text=f"TOTAL: {subtotal}",
                         font=(MONO, 9), text_color=C_MUTED).pack(
                side="right", padx=10)
            # Membros
            for usuario, valor in sorted(membros, key=lambda x: -x[1]):
                row = ctk.CTkFrame(self._dash_f, fg_color=C_BG2,
                                   corner_radius=0, border_width=1,
                                   border_color=C_BG3)
                row.pack(fill="x", pady=1)
                ctk.CTkLabel(row, text=f"  {usuario}", font=(MONO, 10),
                             text_color=C_MUTED, width=110, anchor="w").pack(
                    side="left", padx=4, pady=4)
                pct = int((valor / maxi) * 70) if maxi > 0 else 0
                bar = tk.Canvas(row, width=70, height=4, bg=C_BG3,
                                highlightthickness=0)
                bar.pack(side="left", padx=4)
                bar.create_rectangle(0, 0, pct, 4, fill=C_MUTED, outline="")
                ctk.CTkLabel(row, text=str(valor), font=(MONO, 11, "bold"),
                             text_color=C_WHITE).pack(side="right", padx=10)

        self._lbl_total.configure(text=f"TOTAL GERAL:  {total_geral}")

    def _build_users(self, f):
        ctk.CTkLabel(f, text="CACHE LOCAL", font=(MONO, 8),
                     text_color=C_MUT2).pack(anchor="w", padx=16, pady=(10,6))

        self._user_list = ctk.CTkFrame(f, fg_color="transparent")
        self._user_list.pack(fill="x", padx=16)
        self._render_users()

        ctk.CTkFrame(f, height=1, fg_color=C_BORD,
                     corner_radius=0).pack(fill="x", padx=16, pady=10)

        ctk.CTkLabel(f, text="NOVO USUÁRIO", font=(MONO, 8),
                     text_color=C_MUT2).pack(anchor="w", padx=16, pady=(0,6))

        ecfg = dict(height=36, corner_radius=0, border_width=1,
                    border_color=C_BORD, fg_color=C_BG2,
                    text_color=C_WHITE, font=(MONO, 11),
                    placeholder_text_color=C_MUTED)

        self.new_u = ctk.CTkEntry(f, placeholder_text="NOME DO USUÁRIO", **ecfg)
        self.new_u.pack(fill="x", padx=16, pady=(0,6))
        self.new_s = ctk.CTkEntry(f, placeholder_text="SENHA", show="*", **ecfg)
        self.new_s.pack(fill="x", padx=16, pady=(0,8))

        # Turno
        ctk.CTkLabel(f, text="TURNO", font=(MONO, 8),
                     text_color=C_MUT2).pack(anchor="w", padx=16)
        self.turno_var = ctk.StringVar(value="MANHA")
        turno_f = ctk.CTkFrame(f, fg_color="transparent")
        turno_f.pack(fill="x", padx=16, pady=(2,8))
        for t_key, (t_nome, _) in TURNOS_INFO.items():
            ctk.CTkRadioButton(turno_f, text=t_nome,
                               variable=self.turno_var, value=t_key,
                               font=(MONO, 9), text_color=C_MUTED,
                               fg_color=C_WHITE,
                               hover_color=C_MUT2).pack(
                side="left", padx=6)

        self.chk_adm = ctk.CTkCheckBox(f, text="Perfil admin",
                                        font=(MONO, 10),
                                        text_color=C_MUTED,
                                        fg_color=C_WHITE,
                                        hover_color=C_MUT2)
        self.chk_adm.pack(anchor="w", padx=16, pady=(0,10))

        ctk.CTkButton(f, text="GRAVAR USUÁRIO", command=self._gravar,
                      height=40, corner_radius=0,
                      fg_color=C_WHITE, text_color=C_BG,
                      hover_color="#DDDDDD",
                      font=(MONO, 11, "bold")).pack(fill="x", padx=16)

    def _render_users(self):
        for w in self._user_list.winfo_children():
            w.destroy()
        with sqlite3.connect(DB_LOCAL) as conn:
            users = conn.execute(
                "SELECT nome, tipo, turno FROM usuarios ORDER BY turno, nome").fetchall()
        turno_atual_render = None
        for nome, tipo, turno in users:
            turno = turno or "MANHA"
            if turno != turno_atual_render:
                turno_atual_render = turno
                nome_t = TURNOS_INFO.get(turno, (turno, ""))[0]
                ctk.CTkLabel(self._user_list, text=nome_t,
                             font=(MONO, 8), text_color=C_MUT2).pack(
                    anchor="w", padx=4, pady=(8,2))
            row = ctk.CTkFrame(self._user_list, fg_color=C_BG2,
                               corner_radius=0, border_width=1,
                               border_color=C_BG3)
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=nome, font=(MONO, 10),
                         text_color=C_WHITE).pack(side="left", padx=10, pady=6)
            ctk.CTkLabel(row,
                         text="ADMIN" if tipo else "OPER",
                         font=(MONO, 7),
                         text_color=C_WHITE if tipo else C_MUTED,
                         fg_color=C_BG3 if tipo else "transparent",
                         corner_radius=0).pack(side="right", padx=6)
            ctk.CTkButton(row, text="✕",
                          command=lambda n=nome: self._deletar(n),
                          width=28, height=28, corner_radius=0,
                          fg_color="transparent", text_color=C_RED,
                          hover_color=C_BG3,
                          font=(MONO, 10)).pack(side="right", padx=4)

    def _deletar(self, nome):
        if messagebox.askyesno("Deletar", f"Remover {nome}?"):
            with sqlite3.connect(DB_LOCAL) as conn:
                conn.execute("DELETE FROM usuarios WHERE nome=?", (nome,))
            self._render_users()

    def _gravar(self):
        u = self.new_u.get().upper().strip()
        s = self.new_s.get().strip()
        t = 1 if self.chk_adm.get() else 0
        turno = self.turno_var.get()
        if not u or not s:
            messagebox.showwarning("Aviso", "Preencha nome e senha.")
            return
        planilha = conectar_google(ID_PLANILHA_USUARIOS)
        if planilha is None:
            messagebox.showerror("Sem conexão", "Não foi possível acessar a nuvem.")
            return
        try:
            # Planilha: nome | senha | tipo | turno
            planilha.worksheet(ABA_USUARIOS).append_row([u, s, str(t), turno])
            with sqlite3.connect(DB_LOCAL) as conn:
                conn.execute("INSERT OR REPLACE INTO usuarios VALUES (?,?,?,?)",
                             (u, s, t, turno))
            self._render_users()
            self.new_u.delete(0, "end")
            self.new_s.delete(0, "end")
            messagebox.showinfo("Sucesso", f"Usuário {u} gravado.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    # ── ABA CONFIG ────────────────────────────────────────────────────────────
    def _build_config(self, f):
        def sec(txt):
            ctk.CTkLabel(f, text=txt, font=(MONO, 8),
                         text_color=C_MUT2).pack(anchor="w", padx=20, pady=(14,4))

        def row(lbl, widget_fn):
            r = ctk.CTkFrame(f, fg_color="transparent")
            r.pack(fill="x", padx=20, pady=3)
            ctk.CTkLabel(r, text=lbl, font=(MONO, 10),
                         text_color=C_MUTED).pack(side="left")
            widget_fn(r)
            ctk.CTkFrame(f, height=1, fg_color=C_BG3,
                         corner_radius=0).pack(fill="x", padx=20)

        sec("CONTAGEM")

        self._meta_var = tk.IntVar(value=self.cfg["meta_diaria"])
        def meta_w(r):
            tk.Spinbox(r, from_=1, to=9999, textvariable=self._meta_var,
                       width=6, font=(MONO, 10), bg=C_BG2, fg=C_WHITE,
                       buttonbackground=C_BG3, relief="flat",
                       insertbackground=C_WHITE).pack(side="right")
        row("Meta diária", meta_w)

        self._som_var = ctk.BooleanVar(value=self.cfg["som_ativo"])
        def som_w(r):
            ctk.CTkCheckBox(r, text="", variable=self._som_var,
                            fg_color=C_WHITE, hover_color=C_MUT2,
                            width=24, height=24).pack(side="right")
        row("Som ao contar", som_w)

        # Captura de teclas
        self._vk_mais  = tk.IntVar(value=self.cfg["tecla_mais"])
        self._vk_menos = tk.IntVar(value=self.cfg["tecla_menos"])

        for campo, var, nome in [
            ("tecla_mais",  self._vk_mais,  "Tecla +"),
            ("tecla_menos", self._vk_menos, "Tecla −"),
        ]:
            def make_row(c=campo, v=var, n=nome):
                def w(r):
                    lbl = ctk.CTkLabel(r, text=f"VK {v.get()}",
                                       font=(MONO, 9), text_color=C_WHITE,
                                       fg_color=C_BG2, corner_radius=0)
                    lbl.pack(side="right", padx=(4,0))
                    def cap():
                        lbl.configure(text="Pressione...")
                        _q = queue.Queue()
                        def on_p(k):
                            if hasattr(k, "vk") and k.vk:
                                _q.put(k.vk); return False
                        kb.Listener(on_press=on_p, daemon=True).start()
                        def aguardar():
                            try:
                                vk = _q.get_nowait()
                                self.cfg[c] = vk; v.set(vk)
                                lbl.configure(text=f"VK {vk}")
                            except queue.Empty:
                                self.after(50, aguardar)
                        self.after(50, aguardar)
                    ctk.CTkButton(r, text="Capturar", command=cap,
                                  width=80, height=26, corner_radius=0,
                                  fg_color=C_BG2, text_color=C_MUTED,
                                  hover_color=C_BG3,
                                  font=(MONO, 8)).pack(side="right", padx=4)
                row(n, w)
            make_row()

        sec("SISTEMA")

        self._notif_var   = ctk.BooleanVar(value=self.cfg["notif_meta"])
        self._startup_var = ctk.BooleanVar(value=self.cfg["iniciar_windows"])

        def notif_w(r):
            ctk.CTkCheckBox(r, text="", variable=self._notif_var,
                            fg_color=C_WHITE, hover_color=C_MUT2,
                            width=24, height=24).pack(side="right")
        def startup_w(r):
            ctk.CTkCheckBox(r, text="", variable=self._startup_var,
                            fg_color=C_WHITE, hover_color=C_MUT2,
                            width=24, height=24).pack(side="right")

        row("Notificação ao bater meta", notif_w)
        row("Iniciar com o Windows",     startup_w)

        ctk.CTkButton(f, text="SALVAR CONFIGURAÇÕES",
                      command=self._salvar_cfg,
                      height=42, corner_radius=0,
                      fg_color=C_WHITE, text_color=C_BG,
                      hover_color="#DDDDDD",
                      font=(MONO, 11, "bold")).pack(fill="x", padx=20, pady=16)

    def _salvar_cfg(self):
        self.cfg["meta_diaria"]     = self._meta_var.get()
        self.cfg["som_ativo"]       = bool(self._som_var.get())
        self.cfg["notif_meta"]      = bool(self._notif_var.get())
        self.cfg["iniciar_windows"] = bool(self._startup_var.get())
        cfg_save(self.cfg)
        set_startup(self.cfg["iniciar_windows"])
        messagebox.showinfo("Salvo", "Configurações salvas.")

    # ── ABA AJUDA ─────────────────────────────────────────────────────────────
    def _build_ajuda(self, f):
        ctk.CTkLabel(f, text="[ ATALHOS ]",
                     font=(MONO, 13, "bold"),
                     text_color=C_WHITE).pack(anchor="w", padx=28, pady=(24,14))

        for tecla, desc in [
            (f"VK {self.cfg.get('tecla_mais',107)}",  "Soma 1 ao contador"),
            (f"VK {self.cfg.get('tecla_menos',109)}", "Subtrai 1 do contador"),
            ("Botão +/−",  "Mesmo efeito, via mouse"),
            ("Auto sync",  "A cada 5 minutos"),
            ("Cache DB",   "Funciona sem internet"),
            ("Reset",      "Zera o dia (com confirmação)"),
        ]:
            row = ctk.CTkFrame(f, fg_color=C_BG2, corner_radius=0,
                               border_width=1, border_color=C_BG3)
            row.pack(fill="x", padx=28, pady=3)
            ctk.CTkLabel(row, text=tecla, font=(MONO, 10, "bold"),
                         text_color=C_WHITE, width=110, anchor="w").pack(
                side="left", padx=12, pady=8)
            ctk.CTkFrame(row, width=1, fg_color=C_BORD,
                         corner_radius=0).pack(side="left", fill="y", pady=4)
            ctk.CTkLabel(row, text=desc, font=(MONO, 10),
                         text_color=C_MUTED).pack(side="left", padx=12)

        ctk.CTkLabel(f, text="v19.0  ·  customtkinter",
                     font=(MONO, 8), text_color=C_MUT2).pack(
            anchor="e", padx=28, pady=20)

    # ── TECLADO ───────────────────────────────────────────────────────────────
    def _iniciar_teclado(self):
        if self._kb_lst:
            self._kb_lst.stop()
        vk_mais  = self.cfg.get("tecla_mais",  107)
        vk_menos = self.cfg.get("tecla_menos", 109)

        def on_press(k):
            try:
                if hasattr(k, "vk"):
                    if k.vk == vk_mais:   self._kb_q.put(1)
                    elif k.vk == vk_menos: self._kb_q.put(-1)
            except Exception:
                pass

        self._kb_lst = kb.Listener(on_press=on_press, daemon=True)
        self._kb_lst.start()
        self._processar_kb()

    def _processar_kb(self):
        try:
            while True:
                self._update_val(self._kb_q.get_nowait())
        except queue.Empty:
            pass
        self.after(50, self._processar_kb)

    # ── SAIR ──────────────────────────────────────────────────────────────────
    def _sair(self):
        if self._kb_lst:
            self._kb_lst.stop()
            self._kb_lst = None
        self.user_logado = None
        self._tela_login()


if __name__ == "__main__":
    iniciar_bancos()
    ctk.set_appearance_mode("Dark")
    AppCIOSP().mainloop()