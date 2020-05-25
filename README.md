# Logistic Routing Problem

<img src="https://picjumbo.com/wp-content/uploads/white-tir-truck-in-motion-driving-on-highway_free_stock_photos_picjumbo_DSC04205-1080x720.jpg" class="img-responsive" width="50%" height="50%"><img src="https://upload.wikimedia.org/wikipedia/commons/1/1a/Luftaufnahmen_Nordseekueste_2013_05_by-RaBoe_tele_46.jpg" class="img-responsive" width="45%" height="45%">

## Tujuan Tugas
1. Review materi pathfinding pada mata kuliah Strategi Algoritma.
2. Mengenal multiple-agent TSP.
3. Melakukan visualisasi data.

## Deskripsi Masalah
Welcome to **Oldenburg** ! Kota kecil cantik ini merupakan sebuah kota kecil di timur kota Bremen , Jerman , dengan penduduk kurang lebih 168 ribu jiwa [2018]. Kota kecil ini cocok menjadi lahan uji coba untuk melakukan pemodelan sederhana pembuatan rute pengantaran logistik.<br>
Setiap beberapa jam sekali, sebuah perusahaan logistik akan mengirimkan beberapa kurirnya untuk mengantar barang dari kantor pusat mereka ke beberapa titik tujuan yang tersebar di oenjuru kota Oldenburg. Anda diminta untuk mencari rute untuk seluruh kurir sehingga jarak yang ditempuh oleh semua kurir paling kecil, dan perusahaan logistik dapat menghemat biaya bensin.

## Multiple-Agent TSP
Masalah pengantaran barang untuk satu kendaraan dengan fungsi objektif jarak minimal dapat dimodelkan oleh Travelling Salesman Problem. Akan tetapi, perusahaan logistik biasanya memiliki lebih dari satu kendaraan yang berangkat bersamaan, sehingga TSP kurang cocok digunakan. Generalisasi TSP untuk beberapa agen adalah **multiple-agent TSP (mTSP)**, dan model masalah ini akan kita gunakan. Pada mTSP, akan terdapat *m* tur yang akan dibangun. Syarat dari semua tur mirip dengan TSP, yaitu bahwa seluruh tur akan kembali ke simpul awal (mewakili kantor pusat) dan setiap tujuan hanya akan dilewati oleh satu tur.

## Tugas
Kita akan menggunakan dataset jalanan pada kota Oldenburg yang dapat diakses pada <a href="https://www.cs.utah.edu/~lifeifei/SpatialDataset.htm">tautan ini.</a> Lakukan pengunduhan untuk kedua data jalanan di kota Oldenburg. Data pertama merupakan koordinat simpul, data kedua merupakan data sisi antar simpul.<br>
Seperti yang disebutkan sebelumnya, kita akan menggunakan pendekatan mTSP dalam permasalahan ini. Untuk mempermudah anda dan mempermudah penilaian, tugas akan dibagi dalam beberapa tahap.

### Milestone 1
Pada milestone 1, anda diminta untuk membangun sebuah upagraf dari graf jalan keseluruhan kota Oldenburg. Upagraf tersebut merupakan sebuah graf lengkap tak berarah, dengan simpul-simpulnya adalah titik tujuan pengiriman barang ditambah titik yang mewakili kantor pusat perusahaan logistik. Hasilkan sebuah matriks jarak antar simpul.

### Milestone 2
Pada Milestone 2 , anda akan menggunakan upagraf yang telah dihasilkan pada Milestone 1 untuk membangun rute dari para kurir dengan pendekatan mTSP. Tampilkan rute-rute yang terbentuk.

### Milestone 3
Setelah berhasil mendapatkan rute bagi para kurir, selanjutnya anda diminta untuk menggambarkan rute dari para kurir. Visualisasi rute yang digunakan minimal membedakan warna rute untuk tiap kurir dan menampilkan upagraf yang digunakan untuk membuat rute. Nilai lebih akan diberikan jika anda dapat menampilkan rute beserta seluruh peta jalan di kota Oldenburg.

## Pengerjaan
Lakukan *fork* terhadap *repository* ini.<br>
Spek tugas cukup umum, sehingga asisten tidak membatasi algoritma maupun bahasa pemrograman yang digunakan, walaupun penggunaan Python disarankan. Algoritma yang digunakan untuk pathfinding harus optimal, namun hasil dari mTSP tidak harus optimal (*Note : beberapa pustaka optimization bisa menghasilkan solusi sub-optimal dalam batas waktu tertentu* ). Bila merasa sudah menyelesaikan tugas, silahkan lakukan pull request dan hubungi asisten lewat email untuk melakukan demo.<br>
Pastikan ada menambahkan/menggati README ini saat mengumpulkan. README minimal mengandung :
1. Progress (sudah sampai milestone keberapa)
2. Pendekatan algoritma yang digunakan untuk pathfinding dan penyelesaian mTSP, serta 
3. Cara menjalankan program.

Pengerjaan dapat dilakukan berkelompok, namun poin maksimal untuk setiap orang adalah poin maksimal dibagi jumlah orang per kelompok.<br>
Anda bebas menggunakan pustaka maupun referensi apapun untuk mengerjakan tugas, kecuali kode/pustaka jadi yang melakukan *routing*, karena tujuan tugas adalah membuat sebuah prototipe pembuatan rute. Pastikan anda mencantumkan sumber bilamana anda menggunakan kode dari orang lain. Akan tetapi, pemahaman terhadap solusi masalah menjadi bagian penting dari penilaian , sehingga anda disarankan untuk menuliskan kode anda sendiri.<br>

## Penilaian
Saat ini, nilai belum ditentukan, akan tetapi nilai akan diberikan untuk tiap *milestone*. Penilaian akan dilakukan berdasarkan : 
1. kode sumber,
2. demo aplikasi dan ,
3. pemahaman terhadap solusi masalah. 
Demo hanya dapat dilakukan sekali. Asisten juga akan menjalankan **plagiarism checking** antar kode sumber peserta. Bila ditemukan adanya kecurangan, maka nilai peserta bersangkutan adalah 0 tanpa pengubahan, dan pengurangan poin maksimal tidak akan berlaku. Perhatikan bahwa selama anda mencantumkan asal kode yang anda salin dan tidak menyalin kode milik teman anda, anda tidak akan bermasalah.

## Kontak
Silahkan hubungi asisten lewat line @alamhasabiebaru atau lewat email 13517096@std.stei.itb.ac.id . *Note : waktu menjawab bervariasi, namun email biasanya akan dibalas kurang dari sehari. Line mungkin tidak dibalas dalam waktu satu-dua hari. Mohon bersabar :)*. Pertanyaan juga dipersilahkan.

## Referensi
Silahkan gunakan referensi berikut sebagai awal pengerjaan tugas:<br>
[1] Dataset : https://www.cs.utah.edu/~lifeifei/SpatialDataset.htm<br>
[2] Pengenalan dan formulasi mTSP : https://neos-guide.org/content/multiple-traveling-salesman-problem-mtsp<br>
[3] MIP , pustaka Python untuk optimisasi : https://python-mip.readthedocs.io/en/latest/intro.html<br>
[4] OpenGL untuk Python : https://stackabuse.com/brief-introduction-to-opengl-in-python-with-pyopengl/<br>



