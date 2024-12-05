from PIL import Image
import os
# À exécuter manuellement

def resize_image(input_path, output_path, size):
    with Image.open(input_path) as img:
        img = img.resize(size, Image.LANCZOS)
        img.save(output_path)


def resize_images_in_directory(input_directory, output_directory, size):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            input_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, filename)
            with Image.open(input_path) as img:
                img = img.resize(size, Image.LANCZOS)
                img.save(output_path)
                print(f'Taille du fichier {filename} changée')


# Exemple d'utilisation
if __name__ == "__main__":
    input_directory = 'images_videos/test'  # Répertoire contenant les images originales
    output_directory = 'images_videos/nvll_t_pkmn'  # Répertoire où enregistrer les images redimensionnées
    size = (250, 250)  # Nouvelle taille des images (largeur, hauteur)

    resize_images_in_directory(input_directory, output_directory, size)
