import curses
import time
import random
import math
from itertools import cycle

HEADER_FRAMES = [
    [
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓",
        "┃                                                                                        ┃",
        "┃   ██████╗██╗  ██╗███████╗ █████╗ ████████╗    ███╗   ███╗███████╗███╗   ███╗ ██████╗   ┃",
        "┃  ██╔════╝██║  ██║██╔════╝██╔══██╗╚══██╔══╝    ████╗ ████║██╔════╝████╗ ████║██╔═══██╗  ┃",
        "┃  ██║     ███████║█████╗  ███████║   ██║       ██╔████╔██║█████╗  ██╔████╔██║██║   ██║  ┃",
        "┃  ██║     ██╔══██║██╔══╝  ██╔══██║   ██║       ██║╚██╔╝██║██╔══╝  ██║╚██╔╝██║██║   ██║  ┃",
        "┃  ╚██████╗██║  ██║███████╗██║  ██║   ██║       ██║ ╚═╝ ██║███████╗██║ ╚═╝ ██║╚██████╔╝  ┃",
        "┃   ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝       ╚═╝     ╚═╝╚══════╝╚═╝     ╚═╝ ╚═════╝   ┃",
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
    ]
]

BAR_CHARS = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
BOX_STYLES = [
    {"title": "═══ {} ═══", "tl": "╔", "tr": "╗", "bl": "╚", "br": "╝", "h": "═", "v": "║"},
    {"title": "┌── {} ──┐", "tl": "┌", "tr": "┐", "bl": "└", "br": "┘", "h": "─", "v": "│"},
    {"title": "╭── {} ──╮", "tl": "╭", "tr": "╮", "bl": "╰", "br": "╯", "h": "─", "v": "│"},
    {"title": "╔══ {} ══╗", "tl": "╔", "tr": "╗", "bl": "╚", "br": "╝", "h": "═", "v": "║"}
]


def init_colors():
    """Inicializa cores mais vibrantes e gradientes"""
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)       # Vermelho
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)     # Verde
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)      # Azul
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)     # Branco
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)      # Ciano
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)   # Magenta
    curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_BLACK)    # Amarelo
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_CYAN)      # Selecionado
    curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_GREEN)     # Ativo
    curses.init_pair(10, curses.COLOR_YELLOW, curses.COLOR_BLACK)   # Títulos
    curses.init_pair(11, curses.COLOR_WHITE, curses.COLOR_RED)      # Alertas
    curses.init_pair(12, 208, curses.COLOR_BLACK)                   # Laranja
    curses.init_pair(13, 141, curses.COLOR_BLACK)                   # Roxo claro
    curses.init_pair(14, 45, curses.COLOR_BLACK)                    # Azul claro

def get_random_style():
    """Retorna um estilo de caixa aleatório"""
    return random.choice(BOX_STYLES)

def draw_box(stdscr, y, x, h, w, title="", style=None, color=4):
    """Desenha uma caixa com estilo personalizado"""
    if style is None:
        style = get_random_style()
    
    try:
        formatted_title = style["title"].format(title) if title else ""
        title_pos = (w - len(formatted_title)) // 2 if title else 0
        
        stdscr.addstr(y, x, style["tl"] + style["h"] * (w - 2) + style["tr"], curses.color_pair(color))
        for i in range(1, h - 1):
            stdscr.addstr(y + i, x, style["v"], curses.color_pair(color))
            stdscr.addstr(y + i, x + w - 1, style["v"], curses.color_pair(color))
        stdscr.addstr(y + h - 1, x, style["bl"] + style["h"] * (w - 2) + style["br"], curses.color_pair(color))
        
        if title and len(formatted_title) < w - 2:
            stdscr.addstr(y, x + title_pos, formatted_title, curses.color_pair(10) | curses.A_BOLD)
            
    except curses.error:
        pass

