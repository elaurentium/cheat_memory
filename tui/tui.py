import curses
import time
import random
import math
from itertools import cycle

# ASCII Art animado para o cabeçalho
HEADER_FRAMES = [
    [
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓",
        "┃                                                                                   ┃",
        "┃   ██████╗██╗  ██╗███████╗ █████╗ ████████╗    ███╗   ███╗███████╗███╗   ███╗ ██████╗  ┃",
        "┃  ██╔════╝██║  ██║██╔════╝██╔══██╗╚══██╔══╝    ████╗ ████║██╔════╝████╗ ████║██╔═══██╗ ┃",
        "┃  ██║     ███████║█████╗  ███████║   ██║       ██╔████╔██║█████╗  ██╔████╔██║██║   ██║ ┃",
        "┃  ██║     ██╔══██║██╔══╝  ██╔══██║   ██║       ██║╚██╔╝██║██╔══╝  ██║╚██╔╝██║██║   ██║ ┃",
        "┃  ╚██████╗██║  ██║███████╗██║  ██║   ██║       ██║ ╚═╝ ██║███████╗██║ ╚═╝ ██║╚██████╔╝ ┃",
        "┃   ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝       ╚═╝     ╚═╝╚══════╝╚═╝     ╚═╝ ╚═════╝  ┃",
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
    ],
    [
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓",
        "┃                                                                                   ┃",
        "┃   ██████╗██╗  ██╗███████╗ █████╗ ████████╗    ███╗   ███╗███████╗███╗   ███╗ ██████╗  ┃",
        "┃  ██╔════╝██║  ██║██╔════╝██╔══██╗╚══██╔══╝    ████╗ ████║██╔════╝████╗ ████║██╔═══██╗ ┃",
        "┃  ██║     ███████║█████╗  ███████║   ██║       ██╔████╔██║█████╗  ██╔████╔██║██║   ██║ ┃",
        "┃  ██║     ██╔══██║██╔══╝  ██╔══██║   ██║       ██║╚██╔╝██║██╔══╝  ██║╚██╔╝██║██║   ██║ ┃",
        "┃  ╚██████╗██║  ██║███████╗██║  ██║   ██║▄█╗    ██║ ╚═╝ ██║███████╗██║ ╚═╝ ██║╚██████╔╝ ┃",
        "┃   ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝╚═╝    ╚═╝     ╚═╝╚══════╝╚═╝     ╚═╝ ╚═════╝  ┃",
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
    ],
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

# Caracteres para barras estilizadas
BAR_CHARS = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
BOX_STYLES = [
    {"title": "═══ {} ═══", "tl": "╔", "tr": "╗", "bl": "╚", "br": "╝", "h": "═", "v": "║"},
    {"title": "┌── {} ──┐", "tl": "┌", "tr": "┐", "bl": "└", "br": "┘", "h": "─", "v": "│"},
    {"title": "╭── {} ──╮", "tl": "╭", "tr": "╮", "bl": "╰", "br": "╯", "h": "─", "v": "│"},
    {"title": "╔══ {} ══╗", "tl": "╔", "tr": "╗", "bl": "╚", "br": "╝", "h": "═", "v": "║"}
]

STATUS_ICONS = {
    "Running": "⚡",
    "Sleeping": "💤",
    "Stopped": "⏹️",
    "Zombie": "💀",
    "Idle": "⌛"
}

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

def draw_process_list(stdscr, y, x, h, w, processes, selected_idx, selected_process_idx, current_time):
    """Desenha lista de processos com efeitos de destaque e animações"""
    box_style = BOX_STYLES[3]
    draw_box(stdscr, y, x, h, w, "⚡ Process Monitor ⚡", box_style, 10)
    
    try:
        header = "PID    CPU%  MEM%  STATUS"
        header_y = y + 1
        stdscr.addstr(header_y, x + 2, header, curses.color_pair(4) | curses.A_BOLD)
        
        separator_y = y + 2
        stdscr.addstr(separator_y, x + 2, "─" * (w - 4), curses.color_pair(4))
        
        list_start_y = y + 3
        visible_rows = h - 5
        
        for i, proc in enumerate(processes):
            if i >= visible_rows:
                break
                
            row_y = list_start_y + i
            status_icon = STATUS_ICONS.get(proc['status'], "•")
            line = f"{proc['pid']:<6} {proc['cpu']:<5} {proc['mem']:<5} {status_icon} {proc['status']}"
            
            style = curses.A_NORMAL
            color = 4
            
            if i == selected_idx:
                style |= curses.A_BOLD
                color = 8
                if int(current_time * 2) % 2 == 0:
                    style |= curses.A_REVERSE
            
            if i == selected_process_idx:
                prefix = "✓ "
                color = 9
            else:
                prefix = "  "
            
            if proc['cpu'] > 30 or proc['mem'] > 15:
                if i != selected_idx and i != selected_process_idx:
                    style |= curses.A_BOLD
                    if proc['cpu'] > 40 or proc['mem'] > 18:
                        color = 11
            
            stdscr.addstr(row_y, x + 2, prefix + line, curses.color_pair(color) | style)
            
            if i == selected_idx:
                cpu_bar_x = x + w - 20
                cpu_bar_width = 14
                stdscr.addstr(row_y, cpu_bar_x - 4, "CPU:", curses.color_pair(4))
                draw_fancy_bar(stdscr, row_y, cpu_bar_x, cpu_bar_width, proc['cpu'], 1)
                
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

def generate_random_processes(num=10):
    """Gera processos aleatórios com nomes mais interessantes"""
    process_names = ["system", "browser", "editor", "server", "database", 
                    "network", "kernel", "logger", "cache", "monitor", 
                    "backup", "security", "crypto", "media", "compiler"]
    statuses = ["Running", "Sleeping", "Stopped", "Zombie", "Idle"]
    
    processes = []
    for i in range(num):
        name = random.choice(process_names)
        processes.append({
            "pid": f"{1000 + i}",
            "cpu": random.randint(5, 50),
            "mem": random.randint(1, 20),
            "status": random.choice(statuses),
            "name": f"{name}_{i}"
        })
    return processes

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
    animation_frame = 0
    frame_cycle = cycle(range(len(HEADER_FRAMES)))

    processes = generate_random_processes(12)
    text_content = generate_demo_text()

    key_hints = ["q: Quit", "↑↓: Navigate", "Enter: Select", "r: Refresh", "PgUp/PgDn: Scroll"]

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
        if frame_count % 30 == 0:
            for proc in processes:
                proc["cpu"] = max(5, min(proc["cpu"] + random.randint(-5, 5), 95))
                proc["mem"] = max(1, min(proc["mem"] + random.randint(-2, 2), 50))

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

        draw_process_list(stdscr, header_h, 0, proc_h, proc_w, processes, selected_idx, selected_process_idx, current_time)

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
                selected_idx = max(0, selected_idx - 1)
            elif key == curses.KEY_DOWN:
                selected_idx = min(len(processes) - 1, selected_idx + 1)
            elif key == curses.KEY_ENTER or key in [10, 13]:
                selected_process_idx = selected_idx
            elif key == ord('r'):
                processes = generate_random_processes(12)
                text_content = generate_demo_text()
            elif key == curses.KEY_PAGEDOWN:
                text_scroll = min(len(text_content.split('\n')) - text_h + 4, text_scroll + text_h - 4)
            elif key == curses.KEY_PAGEUP:
                text_scroll = max(0, text_scroll - text_h + 4)
            elif key == curses.KEY_RESIZE:
                h, w = stdscr.getmaxyx()
                stdscr.clear()
        except curses.error:
            continue

curses.wrapper(main)