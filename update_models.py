import re

with open(r'c:\proyectos\ticsystem\core\models.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_save = '''    def save(self, *args, **kwargs):
        if self.nombres:
            self.nombres = self.nombres.strip().upper()
        if self.apellidos:
            self.apellidos = self.apellidos.strip().upper()
        if self.rut:
            self.rut = self.rut.strip().upper()
        super().save(*args, **kwargs)'''

new_save = '''    def save(self, *args, **kwargs):
        if self.nombres:
            self.nombres = self.nombres.strip().upper()
        if self.apellidos:
            self.apellidos = self.apellidos.strip().upper()
        if self.rut:
            clean_rut = "".join([c for c in self.rut.upper() if c.isdigit() or c == 'K'])
            if len(clean_rut) > 1:
                self.rut = f"{clean_rut[:-1]}-{clean_rut[-1]}"
            else:
                self.rut = clean_rut
        super().save(*args, **kwargs)'''

if old_save in content:
    content = content.replace(old_save, new_save)
    with open(r'c:\proyectos\ticsystem\core\models.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("models.py updated")
else:
    print("Could not find old save method")
