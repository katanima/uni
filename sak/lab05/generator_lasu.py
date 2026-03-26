import bpy
import math
import random
import os
from mathutils import Vector, Euler

TYPY_ROSLIN = {
    "drzewo": {
        "wysokosc": (3.0, 5.0),
        "liczba_lisci": (4, 6),
        "promien_lisci": (0.4, 0.7),
        "liczba_korzeni": (4, 6),
        "kolor_lodygi": (0.15, 0.08, 0.02, 1.0),
        "kolor_lisci": (0.05, 0.35, 0.1, 1.0),
        "metalicznosc": 0.7,
        "szorstkosc": 0.3
    },
    "krzew": {
        "wysokosc": (0.8, 1.8),
        "liczba_lisci": (5, 8),
        "promien_lisci": (0.5, 0.9),
        "liczba_korzeni": (2, 4),
        "kolor_lodygi": (0.25, 0.15, 0.05, 1.0),
        "kolor_lisci": (0.1, 0.5, 0.05, 1.0),
        "metalicznosc": 0.5,
        "szorstkosc": 0.5
    },
    "paproc": {
        "wysokosc": (0.5, 1.2),
        "liczba_lisci": (6, 10),
        "promien_lisci": (0.6, 1.0),
        "liczba_korzeni": (2, 3),
        "kolor_lodygi": (0.2, 0.3, 0.1, 1.0),
        "kolor_lisci": (0.0, 0.6, 0.15, 1.0),
        "metalicznosc": 0.3,
        "szorstkosc": 0.6
    }
}

def stworz_material(nazwa, kolor, metalicznosc=0.5, szorstkosc=0.5, emisja=0.0):
    mat = bpy.data.materials.new(name=nazwa)
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (300, 0)
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = kolor
    bsdf.inputs['Metallic'].default_value = metalicznosc
    bsdf.inputs['Roughness'].default_value = szorstkosc
    
    if emisja > 0:
        bsdf.inputs['Emission Strength'].default_value = emisja
        bsdf.inputs['Emission Color'].default_value = kolor[:3] + (1.0,)
    
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def stworz_lodyge(wysokosc, promien=0.25, pozycja=(0, 0, 0), material=None):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32,
        radius=promien,
        depth=wysokosc,
        location=(pozycja[0], pozycja[1], pozycja[2] + wysokosc/2)
    )
    lodyga = bpy.context.active_object
    lodyga.name = "Lodyga"
    
    if material:
        if lodyga.data.materials:
            lodyga.data.materials[0] = material
        else:
            lodyga.data.materials.append(material)
    
    return lodyga

def stworz_liscie(liczba_lisci, wysokosc_lodygi, promien_lisci, pozycja=(0, 0, 0), material=None):
    lista_lisci = []
    kat_miedzy = 2 * math.pi / liczba_lisci
    
    for i in range(liczba_lisci):
        kat = i * kat_miedzy
        promien_rozmieszczenia = 0.4
        
        x = pozycja[0] + math.cos(kat) * promien_rozmieszczenia
        y = pozycja[1] + math.sin(kat) * promien_rozmieszczenia
        z = pozycja[2] + wysokosc_lodygi - 0.2
        
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, z))
        lisc = bpy.context.active_object
        lisc.name = f"Lisc_{i+1}"
        
        lisc.scale = (promien_lisci * 1.2, promien_lisci * 0.6, promien_lisci * 0.1)
        lisc.rotation_euler = Euler(
            (math.radians(30), math.radians(kat * 180 / math.pi + 45), math.radians(15)),
            'XYZ'
        )
        
        if material:
            if lisc.data.materials:
                lisc.data.materials[0] = material
            else:
                lisc.data.materials.append(material)
        
        lista_lisci.append(lisc)
    
    return lista_lisci