def draw_fancy_bar(stdscr, y, x, width, percentage, color_pair):
    """Desenha uma barra com caracteres de preenchimento gradual"""
    try:
        fill_width = int(width * percentage / 100)
        if fill_width > 0:
            stdscr.addstr(y, x, "█" * fill_width, curses.color_pair(color_pair))
            if fill_width < width and fill_width > 0:
                partial_idx = int((percentage % (100/width)) / (100/width) * (len(BAR_CHARS) - 1))
                stdscr.addstr(y, x + fill_width, BAR_CHARS[partial_idx], curses.color_pair(color_pair))
            if fill_width + 1 < width:
                stdscr.addstr(y, x + fill_width + 1, " " * (width - fill_width - 1))
    except curses.error:
        pass

def pulse_effect(val, time_factor=5):
    """Cria um efeito de pulsação baseado no tempo"""
    return val * (0.8 + 0.2 * math.sin(time.time() * time_factor))

def draw_vertical_bar_chart(stdscr, y, x, h, w, data, current_time):
    """Desenha um gráfico de barras vertical com efeito de pulsação"""
    box_style = BOX_STYLES[0]
    draw_box(stdscr, y, x, h, w, "☰ CPU Monitor ☰", box_style, 10)
    
    max_val = max(data.values(), default=1)
    bar_width = (w - 6) // len(data)
    if bar_width < 2:
        return

    try:
        colors = {"Core1": 1, "Core2": 2, "Core3": 3, "Core4": 5}
        for idx, (label, value) in enumerate(data.items()):
            pulse = pulse_effect(1, 3) if value > max_val * 0.7 else 1
            bar_height = int((value / max_val) * pulse * (h - 6))
            bar_height = max(1, min(bar_height, h - 6))
            
            color = colors.get(label, idx % 7 + 1)
            
            for i in range(bar_height):
                bar_y = y + h - 3 - i
                bar_x = x + 3 + idx * bar_width
                color_mod = min(14, color + int(i / bar_height * 2)) if i > bar_height // 2 else color
                stdscr.addstr(bar_y, bar_x, "█" * (bar_width - 1), curses.color_pair(color_mod))
            
            if bar_height > 0:
                val_str = f"{value}%"
                val_pos = bar_x + (bar_width - len(val_str)) // 2
                stdscr.addstr(y + h - 3 - bar_height - 1, val_pos, val_str, curses.color_pair(color) | curses.A_BOLD)
            
            label = label[:bar_width-1]
            label_pos = bar_x + (bar_width - len(label)) // 2
            stdscr.addstr(y + h - 2, label_pos, label, curses.color_pair(10))
    except curses.error:
        pass

def draw_horizontal_bar_chart(stdscr, y, x, h, w, data, current_time):
    """Desenha um gráfico de barras horizontal com efeitos visuais"""
    box_style = BOX_STYLES[2]
    draw_box(stdscr, y, x, h, w, "⚙ Memory Usage ⚙", box_style, 10)
    
    max_val = max(data.values(), default=1)
    max_label_len = max(len(label) for label in data.keys()) + 2

    try:
        colors = {"Used": 1, "Free": 2, "Cache": 3}
        for idx, (label, value) in enumerate(data.items()):
            bar_y = y + 2 + idx * 2
            if bar_y >= y + h - 2:
                break
                
            bar_max_length = w - max_label_len - 10
            pulse = pulse_effect(1, 2) if value > max_val * 0.7 else 1
            bar_length = int((value / max_val) * pulse * bar_max_length)
            bar_length = max(1, min(bar_length, bar_max_length))
            
            color = colors.get(label, idx % 7 + 1)
            
            stdscr.addstr(bar_y, x + 2, f"{label:<{max_label_len}}", curses.color_pair(4))
            
            for i in range(bar_length):
                intensity = i / bar_length
                char = "█"
                color_mod = color
                if intensity > 0.7:
                    color_mod = min(14, color + 2)
                elif intensity > 0.4:
                    color_mod = min(14, color + 1)
                    
                stdscr.addstr(bar_y, x + 2 + max_label_len + i, char, curses.color_pair(color_mod))
            
            val_str = f" {value}%"
            stdscr.addstr(bar_y, x + 2 + max_label_len + bar_length, val_str, 
                         curses.color_pair(4) | curses.A_BOLD)
            
    except curses.error:
        pass

