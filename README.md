# Logistic Routing Problem

<img src="https://picjumbo.com/wp-content/uploads/white-tir-truck-in-motion-driving-on-highway_free_stock_photos_picjumbo_DSC04205-1080x720.jpg" class="img-responsive" width="50%" height="50%"><img src="https://upload.wikimedia.org/wikipedia/commons/1/1a/Luftaufnahmen_Nordseekueste_2013_05_by-RaBoe_tele_46.jpg" class="img-responsive" width="50%" height="50%">

## Prerequisites
Untuk menjalankan program, perangkat anda perlu memiliki dependencies berikut ini
1. [Python (v3.7.0 or higher)](https://www.python.org/downloads/)
2. [Python-MIP](https://docs.python-mip.com/en/latest/install.html)
3. [NetworkX for Python](https://networkx.github.io/documentation/stable/install.html)
4. [Matplotlib](https://matplotlib.org/3.2.1/users/installing.html)

Apabila anda memiliki package manager [pip](https://pypi.org/project/pip/), anda dapat menginstal dependencies nomor 2 sampai 4 dengan menjalankan perintah berikut
```
pip install requirements.txt
```

## Running
Untuk simpul-simpul yang ingin ditelusuri, ubahlah file **post.txt** pada directory **data**, dengan baris pertama merupakan indeks simpul awal (kantor pusat logistik) dan simpul lainnya dipisahkan *newline*.

Contoh isi file *post.txt*
```
1
2
3
4
```
Jalankan perintah berikut pada directory **bin**
- Untuk peta Oldenburg
```
python main.py ol
```
- Untuk peta San Francisco
```
python main.py sf
```

## Multiple-Agent TSP
Masalah pengantaran barang untuk satu kendaraan dengan fungsi objektif jarak minimal dapat dimodelkan oleh Travelling Salesman Problem. Akan tetapi, perusahaan logistik biasanya memiliki lebih dari satu kendaraan yang berangkat bersamaan, sehingga TSP kurang cocok digunakan. Generalisasi TSP untuk beberapa agen adalah **multiple-agent TSP (mTSP)**, dan model masalah ini akan kita gunakan. Pada mTSP, akan terdapat *m* tur yang akan dibangun. Syarat dari semua tur mirip dengan TSP, yaitu bahwa seluruh tur akan kembali ke simpul awal (mewakili kantor pusat) dan setiap tujuan hanya akan dilewati oleh satu tur.

## Solution
### Pathfinding
Dalam membentuk upagraf dari simpul-simpul kota yang diinginkan, algoritma pathfinding yang dimanfaatkan adalah A* (a-star) dengan fungsi biaya/cost didefinisikan sebagai berikut

<img src=https://latex.codecogs.com/gif.latex?f%28n%29%20%3D%20g%28n%29%20&plus;%20h%28n%29>

dengan g(n) merupakan biaya/cost yang dibutuhkan untuk mencapai simpul n dan h(n) merupakan nilai heuristik yang memperkirakan biaya/cost yang dibutuhkan untuk mencapai simpul tujuan. Nilai heuristik yang dimanfaatkan dalam implementasi program ini adalah **Euclidean Distance** antara simpul n dengan simpul tujuan.

<img src=https://latex.codecogs.com/gif.latex?d%3D%5Csqrt%7B%28x_1-x_2%29%5E2&plus;%28y_1-y_2%29%5E2%7D>

### Mutiple Travelling Salesman Problem

#### 1. Reduced Cost Matrix

Persoalan mTSP dapat diaproksimasi solusinya dengan membagi-bagi titik menjadi sebanyak **m** subgraf lengkap yang akan dicari tur minimumnya. Sirkuit Hamilton minimum ini dapat dicari dengan merepresentasikan tiap subgraf menjadi matriks ketetanggaan dengan contoh sebagai berikut.

<img src=https://latex.codecogs.com/gif.latex?%5Cbegin%7Bbmatrix%7D%20%5Cinfty%20%2614%2617%262%268%5C%5C%2012%26%5Cinfty%2619%262%267%5C%5C%2010%263%26%5Cinfty%264%262%5C%5C%205%263%2612%26%5Cinfty%269%5C%5C%2011%267%264%2612%26%5Cinfty%20%5Cend%7Bbmatrix%7D>

Matrix ini kemudian akan direduksi sedemikian rupa sehingga pada setiap kolom dan baris matriks terdapat sedikitnya satu sel yang bernilai nol.

<img src=https://latex.codecogs.com/gif.latex?%5Cbegin%7Bbmatrix%7D%20%5Cinfty%20%2612%2615%260%266%5C%5C%208%26%5Cinfty%2617%260%265%5C%5C%206%261%26%5Cinfty%262%260%5C%5C%200%260%269%26%5Cinfty%266%5C%5C%202%260%260%265%26%5Cinfty%20%5Cend%7Bbmatrix%7D>

Total nilai yang dikurangi dari matriks awal (r) adalah sebesar 18.

Dengan memanfaatkan reduced cost matrix ini, nilai tur yang seminimum mungkin dapat dicari dengan pendekatan Branch and Bound, dimana nilai cost untuk setiap simpul c(i) ditulis sebagai

<img src=https://latex.codecogs.com/gif.latex?%5Chat%7Bc%7D%28S%29%20%3D%20%5Chat%7Bc%7D%28P%29%20&plus;%20A%28i%2Cj%29%20&plus;%20r>

dengan *c(P)* merupakan cost dari simpul parent pada pohon pencarian dan *A(i,j)* merupakan nilai sel matriks yang dipilih

#### 2. Pemodelan MIP

Permasalahan m-TSP merupakan permasalahan optimasi yang diselesaikan dengan pendekatan **mixed integer programming (MIP)** dengan fungsi objektif sebagai berikut.

<img src=https://latex.codecogs.com/gif.latex?min%5Csum_%7B%5C%28i%2Cj%29%20%5Cin%20V%7Dc%5Ctextsubscript%7Bij%7D%20x%5Ctextsubscript%7Bij%7D>

Batasan-batasan (constraints) berupa persamaan linear yang ditambahkan kedalam model MIP ini adalah

<img src=https://latex.codecogs.com/gif.latex?%5Csum_%7Bi%20%5Cin%20V-%5C%7B0%5C%7D%7Dx%5Ctextsubscript%7Bi0%7D%3Dm>

<img src=https://latex.codecogs.com/gif.latex?%5Csum_%7Bj%20%5Cin%20V-%5C%7B0%5C%7D%7Dx%5Ctextsubscript%7B0j%7D%3Dm>

Dengan asumsi simpul (node) 0 merupakan simpul dimulainya tur, kedua persamaan di atas berfungsi untuk memastikan bahwa tepat sebanyak m kendaraan  logistik yang berangkat dan kembali ke simpul 0.

<img src=https://latex.codecogs.com/gif.latex?%5Csum_%7Bi%20%5Cin%20V%7Dx_%7Bij%7D%3D1%2C%5Cforall%20j%20%5Cin%20V-%5C%7B0%5C%7D>
<br>
<img src=https://latex.codecogs.com/gif.latex?%5Csum_%7Bj%20%5Cin%20V%7Dx_%7Bij%7D%3D1%2C%5Cforall%20i%20%5Cin%20V-%5C%7B0%5C%7D>

Sementara itu, kedua persamaan di atas bermanfaat untuk membatasi agar simpul lainnya (selain simpul awal 0) agar hanya dikunjungi tepat sekali saja.

Untuk mengeliminasi subtour, constraint ini ditambahkan ke dalam model MIP yang sudah ada [MTZ, 1960].

<img src=https://latex.codecogs.com/gif.latex?u_i-u_j&plus;p%5Ccdot%20x_%7Bij%7D%5Cle%20p-1%2C%5Cforall%201%20%5Cle%20i%20%5Cne%20j%20%5Cle%20n>

dengan **n** merupakan jumlah nodes pada graf dan **p** merupakan jumlah node maksimum yang dapat dikunjungi sebuah kendaraan logistik (salesman) 

## Referensi
1. Dataset : https://www.cs.utah.edu/~lifeifei/SpatialDataset.htm
2. Pengenalan dan formulasi mTSP : https://neos-guide.org/content/multiple-traveling-salesman-problem-mtsp
3. MIP , pustaka Python untuk optimisasi : https://python-mip.readthedocs.io/en/latest/intro.html
4. Li, Feifei, Dihan Cheng, Marios Hadjieleftheriou, George Kollios, and Shang-Hua Teng. "On trip planning queries in spatial databases." In International symposium on spatial and temporal databases, pp. 273-290. Springer, Berlin, Heidelberg, 2005.
5. Matai, Rajesh, Surya Prakash Singh, and Murari Lal Mittal. "Traveling salesman problem: an overview of applications, formulations, and solution approaches." Traveling salesman problem, theory and applications 1, 2010.
6. K-Means Clustering Algorithm: https://stanford.edu/~cpiech/cs221/handouts/kmeans.html
7. Python MIP for TSP Problem: https://python-mip.readthedocs.io/en/latest/examples.html
8. Reduced Cost Matrix for TSP: http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.734.8448&rep=rep1&type=pdf

## Credits
Thank you for Li Fei Fei et. al. for providing the data.