def stworz_korzenie(liczba_korzeni, promien_korzenia=0.15, pozycja=(0, 0, 0), material=None):
    lista_korzeni = []
    kat_miedzy = 2 * math.pi / liczba_korzeni
    
    for i in range(liczba_korzeni):
        kat = i * kat_miedzy
        promien_rozmieszczenia = 0.35
        
        x = pozycja[0] + math.cos(kat) * promien_rozmieszczenia
        y = pozycja[1] + math.sin(kat) * promien_rozmieszczenia
        z = pozycja[2] + 0.1
        
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, z))
        korzen = bpy.context.active_object
        korzen.name = f"Korzen_{i+1}"
        
        korzen.scale = (promien_korzenia * 0.8, promien_korzenia * 0.8, promien_korzenia * 0.4)
        korzen.rotation_euler = Euler(
            (math.radians(20), math.radians(kat * 180 / math.pi), math.radians(10)),
            'XYZ'
        )
        
        if material:
            if korzen.data.materials:
                korzen.data.materials[0] = material
            else:
                korzen.data.materials.append(material)
        
        lista_korzeni.append(korzen)
    
    return lista_korzeni

def stworz_rosline(wysokosc=2.0, liczba_lisci=4, promien_lisci=0.3, liczba_korzeni=4, 
                   pozycja=(0, 0, 0), kolor_lodygi=None, kolor_lisci=None,
                   metalicznosc_lodygi=0.7, szorstkosc_lodygi=0.3,
                   metalicznosc_lisci=0.5, szorstkosc_lisci=0.4):
    
    if kolor_lodygi is None:
        kolor_lodygi = (0.7, 0.4, 0.2, 1.0)
    if kolor_lisci is None:
        kolor_lisci = (0.2, 0.8, 0.6, 1.0)
    
    mat_lodyga = stworz_material("Material_Lodyga", kolor_lodygi, metalicznosc_lodygi, szorstkosc_lodygi)
    mat_lisc = stworz_material("Material_Lisc", kolor_lisci, metalicznosc_lisci, szorstkosc_lisci)
    mat_korzen = stworz_material("Material_Korzen", (0.5, 0.3, 0.2, 1.0), 0.7, 0.5)
    
    lodyga = stworz_lodyge(wysokosc, promien=0.25, pozycja=pozycja, material=mat_lodyga)
    liscie = stworz_liscie(liczba_lisci, wysokosc, promien_lisci, pozycja=pozycja, material=mat_lisc)
    korzenie = stworz_korzenie(liczba_korzeni, promien_korzenia=0.2, pozycja=pozycja, material=mat_korzen)
    
    return [lodyga] + liscie + korzenie

def wybierz_typ_biomu(x, z, rozmiar_pola):
    max_odleglosc = rozmiar_pola / 2
    odleglosc = math.sqrt(x*x + z*z)
    procent = odleglosc / max_odleglosc
    
    if procent < 0.25:
        return "drzewo"
    elif procent < 0.5:
        return "drzewo" if random.random() < 0.6 else "krzew"
    elif procent < 0.75:
        return "krzew" if random.random() < 0.7 else "paproc"
    else:
        return "paproc"

def stworz_rosline_typ(x, z, typ):
    params = TYPY_ROSLIN[typ]
    
    wysokosc = random.uniform(*params["wysokosc"])
    liczba_lisci = random.randint(*params["liczba_lisci"])
    promien_lisci = random.uniform(*params["promien_lisci"])
    liczba_korzeni = random.randint(*params["liczba_korzeni"])
    
    kolor_lodygi = params["kolor_lodygi"]
    kolor_lisci = params["kolor_lisci"]
    metalicznosc_lodygi = params.get("metalicznosc", 0.5)
    szorstkosc_lodygi = params.get("szorstkosc", 0.5)
    metalicznosc_lisci = params.get("metalicznosc", 0.5)
    szorstkosc_lisci = params.get("szorstkosc", 0.5)
    
    skala_globalna = random.uniform(0.8, 1.2)
    wysokosc *= skala_globalna
    promien_lisci *= skala_globalna
    
    return stworz_rosline(
        wysokosc=wysokosc,
        liczba_lisci=liczba_lisci,
        promien_lisci=promien_lisci,
        liczba_korzeni=liczba_korzeni,
        pozycja=(x, z, 0),
        kolor_lodygi=kolor_lodygi,
        kolor_lisci=kolor_lisci,
        metalicznosc_lodygi=metalicznosc_lodygi,
        szorstkosc_lodygi=szorstkosc_lodygi,
        metalicznosc_lisci=metalicznosc_lisci,
        szorstkosc_lisci=szorstkosc_lisci
    )