def draw_process_list(stdscr, y, x, h, w, processes, selected_idx, selected_process_idx, scroll_offset, current_time):
    """Desenha lista de processos com PID e Path, com rolagem"""
    box_style = BOX_STYLES[3]
    draw_box(stdscr, y, x, h, w, "⚡ Process Monitor ⚡", box_style, 10)
    
    try:
        header = "PID     Path"
        header_y = y + 1
        stdscr.addstr(header_y, x + 2, header, curses.color_pair(4) | curses.A_BOLD)
        
        separator_y = y + 2
        stdscr.addstr(separator_y, x + 2, "─" * (w - 4), curses.color_pair(4))
        
        list_start_y = y + 3
        visible_rows = h - 5
        
        # Calcula os índices dos processos visíveis
        start_idx = scroll_offset
        end_idx = min(start_idx + visible_rows, len(processes))
        
        for i, proc_idx in enumerate(range(start_idx, end_idx)):
            proc = processes[proc_idx]
            row_y = list_start_y + i
            path = proc['path'][:w-14]  # Trunca o path para caber na tela
            line = f"{proc['pid']:<7} {path}"
            
            style = curses.A_NORMAL
            color = 4
            
            if proc_idx == selected_idx:
                style |= curses.A_BOLD
                color = 8
                if int(current_time * 2) % 2 == 0:
                    style |= curses.A_REVERSE
            
            if proc_idx == selected_process_idx:
                prefix = "✓ "
                color = 9
            else:
                prefix = "  "
            
            stdscr.addstr(row_y, x + 2, prefix + line, curses.color_pair(color) | style)
            
        # Indicador de rolagem
        if len(processes) > visible_rows:
            scroll_percent = min(100, int(scroll_offset / max(1, len(processes) - visible_rows) * 100))
            scroll_indicator = f"▲ {scroll_percent}% ▼"
            stdscr.addstr(y + h - 2, x + w - len(scroll_indicator) - 2, 
                         scroll_indicator, curses.color_pair(7))
                
    except curses.error:
        pass

def draw_text_section(stdscr, y, x, h, w, title, text, scroll_offset):
    """Desenha seção de texto com efeitos visuais"""
    box_style = BOX_STYLES[1]
    draw_box(stdscr, y, x, h, w, title, box_style, 5)
    
    if not text:
        text = "No details available."
    
    lines = text.split('\n')
    visible_lines = h - 4
    start_idx = min(scroll_offset, max(0, len(lines) - visible_lines))
    end_idx = min(start_idx + visible_lines, len(lines))

    try:
        for i, line in enumerate(lines[start_idx:end_idx]):
            line_y = y + 2 + i
            line_text = line[:w-6]
            color = 14 if line_text.startswith("  ") or line_text.startswith("\t") else 4
            stdscr.addstr(line_y, x + 3, line_text, curses.color_pair(color))
            
        if len(lines) > visible_lines:
            scroll_percent = min(100, int(start_idx / max(1, len(lines) - visible_lines) * 100))
            scroll_indicator = f"▲ {scroll_percent}% ▼"
            stdscr.addstr(y + h - 2, x + w - len(scroll_indicator) - 2, 
                         scroll_indicator, curses.color_pair(7))
    except curses.error:
        pass

def draw_status_bar(stdscr, y, x, w, key_hints):
    """Desenha barra de status com informações úteis"""
    try:
        statusbar = " " + " | ".join(key_hints)
        statusbar = statusbar[:w-2]
        statusbar = statusbar + " " * (w - len(statusbar) - 1)
        stdscr.addstr(y, x, statusbar, curses.color_pair(5) | curses.A_BOLD)
        
        time_str = time.strftime(" %H:%M:%S ", time.localtime())
        stdscr.addstr(y, x + w - len(time_str) - 1, time_str, 
                     curses.color_pair(10) | curses.A_BOLD)
    except curses.error:
        pass

