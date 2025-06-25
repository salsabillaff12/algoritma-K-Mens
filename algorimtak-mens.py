# Algoritma K-Means Clustering Manual tanpa library
# Dataset: Mall_Customers.csv
# Fitur: Annual Income (k$) dan Spending Score (1-100)

# Fungsi untuk memisahkan string berdasarkan koma
def split_line(line):
    result = []
    current = ""
    for char in line:
        if char == ',':
            result.append(current)
            current = ""
        else:
            current += char
    result.append(current.strip())
    return result

# Fungsi untuk membaca data dari file CSV
def load_data_mall_customers(lines):
    data = []
    for line in lines[1:]:  # Lewati baris header
        parts = split_line(line.strip())
        if len(parts) >= 5:
            customerID = float(parts[0])
            income = float(parts[3])
            score = float(parts[4])
            data.append([customerID, income, score])
    return data

# Fungsi untuk menghitung jarak Euclidean antar dua titik
def euclidean_distance(a, b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2) ** 0.5

# Fungsi untuk mengelompokkan setiap titik ke centroid terdekat
def assign_clusters(data, centroids, show_details=False):
    assignments = []
    if show_details:
        print("\n--- Fase Penugasan ---")
        print(f"Centroid saat ini: {centroids}")
    
    for idx, point in enumerate(data):
        distances = []
        min_dist = euclidean_distance(point, centroids[0])
        cluster = 0
        distances.append(min_dist)
        
        for i in range(1, len(centroids)):
            dist = euclidean_distance(point, centroids[i])
            distances.append(dist)
            if dist < min_dist:
                min_dist = dist
                cluster = i
        
        assignments.append(cluster)
        
        if show_details and idx < 10:  # Tampilkan detail untuk 10 titik pertama
            print(f"Titik {point[1:]}: jarak = {[round(d, 2) for d in distances]}, ditugaskan ke cluster {cluster}")
    
    return assignments

# Fungsi untuk menghitung centroid baru dari data pada masing-masing cluster
def update_centroids(data, assignments, k, show_details=False):
    new_centroids = []
    
    if show_details:
        print("\n--- Fase Pembaruan Centroid ---")
    
    for i in range(k):
        sum_x = 0
        sum_y = 0
        count = 0
        cluster_points = []
        
        for j in range(len(data)):
            if assignments[j] == i:
                sum_x += data[j][0]
                sum_y += data[j][1]
                count += 1
                cluster_points.append(data[j][1:])  # Simpan tanpa customer ID
        
        if count == 0:
            new_centroids.append([0, 0])
            if show_details:
                print(f"Cluster {i}: Tidak ada titik yang ditugaskan, centroid = [0, 0]")
        else:
            new_centroid = [sum_x / count, sum_y / count]
            new_centroids.append(new_centroid)
            if show_details:
                print(f"Cluster {i}: {count} titik, centroid = [{round(new_centroid[0], 2)}, {round(new_centroid[1], 2)}]")
                if len(cluster_points) <= 5:  # Tampilkan titik jika cluster kecil
                    print(f"  Titik: {cluster_points}")
    
    return new_centroids

# Fungsi utama algoritma K-Means
def kmeans_clustering(data, k, max_iter=100):
    print(f"=== Algoritma K-Means Clustering Dimulai ===")
    print(f"Jumlah titik data: {len(data)}")
    print(f"Jumlah cluster (k): {k}")
    print(f"Iterasi maksimum: {max_iter}")
    
    # Inisialisasi centroid dengan k data pertama
    centroids = []
    for i in range(k):
        centroids.append(data[i])
    
    print(f"\nCentroid awal: {centroids}")
    
    for iteration in range(max_iter):
        print(f"\n{'='*50}")
        print(f"ITERASI {iteration + 1}")
        print(f"{'='*50}")
        
        # Fase penugasan
        clusters = assign_clusters(data, centroids, show_details=True)
        
        # Perbarui centroid
        new_centroids = update_centroids(data, clusters, k, show_details=True)
        
        # Periksa konvergensi
        converged = True
        print(f"\n--- Pemeriksaan Konvergensi ---")
        for i in range(len(centroids)):
            old_c = [round(centroids[i][0], 4), round(centroids[i][1], 4)]
            new_c = [round(new_centroids[i][0], 4), round(new_centroids[i][1], 4)]
            print(f"Cluster {i}: {old_c} -> {new_c}")
            if old_c != new_c:
                converged = False
        
        if converged:
            print(f"\nKonvergensi tercapai! Algoritma berhenti pada iterasi {iteration + 1}")
            break
        else:
            print("Centroid berubah, melanjutkan...")
        
        centroids = new_centroids
    
    print(f"\n{'='*50}")
    print("HASIL AKHIR")
    print(f"{'='*50}")
    
    return clusters, centroids

# Fungsi untuk menampilkan hasil clustering
def print_results(data, clusters, centroids):
    print("\nHasil Clustering Terperinci:")
    
    # Kelompokkan berdasarkan cluster
    for cluster_id in range(len(centroids)):
        cluster_points = []
        for i in range(len(data)):
            if clusters[i] == cluster_id:
                cluster_points.append((data[i][0], data[i][1], data[i][2]))
        
        print(f"\nCluster {cluster_id} (Centroid: [{round(centroids[cluster_id][0], 2)}, {round(centroids[cluster_id][1], 2)}]):")
        print(f"Jumlah titik: {len(cluster_points)}")
        
        if len(cluster_points) <= 10:  # Tampilkan semua titik jika cluster kecil
            for point in cluster_points:
                print(f"  Pelanggan {int(point[0])}: Pendapatan={point[1]}, Skor={point[2]}")
        else:  # Tampilkan 5 titik pertama jika cluster besar
            for i in range(5):
                point = cluster_points[i]
                print(f"  Pelanggan {int(point[0])}: Pendapatan={point[1]}, Skor={point[2]}")
            print(f"  ... dan {len(cluster_points) - 5} titik lainnya")

# Eksekusi Program
file_path = "Mall_Customers.csv"
lines = open(file_path, "r").readlines()
data = load_data_mall_customers(lines)
k = 3  # Jumlah cluster
clusters, centroids = kmeans_clustering(data, k)
print_results(data, clusters, centroids)