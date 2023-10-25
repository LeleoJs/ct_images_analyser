import cv2
import os
import numpy as np
import open3d as o3d

def arrayImagensTo3d(arrayImagens, z_scale_mult):
    colXcoordinates, colYcoordinates, colZcoordinates = [], [], []

    for i, img in enumerate(arrayImagens):

        """ Otimizado pelo chat gpt """
        non_zero_indices = np.argwhere(img > 0)
        non_zero_indices = non_zero_indices[:, [1, 0]]  # Inverte as coordenadas x e y

        colXcoordinates.extend(non_zero_indices[:, 0])
        colYcoordinates.extend(non_zero_indices[:, 1])
        colZcoordinates.extend([i * z_scale_mult] * len(non_zero_indices))

        """ Original """
    #for coord_xPixel, linha in enumerate(img):
    #    for coord_yPixel, elemento in enumerate(linha):
    #        if elemento > 0:
    #            colXcoordinates.append(coord_xPixel)
    #            colYcoordinates.append(coord_yPixel) 
    #            colZcoordinates.append(i * z_scale_mult)

    colXcoordinates_np = np.array(colXcoordinates)
    colYcoordinates_np = np.array(colYcoordinates)
    colZcoordinates_np = np.array(colZcoordinates)

    xyz = np.column_stack((colXcoordinates_np, colYcoordinates_np, colZcoordinates_np))

    return xyz

# Numero de arquivos de imagem na pasta
path = '/home/leonardo/Desktop/CT_slices_2_3d/data/data'
num_files = len([f for f in os.listdir(path)
                if os.path.isfile(os.path.join(path, f))])

# Junta um array com as imagens que serão analisadas
img_grayscale = []
for i in range(num_files):
    img_grayscale.append(cv2.imread('/home/leonardo/Desktop/CT_slices_2_3d/data/data/pulmonar_image_'+str(i+1)+'.jpeg', 0))
print("Imagens capturadas: " + str(len(img_grayscale)))

# Converter a lista img_grayscale em um array NumPy
grayscale = np.array(img_grayscale)


threshold_value = 128  # Valor de limite (ajuste conforme necessário)
binary_image = cv2.threshold(grayscale, threshold_value, 255, cv2.THRESH_BINARY)


#Cria um objeto vazio de nuvem de pontos
pcd_demo = o3d.geometry.PointCloud()

#Transforma o array do numpy para um vetor 3d e transfere para points
pcd_demo.points = o3d.utility.Vector3dVector(arrayImagensTo3d(grayscale,3)) 
print("xyz\n",arrayImagensTo3d(grayscale,3))

#Abre a janela de visualizacao para mostrar a figura
o3d.visualization.draw_geometries([pcd_demo])

#Escreve o "pcd_demo" com "print_pcd_demo.pcd" para futura leitura
o3d.io.write_point_cloud("print_pcd_demo.pcd",pcd_demo)
