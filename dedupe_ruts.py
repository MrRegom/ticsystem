from core.models import Funcionario
from django.db.models import Count

all_funcs = Funcionario.objects.all()

# 1. Clean RUTs in memory to find duplicates
cleaned_map = {}
for f in all_funcs:
    if f.rut:
        clean_rut = "".join([c for c in f.rut.upper() if c.isdigit() or c == 'K'])
        if len(clean_rut) > 1:
            clean_rut = f"{clean_rut[:-1]}-{clean_rut[-1]}"
            
        if clean_rut in cleaned_map:
            cleaned_map[clean_rut].append(f)
        else:
            cleaned_map[clean_rut] = [f]

# 2. Handle duplicates by deleting the newer ones
for clean_rut, func_list in cleaned_map.items():
    if len(func_list) > 1:
        # Sort by id, keep the oldest one
        func_list.sort(key=lambda x: x.id)
        for duplicate in func_list[1:]:
            print(f"Deleting duplicate RUT: {duplicate.rut} - {duplicate.nombre}")
            duplicate.delete()

# 3. Save remaining Funcionario to apply the new RUT format
f_count = 0
for f in Funcionario.objects.all():
    f.save()
    f_count += 1
print(f"Actualizados {f_count} Funcionarios con el nuevo formato de RUT.")