def stworz_podloze(rozmiar_pola=10.0):
    bpy.ops.mesh.primitive_plane_add(size=rozmiar_pola, location=(0, 0, -0.1))
    podloze = bpy.context.active_object
    podloze.name = "Podloze"
    
    mat_podloze = stworz_material("Material_Podloze", (0.15, 0.12, 0.08, 1.0), 0.05, 0.95)
    if podloze.data.materials:
        podloze.data.materials[0] = mat_podloze
    else:
        podloze.data.materials.append(mat_podloze)
    
    return podloze

def stworz_swiatlo_i_kamera():
    bpy.ops.object.light_add(type='SUN', location=(8, -6, 12))
    slonce = bpy.context.active_object
    slonce.data.energy = 4.0
    slonce.data.angle = 0.4
    slonce.name = "Slonce"
    
    bpy.ops.object.light_add(type='AREA', location=(-3, -4, 5))
    wypelnienie = bpy.context.active_object
    wypelnienie.data.energy = 100
    wypelnienie.data.size = 4.0
    wypelnienie.name = "Swiatlo_Wypelniajace"
    
    bpy.ops.object.camera_add(location=(6, -5, 4.5))
    kamera = bpy.context.active_object
    kamera.rotation_euler = Euler((math.radians(50), 0, math.radians(40)), 'XYZ')
    kamera.name = "Kamera_Lasu"
    bpy.context.scene.camera = kamera

def generuj_las(liczba_roslin=40, rozmiar_pola=14.0, seed=42):
    random.seed(seed)
    
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    for collection in bpy.data.collections:
        if collection.name.startswith("Las"):
            bpy.context.scene.collection.children.unlink(collection)
            bpy.data.collections.remove(collection)
    
    glowna_kolekcja = bpy.data.collections.new("Las")
    bpy.context.scene.collection.children.link(glowna_kolekcja)
    
    podloze = stworz_podloze(rozmiar_pola)
    glowna_kolekcja.objects.link(podloze)
    
    for i in range(liczba_roslin):
        odleglosc_od_srodka = random.random() ** 1.2
        maks_odleglosc = rozmiar_pola / 2
        promien = odleglosc_od_srodka * maks_odleglosc
        kat = random.uniform(0, 2 * math.pi)
        
        x = math.cos(kat) * promien
        z = math.sin(kat) * promien
        
        typ = wybierz_typ_biomu(x, z, rozmiar_pola)
        
        obiekty = stworz_rosline_typ(x, z, typ)
        
        for obj in obiekty:
            glowna_kolekcja.objects.link(obj)
    
    stworz_swiatlo_i_kamera()
    
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.filepath = os.path.abspath("las_05.png")
    scene.render.image_settings.file_format = 'PNG'
    scene.render.resolution_x = 1200
    scene.render.resolution_y = 800
    
    scene.eevee.taa_render_samples = 64
    scene.render.film_transparent = False
    
    world = scene.world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get('Background')
    if bg_node:
        bg_node.inputs[0].default_value = (0.1, 0.15, 0.25, 1.0)
    
    bpy.ops.render.render(write_still=True)
    print(f"Render zapisany: las_05.png")
    
    return glowna_kolekcja

if __name__ == "__main__":
    generuj_las(liczba_roslin=45, rozmiar_pola=14.0, seed=42)