def draw_header(stdscr, y, x, w, current_frame):
    """Desenha cabeçalho com animação"""
    frame = HEADER_FRAMES[current_frame]
    try:
        for i, line in enumerate(frame):
            if y + i >= curses.LINES:
                break
            padding = max(0, (w - len(line)) // 2)
            stdscr.addstr(y + i, x + padding, line[:w-padding], curses.color_pair(random.randint(1, 7)))
    except curses.error:
        pass

def get_process_list():
    """Retorna a lista de processos fornecida"""
    return [
        {"pid": "1", "path": "/sbin/init"},
        {"pid": "2", "path": "/init"},
        {"pid": "6", "path": "plan9"},
        {"pid": "58", "path": "/usr/lib/systemd/systemd-journald"},
        {"pid": "102", "path": "/usr/lib/systemd/systemd-udevd"},
        {"pid": "149", "path": "/usr/lib/systemd/systemd-resolved"},
        {"pid": "150", "path": "/usr/lib/systemd/systemd-timesyncd"},
        {"pid": "161", "path": "/usr/sbin/cron"},
        {"pid": "162", "path": "@dbus-daemon"},
        {"pid": "176", "path": "/usr/lib/systemd/systemd-logind"},
        {"pid": "179", "path": "/usr/libexec/wsl-pro-service"},
        {"pid": "187", "path": "/sbin/agetty"},
        {"pid": "197", "path": "/sbin/agetty"},
        {"pid": "198", "path": "/usr/sbin/rsyslogd"},
        {"pid": "218", "path": "/usr/bin/python3"},
        {"pid": "225", "path": "sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups"},
        {"pid": "246", "path": "/usr/bin/containerd"},
        {"pid": "458", "path": "/init"},
        {"pid": "459", "path": "/init"},
        {"pid": "460", "path": "-zsh"},
        {"pid": "461", "path": "/bin/login"},
        {"pid": "464", "path": "/usr/bin/dockerd"},
        {"pid": "544", "path": "/usr/lib/systemd/systemd"},
        {"pid": "545", "path": "(sd-pam)"},
        {"pid": "558", "path": "-zsh"},
        {"pid": "1229", "path": "/init"},
        {"pid": "11919", "path": "/init"},
        {"pid": "12888", "path": "/usr/lib/polkit-1/polkitd"},
        {"pid": "40414", "path": "/init"},
        {"pid": "40415", "path": "/init"},
        {"pid": "40416", "path": "sh"},
        {"pid": "40417", "path": "sh"},
        {"pid": "40422", "path": "sh"},
        {"pid": "40426", "path": "/home/evandro/.vscode-server/bin/7c6fdfb0b8f2f675eb0b47f3d95eeca78962565b/node"},
        {"pid": "40437", "path": "/init"},
        {"pid": "40438", "path": "/init"},
        {"pid": "40439", "path": "/home/evandro/.vscode-server/bin/7c6fdfb0b8f2f675eb0b47f3d95eeca78962565b/node"},
        {"pid": "40446", "path": "/init"},
        {"pid": "40447", "path": "/init"},
        {"pid": "40448", "path": "/home/evandro/.vscode-server/bin/7c6fdfb0b8f2f675eb0b47f3d95eeca78962565b/node"},
        {"pid": "40449", "path": "/home/evandro/.vscode-server/bin/7c6fdfb0b8f2f675eb0b47f3d95eeca78962565b/node"},
        {"pid": "40467", "path": "/home/evandro/.vscode-server/bin/7c6fdfb0b8f2f675eb0b47f3d95eeca78962565b/node"},
        {"pid": "40507", "path": "/home/evandro/.vscode-server/bin/7c6fdfb0b8f2f675eb0b47f3d95eeca78962565b/node"},
        {"pid": "40528", "path": "/init"},
        {"pid": "40531", "path": "/init"},
        {"pid": "40540", "path": "/init"},
        {"pid": "40572", "path": "/home/evandro/.vscode-server/extensions/ms-python.python-2025.4.0-linux-x64/python-env-tools/bin/pet"},
        {"pid": "40697", "path": "/init"},
        {"pid": "40698", "path": "/init"},
        {"pid": "40699", "path": "/bin/sh"},
        {"pid": "40700", "path": "/bin/sh"},
        {"pid": "40710", "path": "/home/evandro/.vscode-server/bin/7c6fdfb0b8f2f675eb0b47f3d95eeca78962565b/node"},
        {"pid": "40786", "path": "/usr/bin/zsh"},
        {"pid": "40788", "path": "/usr/bin/zsh"},
        {"pid": "40880", "path": "/bin/sh"},
        {"pid": "40906", "path": "/home/evandro/.vscode-server/bin/7c6fdfb0b8f2f675eb0b47f3d95eeca78962565b/node"},
        {"pid": "40947", "path": "/home/evandro/.vscode-server/extensions/ms-vscode.cpptools-1.25.0-linux-x64/bin/cpptools"},
        {"pid": "40962", "path": "/usr/bin/zsh"},
        {"pid": "41001", "path": "/home/evandro/.vscode-server/bin/7c6fdfb0b8f2f675eb0b47f3d95eeca78962565b/node"},
        {"pid": "41175", "path": "/home/evandro/.vscode-server/extensions/codeium.codeium-1.42.7/dist/c2d78b189732d0db86e3055e1a49c2a75d623a38/language_server_linux_x64"},
        {"pid": "41188", "path": "/home/evandro/.vscode-server/extensions/codeium.codeium-1.42.7/dist/c2d78b189732d0db86e3055e1a49c2a75d623a38/language_server_linux_x64"},
        {"pid": "41621", "path": "/home/evandro/.vscode-server/extensions/ms-vscode.cpptools-1.25.0-linux-x64/bin/cpptools-srv"},
        {"pid": "41810", "path": "/bin/bash"},
        {"pid": "41829", "path": "sudo"},
        {"pid": "41830", "path": "sudo"},
        {"pid": "41831", "path": "./cheat"}
    ]

def generate_demo_text():
    """Gera texto de demonstração mais informativo"""
    texts = [
        """Process Information:
        
This panel shows detailed information about the selected process.
You can see memory usage, threads, open files and other details.

Performance Metrics:
- CPU Usage Trend: Variable
- Memory Allocation: Stable
- I/O Operations: Normal
- Network Usage: Low

Process started at: 08:12:45
User: system
Priority: normal
""",
        """System Overview:
        
Current system status is operational.
All services are running normally.
Last system check: Today at 08:00

Resource Utilization:
- RAM: 4.2GB / 16GB
- Swap: 0.5GB / 8GB
- Disk: 45% used
- Network: 5MB/s

System uptime: 3 days, 7 hours
"""
    ]
    return random.choice(texts)

def main(stdscr):
    """Função principal do programa"""
    curses.curs_set(0)
    init_colors()
    stdscr.nodelay(True)

    selected_idx = 0
    selected_process_idx = None
    text_scroll = 0
    process_scroll = 0  # Novo: deslocamento de rolagem para a lista de processos
    animation_frame = 0
    frame_cycle = cycle(range(len(HEADER_FRAMES)))

    processes = get_process_list()
    text_content = generate_demo_text()

    key_hints = ["q: Quit", "↑↓: Navigate", "Enter: Select", "r: Refresh", "PgUp/PgDn: Scroll Text"]

    processes_style = BOX_STYLES[0]
    chart_style = BOX_STYLES[1]
    text_style = BOX_STYLES[2]

    last_frame_time = time.time()
    frame_count = 0

    while True:
        current_time = time.time()
        frame_time = current_time - last_frame_time
        if frame_time < 1/30:
            time.sleep(1/30 - frame_time)
            continue
        last_frame_time = current_time
        frame_count += 1

        if frame_count % 10 == 0:
            animation_frame = next(frame_cycle)

        h, w = stdscr.getmaxyx()
        if h < 24 or w < 80:
            stdscr.clear()
            try:
                msg = "Terminal muito pequeno! Por favor, redimensione (mín: 80x24)."
                stdscr.addstr(0, 0, msg, curses.color_pair(11) | curses.A_BOLD)
            except curses.error:
                pass
            stdscr.refresh()
            continue

        stdscr.erase()

        header_h = 10
        status_h = 1
        content_h = h - header_h - status_h
        chart_h = content_h // 2
        chart_w = w // 2
        proc_h = content_h
        proc_w = w // 2
        text_h = content_h - chart_h
        text_w = w - proc_w

        if chart_h < 5 or chart_w < 20 or proc_h < 5 or proc_w < 20 or text_h < 5 or text_w < 20:
            stdscr.clear()
            try:
                msg = "Terminal muito pequeno para exibir todos os elementos!"
                stdscr.addstr(0, 0, msg, curses.color_pair(11) | curses.A_BOLD)
            except curses.error:
                pass
            stdscr.refresh()
            continue

        draw_header(stdscr, 0, 0, w, animation_frame)
        draw_status_bar(stdscr, h - status_h, 0, w, key_hints)

        draw_process_list(stdscr, header_h, 0, proc_h, proc_w, processes, selected_idx, selected_process_idx, process_scroll, current_time)

        cpu_data = {
            "Core1": random.randint(10, 90),
            "Core2": random.randint(10, 90),
            "Core3": random.randint(10, 90),
            "Core4": random.randint(10, 90)
        }
        draw_vertical_bar_chart(stdscr, header_h, proc_w, chart_h, chart_w, cpu_data, current_time)

        mem_data = {
            "Used": random.randint(20, 80),
            "Free": random.randint(10, 50),
            "Cache": random.randint(5, 30)
        }
        draw_horizontal_bar_chart(stdscr, header_h + chart_h, proc_w, chart_h, chart_w, mem_data, current_time)

        draw_text_section(stdscr, header_h + chart_h, proc_w, text_h, text_w, "Details", text_content, text_scroll)

        stdscr.refresh()

        try:
            key = stdscr.getch()
            if key == -1:
                continue
            if key == ord('q'):
                break
            elif key == curses.KEY_UP:
                if selected_idx > 0:
                    selected_idx -= 1
                    # Ajusta o scroll para manter o item selecionado visível
                    if selected_idx < process_scroll:
                        process_scroll = selected_idx
            elif key == curses.KEY_DOWN:
                if selected_idx < len(processes) - 1:
                    selected_idx += 1
                    # Ajusta o scroll para manter o item selecionado visível
                    if selected_idx >= process_scroll + (proc_h - 5):
                        process_scroll = selected_idx - (proc_h - 6)
            elif key == curses.KEY_ENTER or key in [10, 13]:
                selected_process_idx = selected_idx
            elif key == ord('r'):
                processes = get_process_list()
                text_content = generate_demo_text()
                selected_idx = min(selected_idx, len(processes) - 1)  # Evita índice inválido
                process_scroll = min(process_scroll, max(0, len(processes) - (proc_h - 5)))
            elif key == curses.KEY_PAGEDOWN:
                text_scroll = min(len(text_content.split('\n')) - text_h + 4, text_scroll + text_h - 4)
            elif key == curses.KEY_PAGEUP:
                text_scroll = max(0, text_scroll - text_h + 4)
            elif key == curses.KEY_RESIZE:
                h, w = stdscr.getmaxyx()
                stdscr.clear()
                # Ajusta scroll e índice para evitar ultrapassar limites
                selected_idx = min(selected_idx, len(processes) - 1)
                process_scroll = min(process_scroll, max(0, len(processes) - (proc_h - 5)))
        except curses.error:
            continue

curses.wrapper(main)