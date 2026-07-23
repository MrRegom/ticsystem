import sys

def check_divs(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    lines = html.split('\n')
    try:
        grid_start = next(i for i, l in enumerate(lines) if 'class="dashboard-grid"' in l)
        print('Grid Start:', grid_start)
    except StopIteration:
        print("No dashboard-grid found")
        return
        
    depth = 0
    for i, l in enumerate(lines[grid_start:], start=grid_start):
        depth += l.count('<div')
        depth -= l.count('</div')
        print(f"{i}: {depth} - {l.strip()}")
        if depth == 0 and '<div' in l:
            print('Grid End:', i, l)
            break
        if depth < 0:
            print('UNDERFLOW at', i)
            break

check_divs(r'c:\proyectos\ticsystem\core\templates\core\inicio.html')
